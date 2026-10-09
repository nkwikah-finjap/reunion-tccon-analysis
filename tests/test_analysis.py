import unittest
import numpy as np
import pandas as pd
from analysis import to_unit,aggregate_observations
class Tests(unittest.TestCase):
    def test_already_ppm_not_scaled(self): np.testing.assert_allclose(to_unit([410.0],'ppm','ppm'),[410.0])
    def test_ppm_to_ppb(self): np.testing.assert_allclose(to_unit([1.82],'ppm','ppb'),[1820.0])
    def test_mole_fraction(self): np.testing.assert_allclose(to_unit([410e-6],'mol/mol','ppm'),[410.0])
    def test_unknown_unit(self):
        with self.assertRaises(ValueError): to_unit([1],'bananas','ppm')
    def test_gap_not_filled(self):
        f=pd.DataFrame({'time':pd.to_datetime(['2020-01-01','2020-01-03']), 'xco2_ppm':[400.,402.],'xco_ppb':[50.,52.],'xch4_ppb':[1800.,1802.]})
        d=aggregate_observations(f)
        self.assertEqual(len(d),2);self.assertEqual(d.n_observations.sum(),2)
