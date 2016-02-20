# -*- coding: utf-8 -*-

import time

import config
import debug
import art
import art_chk
import tool_file

################################################################################
###
################################################################################

def set_progress(mul):
	art.init_process(mul)

	return

################################################################################
###
################################################################################

def chk_file_name():tool_file.chk_file(config.PATH_SRC)

def chk_one_xml():
	set_progress(config.PROCESS_ONE)
	art_chk.check_xml()

	return

def chk_mul_xml():
	set_progress(config.PROCESS_MUL)
	art_chk.check_xml()

	return

def quit_tool():
	debug.pr_str(u'bye~~~~')
	quit()

	return

################################################################################
###
################################################################################

MENU = (
	('1',		'check file name',		chk_file_name, ),
	('21',		'check_art_xml one',		chk_one_xml, ),
	('22',		'check_art_xml mul',		chk_mul_xml, ),
	('q',		'quit',				quit_tool, ),
)

OPT_HO, DESC_HO, FUNC_HO = zip(*MENU)
OPT_DESC = [(opt, desc, ) for opt, desc, func in MENU]

TIP = u'Please choose what u want:'

def opt2func(opt):return FUNC_HO[list(OPT_HO).index(opt)]
def opt2desc(opt):return DESC_HO[list(OPT_HO).index(opt)]

def opt2str(menu):
	s = u''
	for (opt, desc) in menu:s += opt + ':\t' + desc + '\n'

	return s

def show_menu(tip, menu):
	fmt = u'%s\n\n%s\nPlease choose:'
	prm = (tip, opt2str(menu))

	msg = fmt % prm

	return raw_input(msg).lower()

def get_option(tip, menu, opt_ho):
	opt = show_menu(tip, menu)

	if opt not in opt_ho:
		debug.pr_warn('your choice not in opt_all!!!!!')
		return get_option(tip, menu, opt_ho)

	return opt

################################################################################
###
################################################################################

if __name__ == '__main__':
	opt = get_option(TIP, OPT_DESC, OPT_HO)

	ntBgn = time.time()

	func = opt2func(opt)
	func()

	debug.pr_info('%s costs %s' % (opt2desc(opt), time.time() - ntBgn, ))
