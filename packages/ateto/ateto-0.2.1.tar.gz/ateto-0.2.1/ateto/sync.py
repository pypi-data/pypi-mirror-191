import os
from typing import Dict, List, Optional

import click
import requests

from ateto.conf import (
    ANKI_CONNECT,
    MEDIAS_SOURCE_PATH,
    TEMPLATES_CSS_FILENAME,
    TEMPLATES_DELIMITER,
    TEMPLATES_EXTENSION,
)
from ateto.medias import list_medias_filenames
from ateto.utils import (
    get_cards,
    get_cards_paths,
    get_css_path,
    get_model_path,
)


def request_anki(action, params: Optional = None, url=ANKI_CONNECT.URL):
    """Return the result of the AnkiConnect action or raise an error"""
    json = {
        "action": action,
        "version": 6,
    }

    if params is not None:
        json["params"] = params

    response = requests.post(url, json=json)
    try:
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        click.secho(
            "An error occured, make sure Anki is running and AnkiConnect addon is installed.",
            fg="red",
        )
        raise

    anki_response = response.json()

    # code from AnkiConnect
    if len(anki_response) != 2:
        raise ValueError("response has an unexpected number of fields")
    if "error" not in anki_response:
        raise ValueError("response is missing required error field")
    if "result" not in anki_response:
        raise ValueError("response is missing required result field")
    if anki_response["error"] is not None:
        raise ValueError(anki_response["error"])

    return anki_response["result"]


def write_model_export(name, html, css):
    """Write a model from anki connect to model_export."""
    model_path = get_model_path(name)
    os.makedirs(model_path, exist_ok=True)
    for card_name, sides in html.items():
        card_path = model_path / card_name
        with open(card_path.with_suffix(TEMPLATES_EXTENSION), "w") as card_file:
            card_file.write(TEMPLATES_DELIMITER.join([sides["Front"], sides["Back"]]))

    with open(model_path / TEMPLATES_CSS_FILENAME, "w") as css_file:
        css_file.write(css["css"])


def get_export_requests(
    model_names: Optional[List[str]] = None,
) -> Dict[str, List]:
    """Get every model in Anki and return requests to export them in models_export"""
    export_requests = {"names": [], "requests": []}
    for model_name in model_names or request_anki("modelNames"):
        export_requests["names"].append(model_name)
        export_requests["requests"].append(
            {"action": "modelTemplates", "params": {"modelName": model_name}}
        )
        export_requests["requests"].append(
            {"action": "modelStyling", "params": {"modelName": model_name}},
        )
    return export_requests


def export_templates(model_names: Optional[List[str]] = None) -> List[str]:
    """Export templates from anki in models_export"""
    export_requests = get_export_requests(model_names)

    results = request_anki("multi", params={"actions": export_requests["requests"]})
    for index, model_name in enumerate(export_requests["names"]):
        html = results[index * 2]
        css = results[index * 2 + 1]
        write_model_export(model_name, html, css)

    return export_requests["names"]


def get_import_requests(model_name: str) -> List[Dict]:
    cards = {}
    for card in get_cards_paths(model_name):
        front, back = get_cards(card)
        cards[card.stem] = {"Front": front, "Back": back}

    import_requests = [
        {
            "action": ANKI_CONNECT.REQUESTS.MODEL_TEMPLATES_UPDATE,
            "params": {"model": {"name": model_name, "templates": cards}},
        }
    ]

    with open(get_css_path(model_name)) as css_file:
        import_requests.append(
            {
                "action": ANKI_CONNECT.REQUESTS.MODEL_STYLE_UPDATE,
                "params": {"model": {"name": model_name, "css": css_file.read()}},
            }
        )
    return import_requests


def get_import_medias_requests():
    """Generate requests to import medias in anki."""
    import_requests = []
    for filename in list_medias_filenames():
        import_requests.append(
            {
                "action": "storeMediaFile",
                "params": {
                    "filename": filename,
                    "path": str(MEDIAS_SOURCE_PATH / filename),
                },
            }
        )
    return import_requests


def import_medias_in_anki():
    """Perform requests to import medias in Anki"""
    request_anki("multi", {"actions": get_import_medias_requests()})


def import_all_templates(
    models_names: Optional[List[str]] = None, with_medias: bool = False
):
    import_requests = get_import_medias_requests() if with_medias else []

    for model_name in models_names or request_anki("modelNames"):
        try:
            import_requests.extend(get_import_requests(model_name))
        except FileNotFoundError:
            pass

    request_anki("multi", {"actions": import_requests})
