#!/usr/bin/env python3

import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from src.split_date_continues import main, split_date_continues


class TestSplitDateContinues(unittest.TestCase):

    def setUp(self):
        self.df = split_date_continues()

    def test_shape(self):
        self.assertEqual(
            self.df.shape, (37128, 25),
            msg="split_date_continues() should return a DataFrame with "
                "shape (37128, 25) -- one row per hour in the source data "
                "and one column per bike counter plus the five split date "
                "columns. Got shape %r." % (self.df.shape,))

    def test_columns(self):
        np.testing.assert_array_equal(
            self.df.columns[:6],
            ['Weekday', 'Day', 'Month', 'Year', 'Hour', 'Auroransilta'],
            err_msg="The first six column names should be ['Weekday', "
                    "'Day', 'Month', 'Year', 'Hour', 'Auroransilta'], in "
                    "that order -- the split date columns must come first, "
                    "followed by the original counter columns.")

    def test_dtypes(self):
        np.testing.assert_array_equal(
            self.df.dtypes[:6],
            [object, int, int, int, int, float],
            err_msg="The first six columns should have dtypes [object, "
                    "int, int, int, int, float] (Weekday is a string, Day/"
                    "Month/Year/Hour are ints, and the first counter "
                    "column is a float because it contains NaNs).")

    def test_content(self):
        value = self.df.loc[0, "Auroransilta"]
        self.assertTrue(
            np.isnan(value),
            msg="Row 0, column 'Auroransilta' should be NaN (that counter "
                "reading is blank in the source CSV for that hour). Got "
                "%r." % (value,))
        self.assertEqual(
            self.df.loc[0, "Baana"], 8.0,
            msg="Row 0, column 'Baana' should be 8.0, matching the source "
                "CSV. Got %r." % (self.df.loc[0, "Baana"],))

    def test_calls(self):
        with patch("src.split_date_continues.split_date_continues",
                   wraps=split_date_continues) as psplit, \
             patch("src.split_date_continues.pd.read_csv",
                   wraps=pd.read_csv) as prc, \
             patch("src.split_date_continues.pd.concat",
                   wraps=pd.concat) as pconcat:
            main()
            psplit.assert_called_once()
            prc.assert_called_once()
            pconcat.assert_called()


if __name__ == '__main__':
    unittest.main()
