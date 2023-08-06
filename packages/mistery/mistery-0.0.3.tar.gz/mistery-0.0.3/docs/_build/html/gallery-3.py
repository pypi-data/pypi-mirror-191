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