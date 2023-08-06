.. mistery documentation master file, created by
   sphinx-quickstart on Fri Jan 27 22:18:53 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

*mistery*
=========

*mistery* (c.f. "MIST query") is a Python module for retrieving data
from the `MESA Isochrones and Stellar Tracks
<http://waps.cfa.harvard.edu/MIST/>`_ (MIST) database of stellar
models.  The module allows you to fetch data by submitting requests to
the web interpolator.  It is intended as a lightweight teaching tool
that lets students access real-world stellar model data with
minimal effort.  If you're
doing intensive scientific work, you may prefer to access the data in
other ways (e.g. by downloading `packaged model
grids <http://waps.cfa.harvard.edu/MIST/model_grids.html>`_).

Installation
------------

.. code-block::

   pip install mistery

Quickstart
----------

You can fetch a single track with :py:meth:`mistery.get_track`. e.g.

.. code-block:: python

    track = mistery.get_track(M=2.0, FeH=-0.5)

The data is returned as a `structured NumPy array <https://numpy.org/doc/stable/user/basics.rec.html>`_.
i.e. you can access the columns by name rather than number.  To see a list of names, use

.. code-block:: python

    print(track.dtype.names)

and access columns with statements like ``track['log_L']``.

You can download tracks for multiple masses in one call by instead
passing an iterable of masses to :py:meth:`mistery.get_tracks`, e.g.

.. code-block:: python

    tracks = mistery.get_tracks(Ms=[1.5, 3.0], FeH=-0.3)

The data in ``tracks`` is now a list of tracks and can be accessed
with e.g. ``tracks[0]['log_L']``.

Similar functions are available for isochrones.  :py:meth:`mistery.get_isochrone`
fetches one isochrone; :py:meth:`mistery.get_isochrones` fetches isochrones for
multiple ages.

All functions take additional keyword arguments that correspond partly
(though neither perfectly nor entirely) to fields in the web forms on
the MIST website.

The :ref:`gallery <gallery>` contains more advanced examples.  The
:ref:`api` has detailed documentation for each function.

Contributing
------------

The development version of *mistery* is hosted in `a GitLab repository
<https://gitlab.com/warrickball/mistery/>`_.  If you have a problem,
you can open `an issue
<https://gitlab.com/warrickball/mistery/issues>`_, in which you should
try to explain as completely as possible what you tried to do, what
happened instead, and the environment in which you tried (e.g. Python
version, how you installed *mistery*, etc).

If you want to fix a bug, you are welcome to do so by opening a merge
request.  Bear in mind that *mistery* aims to do little more than
fetch MIST data, and even then is knowingly incomplete.  I don't plan
to add more features than retrieving tracks and isochrones.

.. toctree::
   :maxdepth: 2
   :caption: Contents

   gallery
   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
