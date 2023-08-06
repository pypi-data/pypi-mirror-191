import logging
import time
from pathlib import Path
from typing import Callable

import click
from jinja2.exceptions import TemplateNotFound
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from ateto.conf import (
    MEDIAS_SOURCE_PATH,
    MODELS_SOURCE_PATH,
    NOTES_DATA,
    SUPERTEMPLATES_PATH,
)
from ateto.medias import link_models_medias
from ateto.models import Model
from ateto.sync import import_all_templates
from ateto.templates import (
    compile_supertemplates,
    compile_test_templates,
)

TIMEOUT = 2


def recursive_schedule(event_handler: Callable, observer: Observer, path: Path) -> None:
    """To watch symlinks"""
    if path.is_symlink():
        observer.schedule(event_handler, path.resolve())

    for subpath in path.iterdir():
        try:
            recursive_schedule(event_handler, observer, subpath)
        except NotADirectoryError:
            pass


class FileSystemEventHandlerWorkaround(FileSystemEventHandler):
    def __init__(self):
        self.last_trigger = time.time()

    def on_any_event(self, event):
        if time.time() - self.last_trigger < TIMEOUT:
            return

        self.run()
        self.last_trigger = time.time()


class CompileHandler(FileSystemEventHandlerWorkaround):
    """Compile test templates.

    If import_in_anki==True, import them in Anki with AnkiConnect"""

    def __init__(
        self,
        path_filter: str = "",
        do_supertemplates: bool = False,
        with_medias: bool = False,
        import_in_anki: bool = False,
        debug: bool = False,
    ):
        super().__init__()
        self.path_filter = path_filter
        self.do_supertemplates = do_supertemplates
        self.with_medias = with_medias
        self.import_in_anki = import_in_anki
        self.debug = debug

    def run(self):
        """Manage compilation and import in anki"""
        if self.do_supertemplates:
            click.echo("Output supertemplates to models_export")

            try:
                compile_supertemplates(
                    SUPERTEMPLATES_PATH,
                    MODELS_SOURCE_PATH,
                    with_medias=self.with_medias,
                    debug=self.debug,
                )
            except TemplateNotFound as error:
                click.secho(f"  Erreur: {error}", color="red")
        else:
            click.echo("Write test templates in html_output")
        compile_test_templates(self.path_filter)

        if self.with_medias:
            link_models_medias()

        if self.import_in_anki:
            import_all_templates(with_medias=self.with_medias)


def watch_input(
    path_filter: str = "",
    do_supertemplates: bool = False,
    import_in_anki: bool = False,
    with_medias: bool = False,
    debug: bool = False,
) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    observer = Observer(timeout=TIMEOUT)
    compile_handler = CompileHandler(
        path_filter, do_supertemplates, with_medias, import_in_anki, debug
    )

    if import_in_anki:
        import_all_templates(with_medias=with_medias)

    if path_filter:
        paths = list(MODELS_SOURCE_PATH.glob(path_filter))

        if do_supertemplates:
            paths.extend(list(SUPERTEMPLATES_PATH.glob(path_filter)))

        paths.extend(NOTES_DATA.glob(path_filter))

        for path in paths:
            observer.schedule(compile_handler, path)

        if with_medias:
            observer.schedule(compile_handler, MEDIAS_SOURCE_PATH)
    else:
        observer.schedule(compile_handler, MODELS_SOURCE_PATH, recursive=True)
        observer.schedule(compile_handler, NOTES_DATA)

        if do_supertemplates:
            observer.schedule(compile_handler, SUPERTEMPLATES_PATH, recursive=True)

    observer.start()

    try:
        while observer.is_alive():
            time.sleep(TIMEOUT)
    finally:
        observer.stop()
        observer.join()
