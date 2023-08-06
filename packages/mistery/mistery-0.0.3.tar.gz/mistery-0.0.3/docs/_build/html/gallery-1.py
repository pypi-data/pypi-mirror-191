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