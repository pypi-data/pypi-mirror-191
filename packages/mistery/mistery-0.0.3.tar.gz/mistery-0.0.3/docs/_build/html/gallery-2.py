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