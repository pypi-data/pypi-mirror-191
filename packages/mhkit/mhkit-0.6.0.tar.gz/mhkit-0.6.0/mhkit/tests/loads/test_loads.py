from os.path import abspath, dirname, join, isfile, normpath, relpath
from numpy.testing import assert_array_almost_equal, assert_allclose
from pandas._testing.asserters import assert_series_equal
from pandas.testing import assert_frame_equal
from mhkit import utils
from mhkit.wave import resource
import mhkit.loads as loads
import pandas as pd
from scipy import stats
import numpy as np
import unittest
import json
import os

testdir = dirname(abspath(__file__))
datadir = normpath(join(testdir,relpath('../../../examples/data/loads')))

class TestLoads(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        loads_data_file = join(datadir, "loads_data_dict.json")
        with open(loads_data_file, 'r') as fp:
            data_dict = json.load(fp)
        # convert dictionaries into dataframes
        data = {
                key: pd.DataFrame(data_dict[key])
                for key in data_dict
               }
        self.data = data

        self.fatigue_tower = 3804
        self.fatigue_blade = 1388

        # import blade cal data
        blade_data = pd.read_csv(join(datadir,'blade_cal.csv'),header=None)
        blade_data.columns = ['flap_raw','edge_raw','flap_scaled','edge_scaled']
        self.blade_data = blade_data
        self.flap_offset = 9.19906E-05
        self.edge_offset = -0.000310854
        self.blade_matrix = [1034671.4,-126487.28,82507.959,1154090.7]

    def test_bin_statistics(self):
        # create array containg wind speeds to use as bin edges
        bin_edges = np.arange(3,26,1)

        # Apply function to calculate means
        load_means =self.data['means']
        bin_against = load_means['uWind_80m']
        [b_means, b_means_std] = loads.general.bin_statistics(load_means, bin_against, bin_edges)

        assert_frame_equal(self.data['bin_means'],b_means)
        assert_frame_equal(self.data['bin_means_std'],b_means_std)

    def test_blade_moments(self):
        flap_raw = self.blade_data['flap_raw']
        flap_offset = self.flap_offset
        edge_raw = self.blade_data['edge_raw']
        edge_offset = self.edge_offset

        M_flap, M_edge = loads.general.blade_moments(self.blade_matrix,flap_offset,flap_raw,edge_offset,edge_raw)

        for i,j in zip(M_flap,self.blade_data['flap_scaled']):
            self.assertAlmostEqual(i,j,places=1)
        for i,j in zip(M_edge,self.blade_data['edge_scaled']):
            self.assertAlmostEqual(i,j,places=1)


    def test_damage_equivalent_loads(self):
        loads_data = self.data['loads']
        tower_load = loads_data['TB_ForeAft']
        blade_load = loads_data['BL1_FlapMom']
        DEL_tower = loads.general.damage_equivalent_load(tower_load, 4,bin_num=100,data_length=600)
        DEL_blade = loads.general.damage_equivalent_load(blade_load,10,bin_num=100,data_length=600)

        self.assertAlmostEqual(DEL_tower,self.fatigue_tower,delta=self.fatigue_tower*0.04)
        self.assertAlmostEqual(DEL_blade,self.fatigue_blade,delta=self.fatigue_blade*0.04)


    def test_plot_statistics(self):
        # Define path
        savepath = abspath(join(testdir, 'test_scatplotter.png'))

        # Generate plot
        loads.graphics.plot_statistics( self.data['means']['uWind_80m'],
                               self.data['means']['TB_ForeAft'],
                               self.data['maxs']['TB_ForeAft'],
                               self.data['mins']['TB_ForeAft'],
                               y_stdev=self.data['std']['TB_ForeAft'],
                               x_label='Wind Speed [m/s]',
                               y_label='Tower Base Mom [kNm]',
                               save_path=savepath)

        self.assertTrue(isfile(savepath))


    def test_plot_bin_statistics(self):
        # Define signal name, path, and bin centers
        savepath = abspath(join(testdir, 'test_binplotter.png'))
        bin_centers = np.arange(3.5,25.5,step=1)
        signal_name = 'TB_ForeAft'

        # Specify inputs to be used in plotting
        bin_mean = self.data['bin_means'][signal_name]
        bin_max  = self.data['bin_maxs'][signal_name]
        bin_min  = self.data['bin_mins'][signal_name]
        bin_mean_std = self.data['bin_means_std'][signal_name]
        bin_max_std = self.data['bin_maxs_std'][signal_name]
        bin_min_std = self.data['bin_mins_std'][signal_name]

        # Generate plot
        loads.graphics.plot_bin_statistics(bin_centers,
                                  bin_mean, bin_max, bin_min,
                                  bin_mean_std, bin_max_std, bin_min_std,
                                  x_label='Wind Speed [m/s]',
                                  y_label=signal_name,
                                  title='Binned Stats',
                                  save_path=savepath)

        self.assertTrue(isfile(savepath))

class TestWDRT(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        mler_file = join(datadir, "mler.csv")
        mler_data = pd.read_csv(mler_file,index_col=None)
        mler_tsfile = join(datadir,"mler_ts.csv")
        mler_ts = pd.read_csv(mler_tsfile,index_col=0)
        self.mler_ts = mler_ts
        self.wave_freq = np.linspace( 0.,1,500)
        self.mler = mler_data
        self.sim = loads.extreme.mler_simulation()

    def test_mler_coefficients(self):
        Hs = 9.0  # significant wave height
        Tp = 15.1  # time period of waves
        pm = resource.pierson_moskowitz_spectrum(self.wave_freq, Tp, Hs)
        mler_data = loads.extreme.mler_coefficients(
            self.mler['RAO'].astype(complex), pm, 1)
        mler_data.reset_index(drop=True, inplace=True)

        assert_series_equal(mler_data['WaveSpectrum'], self.mler['Res_Spec'],
                            check_exact=False, check_names=False, atol=0.001)
        assert_series_equal(mler_data['Phase'], self.mler['phase'],
                            check_exact=False, check_names=False, rtol=0.001)

    def test_mler_simulation(self):
        T = np.linspace(-150, 150, 301)
        X = np.linspace(-300, 300, 601)
        sim = loads.extreme.mler_simulation()

        assert_array_almost_equal(sim['X'], X)
        assert_array_almost_equal(sim['T'], T)

    def test_mler_wave_amp_normalize(self):
        wave_freq = np.linspace(0., 1, 500)
        mler = pd.DataFrame(index=wave_freq)
        mler['WaveSpectrum'] = self.mler['Res_Spec'].values
        mler['Phase'] = self.mler['phase'].values
        k = resource.wave_number(wave_freq, 70)
        k = k.fillna(0)
        mler_norm = loads.extreme.mler_wave_amp_normalize(
            4.5*1.9, mler, self.sim, k.k.values)
        mler_norm.reset_index(drop=True, inplace=True)

        assert_series_equal(mler_norm['WaveSpectrum'], self.mler['Norm_Spec'],check_exact=False,atol=0.001,check_names=False)

    def test_mler_export_time_series(self):
        wave_freq = np.linspace(0., 1, 500)
        mler = pd.DataFrame(index=wave_freq)
        mler['WaveSpectrum'] = self.mler['Norm_Spec'].values
        mler['Phase'] = self.mler['phase'].values
        k = resource.wave_number(wave_freq, 70)
        k = k.fillna(0)
        RAO = self.mler['RAO'].astype(complex)
        mler_ts = loads.extreme.mler_export_time_series(
            RAO.values, mler, self.sim, k.k.values)

        assert_frame_equal(self.mler_ts, mler_ts, atol=0.0001)

    def test_return_year_value(self):
        dist = stats.norm
        return_year = 50
        short_term_period = 1

        val = loads.extreme.return_year_value(dist.ppf, return_year, short_term_period)
        want = 4.5839339
        self.assertAlmostEqual(want, val, 5)

    def test_longterm_extreme(self):
        ste_1 = stats.norm
        ste_2 = stats.norm
        ste = [ste_1, ste_2]
        w = [0.5, 0.5]
        lte = loads.extreme.full_seastate_long_term_extreme(ste, w)
        x = np.random.rand()
        assert_allclose(lte.cdf(x), w[0]*ste[0].cdf(x) + w[1]*ste[1].cdf(x))

    def test_shortterm_extreme(self):
        methods = ['peaks_weibull', 'peaks_weibull_tail_fit',
                   'peaks_over_threshold', 'block_maxima_gev',
                   'block_maxima_gumbel']
        filename = "time_series_for_extremes.txt"
        data = np.loadtxt(os.path.join(datadir, filename))
        t = data[:, 0]
        data = data[:, 1]
        t_st = 1.0 * 60 * 60
        x = 1.6
        cdfs_1 = [0.006750456316537166, 0.5921659393757381, 0.6156789503874247,
                  0.6075807789811315, 0.9033574618279865]
        for method, cdf_1 in zip(methods, cdfs_1):
            ste = loads.extreme.ste(t, data, t_st, method)
            assert_allclose(ste.cdf(x), cdf_1)


if __name__ == '__main__':
    unittest.main()
