# -*- coding: utf-8 -*-

import art
import debug
import config

import tool_file

################################################################################
###
################################################################################

def getAllSrc():
	col_src = tool_file.col_src_hard(config.PATH_SRC)

	return col_src, {}, {}

################################################################################
###
################################################################################

def collect_art_src():
	col_src, col_ref, col_bug = getAllSrc()

	art._art_src_ori_ = col_src
	art._art_src_col_ = col_src

	art._ref_src_ = col_ref
	art._err_src_ = col_bug

	for symf, symr_mul in col_ref.iteritems():
		if not debug.tr_exists('art_src', 'src_key', symf, echo=True):continue

		for symr in symr_mul:
			if not debug.tr_exists(symf, 'src_val', symr, echo=False):
				art._err_src_.setdefault(symf, set())
				art._err_src_[symf].add(symr)
				continue

			art._art_src_col_.add(symr)

	return

################################################################################
###
################################################################################

