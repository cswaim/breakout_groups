#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
import unittest
import os
from pathlib import Path
from numpy import testing as npt
#from inc import config as cfg
import breakout_groups as bg
 
class TestConfig(unittest.TestCase):
    """ tests for the """ 

    testfile_path = "tests/testfiles/"

    @classmethod
    def setUpClass(cls):
        """class set up""" 
        print("\n ------- \nTesting module - test_breakout_groups.py")
        if not os.path.exists(cls.testfile_path):
            os.mkdir(cls.testfile_path)

        # set path to test data file
        bg.cfg.datadir = str(Path.joinpath(bg.cfg.wkdir_path, cls.testfile_path))

        return

    @classmethod
    def tearDownClass(cls):

        if os.path.exists(cls.testfile_path):
            for pth, dir, files in os.walk(cls.testfile_path):
                for fl in files:
                    os.remove(f"{cls.testfile_path}{fl}")
            os.rmdir(cls.testfile_path)
        return

    def setUp(self):

        return

    def tearDown(self):

        return

    def test_get_combinatins(self):

        expected_wkdir_name = "breakout_groups"
        result_freq = []

        wd = Path(cfg.wkdir)
        self.assertEqual(wd.name, expected_wkdir_name)
        cfg.debug_print()
        # npt.assert_almost_equal(expected_freq, result_freq,2)

if __name__ == '__main__':
    #unittest.main()

    cf = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    unittest.TextTestRunner(verbosity=2).run(cf)