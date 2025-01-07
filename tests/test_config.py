#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_config.py
#
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import os
from src import config as cfg
import pytest

# Simple example of pytest temporary directories.
# tmp_dir is a built_in fixture
# ToDo move this fixture to conftest.py
# Also, this is an example of a pytest marker
def test_make_temp_directory(tmp_path):
    """test make temp dir"""
    base_dir = tmp_path / "breakout_groups"
    base_dir.mkdir()
    # does the directory exist?
    assert base_dir.exists()
    assert base_dir.is_dir()

# ToDo Convert to a fixture so that config info is available everywhere
def test_default_config(config_event_defaults, tmp_path):
    """test set_default_config"""
    base_dir = tmp_path / "breakout_groups"
    base_dir.mkdir()
    cfg.datadir = str(base_dir) + os.sep
    # load the default values
    config = cfg.cp.read_config_file(cfg.config)
    # When experienting with different config value,
    #    might not pass.
    assert cfg.n_attendees == 11
    assert cfg.group_size == 3
    assert cfg.n_groups == 3
    assert cfg.n_sessions == 4

def test_build_session_labels():
    """test the building of the session labels"""
    cfg.cp.build_group_labels(cfg.config)
    res0 = ["group1", "group2", "group3", "group4", "group5"]
    res2 = ["Portales", "Santa Fe", "Taos", "Chama", "Cuba"]
    assert cfg.group_labels[0] == res0
    assert cfg.group_labels[2] == res2

def test_adding_new_data_item(config_event_defaults, tmp_path):
    """test add new data item"""

    def prt_file(base_dir, flnm):
        fp = base_dir.joinpath(flnm)
        with open(base_dir.joinpath(flnm), "r") as cf:
            fdata = cf.read()
        print(fdata)

    base_dir = tmp_path / "breakout_groups"
    base_dir.mkdir()
    cfg.datadir = str(base_dir) + os.sep
    # load the default values
    config = cfg.cp.read_config_file(cfg.config)
    orig_version = config.get("SYSTEM", "sys_cfg_version")

    # remove items from config & change version
    new_version = "0.0.0"
    config.remove_option("EVENT", "n_attendees")
    config.remove_option("SYSTEM", "sys_group_algorithm")
    config.set("SYSTEM", "sys_version", new_version)
    cfg.cp.write_cfg(config)
    config = cfg.cp.set_config_module_variables(config)

    assert config.has_option("EVENT", "n_attendees") is False
    assert config.has_option("SYSTEM", "sys_group_algorithm") is False

    # read and build missing options
    config = cfg.cp.read_config_file(cfg.config)
    # confirm options are added back when missing
    assert orig_version == cfg.sys_cfg_version
    assert config.has_option("EVENT", "n_attendees") is True
    assert config.has_option("SYSTEM", "sys_group_algorithm") is True

def test_add_missing_group_labels(config_event_defaults, tmp_path):
    """test add missing group labels"""
    base_dir = tmp_path / "breakout_groups"
    base_dir.mkdir()
    cfg.datadir = str(base_dir) + os.sep
    # load the default values
    config = cfg.cp.read_config_file(cfg.config)
    orig_version = config.get("SYSTEM", "sys_cfg_version")

    # remove group labels from config
    config.remove_section("GROUP_LABELS")
    cfg.cp.write_cfg(config)
    # config = cfg.cp.set_config_variables(config)
    assert config.has_section("GROUP_LABELS") is False

    # read and build missing options
    config = cfg.cp.read_config_file(cfg.config)
    assert orig_version == cfg.sys_cfg_version
    assert config.has_section("GROUP_LABELS") is True
    assert config.has_option("GROUP_LABELS", "sess2") is True

    # remove group labels from config
    config.remove_option("GROUP_LABELS", "sess2")
    cfg.cp.write_cfg(config)
    # config = cfg.cp.set_config_variables(config)
    assert config.has_option("GROUP_LABELS", "sess2") is False

    # read and build missing options
    config = cfg.cp.read_config_file(cfg.config)
    assert orig_version == cfg.sys_cfg_version
    assert config.has_option("GROUP_LABELS", "sess2") is True

def test_remove_default_comments(config_event_defaults):
    """test remove_default_comments"""
    # load the default values
    config = cfg.cp.set_default_config(cfg.config)
    comments = dict(
        (k, v) for k, v in config["GROUP_LABELS"].items() if k.startswith("#")
    )
    cfg.cp.remove_default_comments(cfg.config)

    for k in comments.keys():
        assert config.has_option("GROUP_LABELS", k) is False

def test_set_session_label_values(config_event_defaults):
    """test setting of sesion lables"""
    # load the default values
    cfg.session_labels.pop()
    config = cfg.cp.set_default_config(cfg.config)
    cfg.cp.set_session_label_values(config)
    assert cfg.session_labels[0] == ' Fri 9:00pm'
    assert cfg.session_labels[1] == '   Sat 9:00'
    assert cfg.session_labels[3] == ' Session 04'

def test_print_config_vars(config_event_defaults):
    """test of print routine"""
    # load the default values
    config = cfg.cp.set_default_config(cfg.config)
    cfg.cp.remove_default_comments(cfg.config)
    cfg.cu.print_config_vars(heading="with comments")
    cfg.cu.print_config_vars(heading="no comments", comments=False)
