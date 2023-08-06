import logging
from pathlib import Path

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape

from ateto.conf import (
    MEDIAS_SOURCE_PATH,
    MODELS_SOURCE_PATH,
    ROOT_PATH,
    SUPERTEMPLATES_COMMENT_END,
    SUPERTEMPLATES_COMMENT_START,
    SUPERTEMPLATES_IGNORED_SUFFIXES,
    SUPERTEMPLATES_MEDIAS_PATH,
    SUPERTEMPLATES_PATH,
    SUPERTEMPLATES_VARIABLE_END,
    SUPERTEMPLATES_VARIABLE_START,
)
from ateto.medias import link_models_medias, link_output_medias
from ateto.models import Model
from ateto.utils import get_models_dirs


def compile_test_templates(path_filter, verbose=False):
    """Write the templates."""
    compiled = []

    for model_dir in get_models_dirs(path_filter=path_filter):
        model = Model(model_dir)
        soup = model.write_test_templates()

        if verbose and soup:
            click.echo(f"  {model.name}")
        if soup:
            compiled.append(model)

    return compiled


def get_supertemplates_env(source_path):
    return Environment(
        loader=FileSystemLoader(source_path),
        autoescape=select_autoescape(),
        variable_start_string=SUPERTEMPLATES_VARIABLE_START,
        variable_end_string=SUPERTEMPLATES_VARIABLE_END,
        comment_start_string=SUPERTEMPLATES_COMMENT_START,
        comment_end_string=SUPERTEMPLATES_COMMENT_END,
    )


def compile_supertemplates(
    source_path: str | Path,
    output_path: str | Path,
    with_medias: bool = False,
    debug: bool = False,
):
    """Build jinja templates to an Anki template"""
    source_path = Path(source_path)
    output_path = Path(output_path)

    logging.debug(f"build templates of {source_path} into {output_path}")
    env = get_supertemplates_env(source_path)

    for model_path in source_path.iterdir():
        if not model_path.is_dir() or model_path.stem.startswith("_"):
            continue

        model_output = output_path / model_path.name
        output_path.mkdir(exist_ok=True)
        model_output.mkdir(exist_ok=True)

        logging.debug(f"Build model {model_path} into {model_output}")

        for card_path in model_path.iterdir():
            if card_path.suffix in SUPERTEMPLATES_IGNORED_SUFFIXES:
                continue

            logging.debug(f"Create card {card_path.name}")
            card_output = model_output / card_path.name

            template = env.get_template(str(card_path.relative_to(source_path)))

            with open(card_output, "w") as card_file:
                card_file.write(
                    template.render(
                        model=model_path.name, card=card_path.stem, is_debug=debug
                    )
                )

    if with_medias:
        for file_path in SUPERTEMPLATES_MEDIAS_PATH.iterdir():
            relative_path = file_path.relative_to(source_path)
            template = env.get_template(str(relative_path))
            with open(MEDIAS_SOURCE_PATH / file_path.name, "w") as export_file:
                export_file.write(template.render(is_debug=debug))


def compile_all(
    path_filter: str,
    supertemplates: bool = False,
    with_medias: bool = False,
    with_images: bool = False,
    debug: bool = False,
    verbose: bool = False,
):
    """Compile test template and supertemplates eventually.

    Then link medias or images if we want."""
    if supertemplates:
        if verbose:
            click.secho("Build supertemplates", fg="yellow", bold=True)
        compile_supertemplates(SUPERTEMPLATES_PATH, MODELS_SOURCE_PATH, debug)

    if verbose:
        click.secho("Compile templates and data in sample files", fg="green", bold=True)
    compiled = compile_test_templates(path_filter, verbose=verbose)
    if not compiled:
        click.echo("  Nothing found, try to sync models or populate date")

    if with_medias:
        link_models_medias()

    if with_images:
        link_output_medias()
