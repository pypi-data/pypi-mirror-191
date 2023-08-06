"""Tools to guess paths"""
from pathlib import Path
from typing import List

from ateto.conf import (
    MODELS_SOURCE_PATH,
    NOTES_DATA,
    TEMPLATES_CSS_FILENAME,
    TEMPLATES_DELIMITER,
    TEMPLATES_EXTENSION,
    TEMPLATES_OUTPUT_PATH,
)


def get_model_path(model_name: str) -> Path:
    """Return the path of model dir in models_export"""
    return MODELS_SOURCE_PATH / model_name


def get_cards_paths(model_name: str) -> List[Path]:
    """Return the paths of templates cards for model_name"""
    model_path = get_model_path(model_name)
    paths = []
    for path in model_path.iterdir():
        if path.suffix == TEMPLATES_EXTENSION:
            paths.append(path)
    return sorted(paths)


def get_css_path(model_name: str) -> Path:
    """Return the path of the CSS file in models_export"""
    return get_model_path(model_name) / TEMPLATES_CSS_FILENAME


def get_data_path(model_name: str) -> Path:
    """Return path of data for model_name"""
    return (NOTES_DATA / model_name).with_suffix(".yaml")


def get_output_path(model_name: str) -> Path:
    """Return path of HTML test file"""
    return (TEMPLATES_OUTPUT_PATH / model_name).with_suffix(".html")


def get_output_path_css(model_name: str) -> Path:
    """Return path of CSS test file"""
    return get_output_path(model_name).with_suffix(".css")


def is_valid_model_path(path: Path) -> bool:
    """Accept only directories not 'hidden'"""
    return path.is_dir() and (path.name[0] not in [".", "_"])


def get_models_dirs(
    source_path: Path = MODELS_SOURCE_PATH, path_filter: str = ""
) -> List[Path]:
    """Return the paths of exported models.

    path_filter could be :

    * empty (= "*") : all the valid models are returned
    * a string : it's the name of the only folder returned if valid
    * containing a wildcard : all the corresponding valid models are returned
    """
    if "*" in path_filter:
        paths = source_path.glob(path_filter)
    elif path_filter:
        paths = [source_path / path_filter]
    else:
        paths = source_path.iterdir()

    return [p for p in paths if is_valid_model_path(p)]


def get_default_html_output(file_path: str | Path = "") -> str:
    """Return a default template for HTML output files."""
    if not file_path:
        file_path = Path(__file__).parent.parent / "data/default_output.html"
    else:
        file_path = Path(file_path)

    with open(file_path) as htmlfile:
        return htmlfile.read()


def get_cards(path: Path, delimiter: str = ""):
    """Read the file and split it in two templates"""
    with open(path) as cardfile:
        return cardfile.read().split(delimiter or TEMPLATES_DELIMITER)
