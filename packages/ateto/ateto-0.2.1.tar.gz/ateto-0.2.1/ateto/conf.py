"""Defaults parameters for this project.

TODO: give access to a configuration file."""

from collections import namedtuple

from xdg import xdg_data_home

_AnkiRequests = namedtuple(
    "AnkiRequests",
    (
        "NOTES_FIND",
        "NOTES_INFO",
        "MODEL_TEMPLATES",
        "MODEL_STYLE",
        "MODEL_TEMPLATES_UPDATE",
        "MODEL_STYLE_UPDATE",
    ),
)
ANKI_CONNECT = namedtuple("AnkiConnectConstants", ("URL", "REQUESTS"))(
    "http://localhost:8765",
    _AnkiRequests(
        "findNotes",
        "notesInfo",
        "modelTemplates",
        "modelStyling",
        "updateModelTemplates",
        "updateModelStyling",
    ),
)

# useful for populate data
DEFAULT_TEST_TAG = "template_test_data"

ROOT_PATH = xdg_data_home() / "ateto"
MODELS_SOURCE_PATH = ROOT_PATH / "models_export"
TEMPLATES_OUTPUT_PATH = ROOT_PATH / "html_output"
NOTES_DATA = ROOT_PATH / "data"

ANKI_PROFILE_NAME = "principal"
ANKI_COLLECTION_PATH = (
    xdg_data_home() / "Anki2" / ANKI_PROFILE_NAME / "collection.media"
)

# we should get the values from the anki profile
TEMPLATES_CSS_FILENAME = "style.css"
TEMPLATES_DELIMITER = "\n\n```\n\n"
TEMPLATES_EXTENSION = ".html"

MEDIAS_PATH_NAME = "_medias"
MEDIAS_SOURCE_PATH = MODELS_SOURCE_PATH / MEDIAS_PATH_NAME
MEDIAS_EXTENSIONS = ("js", "css")

SUPERTEMPLATES_PATH = ROOT_PATH / "supertemplates"
SUPERTEMPLATES_MEDIAS_PATH = SUPERTEMPLATES_PATH / MEDIAS_PATH_NAME
SUPERTEMPLATES_IGNORED_SUFFIXES = (".jinja",)
SUPERTEMPLATES_VARIABLE_START = "{$"
SUPERTEMPLATES_VARIABLE_END = "$}"
SUPERTEMPLATES_COMMENT_START = "{*"
SUPERTEMPLATES_COMMENT_END = "*}"
