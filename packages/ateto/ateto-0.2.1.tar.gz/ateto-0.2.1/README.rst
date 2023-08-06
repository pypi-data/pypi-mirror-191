Ateto : Anki templates tools
============================

`ateto` is a set of tools to write templates outside of Anki.

Why ?
-----

It's a collection of scripts I try to reorganize. It started with the Anki
addon called `Templates Import / Export
<https://ankiweb.net/shared/info/712027367>`_, a python tool, `Anki Template
Tester <https://github.com/klieret/anki-template-tester>`_ and now ... look at
this ! Yes, the name is not much creative.

In short, it can :

* **export models templates** (HTML and CSS) from Anki to
  files (inside `$XDG_DATA_HOME/ateto`)
* take some note as samples from Anki and **test the templates**
  with them (producing a file like `html_output/Basic.html`)
* **import** models templates and some shared medias (like `_base.css`)
  to Anki

From the command line, with something like this::

  ateto sync # export from anki
  ateto compile # write test templates files
  ateto sync -i # import in anki

There is also a shorthand command called ``ateto`` and a "watcher". It's useful
to compile test templates at each modification::

  ateto watch

Installation
------------

This should work::

  python -m pip install ateto

Requirements
~~~~~~~~~~~~

Right now it depends on the `AnkiConnect
<https://ankiweb.net/shared/info/2055492159>`_ Anki addon and
anki-templates-tester that I put inside this project to keep things simple.

Default working directory
-------------------------

The default working directory is `$XDG_DATA_HOME/ateto` (something like
`~/.local/share/ateto`). The templates of each Anki "note type" (or "model")
are stored in `models_export`.

Simple how to
-------------

Sync templates with Anki
~~~~~~~~~~~~~~~~~~~~~~~~

First, while Anki is running, we need to export models templates with
AnkiConnect::

  ateto sync

If we change some files in `models_export`, we can import them in Anki with::

  ateto sync -i

Compile test templates
~~~~~~~~~~~~~~~~~~~~~~

We need to get some sample data from Anki and then compile templates. But
first, open Anki and tag some notes with `template_test_data`::

  ateto populate
  ateto compile

Images and CSS or JS assets
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If there is missing images run::

  ateto link

All files under the `models_export/_medias` directory will be linked in
`html_output` with `compile -m`::

  ateto compile -m

But you have to create them first.

Supertemplates
~~~~~~~~~~~~~~

`models_export` contains template export of Anki notes templates. It's basic
HTML. There is "supertemplates" : it's Jinja2 templates that we can use to
generate the models, they are in `supertemplates` folder.

To build the supertemplates use `-s` option with `compile`::

  ateto compile -s

HTML and CSS files in supertemplates are processed, then `models_export` are
converted to `html_output`.

Watcher
~~~~~~~

It's my favorite part. When I'm working on some templates, I want modifications
to be automatically compiled in templates and output HTML some I use `watch`
command::

  ateto watch

And I want it all, supertemplates, medias and images. I want them to be
imported in Anki too. Images are only linked when starting, not watched ::

  ateto watch -ai

More
----

Debug mode
~~~~~~~~~~

`watch` and `compile` commands can be run with debug mode (`-d` option).
This will run supertemplates with a context where `is_debug=True`. It's
useful to debug AnkiDroid with something like this in templates files ::

  {% if is_debug %}
    <script src="https://cdn.jsdelivr.net/npm/eruda"></script>
    <script>eruda.init();</script>
  {% endif %}

File tree
~~~~~~~~~

So at the end, in `$XDG_DATA_HOME`, we have 4 main folders ::

* /supertemplates

  * ModelName/ directories

    * .jinja files
    * .html files
    * style.css file

  * _medias/ directory (optional)

    * .css files
    * .js files

* /models_export

  * ModelName/ directories

    * CardName.html files
    * style.css file

  * _medias/ directory (optional)

    * .css files
    * .js files

* /data

  * ModelName.yaml files
  * ModelName_override.yaml optional files

* /html_output

  * ModelName.html files
  * ModelName.css files
  * .css files linked from models_export/_medias
  * .js files linked from models_export/_medias
  * .png, .jpg, etc. files linked from anki_collection

The content of ``supertemplates`` is only created by hand and
compiled into ``models_export``.

All the content of ``models_export`` is synced with Anki (Ankiconnect). _medias
are treated with a special procedure.

The content of ``data`` is populated from Anki. _override.yaml files are
created by hand if necessary.

``html_output`` is the result of different actions :

* ModelName.html and ModelName.css files are the result of ``models_export``
  and ``data`` files
* others CSS or JS are linked to ``models_export/_medias``
* images are linked to the Anki collection
