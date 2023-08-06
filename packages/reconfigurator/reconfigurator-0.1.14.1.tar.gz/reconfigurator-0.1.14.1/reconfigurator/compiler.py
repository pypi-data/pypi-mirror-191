#!/usr/bin/python3
"""
This script contains functions for compiling a dense configuration file into a list of configurations.
"""
__license__ = "BSD-3"
__docformat__ = 'reStructuredText'
__author__ = "Jared Beard"

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import itertools
from collections.abc import Iterable
from copy import deepcopy

import nestifydict as nd

from sample import *

__all__ = ["compile_to_list", "compile_as_generator"]
    
def compile_to_list(config : dict):
    """
    Compiles dense configuration to get list of all sets of configurations
    
    :param config: (dict) dense configuration file
    :return: (list) all configurations captured
    """
    return list(compile_as_generator(config))
    

def compile_as_generator(config : dict):
    """
    Compiles dense configuration using a generator to get all sets of configurations
    
    :param config: (dict) dense configuration file
    :return: (dict) a single configuration
    """
    default_config = {}
    if "default" in config:
            default_config = config.pop("default")  
    config = push_default(default_config, config)

    n_copies = 1
    if "n_copies" in config:
            n_copies = config.pop("n_copies")
    
    if "stitch" not in config:
        for i in range(n_copies):
            yield config
    else:
        stitch_config = config.pop("stitch")
        
        for i in range(n_copies):
            if isinstance(stitch_config,list):
                for el in stitch_all(stitch_config, config):
                    yield el 
            else:
                for el in stitch(stitch_config, config):
                    yield el

def push_default(default_config: dict, config : dict):
    """
    Distributes default settings to dictionary
    
    :param default_config: (dict) configuration file defaults
    :param config: (dict) configuration file
    :return: (dict) configuration file with defaults
    """
    if "sample" in default_config:
        s = default_config.pop("sample")
    else:
        s = []
    for el in config:
        if isinstance(config[el], dict):
            config[el] = nd.merge(default_config, config[el])
    config = nd.merge(default_config, config)
    return sample_all(s, config)

def stitch_all(stitch_configs : dict, configs : dict):
    """
    Generator that will stitch together compiled configurations.
    Stitch should be specified as a list. If the element encountered is
    
    :param stitch_config: (list) how to stitch together configurations
    :param config: (dict) dense configuration
    :return: yields all combinations. 
    """
    for el in stitch_configs:
        for itm in stitch(el, deepcopy(configs)):
            yield itm      

def stitch(stitch_config, configs : dict):
    """
    Stitching is the process of combining configurations from different groups. 
    To define a stitch, users must include a key called stitch which contains the name of variables we want to stitch/compose into a set of configurations.
    Stitch will be parse as follows:
    - a tuple: stitch variables as the component product (combination of the elements in the variable)
    - a list: stitch variables in a pairwise fashion (they will be matched one-to-one for each value in the variables which must be of the same length)
    - a key: parse variable sequentially. If the values contained in the member 
        - a dict: elements will be compiled as a normal
        - any other iterable: elements will be parse sequentially then be returned (or if dict, compiled)
        - any other type: elements will be returned as is 
    
    :param stitch_config: () how to stitch together configurations
    :param config: (dict) dense configuration
    :return: yields all combinations. 
    """
    if isinstance(stitch_config,tuple) or isinstance(stitch_config,list):
        d_filter = {}

        for el in stitch_config:
            key = nd.find_key(configs,el)
            if key != None:
                temp_dict = nd.recursive_get(configs, key)
                if isinstance(temp_dict, dict):
                    nd.recursive_set(configs, key, compile_to_list(temp_dict))

        d_flat = nd.unstructure(configs)
        
        for el in stitch_config:
            if el in d_flat:
                d_filter[el] = d_flat[el]

        d_flat = nd.unstructure(configs)
        d_filter = {}
        for el in stitch_config:
            d_filter[el] = d_flat[el]
            if not isinstance(d_filter[el], list):
                    d_filter[el] = [d_filter[el]]

        if isinstance(stitch_config,tuple):
            gen = itertools.product(*d_filter.values())
        else:
            gen = pairwise(list(d_filter.values()))

        for config in gen:
            temp = dict(zip(list(d_filter.keys()), deepcopy(config)))
            temp = nd.merge(d_flat,temp)
            for itm in compile_as_generator(nd.structure(temp,configs)):
                yield itm

    elif nd.find_key(configs, stitch_config) != None:
        temp_config = nd.recursive_get(configs, nd.find_key(configs, stitch_config))
        if isinstance(temp_config,dict):
            for itm in compile_as_generator(temp_config):
                temp = deepcopy(configs)
                temp[stitch_config] = itm
                yield temp

        elif isinstance(temp_config,Iterable):
            for el in temp_config:
                temp = deepcopy(configs)
                if isinstance(el,dict):
                    for itm in compile_as_generator(el):
                        temp[stitch_config] = itm
                        yield temp
                else:
                    temp[stitch_config] = el
                    yield temp
        else:
            yield configs
    else:
        yield configs

def pairwise(groups : Iterable):
    """
    Takes element from each group and pairs them together by index

    :param groups: (list) list of lists
    :return: (generator) yields all combinations
    """
    for i in range(len(groups[0])):
        els = [0]*len(groups)
        for j in range(len(groups)):
            els[j] = groups[j][i]
        yield els
