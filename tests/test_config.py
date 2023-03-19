#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>
 
import unittest
import os
from pathlib import Path
from src import config as cfg
from numpy import testing as npt

"""
assert samples
        self.assertEqual(wd.name, expected_wkdir_name)
        npt.assert_almost_equal(expected_freq, result_freq,2)
"""
 
class TestConfig(unittest.TestCase):
    """ tests for the """ 

    testfile_path = "tests/testfiles/"

    @classmethod
    def setUpClass(cls):
        """class set up""" 
        print("\n ------- \nTesting modules - test_config.py")
        if not os.path.exists(cls.testfile_path):
            os.mkdir(cls.testfile_path)

        cfg.datadir = str(Path.joinpath(cfg.wkdir_path, cls.testfile_path)) + os.sep
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

    def test_a_check_directories(self):
        """ test check the directory settings """
        # absolute path on different systems will vary, just use name as starting point
        expected_wkdir_name = "breakout_groups"

        wd = Path(cfg.wkdir)
        self.assertEqual(wd.name, expected_wkdir_name)
        cfg.debug_print()

    def test_set_default_config(self):
        """test set_default_config """
        # load the default values
        config = cfg.read_config_file(cfg.config)

        self.assertEqual(config.getint('DEFAULT','attendees'), 30)
        self.assertEqual(config.getint('DEFAULT','group_size'), 6)
        self.assertEqual(config.getint('DEFAULT','groups_per_session'), 5) 
        self.assertEqual(config.getint('DEFAULT','sessions'), 3)         

    def test_remove_default_comments(self,):
        """test remove_default_comments """
        pass

    def test_write_ini(self,):
        """test write on ini_file"""
        pass

if __name__ == '__main__':
    #unittest.main()

    cf = unittest.TestLoader().loadTestsFromTestCase(TestConfig)
    unittest.TextTestRunner(verbosity=2).run(cf)