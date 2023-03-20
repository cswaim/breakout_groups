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
-cov  generate a coverage report.  Ask me about this.


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
   do those tasks.  More on Fixtures later


"""
 
import pytest
import os
from pathlib import Path
from src import config as cfg
from numpy import testing as npt


def test_config_files():
   assert True
