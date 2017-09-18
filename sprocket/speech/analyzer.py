# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import

import pyworld


class WORLD(object):
    """WORLD-based speech analyzer & synthesizer

    Attributes
    ----------
    period : float
        frame period (default: 5.0)
    fs : int
        sampling frequency (default: 44100)
    f0_floor : float
        floor in f0 estimation
    f0_ceil : float
        ceil in f0 estimation
    """

    def __init__(self,
                 period=5.0,
                 fs=44100,
                 f0_floor=40.0,
                 f0_ceil=700.0,
                 ):
        super(WORLD, self).__init__()

        self.period = period
        self.fs = fs
        self.f0_floor = f0_floor
        self.f0_ceil = f0_ceil

    def analyze(self, x):
        """Analyze acoustic features based on WORLD

        analyze F0, spectral envelope, aperiodicity

        Paramters
        ---------
        x : array, shape (`T`)
            monoral speech signal in time domain

        Returns
        ---------
        f0 : array, shape (`T`,)
            F0 sequence
        spc : array, shape (`T`, `fftl / 2 + 1`)
            Spectral envelope sequence
        ap: array, shape (`T`, `fftl / 2 + 1`)
            aperiodicity sequence

        """
        f0, time_axis = pyworld.harvest(x, self.fs, f0_floor=self.f0_floor,
                                        f0_ceil=self.f0_ceil,
                                        frame_period=self.period)
        spectrum_envelope = pyworld.cheaptrick(
            x, f0, time_axis, self.fs, f0_floor=self.f0_floor)
        aperiodicity = pyworld.d4c(x, f0, time_axis, self.fs)

        return f0, spectrum_envelope, aperiodicity

    def analyze_f0(self, x):
        """Analyze decomposes a speech signal into F0:

        Paramters
        ---------
        x: array, shape (`T`)
            monoral speech signal in time domain

        Returns
        ---------
        f0 : array, shape (`T`,)
            F0 sequence

        """
        f0, time_axis = pyworld.harvest(x, self.fs, f0_floor=self.f0_floor,
                                        f0_ceil=self.f0_ceil,
                                        frame_period=self.period)
        return f0

    def synthesis(self, f0, spc, ap):
        """Synthesis re-synthesizes a speech waveform from:

        Parameters
        ----------
        f0 : array, shape (`T`)
            F0 sequence
        spc : array, shape (`T`, `dim`)
            Spectral envelope sequence
        ap: array, shape (`T`, `dim`)
            Aperiodicity sequence

        """

        return pyworld.synthesize(f0, spc, ap, self.fs, frame_period=self.period)