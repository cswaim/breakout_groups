import argparse

def get_parser():
    """ get the command line args
        @return object of parser args
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Breakout Groups',
        epilog='''
This module runs the breakout group application, creating interaction reports
 and cards in the data folder

 On the first run, the default config file is created in the data directory.  If
 the init parameter is passed, then the run exits and the config file can be
 modified.  Otherwise the run continues with the defaults.

 To rebuild the config file from the default cfg settings, delete the existing
 cfg file.  A rebuild can also be forced by changing the sys_cfg_version to 0

 The config file can be modified and the job rerun as needed.

 ** Note the same parser is used for both the breakout_group final run and
    the bg_algo_compare run.  The loop-cnt variable is only used in the
    compare run.

 ex:
    python breakout_groups.py          (runs the app - the default)
    python breakout_groups --init      (or -init run one time for setup)
    python breakout_groups --help      (or -h  displays this text)
    python breakout_groups --cfgfl cfgfl-name  (or -cf cfgfl-name )

    python bg_algo_compare.py -lc 100 (override loop cnt, default 10,000)
    python bg_algo_compare.py -lc 100 -cf custom-cfgfl

 If an arg of --help or -h is passed with the command, this message is
     printed

    ''')
    parser.add_argument('-init', '--init', dest="init", action="store_true", default=False, help='just run the init')
    parser.add_argument('-cf', '--cfgfl', type=str, dest="cfgflnm", default=None, help='the name of the custom cfg file')
    parser.add_argument('-lc', '--loop_cnt', type=int, dest="loop_cnt", default=10000, help='set the bg_algo_compare routine loop cnt; default is 10000')

    return parser

def set_cfg_values(parms, cfg):
    """set the cfg values from parms"""
    # set the cfg values
    if parms.cfgflnm:
        cfg.cfg_flnm = parms.cfgflnm
        # reload config with new file name
        cfg.cp.run()

    # cfg filename must be set before running the init
    if parms.init:
        init_text = f"The config file '{cfg.cfg_flnm}' has been created in {cfg.datadir} "
        print(init_text)
        exit()