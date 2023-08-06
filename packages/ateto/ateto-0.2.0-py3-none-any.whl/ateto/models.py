"""Manage Note and Model objects"""
import copy
import logging
import os
import re
import shutil
from collections import namedtuple
from pathlib import Path
from typing import Dict, List, Optional

from bs4 import BeautifulSoup

from anki_template_tester.previewtemplate import TemplateTester
from ateto.conf import (
    ANKI_CONNECT,
    TEMPLATES_DELIMITER,
    TEMPLATES_EXTENSION,
    TEMPLATES_OUTPUT_PATH,
)
from ateto.data import load_data
from ateto.sync import request_anki
from ateto.utils import (
    get_cards,
    get_cards_paths,
    get_css_path,
    get_data_path,
    get_default_html_output,
    get_model_path,
    get_output_path,
    get_output_path_css,
)

# FIXME: there should be a better way ?
# If a cloze text contains the caracter "}" it will fail
CLOZE_REGEX = re.compile(r"\{\{c(?P<number>\d+)::(?P<raw_content>[^\}]+)\}\}")

Cloze = namedtuple("Cloze", ("field_name", "number", "value"))


class Note:
    """A Note, based on the anki data"""

    _id: int
    _fields: dict
    tags: List[str]
    model_name: str
    deck_name: str
    subdeck_name: str

    def __init__(
        self,
        fields: dict,
        noteId: int = -1,
        tags: Optional[List[str]] = None,
        modelName: str = "",
        deck_name: str = None,
        subdeck_name: str = None,
        **kwargs,
    ):
        """Instanciate from the keys of notes in JSON files"""

        self._id = noteId
        self._fields = {}

        for name, content in fields.items():
            try:
                # support the AnkiConnect result JSON
                self._fields[name] = content["value"]
            except TypeError:
                self._fields[name] = content

        self.tags = tags or []
        self.model_name = modelName
        self.deck_name = deck_name or "Deck Name"
        self.subdeck_name = subdeck_name or "Subdeck Name"

    def fields(self, clozes: Optional[List[Cloze]] = None, is_front=True) -> Dict:
        """Return fields with more informations"""
        all_fields = self._fields.copy()

        # Support of Anki "Special fields"
        all_fields["Tags"] = " ".join(self.tags)
        all_fields["Type"] = self.model_name
        all_fields["Deck"] = self.deck_name
        all_fields["Subdeck"] = self.subdeck_name

        # FIXME: support only one cloze
        if not clozes:
            clozes = self.list_clozes()

        for cloze in clozes:
            new_field = f"cloze:{cloze.field_name}"
            raw_content = all_fields.get(new_field, self._fields[cloze.field_name])

            try:
                text, hint = cloze.value.split("::")
            except ValueError:
                text = cloze.value
                hint = "[...]"

            if is_front:
                content = raw_content.replace(
                    f"{{{{c{cloze.number}::{cloze.value}}}}}", hint
                )
            else:
                content = raw_content.replace(
                    f"{{{{c{cloze.number}::{cloze.value}}}}}", text
                )

            all_fields[new_field] = content

        for field_name, value in self._fields.items():
            all_fields[f"type:{field_name}"] = value

            if "<" in value or "&" in value:
                all_fields[f"text:{field_name}"] = BeautifulSoup(
                    value, "html.parser"
                ).text
            else:
                all_fields[f"text:{field_name}"] = value

        field_names = list(all_fields.keys())
        for field_name in field_names:
            # dirty fix, should be a better solution
            for start_spaces in range(1, 3):
                for end_spaces in range(1, 3):
                    key = "".join((" " * start_spaces, field_name, " " * end_spaces))
                    all_fields[key] = all_fields[field_name]

        return all_fields

    def list_clozes(self) -> List[Cloze]:
        """Return each cloze deletions"""
        clozes = []

        for name, value in self._fields.items():
            results = list(CLOZE_REGEX.finditer(value))

            if not results:
                continue

            for result in results:
                groups = result.groupdict()

                if groups.get("number") != "1":
                    logging.error(
                        "Right now, only one Cloze deletion by Note is supported !"
                    )

                clozes.append(
                    Cloze(name, int(groups.get("number")), groups.get("raw_content"))
                )

        return clozes


def render_template(template: str, note: Note, is_front: bool = True) -> BeautifulSoup:
    """Return the content of the template with the note"""
    tester = TemplateTester(template, note.fields(is_front=is_front), "")
    soup = BeautifulSoup(tester.render(), "html.parser")

    content = soup.body
    content.name = "td"
    content.attrs["class"] = "card"

    return content


class Model:
    """A Model list everything we need to output a template"""

    path: Path

    def __init__(self, name_or_path: str | Path):
        if isinstance(name_or_path, Path):
            self.path = name_or_path
        else:
            self.path = get_model_path(name_or_path)

            if not self.path.is_dir():
                os.makedirs(self.path)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def _cards_paths(self) -> List[Path]:
        """Return the paths of cards in a model"""
        return get_cards_paths(self.name)

    @property
    def _css_path(self) -> Path:
        """Return the path of the CSS file"""
        return get_css_path(self.name)

    @property
    def _data_path(self) -> Path:
        return get_data_path(self.name)

    @property
    def output_path(self) -> Path:
        return get_output_path(self.name)

    @property
    def output_path_css(self) -> Path:
        return get_output_path_css(self.name)

    def get_notes(self) -> List[Note]:
        return [Note(**n) for n in load_data(self.name)]

    def create_output_files(self) -> None:
        """Create output dir and link css files"""
        os.makedirs(TEMPLATES_OUTPUT_PATH, exist_ok=True)
        try:
            shutil.copy(self._css_path, self.output_path_css)
        except (FileNotFoundError, FileExistsError):
            pass

    def get_anki_templates(self) -> Dict[str, Dict[str, str]]:
        """Return the cards templates, Front and Back"""
        return request_anki(
            ANKI_CONNECT.REQUESTS.MODEL_TEMPLATES, params={"modelName": self.name}
        )

    def export_templates(self, templates) -> None:
        """Get templates from Anki and save the files in models_export"""
        os.makedirs(self.path, exist_ok=True)
        for name, values in templates.items():
            html_path = (self.path / name).with_suffix(TEMPLATES_EXTENSION)
            with open(html_path, "w") as html_file:
                html_file.write(
                    "{Front}{td}{Back}".format(td=TEMPLATES_DELIMITER, **values)
                )

        css = request_anki(ANKI_CONNECT.REQUESTS.MODEL_STYLE, {"modelName": self.name})[
            "css"
        ]

        with open(self._css_path, "w") as cssfile:
            cssfile.write(css)

    def get_default_soup(self) -> BeautifulSoup:
        default_html = get_default_html_output()
        soup = BeautifulSoup(default_html, "html.parser")

        title = f'Output of note model "{self.name}"'
        soup.find("title").string = title
        soup.find("caption").string = title

        soup.find("link").attrs["href"] = self.output_path_css.name

        return soup

    def create_line(self, note: Note) -> BeautifulSoup:
        """Create a new table line for the `note` fields"""
        line = BeautifulSoup("", "html.parser")

        # We can use a URL like #nid00001 to debug a specific note
        titles_tr = line.new_tag(
            "tr",
            attrs={
                "class": "anki-template-tester-tr",
                "id": f"nid{note._id}",
            },
        )

        note_th = line.new_tag(
            "th", attrs={"class": "anki-template-tester-nid", "rowspan": 2}
        )
        note_link = line.new_tag(
            "a",
            attrs={
                "class": "anki-template-tester-link",
                "href": f"#nid{note._id}",
            },
        )
        note_link.string = f"nid:{note._id}"
        note_th.append(note_link)
        titles_tr.append(note_th)

        # now we can add a title for each card
        for card_path in self._cards_paths:
            for side in ("Front", "Back"):
                td = line.new_tag(
                    "td", attrs={"class": "anki-template-tester-card-name"}
                )
                name = card_path.name.removesuffix(TEMPLATES_EXTENSION)
                td.string = f"{name} — {side}"
                titles_tr.append(td)
        line.append(titles_tr)

        # and add the card templates
        cards_tr = line.new_tag("tr", attrs={"class": "anki-template-tester-tr"})
        for card_path in self._cards_paths:
            templates = get_cards(card_path)

            note._fields["Card"] = card_path.name.removesuffix(TEMPLATES_EXTENSION)

            is_front = True
            for template in templates:
                output = render_template(template, note, is_front)

                cards_tr.append(output)

                if is_front:
                    is_front = False

                    frontside = copy.copy(output)
                    frontside.name = "div"
                    frontside.attrs = {}

                    note._fields["FrontSide"] = str(frontside)
        line.append(cards_tr)

        return line

    def write_test_templates(self) -> str | BeautifulSoup:
        """Write an html output file with each notes and cards"""
        # read files

        notes = self.get_notes()
        if not notes:
            return ""

        # create files
        self.create_output_files()
        soup = self.get_default_soup()

        for note in notes:
            soup.table.append(self.create_line(note))

        with open(self.output_path, "w") as htmlfile:
            result = str(soup)
            result = re.sub(
                r"\[sound:[^\]]+\]",
                """<a class="replay-button soundLink" href="#" onclick="pycmd('play:a:0'); return false;">
    <svg class="playImage" viewBox="0 0 64 64" version="1.1">
        <circle cx="32" cy="32" r="29"></circle>
        <path d="M56.502,32.301l-37.502,20.101l0.329,-40.804l37.173,20.703Z"></path>
    </svg>
</a>""",
                result,
            )
            htmlfile.write(result)

        return soup
