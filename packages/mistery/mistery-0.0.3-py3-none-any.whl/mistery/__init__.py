#!/usr/bin/env python3

import io
from urllib.request import urlopen
from zipfile import ZipFile
import requests
import numpy as np
import numpy.lib.recfunctions as rfn

BASE_URL = 'http://waps.cfa.harvard.edu/MIST/'

PHOTOMETRY_OPTIONS = {
    'CFHTugriz',
    'DECam',
    'HST_ACSHR',
    'HST_ACSWF',
    'HST_WFC3',
    'HST_WFPC2',
    'GALEX',
    'JWST',
    'LSST',
    'PanSTARRS',
    'SDSSugriz',
    'SkyMapper',
    'SPITZER',
    'SPLUS',
    'HSC',
    'IPHAS',
    'Swift',
    'UBVRIplus',
    'UKIDSS',
    'UVIT',
    'VISTA',
    'WashDDOuvby',
    'WFIRST',
    'WISE',
}


def get_track(M=1.0, **kwargs):
    """Returns a single evolutionary track from the MIST database with
    mass ``M`` (in solar units) and other keywords options that are
    passed to :py:meth:`get_tracks` (e.g. ``FeH``).  The
    function really just calls :py:meth:`get_tracks` with ``Ms=[M]``
    and returns a single NumPy structured array, rather than a list
    of them.  See :py:meth:`get_tracks` for more details.
    """
    return get_tracks(Ms=[M], **kwargs)[0]


def get_tracks(Ms=[1.0], FeH=0.0, vvcrit=0.0, Av=0.0, photometry=None):
    """Returns a list of evolutionary tracks from the MIST database.
    The script makes the PHP request, infers the archive's filename,
    decompresses it, combines the theoretical and photometry data if
    necessary and returns a list of NumPy structured arrays.  You can
    get the list of column names with e.g. ::

        tracks = mistery.get_tracks(Ms=[1.0, 2.0], FeH=-0.5)
        print(tracks[0].dtype.names)

    Parameters
    ----------
    Ms: iterable of floats
        Masses of the desired tracks, in solar units.
    FeH: float
        Metallicity [Fe/H] of the tracks.
    vvcrit: float, 0.0 or 0.4 only
        ZAMS rotation rate of the tracks, relative to critical.
    Av: float
        Extinction coefficient.
    photometry: None or str
        Name of the table of photometric bands to
        include. e.g. ``'UBVRIplus'``.
        See :ref:`tables` for all options.

    Returns
    -------
    tracks: list of NumPy structured arrays
        List containing the evolutionary tracks, in the same order as
        ``Ms``.  Always includes the 77 columns of theoretical data
        and also includes photometry if ``photometry`` is not
        ``None``.

    """
    # construct dict first because it catches type errors in arguments
    data = {
        'version': '1.2',
        'v_div_vcrit': 'vvcrit%.1f' % vvcrit,
        'mass_type': 'list',
        'mass_value': '',
        'mass_range_low': '',
        'mass_range_high': '',
        'mass_range_delta': '',
        'mass_list': ' '.join(['%g' % M for M in Ms]),
        'new_met_value': '%g' % FeH,
        'output_option': 'theory',
        'output': 'UBVRIplus',
        'Av_value': '%g' % Av
    }

    assert all([0.1 <= M <= 300 for M in Ms]), "all Ms must be between 0.1 and 300"
    assert -4 <= FeH <= 0.5, "FeH must be between -4.0 and +0.5"
    assert vvcrit in {0.0, 0.4}, "vvcrit must be 0.0 or 0.4"
    assert 0 <= Av <= 6, "Av must be between 0 and 6"
    if photometry is not None:
        assert photometry in PHOTOMETRY_OPTIONS, "invalid photometry option '%s'" % photometry

    # choosing a mass more precisely than 0.0001 Msun causes a variety of issues
    if any([np.abs(M-np.round(M, 4)) > 1e-7 for M in Ms]):
        raise ValueError("mass cannot be more precise than 0.0001 Msun")

    if photometry is not None:
        data['output_option'] = 'photometry'
        data['output'] = photometry

    r = requests.post(
        BASE_URL+'track_form.php',
        data=data
    )

    filename = r.text[18:48]

    # hacked together based on
    # https://stackoverflow.com/a/952834
    f = ZipFile(io.BytesIO(urlopen(BASE_URL + filename).read()))

    tracks = []
    for M in Ms:
        basename = './%07iM.track.eep' % np.round(M*1e4)
        track = np.genfromtxt(f.read(basename).decode().split('\n'),
                              skip_header=11, names=True, dtype=None)

        # if we request photometry, it's delivered in a separate file in the zip
        # so here we handle reading it alongside the relevant track
        # then joining the data by first dropping everything already in the track
        # then merging on star_age, which is the first column in both files
        if photometry is not None:
            cmd = np.genfromtxt(f.read(basename + '.cmd').decode().split('\n'),
                                skip_header=14, names=True, dtype=None)
            cmd = rfn.drop_fields(cmd, track.dtype.names[1:])
            track = rfn.join_by('star_age', track, cmd, jointype='inner', usemask=False)

        tracks.append(track)

    return tracks


def get_isochrone(t=1.0, **kwargs):
    """Returns a single isochrone from the MIST database with
    age ``t`` (in Gyr) and other keywords options that are
    passed to :py:meth:`get_isochrones` (e.g. ``FeH``).  The
    function really just calls :py:meth:`get_isochrones` with ``ts=[t]``
    and returns a single NumPy structured array, rather than a list
    of them.  See :py:meth:`get_isochrones` for more details.
    """
    return get_isochrones(ts=[t], split=False, **kwargs)


def get_isochrones(ts=[1.0], split=True, FeH=0.0, vvcrit=0.0, Av=0.0, theory='basic',
                   photometry=None):
    """Returns a set of isochrones from the MIST database.  The script
    makes the PHP request, infers the filename, and returns a list of
    NumPy structured arrays.  You can get the list of column names
    with e.g. ::

        isochrones = mistery.get_isochrones(ts=[0.3, 1.3], FeH=-0.25)
        print(isochrones[0].dtype.names)

    The data is returned in a single ``.iso`` file, which is split up
    into a list of arrays for each age if ``split=True``.  Otherwise,
    a single array is returned that contains all the isochrones.

    Parameters
    ----------
    ts: iterable of floats
        Ages of the desired isochrones, in billions of years (Gyr).
    split: bool
        If ``True``, return a list of arrays corresponding to each age
        in ``ts``, in that order.  Otherwise, return the single array
        that the web form returns.
    FeH: float
        Metallicity [Fe/H] of the isochrones.
    vvcrit: float, 0.0 or 0.4 only
        ZAMS rotation rate of the isochrones, relative to critical.
    Av: float
        Extinction coefficient.
    theory: None, ``'basic'`` or ``'full'``
        How much theoretical data to include.
    photometry: None or str
        Name of the table of photometric bands to
        include. e.g. ``'UBVRIplus'``.
        See :ref:`tables` for all options.

    Returns
    -------
    isochrones: NumPy structured array or a list of NumPy structured arrays
       If ``split=True``, a list containing the isochrones, in the
       same order as ``ts``.  If ``split=False``, a single array
       containing all the isochrones.  Columns in the arrays depends
       on choice of ``theory`` and ``photometry``.

    """
    # construct dict first because it catches type errors in arguments
    data = {
        'version': '1.2',
        'v_div_vcrit': 'vvcrit%.1f' % vvcrit,
        'age_scale': 'linear',
        'age_type': 'list',
        'age_value': '',
        'age_list': ' '.join(['%g' % (t*1e9) for t in ts]),
        'FeH_value': '%g' % FeH,
        'Av_value': '%g' % Av
    }

    assert all([1e-4 <= t <= 10**1.3 for t in ts]), "all ts (ages) must be between 1e-4 and 10**1.3=19.953"
    assert -4 <= FeH <= 0.5, "FeH must be between -4.0 and +0.5"
    assert vvcrit in {0.0, 0.4}, "vvcrit must be 0.0 or 0.4"
    assert 0 <= Av <= 6, "Av must be between 0 and 6"
    if photometry is not None:
        assert photometry in PHOTOMETRY_OPTIONS, "invalid photometry option '%s'" % photometry

    # choosing an age more precisely than 10ppm causes a variety of issues
    if any([np.abs(t-np.round(t, 5-int(np.log10(t)))) > 1e-7 for t in ts]):
        raise ValueError("age cannot be more precise than 10 ppm")

    # fetch theory, if requested
    if theory in {'basic', 'full'}:
        data['output_option'] = 'theory'
        data['theory_output'] = theory

        r = requests.post(
            BASE_URL+'iso_form.php',
            data=data
        )

        filename = r.text[18:48]
        f = io.BytesIO(urlopen(BASE_URL + filename).read()) # not a zip file
        isos = np.genfromtxt(f, skip_header=10, names=True, dtype=None)
    elif theory is not None:
        raise ValueError("theory argument must be 'basic', 'full' or None, not '%s'" % theory)

    # fetch photometry, if requested
    if photometry is not None:
        data['output_option'] = 'photometry'
        data['output'] = photometry

        r = requests.post(
            BASE_URL+'iso_form.php',
            data=data
        )
        filename = r.text[18:52]

        f = ZipFile(io.BytesIO(urlopen(BASE_URL + filename).read()))

        cmds = np.genfromtxt(f.read(f.namelist()[0]).decode().split('\n'),
                             skip_header=12, names=True, dtype=None)

        if theory is None:
            # no theory data, so photometry is everything
            isos = cmd
        else:
            # combine theory and photometry
            cmds = rfn.drop_fields(cmds, isos.dtype.names)
            isos = rfn.append_fields(isos, cmds.dtype.names, [cmds[k] for k in cmds.dtype.names], usemask=False)

    if not split:
        return isos
    else:
        return [isos[np.isclose(isos['isochrone_age_yr']/1e9, t)] for t in ts]
