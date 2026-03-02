import argparse

import pytest

from src import bg_parser


class DummyCP:
    def __init__(self):
        self.run_calls = 0

    def run(self):
        self.run_calls += 1


class DummyCfg:
    def __init__(self):
        self.cfg_flnm = "default.cfg"
        self.datadir = "/tmp/data/"
        self.cp = DummyCP()


def test_set_cfg_values_cfgfl_sets_filename_and_reloads():
    cfg = DummyCfg()
    parms = argparse.Namespace(cfgflnm="custom.cfg", init=False)

    bg_parser.set_cfg_values(parms, cfg)

    assert cfg.cfg_flnm == "custom.cfg"
    assert cfg.cp.run_calls == 1


def test_set_cfg_values_init_prints_message_and_exits(capsys):
    cfg = DummyCfg()
    parms = argparse.Namespace(cfgflnm=None, init=True)

    with pytest.raises(SystemExit):
        bg_parser.set_cfg_values(parms, cfg)

    out = capsys.readouterr().out
    assert "default.cfg" in out
    assert cfg.datadir in out


def test_set_cfg_values_cfgfl_then_init_uses_new_filename(capsys):
    cfg = DummyCfg()
    parms = argparse.Namespace(cfgflnm="alt.cfg", init=True)

    with pytest.raises(SystemExit):
        bg_parser.set_cfg_values(parms, cfg)

    out = capsys.readouterr().out
    assert "alt.cfg" in out
    assert cfg.cp.run_calls == 1
