# -*- coding: utf-8 -*-

###############################################################################
###
###############################################################################

import sys
import signal
import atexit
import time
import traceback
import multiprocessing

import debug

###############################################################################
###
###############################################################################

PROCESS_TOP = multiprocessing.cpu_count()

QUEUE_TOP = 60
QUEUE_TIMEOUT = 600
JOIN_TIMEOUT = 120

###############################################################################
###
###############################################################################

def raise_error(msg):
	if sys.exc_info()[0]:traceback.print_exc(file=sys.stderr)

	if isinstance(msg, str):sys.stderr.write(msg)

	sys.stderr.flush()

	return

def func_exit(process_cpu):
	for p in process_cpu:
		try:
			p.terminate()
			p.join()
		except:
			pass

	return

###############################################################################
###
###############################################################################

def target_mul(ins, func_mul, lock, queue):
	signal.signal(signal.SIGINT, signal.SIG_IGN)

	while(len(ins)!=0):
		lock.acquire()

		if len(ins):
			symf = ins.pop(0)
		else:
			lock.release()
			return

		lock.release()

		try:
			func_mul(symf, queue)
		except Exception, msg:
			raise_error(msg)

	return

def parse_mul(col, func_parse, func_to, sec_name):
	debug.pr_info('%s (%d child process)' % (sec_name, PROCESS_TOP, ))

	begtime = time.time()

	queue = multiprocessing.Queue(QUEUE_TOP)
	lock = multiprocessing.Lock()
	manager = multiprocessing.Manager()

	ins = manager.list(col)

	process_cpu = []
	for i in xrange(PROCESS_TOP):process_cpu.append(multiprocessing.Process(target=target_mul, args=(ins, func_parse, lock, queue, )))
	atexit.register(func_exit, process_cpu)

	try:
		for p in process_cpu:p.start()
		func_to(len(col), queue)
		for p in process_cpu:p.join()
	except KeyboardInterrupt:
		sys.exit(-1)

	debug.pr_info('%s end! Total file %d, time %s' % (sec_name, len(col), time.time() - begtime, ))

	return

###############################################################################
###
###############################################################################

def target_chain_mul(ins, ref_all, func_form, lock, queue):
	signal.signal(signal.SIGINT, signal.SIG_IGN)

	while(len(ins)!=0):
		lock.acquire()

		if len(ins):
			fname = ins.pop(0)
		else:
			lock.release()
			return

		lock.release()

		try:
			func_form(fname, ref_all, queue)
		except Exception, msg:
			raise_error(msg)

	return

def form_chain_mul(col_src, ref_all, func_form, func_to, sec_name):
	debug.pr_info('%s (%d child process)' % (sec_name, PROCESS_TOP, ))

	begtime = time.time()

	queue = multiprocessing.Queue(QUEUE_TOP)
	lock = multiprocessing.Lock()
	manager = multiprocessing.Manager()

	ins = manager.list(col_src)
	ref_ins = manager.dict(ref_all)

	process_cpu = []
	for i in xrange(PROCESS_TOP):process_cpu.append(multiprocessing.Process(target=target_chain_mul, args=(ins, ref_ins, func_form, lock, queue, )))
	atexit.register(func_exit, process_cpu)

	try:
		for p in process_cpu:p.start()
		func_to(len(col_src), queue)
		for p in process_cpu:p.join()
	except KeyboardInterrupt:
		sys.exit(-1)

	debug.pr_info('%s end! Total file %d, time %s' % (sec_name, len(col_src), time.time() - begtime, ))

	return
	

###############################################################################
###
###############################################################################
