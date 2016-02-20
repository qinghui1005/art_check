# -*- coding: utf-8 -*-

###############################################################################
###
###############################################################################

import sys

import config

from collections import defaultdict

###############################################################################
###
###############################################################################

def init_process(mul):
	mod = sys.modules[globals()['__name__']]

	mod._process_ = mul

	return

def get_process():
	mod = sys.modules[globals()['__name__']]

	return getattr(mod, '_process_', config.PROCESS_ONE)

def init_file():
	mod = sys.modules[globals()['__name__']]

	mod._file_hard_ = set()
	mod._file_soft_ = set()
	mod._art_src_ori_ = set()
	mod._art_src_col_ = set()

	mod._err_src_ = {}
	mod._err_xml_ = defaultdict(set)

	return

def init_ref():
	mod = sys.modules[globals()['__name__']]

	mod._ref_src_ = {}
	mod._ref_xml_ = defaultdict(set)
	mod._ref_chain_ = {}

	return

def init_pck():
	mod = sys.modules[globals()['__name__']]

	mod._file_pck_ = ()

	return

###############################################################################
###
###############################################################################
