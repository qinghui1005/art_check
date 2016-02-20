# -*- coding: utf-8 -*-

###############################################################################
###
###############################################################################

import os
import sys
import zipfile
import struct

import art
import art_src
import art_chain
import config
import tool_xml
import tool_file

from collections import defaultdict
from debug import tr_exists, pr_error, pr_warn
from evolve import QUEUE_TIMEOUT, parse_mul

###############################################################################
###
###############################################################################

def check_xml():
	path_out = config.PATH_OUT
	path_src = config.PATH_SRC

	tool_file.init_output_path(path_out)
	collect_file(path_src)

	do_check()

	return

def collect_file(path_src):
	art.init_file()

	tool_file.col_src_hard(path_src)
	art_src.collect_art_src()

	return

def do_check():
	art.init_ref()

	parse_art_src()

	art_chain.form_art_chain()

	tool_file.write_xml_ref()

	return

###############################################################################
###
###############################################################################

def parse_art_src():
	col_src = art._art_src_col_
	mulif_x = art.get_process() == config.PROCESS_ONE

	parse_xml_proc_one(col_src) if mulif_x else parse_xml_proc_mul(col_src)

	return

def parse_xml_proc_one(col_src):
	file_soft, file_ref, err_ref = set(), defaultdict(set), defaultdict(set)

	for symf in col_src:
		ref = parse_xml(symf)
		for key, val in ref.iteritems():
			file_soft.add(key)
			for v in val:
				if not tr_exists(symf, 'xml', v, echo=False):
					err_ref[key].add(v)
					continue
				if os.path.isdir(v):continue

				file_soft.add(v)
				file_ref[key].add(v)

	art._file_soft_ = file_soft
	art._err_xml_ = err_ref
	art._ref_xml_ = file_ref

	return

def parse_xml_proc_mul(col_src):
	parse_mul(col_src, parse_xml_mul, to_art_ref, 'parse ref')

	return

def parse_xml_mul(symf, queue):
	queue.put(parse_xml(symf), block=True, timeout=QUEUE_TIMEOUT)

	return

def to_art_ref(size, queue):
	for i in xrange(size):
		ref = queue.get(block=True, timeout=QUEUE_TIMEOUT)
		for key, val in ref.iteritems():
			art._file_soft_.add(key)
			for v in val:
				if os.path.isdir(v):continue
				if not tr_exists(key, 'xml', v, echo=False):
					art._err_xml_[key].add(v)
					continue

				art._file_soft_.add(v)
				art._ref_xml_[key].add(v)

	return

################################################################################
###
################################################################################

def parse_xml(symf):
	body, fsuff = os.path.splitext(symf)
	symd, syme = tool_file.symf_1th_dir(symf), fsuff.strip('.')

	ret = defaultdict(set)
	ret[symf] = set()

	if symd not in config.PATH_TAG or syme not in  config.PATH_TAG[symd].keys():
		if syme in config.EXT_XML:pr_warn('need parse %s' % (symf, ))
		return ret

	func_tag = config.PATH_TAG[symd][syme]

	mod = sys.modules[globals()['__name__']]

	etree = tool_xml.xml_root(symf)
	for func, tag_mul in func_tag.iteritems():
		for tag in tag_mul:
			for ele in etree.findall(tag):
				if not ele.text or ele.text.strip() == '':continue

				for ref_mul in getattr(mod, func)(symf, ele.text.strip()):
					for symr, ref in ref_mul.iteritems():ret[symr].update(ref)

	return ret

################################################################################
###
################################################################################

def parse_art_com(symf, ref):
	symr = tool_file.relname_symf(ref)

	yield {symf:[symr], }

def parse_art_ref(symf, ref):
	symr = tool_file.relname_symf(ref)

	yield {symf:[symr], }

	if tr_exists(symf, '', symr, echo=False):yield parse_xml(symr)

def parse_font_system(symf, ref):
	symr = os.path.join(config.PATH_2TH_FONTS, ref)

	yield {symf:[symr], }

def parse_space_cdata(symf, ref):
	objd = os.path.dirname(symf)
	cdata, prefix = ref.split('/')

	dct = {}
	symf_cdata = os.path.join(objd, cdata).replace('\\', '/')

	try:
		cdata_file = zipfile.ZipFile(symf_cdata, 'r')
	except zipfile.BadZipfile:
		pr_error('parse_space_cdata ziperror %s' % (symf, ))
		yield dct

	for item in cdata_file.namelist():
		if item[0:len(prefix)] != prefix:continue

		dct[symf] = [symf_cdata]
		if 'dominantTextures' in item:
			dct.setdefault(symf_cdata, [])
			dct[symf_cdata].extend(_parse_dominant_texture(cdata_file, item))

	yield dct

def _parse_dominant_texture(cdata_file, item):
	fp = cdata_file.open(item)
	header = struct.unpack('<8I', fp.read(4 * 8))
	magic, version, texNum, texNmSize, width, height, pad, sep = header

	col = []
	for i in xrange(texNum):
		texName, = struct.unpack('%ds' % (texNmSize, ), fp.read(texNmSize))
		texName = texName.strip('\x00') + '.tga'

		col.append(tool_file.relname_symf(texName))

	return col

def parse_model_visual(symf, ref):
	ref_visual, ref_prim = ref + '.visual', ref + '.primitives'
	symr_visual, symr_prim = tool_file.relname_symf(ref_visual), tool_file.relname_symf(ref_prim)

	yield {symf:[symr_visual, symr_prim], }

	if tr_exists(symf, '', symr_visual, echo=False):yield parse_xml(symr_visual)

def parse_spec_visual(symf, ref):
	symr = tool_file.relname_symf(ref)
	body, suff = os.path.splitext(symr)

	ref_model, ref_prim = body + '.model',  body + '.primitives'

	col = [symr, ref_prim]
	model_y = True if tr_exists(symf, '', ref_model, echo=True) else False

	if model_y:col.append(ref_model)

	yield {symf:col, }

	if tr_exists(symf, '', symr, echo=False):yield parse_xml(symr)

	if model_y:yield parse_xml(ref_model)

def parse_visual_fx(symf, ref):
	symr = tool_file.relname_symf(ref)
	body, suff = os.path.splitext(symr)

	col = [body + '.9.fxo', body + '.11.fxo']

	yield {symf:col, }

def _parse_texture_one(symf, ref):
	symr = tool_file.relname_symf(ref)
	body, suff = os.path.splitext(symr)
	if symr[-6:] in ['_n.dds']:return [body + '.pcx']
	if suff in ['.pcx', '.bmp', '.tga']:return [symr]
	if suff in ['.dds']:
		col = [body + ext for ext in ['.bmp', '.tga'] if tr_exists(symf, '', tool_file.relname_symf(body + ext), echo=False)]
		if len(col) == 0:col.append(symr)

		return col

	return [symr]

def parse_texture_com(symf, ref):
	col = _parse_texture_one(symf, ref)

	symr = tool_file.relname_symf(ref)
	body, suff = os.path.splitext(symr)

	symr_texanim = body + '.texformat'
	if tr_exists(symf, 'texture->texformat', symr_texanim, echo=False):col.append(symr_texanim)

	yield {symf:col, }

def parse_effect_animation(symf, ref):
	symr = tool_file.relname_symf(ref)
	body, suff = os.path.splitext(symr)

	yield {symf:[body + '.animation'], }

################################################################################
###
#################################################################################
