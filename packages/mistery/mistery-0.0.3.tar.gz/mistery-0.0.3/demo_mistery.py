#!/usr/bin/env python3

from argparse import ArgumentParser
import matplotlib.pyplot as pl
import mistery

parser = ArgumentParser("""
Fetch a MIST track and create an HR diagram,
mostly to make sure the module is working.
""")
parser.add_argument('-M', type=float, default=1.0)
parser.add_argument('--FeH', type=float, default=0.0)
parser.add_argument('-t', type=float, default=1.0)
args = parser.parse_args()

t = mistery.get_track(M=args.M, FeH=args.FeH)
pl.loglog(10**t['log_Teff'], 10**t['log_L'])

iso = mistery.get_isochrone(t=args.t, FeH=args.FeH)
pl.loglog(10**iso['log_Teff'], 10**iso['log_L'])

pl.xlabel('effective temperature (K)')
pl.ylabel('luminosity (solar units)')
pl.gca().invert_xaxis()
pl.show()
