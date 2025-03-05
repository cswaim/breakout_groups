#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  configparms_ext.py
#     read the config file and load the
#     variables in the config.py module
#
#  Copyright 2023 cswaim <cswaim@jcrl.net>
#  Licensed under the Apache License, Version 2.0
#  http://www.apache.org/licenses/LICENSE-2.0

from pathlib import Path
import os
import copy
import importlib.util
import src.config as cfg
from config_tpg.configparms import ConfigParms

# ----------------------------------------------------------------
# NOTE:
# In the methods that return True/False, the boolean value controls
# the flow of looping thru sections/variables.
# False - follow the default flow and process the rest of the logic
#         for the loop
# True - Force the next item in the loop, ie a python `continue`
# ----------------------------------------------------------------

class ConfigParmsExt(ConfigParms):
    """ This class extends the ConfigParms class allowing overrides of
        base class
    """
    def __init__(self, cfg_values=cfg.cfg_values, cfg_comments=cfg.cfg_comments, autorun=False):
        """ on init, load the directory paths, if autorun read the cfg file"""
        super().__init__(cfg_values, cfg_comments, autorun=False)

    def set_directories(self,) -> None:
        """ set the working directory paths in cfg if the project is not the structure defined in the README.md

        The default code is provided
        """
        if cfg.wkdir is None:
            # Find the path to the config module
            config_spec = importlib.util.find_spec("src.config")
            if config_spec is None and config_spec.origin is None:
                raise FileNotFoundError("config.py not found in the module search path.")

            cfg.wkdir_path = Path(config_spec.origin).resolve()
            cfg.srcdir = str(cfg.wkdir_path.parent) + os.sep
            cfg.wkdir = str(Path(cfg.srcdir).resolve().parent) + os.sep
            cfg.datadir = str(Path(cfg.wkdir).resolve()) + os.sep + 'data' + os.sep

    def custom_init_routine(self,) -> None:
        """ Run any custom process need during init of the class.  This is rarely used. """
        pass

    # set custom default values in the config object before writing the config file

    def set_custom_default_sects(self, config, sec, vars) -> bool:
        """ Process any section that needs special handling, such as a
        dictionary that is converted into variables within a section
        in the config file
        """
        #  set to True to skip the rest of the loop
        next_iter = False

        if sec == 'GROUP_LABELS':
            for i, g in enumerate(cfg.group_labels):
                config.set('GROUP_LABELS', f'sess{i}', ','.join(x for x in g))
            next_iter = True

        if sec == 'SESSION_NG_OVERRIDES':
            for k, v in cfg.session_ng_overrides.items():
                config.set('SESSION_NG_OVERRIDES', str(k), str(v))
            next_iter = True

        return next_iter



    def set_custom_default_vars(self, config, sec, vars, var) -> bool:
        """ Process any variable that needs special handling """
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    # set the values in the cfg module

    def set_module_sects(self, config, sec, vars) -> bool:
        """ special processing to set sec in cfg module  """
        #  set to True to skip the rest of the loop
        next_iter = False

        if sec == 'GROUP_LABELS':
            cfg.group_labels = self.build_group_labels(config)
            next_iter = True

        return next_iter

    def set_module_vars(self, config, sec, vars, var) -> bool:
        """ special processing for module variables """
        #  set to True to skip the rest of the loop
        next_iter = False

        # random_seed must be int or it is changed to None
        if var == 'random_seed':
            seed = config.get(sec, var, fallback=getattr(cfg, var))
            if isinstance(seed, (int, float)) or (isinstance(seed, str) and seed.isnumeric()):
                setattr(cfg, var, int(seed))
            else:
                setattr(cfg, var, None)
            next_iter = True

        return next_iter

    def set_custom_module_vars(self, config) -> None:
        """ set any custiom vars that are not being defined in the config.py module
            These generally are values that are derived from values received from the config file

            For example: build a list based on the number of items, as set in a config file varible
        """
        # n_groups is an integer so this is a copy
        cfg.orig_n_groups = cfg.n_groups

        # custom code for group labels and attendee list
        self.set_session_label_values(config)

        cfg.attendees_list = self.gen_attendees_list()

        # set the cfg.session_ng_overrides dict
        cfg.session_ng_overrides = self.build_ng_overrides(config)
        return


    # verify the values in the config parser object

    def verify_config_sects(self, config, sec, vars) -> bool:
        """ special processing for module groups """
        #  set to True to skip the rest of the loop
        next_iter = False

        # set the config labels to match the cfg labels
        if sec == 'GROUP_LABELS':
            conf_gl_len = len(config['GROUP_LABELS'])
            # default len of cfg.group_labels is 4
            # if len(cfg.group_labels) > conf_gl_len:
            #     for i, g in enumerate(cfg.group_labels):
            #         config.set('GROUP_LABELS', f'sess{i}', ','.join(x for x in g))
            #     sorted_lbls = {k:config['GROUP_LABELS'][k] for k in sorted(config['GROUP_LABELS'].keys())}
            #     config['GROUP_LABELS'] = sorted_lbls
            next_iter = True

        # set config ng overrides to match the cfg session_ng_overides
        if sec == 'SESSION_NG_OVERRIDES':
            next_iter = True

        return next_iter

    def verify_config_vars(self, config, sec, vars, var) -> bool:
        """ special processing for module variables"""
        #  set to True to skip the rest of the loop
        next_iter = False
        return next_iter

    #
    # custom routines called in hooks, not hooks
    #

    def set_session_label_values(self, config):
        """set default values of session labels if not set in config file
            for some items, a default value needs to be set, but not retained
            in the config file, this sets it in the module and config obj
        """
        # set defaults in config obj, not config file
        # build all session labels
        if len(cfg.session_labels) == 0 or len(cfg.session_labels[0]) == 0:
            # set labels in cfg module
            cfg.session_labels = self.gen_session_labels(cfg.n_sessions)
            # set labels in config object
            #list_str =
            config.set('EVENT', 'session_labels',  ",".join(x for x in cfg.session_labels))

        # build sessions for any missing label
        if len(cfg.session_labels) < cfg.n_sessions:
            extra_sess = self.gen_session_labels(cfg.n_sessions, len(cfg.session_labels))
            for es in extra_sess:
                cfg.session_labels.append(es)
            # set labels in config object
            config.set('EVENT', 'session_labels',  ",".join(x for x in cfg.session_labels))

        # make each label the same length, pad space to front
        max_len = max(len(s) for s in cfg.session_labels)
        cfg.session_labels = [s.rjust(max_len) for s in cfg.session_labels]

        config.set('EVENT', 'session_labels',  ",".join(x.strip() for x in cfg.session_labels))

    def gen_attendees_list(self,) -> list:
        """generate the list for attendees"""
        attendees_list = [x for x in range(cfg.n_attendees)]
        return attendees_list

    def build_group_labels(self, config) -> list:
        """ read group label dict and build a list of lists of the labels
            for each group in a session this removes the key from the
            dict and does not force a naming convention in the cfg file
        """
        group_labels = []
        for k, v in config['GROUP_LABELS'].items():
            if k not in config['EVENT']:
                group_labels.append([item.strip() for item in v.split(',')])
                #group_labels.append(v.split(','))

        # group_labels is a list of list, check for '' and remove
        ngl = []
        for s in group_labels:
            new_s = [gl for gl in s if gl != '']
            ngl.append(new_s)

        group_labels = ngl

        return group_labels

    def gen_session_labels(self, nsess, bsess=0) -> list:
        """test the session_labels and if empty, gen standard labels
           Session 01, Session 02
        """
        slabels = []
        for x in range(bsess, nsess):
            sn = x +1
            slabels.append(f"Session {sn:02}")

        return slabels

    def build_ng_overrides(self, config) -> dict:
        """build the override dict from the config file"""
        over_dict = {}
        for k, v in config['SESSION_NG_OVERRIDES'].items():
            over_dict[int(k)] = int(v)

        return over_dict