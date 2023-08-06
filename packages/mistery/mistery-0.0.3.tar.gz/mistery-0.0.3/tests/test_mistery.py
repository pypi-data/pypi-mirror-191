import mistery
import numpy as np
import unittest

class TestMistery(unittest.TestCase):

    # @unittest.skip("skip slow test") # useful when working on other tests
    def test_interpolate(self):
        FeH = -0.1238923

        photometry = np.random.choice(list(mistery.PHOTOMETRY_OPTIONS))

        ts = np.round(np.random.uniform(low=0.5, high=2.5, size=3), 5)
        isos = mistery.get_isochrones(ts=ts, FeH=FeH, vvcrit=0.4, Av=1, photometry=photometry)

        Ms = np.round(np.random.uniform(low=0.6, high=1.4, size=3), 4)
        tracks = mistery.get_tracks(Ms=Ms, FeH=FeH, vvcrit=0.4, Av=np.array(1), photometry=photometry)

        passband = tracks[0].dtype.names[-1]

        print(photometry, passband)
    
        # interpolate a track and an isochrone to the same point,
        # where both values of log_L should be close (~per cent)
        for M, track in zip(Ms, tracks):
            for t, iso in zip(ts, isos):
                logL_track = np.interp(t, track['star_age']/1e9, track[passband])
                logL_iso = np.interp(M, iso['initial_mass'], iso[passband])
                np.testing.assert_allclose(logL_track, logL_iso, rtol=1e-2, atol=1e-2)

    def test_argument_bounds(self):
        self.assertRaises(AssertionError, mistery.get_track, M=-1.)
        self.assertRaises(AssertionError, mistery.get_track, M=0.001)
        self.assertRaises(AssertionError, mistery.get_track, M=301.)

        self.assertRaises(AssertionError, mistery.get_isochrone, t=-1.)
        self.assertRaises(AssertionError, mistery.get_isochrone, t=9e-5)
        self.assertRaises(AssertionError, mistery.get_isochrone, t=20)

        for func in [mistery.get_track, mistery.get_tracks,
                     mistery.get_isochrone, mistery.get_isochrones]:

            self.assertRaises(AssertionError, func, FeH=-5)
            self.assertRaises(AssertionError, func, FeH=1)

            self.assertRaises(AssertionError, func, vvcrit=0.2)

            self.assertRaises(AssertionError, func, Av=-1)
            self.assertRaises(AssertionError, func, Av=6.1)

            self.assertRaises(AssertionError, func, photometry='asdfadsf')

    def test_argument_types(self):
        for func in [mistery.get_track, mistery.get_tracks,
                     mistery.get_isochrone, mistery.get_isochrones]:
            for t in ['asdfa', [], {}]:
                self.assertRaises(TypeError, func, FeH=t)
                self.assertRaises(TypeError, func, vvcrit=t)
                self.assertRaises(TypeError, func, Av=t)

            self.assertRaises(AssertionError, func, photometry=0)
            self.assertRaises(TypeError, func, photometry=[])

if __name__ == '__main__':
    unittest.main()
