#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  breakout_groups.py
#  
#  Copyright 2023 cswaim <cswaim@tpginc.net>

import os
from pathlib import Path
import math
from itertools import combinations, chain
import itertools as it

from inc import config as cfg

class BreakoutGroups():
    """ generate breakout groups """ 

    items = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    items = [1,2,3,4,5,6,7,8,9]
    m = ['a','b','c','d', 'e', 'f', 'g']

    members = len(items)
    gs = group_size = 3
    gps = groups_per_session = 0
    sessions = rounds = 3

    def __init__(self) -> None:
        """setup"""
        pass

    def show_opts(self,) -> None:
        """analyze various approaches"""
        p = math.perm(len(self.items), self.group_size)
        c = math.comb(len(self.items), self.group_size)
        f = math.factorial(len(self.items))
        print(f"perm: {p}  comb: {c}  fact: {f}")

    def get_sub(self,)-> None:
        """test combinations"""
        ng = len(self.m) / self.gs
        c = list(combinations(self.m, self.gs))
        ms = [set(i) for i in list(combinations(c, self.gs)) if (len(set(self.m) & set(chain(*i))) == len(self.m))]
        #[{('a', 'b'), ('c', 'd')}, {('a', 'c'), ('b', 'd')}, {('a', 'd'), ('b', 'c')}]
        print("###")
        print(f" memb size: {len(self.m)}")
        print(f"group size: {self.gs}")
        print(f"num groups: {ng}")
        print("---")
        print(f"comb c: {len(c)} - {c}")
        print(f"comb set: {len(ms)} - {ms}")
        print("###")

    def unique_group(iterable, k, n) -> list:
        """Return an iterator, comprising groups of size `k` with combinations of size `n`."""
        # Build separate combinations of `n` characters
        groups = ("".join(i) for i in it.combinations(iterable, n))    # 'AB', 'AC', 'AD', ...

        # Build unique groups of `k` by keeping the longest sets of characters
        return (i for i in it.combinations(groups, k) 
                    if len(set("".join(i))) == sum((map(len, i))))     # ('AB', 'CD'), ('AB', 'CE'), ... 


    def combined(groups1, groups2) -> list:
        """Return an iterator with unique combinations of groups (k and l)."""
        # Build a unique cartesian product of groups `k` and `l`, filtering non-disjoints
        return (i[0] + i[1]
                for i in it.product(groups1, groups2) 
                if set("".join(i[0])).isdisjoint(set("".join(i[-1]))))

    def gen_unique_groups(self) -> None:
        """driver routine"""
        members = "ABCDEFGhi"
        n = 1
        gs = 3
        g1 = self.unique_group(members, gs, n)
        #g2 = unique_group(members, 1, 3)
        #result = list(combined(g1, g2))
        result = list(g1)
        print(f"len: {len(result)}")
        print(f"result: {result}")


 
if __name__ == '__main__':
    
    bg = BreakoutGroups()
