# -*- coding: utf-8 -*-

import art
import config

from collections import defaultdict
from tool_file import symf_relname
from evolve import form_chain_mul, QUEUE_TIMEOUT

################################################################################
###
################################################################################

def form_art_chain():
	art_src = map(symf_relname, art._art_src_ori_)

	ref_src = art._ref_src_
	ref_xml = art._ref_xml_

	ref_all = combine_ref(ref_src, ref_xml)
	mulif_x = art.get_process() == config.PROCESS_ONE

	form_chain_proc_one(art_src, ref_all) if mulif_x else form_chain_proc_mul(art_src, ref_all)

	return

def form_chain_proc_one(art_src, ref_all):
	ref_chain = {}
	for fname in art_src:ref_chain.update(col_chain(fname, ref_all))

	art._ref_chain_ = ref_chain

	return

def form_chain_proc_mul(art_src, ref_all):
	form_chain_mul(art_src, ref_all, col_chain_mul, to_art_chain, 'col chain')

	return

################################################################################
###
################################################################################

def combine_ref(ref_src, ref_xml):
	ref_all = defaultdict(set)

	for symf_src, symr_src_mul in ref_src.iteritems():
		rfname_src_mul = map(symf_relname, symr_src_mul)
		ref_all[symf_relname(symf_src)].update(rfname_src_mul)

	for symf_xml, symr_xml_mul in ref_xml.iteritems():
		fname_xml_mul = map(symf_relname, symr_xml_mul)
		ref_all[symf_relname(symf_xml)].update(fname_xml_mul)

	return ref_all

################################################################################
###
################################################################################

def col_chain(fname_src, ref_all):
	ret, zee = defaultdict(set), []
	if len(ref_all) == 0:return ret
	if fname_src not in ref_all:return {fname_src:set()}

	for fname in ref_all[fname_src]:
		if fname not in ref_all or len(ref_all[fname]) == 0:
			ret[fname_src].add(ref_text(fname_src, fname))
			continue

		result = walk_ref(ref_all, ref_text(fname_src, fname), ref_all[fname])
		for r in result:
			r_src, r_neo = r.split('\t')[0], r.split('\t')[1:]
			ret[r_src].add(r)
			zee.extend(r_neo)

	for z in zee:
		if z not in ret:continue
		ret.pop(z)

	return ret

def col_chain_mul(fname_src, ref_all, queue):
	queue.put(col_chain(fname_src, ref_all), block=True, timeout=QUEUE_TIMEOUT)

	return

def to_art_chain(size, queue):
	for i in xrange(size):
		ret = queue.get(block=True, timeout=QUEUE_TIMEOUT)
		art._ref_chain_.update(ret)

	return

def ref_text(pfile, cfile):return pfile + '\t' + cfile
def walk_ref(ref_all, fname, ref_sub):
	if len(ref_sub) == 0:
		yield ref_text(fname, '')
	else:
		for ref in ref_sub:
			if ref in ref_all:
				for text in walk_ref(ref_all, ref_text(fname, ref), ref_all[ref]):yield text
			else:
				yield ref_text(fname, ref)

################################################################################
###
################################################################################
