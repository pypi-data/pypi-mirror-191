======================
Sphinx CL Domain Theme
======================

Official sphinx theme for the Common Lisp domain for sphinx
https://git.sr.ht/~rsl/sphinxcontrib-cldomain

Forked from `Sphinx Nameko Theme
<https://github.com/nameko/sphinx-nameko-theme>`_. Which was intern
forked from `Sphinx Readable Theme
<https://github.com/ignacysokolowski/sphinx-readable-theme>`_, and
combined with elements of the `Read The Docs
<https://github.com/snide/sphinx_rtd_theme>`_ theme.


Installation and setup
======================


Install from PyPI::

    $ pip install sphinx-cldomain-theme

And add this to your Sphinx ``conf.py``:

.. code-block:: python

    import sphinx_cldomain_theme

    html_theme_path = [sphinx_cldomain_theme.get_html_theme_path()]
    html_theme = 'cldomain'


Example
=======

The official `CL Domain
<https://sphinxcontrib-cldomain.russellsim.org/>`_ documentation uses
this theme.

License
=======

Sphinx CL Domain Theme is licensed under the MIT license.


Changelog
=========

Version 0.0.1
-------------

Initial fork
