#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('..'))


# -- Project information -----------------------------------------------------

project = 'biom_aid'
copyright = '2020-2021, Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand'
author = 'Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand'


# -- General configuration ---------------------------------------------------

master_doc = 'index'

show_authors = True

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc.typehints',
    'sphinx.ext.todo',
    # 'sphinx.ext.autodoc',
    'sphinx.ext.inheritance_diagram',
    # 'autoapi.sphinx',
    # 'autoapi.extension',
    'sphinxcontrib.inkscapeconverter',
]

# Temporary settings, only for core developpers
todo_include_todos = True

autodoc_typehints = 'description'

autoapi_dirs = [
    '..',
]
autoapi_ignore = [
    '*migration*',
    '*devtool*',
    '*tests*',
    '*/manage.py',
]

suppress_warnings = [
    "autoapi",
]

autoapi_keep_files = True


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'fr'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sizzle'
globaltoc_depth = 3


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for LateX/pdf output -------------------------------------------------

latex_documents = [
    (
        'index',
        project + '.tex',
        "Documentation complète BIOM_AID",
        author.replace(',', ' \\and'),
        'manual',
        False,
    ),
]

latex_elements = {
    'maxlistdepth': '10',
}
