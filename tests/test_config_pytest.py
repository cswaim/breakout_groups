#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

"""PyTest - basic operation and concepts.

HOW TO RUN THE TESTS
--------------------
1. Run all tests in a directory
% cd directory
% pytest


2. Run all tests in a file
% pytest test_file.py


3. Run a specific test
% pytest test_file.py::test_specific_one

4. Run all tests with a specific marker associated with some tests
Any of the above commands but with the -m parameter
% pytest -m "end-to-end" 



HANDY COMMAND LINE OPTIONS
--------------------------
-s   Output from all python print() statements is written to console
-v   verbose output.  Lists each test


FIXTURES
--------
Syntactically, these are just Python decorators.  They play many roles
1. Replace start-up and tear_down
2. Paramtrize inputs to tests
3. Global variables, but in a sane manner



ORGANIZATION OF A TEST SUITE
----------------------------
I typically do not create a class for the test cases.
Test cases must begin witht the string "test_" or pytest will ignore them.
Test cases and helper methods may be included, in any order in the file.

The file "conftest.py" plays many roles.
1. It is often the home for all the fixtures used by this suite.
2. Simplifies importing code to be tested - code that is in scr directory



DIFFERENCES FROM UnitTest
-------------------------
There is no explicit setup and tear down methods.  Rather fixtures
   do those tasks.  More on Fixtures later.


HANDY PYTEST FEATURES
---------------------
1. Do you know about brekpoint() and the pytest debugger?
2. Pytest has its own set commands to handle temporary directories.
   The come and go with each test run.  See the fixture named
   "setup_directories"

"""   

from src import config as cfg
import pytest

# Simple example of pytest temporary directories.
# tmp_dir is a built_in fixture
# ToDo move this fixture to conftest.py
# Also, this is an example of a pytest marker
pytest.mark.simple
def test_make_temp_directory(tmp_path):
   base_dir = tmp_path / "breakout_groups"
   base_dir.mkdir()
   # does the directory exist?
   assert base_dir.exists()
   assert base_dir.is_dir()


# ToDo Convert to a fixture so that config info is available everywhere
pytest.mark.not_so_simple
def test_default_config():
   """test set_default_config """
   # load the default values
   config = cfg.read_config_file(cfg.config)
   # breakpoint()
   assert config.getint('DEFAULT','attendees') == 30
   assert config.getint('DEFAULT','group_size') == 6
   assert config.getint('DEFAULT','groups_per_session') == 5
   assert config.getint('DEFAULT','sessions') == 3       