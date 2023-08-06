"""Sphinx CLDomain Theme.

A fork of https://github.com/nameko/sphinx-nameko-theme which was a
a fork of https://github.com/ignacysokolowski/sphinx-readable-theme for use
in CLDomain (https://sphinxcontrib-cldomain.russellsim.org/)

"""

import os


def get_html_theme_path():
    """Return path to directory containing package theme."""
    return os.path.abspath(os.path.dirname(__file__))
