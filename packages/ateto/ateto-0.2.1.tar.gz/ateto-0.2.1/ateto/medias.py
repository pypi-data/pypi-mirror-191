import os
import shutil
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from bs4 import BeautifulSoup

from ateto.conf import (
    ANKI_COLLECTION_PATH,
    MEDIAS_EXTENSIONS,
    MEDIAS_SOURCE_PATH,
    TEMPLATES_OUTPUT_PATH,
)


def list_medias_filenames(
    listing_path: Path = MEDIAS_SOURCE_PATH,
    allowed_extensions: Iterable = MEDIAS_EXTENSIONS,
) -> List:
    """List medias filenames in listing_path."""
    filenames = []

    try:
        for media in listing_path.iterdir():
            if media.suffix.strip(".") in allowed_extensions:
                filenames.append(media.name)
    except FileNotFoundError:
        pass

    return filenames


def copy_media(
    source_path: Path,
    destination_path: Path,
) -> bool:
    """Copy and touch the destination_path"""
    try:
        shutil.copyfile(source_path, destination_path)
        destination_path.touch(exist_ok=True)
        return True
    except FileNotFoundError:
        return False


def copy_medias(
    source_path: Path,
    destination_path: Path,
    allowed_extensions: Iterable,
    list_from_source: bool = False,
) -> Dict[str, bool]:
    """Copy medias from source to destination

    Medias are listed from source or destination, depending
    on the value of list_from_source.
    """

    listing_path = source_path if list_from_source else destination_path
    filenames = list_medias_filenames(listing_path, allowed_extensions)

    results = {}
    for filename in filenames:
        results[filename] = copy_media(
            source_path / filename, destination_path / filename
        )

    destination_path.touch(exist_ok=True)
    return results


def copy_models_medias(
    collection_path: Optional[Path] = ANKI_COLLECTION_PATH,
    allowed_extensions: Optional[Iterable] = MEDIAS_EXTENSIONS,
    export_from_anki: bool = True,
) -> Dict[str, bool]:
    """Copy medias between collection path and models_export.

    Always list allowed medias in models_export and then :

    * export them from Anki collection (export_from_anki=True)
    * import them in Anki collection (export_from_anki=False)
    """
    source = collection_path
    destination = MEDIAS_SOURCE_PATH

    if not export_from_anki:
        source, destination = destination, source

    return copy_medias(
        source, destination, allowed_extensions, list_from_source=not export_from_anki
    )


def import_medias_in_anki():
    copy_models_medias(export_from_anki=False)


def export_medias_from_anki() -> Dict[str, bool]:
    return copy_models_medias(export_from_anki=True)


def list_images_in_page(file_path: Path) -> set:
    """List images src in HTML page"""
    medias = set()

    with open(file_path) as html_file:
        soup = BeautifulSoup(html_file.read(), "html.parser")
        for image in soup.find_all("img"):
            medias.add(image["src"])

    return medias


def list_images_in_output_pages() -> set:
    """List all images src in html_output files"""
    medias = set()

    for file in TEMPLATES_OUTPUT_PATH.iterdir():
        if file.suffix == ".html":
            medias = medias | list_images_in_page(file)

    return medias


def link_models_medias() -> List:
    """Symlink medias in `models_export/_medias`"""
    links = []

    for media_name in list_medias_filenames():
        try:
            source = MEDIAS_SOURCE_PATH / media_name
            destination = TEMPLATES_OUTPUT_PATH / media_name
            os.symlink(source, destination)
            links.append(media_name)
        except FileExistsError:
            pass

    return links


def link_image_from_anki(filename: str) -> bool:
    """Symlink an image from anki to html_output"""
    source = ANKI_COLLECTION_PATH / filename
    try:
        os.symlink(source, TEMPLATES_OUTPUT_PATH / filename)
        return True
    except FileExistsError:
        return False


def link_images_from_anki(ignored_filenames: Optional[Iterable] = ()) -> List[str]:
    """Link all images in output pages to html_output."""
    links = []
    for filename in list_images_in_output_pages():
        # ignore medias in `_medias` dir
        if filename in ignored_filenames:
            continue

        if link_image_from_anki(filename):
            links.append(filename)

    return links


def link_output_medias() -> List[Tuple[str, str]]:
    """Symlink every medias used in html_output."""
    links = link_models_medias()
    new_links = link_images_from_anki(links)

    result = []
    for link in links:
        result.append((link, "models_export"))
    for link in new_links:
        result.append((link, "Anki"))

    return result
