.. _gallery:

Gallery
=======

Defaults
--------

The simplest possible calls.  Without arguments,
:py:meth:`mistery.get_track` returns the evolutionary track of a star
with 1 solar mass star and solar metallicity ([Fe/H]=0),
and :py:meth:`mistery.get_isochrone` returns an isochrone with age
1 Gyr and also solar metallicity.

.. plot::
   :include-source:

   import matplotlib.pyplot as pl
   import mistery

   track = mistery.get_track()
   isochrone = mistery.get_isochrone()

   pl.semilogy(10**track['log_Teff'], 10**track['log_L'], label='track')
   pl.semilogy(10**isochrone['log_Teff'], 10**isochrone['log_L'], label='isochrone')
   pl.xlabel('effective temperature (K)')
   pl.ylabel('luminosity (solar units)')
   pl.xlim(8500, 2500)
   pl.legend()

Multiple isochrones
-------------------

The main-sequence turn-off (MSTO) progresses to lower effective
temperature as a population ages.

.. plot::
   :include-source:

   import matplotlib.pyplot as pl
   import mistery

   ts = [0.5, 1.0, 2.5, 10.0]
   isochrones = mistery.get_isochrones(ts=ts)

   for t, isochrone in zip(ts, isochrones):
       pl.semilogy(10**isochrone['log_Teff'], 10**isochrone['log_L'], label='%.1f' % t)

   pl.xlabel('effective temperature (K)')
   pl.ylabel('luminosity (solar units)')
   pl.xlim(10500, 2500)
   pl.legend(title='age (Gyr)')

Looping over other parameters
-----------------------------

The form allows single calls for multiple masses or ages for tracks or
isochrones, respectively, but for other data we need to loop
ourselves.  Here we plot *B-V* against *V* for default tracks
at different levels of reddening.

.. plot::
   :include-source:

   import matplotlib.pyplot as pl
   import mistery

   Avs = [0, 0.5, 1.0]
   tracks = [mistery.get_track(Av=Av, photometry='UBVRIplus') for Av in Avs]

   for Av, track in zip(Avs, tracks):
      pl.plot(track['Bessell_B']-track['Bessell_V'], track['Bessell_V'], label='%.1f' % Av)

   pl.xlabel('$B-V$')
   pl.ylabel('$V$')
   pl.xlim(0.5, 2.2)
   pl.ylim(8, -5)
   pl.legend(title='$A_v$')
