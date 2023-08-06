"""Manage test data"""
import os
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List

import yaml

from ateto.conf import ANKI_CONNECT, DEFAULT_TEST_TAG, NOTES_DATA
from ateto.sync import request_anki


def get_model_data_dir(model_name: str) -> Path:
    return (NOTES_DATA / model_name).with_suffix(".yaml")


def dump_data(model_name: str, notes: Dict):
    """Dump notes in `data/model_name.yaml`"""
    path = get_model_data_dir(model_name)
    os.makedirs(path.parent, exist_ok=True)

    with open(path, "w") as yaml_file:
        yaml.dump(notes, yaml_file)


def load_data(model_name: str) -> List:
    """Load notes from `data/model_name.yaml`

    If `data/model_name_override.yaml` exists, it overrides
    the data."""
    path = get_model_data_dir(model_name)

    try:
        with open(path) as yaml_file:
            data = yaml.load(yaml_file, yaml.Loader)
    except FileNotFoundError:
        return []

    try:
        with open(path.with_stem(path.stem + "_override")) as yaml_file:
            overrides = yaml.load(yaml_file, yaml.Loader)
    except FileNotFoundError:
        overrides = []

    indexed_ids = {n["noteId"]: i for i, n in enumerate(data)}

    for override in overrides:
        index = indexed_ids.get(override["noteId"], None)
        try:
            data[index] = override
        except TypeError:
            data.append(override)

    return data


def populate_models_data(
    model_filter: str = "*",
    query: str = "note:{model} tag:{tag}",
    tag: str = DEFAULT_TEST_TAG,
) -> OrderedDict[str, List]:
    """Dump YAML files with the notes returned by AnkiConnect

    query can contain the string `{tag}` that will be replaced
    Raise an error if it fails.
    """
    query = f"{query}".format(model=model_filter, tag=tag)

    ids = request_anki(action=ANKI_CONNECT.REQUESTS.NOTES_FIND, params={"query": query})
    if not ids:
        raise ValueError("Nothing found with the query %s" % query)

    notes = request_anki(action=ANKI_CONNECT.REQUESTS.NOTES_INFO, params={"notes": ids})

    notes_by_models = {}
    for note in notes:
        model_name = note["modelName"]
        try:
            notes_by_models[model_name].append(note)
        except KeyError:
            notes_by_models[model_name] = [note]

    for model_name, notes in notes_by_models.items():
        dump_data(model_name, notes)

    return OrderedDict(sorted(list(notes_by_models.items())))
