#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="data_perf.py" company="Invariance Pte">
#  Copyright (C) 2018-2019 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

import unittest
import timeit

from time import time
from datetime import timedelta

from inv_trader.model.enums import Resolution
from inv_trader.backtest.data import DataProvider
from test_kit.stubs import TestStubs
from test_kit.data import TestDataProvider

MILLISECONDS_IN_SECOND = 1000
USDJPY_FXCM = TestStubs.instrument_usdjpy()


class DataProviderPerformanceTest:
    def __init__(self):

        instrument = TestStubs.instrument_usdjpy()
        bid_data = {Resolution.MINUTE: TestDataProvider.usdjpy_1min_bid()[:100000]}
        ask_data = {Resolution.MINUTE: TestDataProvider.usdjpy_1min_ask()[:100000]}

        self.data_provider = DataProvider(instrument,
                                          bid_data,
                                          ask_data)

        self.start = self.data_provider.bars[TestStubs.bartype_usdjpy_1min_bid()][0].timestamp
        self.time = self.start
        print(len(self.data_provider.bars))

    def iterate_bars(self):

        self.data_provider.iterate_bars(self.time)
        self.time += timedelta(minutes=1)


class DataProviderPerformanceTests(unittest.TestCase):

    @staticmethod
    def test_iterate_bars():
        # Arrange
        tests = 3
        number = 10000
        test = DataProviderPerformanceTest()

        total_elapsed = 0

        for x in range(tests):
            srt_time = time()
            timeit.Timer(test.iterate_bars).timeit(number=number)
            end_time = time()
            total_elapsed += round((end_time - srt_time) * MILLISECONDS_IN_SECOND)

        print('\n' + f'OrderIdGeneratorPerformanceTest({number} iterations)')
        print(f'{round(total_elapsed / tests)}ms')

        # ~40ms for 10000 bars