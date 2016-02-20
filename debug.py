# -*- coding: utf-8 -*-

import os

################################################################################
###
################################################################################

def pr_error(msg):print u'error:\t', msg
def pr_info(msg):print u'info:\t', msg
def pr_march(msg):print u'march:\t', msg
def pr_warn(msg):print u'warning:\t', msg
def pr_fname(msg):print u'bad file name:\t', msg
def pr_str(msg):print msg

def tr_exists(src, by, symr, echo=True):
	body, ext = os.path.splitext(symr)
	if len(ext) == 0:
		if os.path.isdir(symr):return True
	else:
		if os.path.exists(symr):return True

	if echo:print u'trace_exists %s [%s]--> %s' % (src, by, symr, )

	return False

def tr_required(symf, tag):
	print u'trace_requied %s, tag %s' % (symf, tag, )

	return

################################################################################
###
################################################################################
