# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ateto']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1,<4.0',
 'beautifulsoup4>=4.1,<5.0',
 'click>=8.1,<9.0',
 'pyyaml>=6.0,<7.0',
 'requests>=2.28,<3.0',
 'watchdog>=2.2,<3.0',
 'xdg>=5.1,<6.0']

entry_points = \
{'console_scripts': ['ateto = ateto.cli:cli']}

setup_kwargs = {
    'name': 'ateto',
    'version': '0.2.1',
    'description': 'This is a set of tools to write templates outside of Anki.',
    'long_description': 'Ateto : Anki templates tools\n============================\n\n`ateto` is a set of tools to write templates outside of Anki.\n\nWhy ?\n-----\n\nIt\'s a collection of scripts I try to reorganize. It started with the Anki\naddon called `Templates Import / Export\n<https://ankiweb.net/shared/info/712027367>`_, a python tool, `Anki Template\nTester <https://github.com/klieret/anki-template-tester>`_ and now ... look at\nthis ! Yes, the name is not much creative.\n\nIn short, it can :\n\n* **export models templates** (HTML and CSS) from Anki to\n  files (inside `$XDG_DATA_HOME/ateto`)\n* take some note as samples from Anki and **test the templates**\n  with them (producing a file like `html_output/Basic.html`)\n* **import** models templates and some shared medias (like `_base.css`)\n  to Anki\n\nFrom the command line, with something like this::\n\n  ateto sync # export from anki\n  ateto compile # write test templates files\n  ateto sync -i # import in anki\n\nThere is also a shorthand command called ``ateto`` and a "watcher". It\'s useful\nto compile test templates at each modification::\n\n  ateto watch\n\nInstallation\n------------\n\nThis should work::\n\n  python -m pip install ateto\n\nRequirements\n~~~~~~~~~~~~\n\nRight now it depends on the `AnkiConnect\n<https://ankiweb.net/shared/info/2055492159>`_ Anki addon and\nanki-templates-tester that I put inside this project to keep things simple.\n\nDefault working directory\n-------------------------\n\nThe default working directory is `$XDG_DATA_HOME/ateto` (something like\n`~/.local/share/ateto`). The templates of each Anki "note type" (or "model")\nare stored in `models_export`.\n\nSimple how to\n-------------\n\nSync templates with Anki\n~~~~~~~~~~~~~~~~~~~~~~~~\n\nFirst, while Anki is running, we need to export models templates with\nAnkiConnect::\n\n  ateto sync\n\nIf we change some files in `models_export`, we can import them in Anki with::\n\n  ateto sync -i\n\nCompile test templates\n~~~~~~~~~~~~~~~~~~~~~~\n\nWe need to get some sample data from Anki and then compile templates. But\nfirst, open Anki and tag some notes with `template_test_data`::\n\n  ateto populate\n  ateto compile\n\nImages and CSS or JS assets\n~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nIf there is missing images run::\n\n  ateto link\n\nAll files under the `models_export/_medias` directory will be linked in\n`html_output` with `compile -m`::\n\n  ateto compile -m\n\nBut you have to create them first.\n\nSupertemplates\n~~~~~~~~~~~~~~\n\n`models_export` contains template export of Anki notes templates. It\'s basic\nHTML. There is "supertemplates" : it\'s Jinja2 templates that we can use to\ngenerate the models, they are in `supertemplates` folder.\n\nTo build the supertemplates use `-s` option with `compile`::\n\n  ateto compile -s\n\nHTML and CSS files in supertemplates are processed, then `models_export` are\nconverted to `html_output`.\n\nWatcher\n~~~~~~~\n\nIt\'s my favorite part. When I\'m working on some templates, I want modifications\nto be automatically compiled in templates and output HTML some I use `watch`\ncommand::\n\n  ateto watch\n\nAnd I want it all, supertemplates, medias and images. I want them to be\nimported in Anki too. Images are only linked when starting, not watched ::\n\n  ateto watch -ai\n\nMore\n----\n\nDebug mode\n~~~~~~~~~~\n\n`watch` and `compile` commands can be run with debug mode (`-d` option).\nThis will run supertemplates with a context where `is_debug=True`. It\'s\nuseful to debug AnkiDroid with something like this in templates files ::\n\n  {% if is_debug %}\n    <script src="https://cdn.jsdelivr.net/npm/eruda"></script>\n    <script>eruda.init();</script>\n  {% endif %}\n\nFile tree\n~~~~~~~~~\n\nSo at the end, in `$XDG_DATA_HOME`, we have 4 main folders ::\n\n* /supertemplates\n\n  * ModelName/ directories\n\n    * .jinja files\n    * .html files\n    * style.css file\n\n  * _medias/ directory (optional)\n\n    * .css files\n    * .js files\n\n* /models_export\n\n  * ModelName/ directories\n\n    * CardName.html files\n    * style.css file\n\n  * _medias/ directory (optional)\n\n    * .css files\n    * .js files\n\n* /data\n\n  * ModelName.yaml files\n  * ModelName_override.yaml optional files\n\n* /html_output\n\n  * ModelName.html files\n  * ModelName.css files\n  * .css files linked from models_export/_medias\n  * .js files linked from models_export/_medias\n  * .png, .jpg, etc. files linked from anki_collection\n\nThe content of ``supertemplates`` is only created by hand and\ncompiled into ``models_export``.\n\nAll the content of ``models_export`` is synced with Anki (Ankiconnect). _medias\nare treated with a special procedure.\n\nThe content of ``data`` is populated from Anki. _override.yaml files are\ncreated by hand if necessary.\n\n``html_output`` is the result of different actions :\n\n* ModelName.html and ModelName.css files are the result of ``models_export``\n  and ``data`` files\n* others CSS or JS are linked to ``models_export/_medias``\n* images are linked to the Anki collection\n',
    'author': 'bisam',
    'author_email': 'bisam@r4.re',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://codeberg.org/bisam/ateto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
