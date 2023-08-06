"""Ateto : anki templates tools

It is a set of tools to export/import templates
and test/edit them outside of Anki
"""
import click
from jinja2.exceptions import TemplateNotFound

from ateto.conf import MEDIAS_SOURCE_PATH, MODELS_SOURCE_PATH, ROOT_PATH
from ateto.data import populate_models_data
from ateto.medias import export_medias_from_anki, link_output_medias
from ateto.sync import (
    export_templates,
    import_all_templates,
    import_medias_in_anki,
)
from ateto.templates import compile_all
from ateto.watcher import watch_input


@click.group()
def cli():
    """Anki templates tools main command"""


@click.command()
@click.option("-f", "--filter", "path_filter", default="*")
@click.option(
    "-s/-S", "--supertemplates/--no-supertemplates", "do_supertemplates", default=False
)
@click.option("-m/-M", "--medias/--no-medias", default=False)
@click.option("-l/-L", "--link-images/--no-link-images", default=False)
@click.option(
    "-i/-I",
    "--import/--no-import",
    "import_in_anki",
    default=False,
    help="Import the templates in Anki",
)
@click.option("-a/-A", "--all/--no-all", "all_", default=False)
@click.option("-d/-D", "--debug/--no-debug", default=False)
def watch(
    path_filter: str,
    do_supertemplates: bool,
    medias: bool,
    link_images: bool,
    all_: bool,
    import_in_anki: bool,
    debug: bool,
):
    """Watch for modifications and output the templates HTML"""

    if all_:
        do_supertemplates = True
        medias = True
        link_images = True

    path = (MODELS_SOURCE_PATH / path_filter).resolve()

    click.secho("Watch for modifications in :", fg="green", bold=True)
    click.echo(f"    {ROOT_PATH}")
    click.secho(
        "If there is a change, will output every templates in :", fg="green", bold=True
    )
    click.echo(f"    {path}")

    try:
        compile_all(
            path_filter, do_supertemplates, medias, link_images, debug, verbose=True
        )
    except TemplateNotFound as error:
        click.secho(f"  fichier manquant : {error}", color="red")

    if import_in_anki:
        import_medias_in_anki()

    watch_input(
        path_filter=path_filter,
        do_supertemplates=do_supertemplates,
        with_medias=medias,
        import_in_anki=import_in_anki,
        debug=debug,
    )


@click.command()
@click.option("-f", "--filter", "model_filter", default="")
@click.option("-t", "--tag", default="")
@click.option("-q", "--query", default="")
def populate(model_filter: str, tag: str, query: str):
    """Dump the Anki notes tagged {DEFAULT_TEST_TAG} in `data` dir"""
    click.secho("Dump Anki notes", fg="green", bold=True)

    populate_kwargs = {}

    if model_filter:
        populate_kwargs["model_filter"] = model_filter
    if tag:
        populate_kwargs["tag"] = tag
    if query:
        populate_kwargs["query"] = query

    notes_by_models = populate_models_data(**populate_kwargs)

    for model_name, notes in notes_by_models.items():
        click.echo(
            " ".join(
                [
                    model_name,
                    ":",
                    click.style(
                        f"{len(notes): 2} notes", fg="green" if notes else "yellow"
                    ),
                ]
            )
        )


@click.command(name="compile")
@click.option("-f", "--filter", "model_filter", default="*")
@click.option("-s/-S", "--supertemplates/--no-supertemplates", default=False)
@click.option("-m/-M", "--medias/--no-medias", default=False)
@click.option("-l/-L", "--link-images/--no-link-images", default=False)
@click.option("-a/-A", "--all/--no-all", "all_", default=False)
@click.option("-d/-D", "--debug/--no-debug", default=False)
def compile_(
    model_filter: str,
    supertemplates: bool,
    medias: bool,
    link_images: bool,
    debug: bool,
    all_: bool,
):
    """Compile template and eventually do more.

    Can compile supertemplates, link medias and images.
    The --debug option is passed to the context of supertemplates"""
    if all_:
        supertemplates = True
        medias = True
        link_images = True

    try:
        compile_all(
            model_filter, supertemplates, medias, link_images, debug, verbose=True
        )
    except TemplateNotFound as error:
        click.secho(f"  fichier manquant : {error}", color="red")


@click.command()
@click.option("-e/-i", "--export/--import", default=True)
@click.option(
    "-m/-M", "--medias/--no-medias", default=False, help="sync _medias folder"
)
@click.option("-t/-T", "--templates/--no-templates", default=True)
@click.option("-c/-C", "--confirm/--no-confirm", default=True)
def sync(export, medias, templates, confirm):
    """Manage import/export between Anki and models_export

    This command export templates (and/or medias) from Anki
    to models_export. With -i option, it's the opposite :
    it imports templates in Anki.

    By default, only templates are synced (HTML and CSS). It
    can be combined with medias (-m). Medias can be synced
    without templates with -mT.
    """
    if not (templates or medias):
        click.secho("Nothing will happen, select -m or -t !", fg="red")
        return

    operation_name = "Export" if export else "Import"
    source, destination = ("Anki", "models_export")
    direction = "to" if export else "in"
    if not export:
        source, destination = destination, source

    what = []
    if templates:
        what.append("templates")
    if medias:
        what.append("medias")
    scope = " and ".join(what)

    click.secho(
        f"{operation_name} {scope} from {source} {direction} {destination}",
        fg="green",
        bold=True,
    )

    if confirm:
        click.confirm("Do you want to continue?", abort=True)

    if export:
        if templates:
            export_templates()
        if medias:
            for media, result in export_medias_from_anki().items():
                if result:
                    click.echo(f"* {media} copied from Anki collection")
                else:
                    click.secho(
                        f"* {media} not found in Anki collection", fg="red", bold=True
                    )
    else:
        if templates:
            import_all_templates()
        if medias:
            import_medias_in_anki()


@click.command()
def link():
    """Link medias in Anki collection to the html_output"""

    click.secho(
        "Link files from collection or models_export to html_output",
        fg="green",
        bold=True,
    )

    links = link_output_medias()
    for media, source in links:
        click.echo(f"  link {media} from {source} to html_output")
    if not links:
        click.echo("  Nothing to link")


@click.command()
@click.argument("media_names", nargs=-1)
def add_medias(media_names):
    """Create an empty file in models_export/_medias"""
    MEDIAS_SOURCE_PATH.mkdir(exist_ok=True)

    for media_name in media_names:
        path = MEDIAS_SOURCE_PATH / media_name
        click.echo(f"Check for {path}")
        path.touch()


cli.add_command(watch)
cli.add_command(populate)
cli.add_command(compile_)
cli.add_command(link)
cli.add_command(sync)
cli.add_command(add_medias)

if __name__ == "__main__":
    cli()
