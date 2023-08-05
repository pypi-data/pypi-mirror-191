from os.path import abspath, dirname, join, isfile, normpath, relpath
from pandas.testing import assert_frame_equal
from numpy.testing import assert_allclose
from scipy.interpolate import interp1d
from random import seed, randint
import matplotlib.pylab as plt
from datetime import datetime
import xarray.testing as xrt
import mhkit.wave as wave
from io import StringIO
import pandas as pd
import numpy as np
import contextlib
import unittest
import netCDF4
import inspect
import pickle
import time
import json
import sys
import os


testdir = dirname(abspath(__file__))
plotdir = join(testdir, 'plots')
isdir = os.path.isdir(plotdir)
if not isdir: os.mkdir(plotdir)
datadir = normpath(join(testdir,relpath('../../../examples/data/wave')))


class TestResourceSpectrum(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        omega = np.arange(0.1,3.5,0.01)
        self.f = omega/(2*np.pi)
        self.Hs = 2.5
        self.Tp = 8
        df = self.f[1] - self.f[0]
        Trep = 1/df
        self.t = np.arange(0, Trep, 0.05)

    @classmethod
    def tearDownClass(self):
        pass

    def test_pierson_moskowitz_spectrum(self):
        S = wave.resource.pierson_moskowitz_spectrum(self.f,self.Tp,self.Hs)
        Hm0 = wave.resource.significant_wave_height(S).iloc[0,0]
        Tp0 = wave.resource.peak_period(S).iloc[0,0]

        errorHm0 = np.abs(self.Tp - Tp0)/self.Tp
        errorTp0 = np.abs(self.Hs - Hm0)/self.Hs

        self.assertLess(errorHm0, 0.01)
        self.assertLess(errorTp0, 0.01)

    def test_jonswap_spectrum(self):
        S = wave.resource.jonswap_spectrum(self.f, self.Tp, self.Hs)
        Hm0 = wave.resource.significant_wave_height(S).iloc[0,0]
        Tp0 = wave.resource.peak_period(S).iloc[0,0]

        errorHm0 = np.abs(self.Tp - Tp0)/self.Tp
        errorTp0 = np.abs(self.Hs - Hm0)/self.Hs

        self.assertLess(errorHm0, 0.01)
        self.assertLess(errorTp0, 0.01)

    def test_surface_elevation_phases_np_and_pd(self):
        S0 = wave.resource.jonswap_spectrum(self.f,self.Tp,self.Hs)
        S1 = wave.resource.jonswap_spectrum(self.f,self.Tp,self.Hs*1.1)
        S = pd.concat([S0, S1], axis=1)

        phases_np = np.random.rand(S.shape[0], S.shape[1]) * 2 * np.pi
        phases_pd = pd.DataFrame(phases_np, index=S.index, columns=S.columns)

        eta_np = wave.resource.surface_elevation(S, self.t, phases=phases_np, seed=1)
        eta_pd = wave.resource.surface_elevation(S, self.t, phases=phases_pd, seed=1)

        assert_frame_equal(eta_np, eta_pd)

    def test_surface_elevation_frequency_bins_np_and_pd(self):
        S0 = wave.resource.jonswap_spectrum(self.f,self.Tp,self.Hs)
        S1 = wave.resource.jonswap_spectrum(self.f,self.Tp,self.Hs*1.1)
        S = pd.concat([S0, S1], axis=1)

        eta0 = wave.resource.surface_elevation(S, self.t, seed=1)

        f_bins_np = np.array([np.diff(S.index)[0]]*len(S))
        f_bins_pd = pd.DataFrame(f_bins_np, index=S.index, columns=['df'])

        eta_np = wave.resource.surface_elevation(S, self.t, frequency_bins=f_bins_np, seed=1)
        eta_pd = wave.resource.surface_elevation(S, self.t, frequency_bins=f_bins_pd, seed=1)

        assert_frame_equal(eta0, eta_np)
        assert_frame_equal(eta_np, eta_pd)

    def test_surface_elevation_moments(self):
        S = wave.resource.jonswap_spectrum(self.f, self.Tp, self.Hs)
        eta = wave.resource.surface_elevation(S, self.t, seed=1)
        dt = self.t[1] - self.t[0]
        Sn = wave.resource.elevation_spectrum(eta, 1/dt, len(eta.values),
                                              detrend=False, window='boxcar',
                                              noverlap=0)

        m0 = wave.resource.frequency_moment(S,0).m0.values[0]
        m0n = wave.resource.frequency_moment(Sn,0).m0.values[0]
        errorm0 = np.abs((m0 - m0n)/m0)

        self.assertLess(errorm0, 0.01)

        m1 = wave.resource.frequency_moment(S,1).m1.values[0]
        m1n = wave.resource.frequency_moment(Sn,1).m1.values[0]
        errorm1 = np.abs((m1 - m1n)/m1)

        self.assertLess(errorm1, 0.01)

    def test_surface_elevation_rmse(self):
        S = wave.resource.jonswap_spectrum(self.f, self.Tp, self.Hs)
        eta = wave.resource.surface_elevation(S, self.t, seed=1)
        dt = self.t[1] - self.t[0]
        Sn = wave.resource.elevation_spectrum(eta, 1/dt, len(eta),
                                              detrend=False, window='boxcar',
                                              noverlap=0)

        fSn = interp1d(Sn.index.values, Sn.values, axis=0)
        rmse = (S.values - fSn(S.index.values))**2
        rmse_sum = (np.sum(rmse)/len(rmse))**0.5

        self.assertLess(rmse_sum, 0.02)

    def test_plot_spectrum(self):
        filename = abspath(join(plotdir, 'wave_plot_spectrum.png'))
        if isfile(filename):
            os.remove(filename)

        S = wave.resource.pierson_moskowitz_spectrum(self.f,self.Tp,self.Hs)

        plt.figure()
        wave.graphics.plot_spectrum(S)
        plt.savefig(filename, format='png')
        plt.close()

        self.assertTrue(isfile(filename))

    def test_plot_chakrabarti(self):
        filename = abspath(join(plotdir, 'wave_plot_chakrabarti.png'))
        if isfile(filename):
            os.remove(filename)

        D = 5
        H = 10
        lambda_w = 200

        wave.graphics.plot_chakrabarti(H, lambda_w, D)
        plt.savefig(filename)

    def test_plot_chakrabarti_np(self):
        filename = abspath(join(plotdir, 'wave_plot_chakrabarti_np.png'))
        if isfile(filename):
            os.remove(filename)

        D = np.linspace(5, 15, 5)
        H = 10 * np.ones_like(D)
        lambda_w = 200 * np.ones_like(D)

        wave.graphics.plot_chakrabarti(H, lambda_w, D)
        plt.savefig(filename)

        self.assertTrue(isfile(filename))

    def test_plot_chakrabarti_pd(self):
        filename = abspath(join(plotdir, 'wave_plot_chakrabarti_pd.png'))
        if isfile(filename):
            os.remove(filename)

        D = np.linspace(5, 15, 5)
        H = 10 * np.ones_like(D)
        lambda_w = 200 * np.ones_like(D)
        df = pd.DataFrame([H.flatten(),lambda_w.flatten(),D.flatten()],
                         index=['H','lambda_w','D']).transpose()

        wave.graphics.plot_chakrabarti(df.H, df.lambda_w, df.D)
        plt.savefig(filename)

        self.assertTrue(isfile(filename))

if __name__ == '__main__':
    unittest.main()
    