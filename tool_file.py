# -*- coding: utf-8 -*-

import os
import fnmatch

import art
import config
import debug

################################################################################
### symd symf syme symr 目录名 文件名(全路径) 后缀名 引用文件名(全路径) fname 相对目录
################################################################################

def relname_symf(fname):
	path_base = config.PATH_CONFG if 'confg' in fname else config.PATH_RES

	return os.path.join(path_base, fname)

def symf_relname(symf):
	symf = symf.replace('\\', '/')
	path_base = config.PATH_RES if config.PATH_RES in symf else config.PATH_CONFG

	return symf.split(path_base)[1]

def symf_1th_dir(symf):
	if 'confg' in symf:return config.PATH_1TH_GUI

	fname = symf_relname(symf)

	dir_1th = fname.split('/')[0] + '/' if '/' in fname else ''

	return os.path.join(config.PATH_RES, dir_1th)

################################################################################
###
################################################################################

def path_include(fdir):return not path_exclude(fdir)
def path_exclude(fdir):
	for fdir_ex in config.DIR_EXCLUDE:
		if fdir_ex in fdir:return True

	return False

def col_all_dir(path):
	file_chk = lambda x:path_exclude(x) or os.path.isfile(os.path.join(path, x))
	dir_col = [fpath for fpath in os.listdir(path) if not file_chk(fpath)]

	return sorted(dir_col)

def col_all_file(path):
	col = set()
	for root, dirs, files in os.walk(path):
		if path_exclude(root):continue
		if len(dirs) == 0 and len(files) == 0:continue

		col.update(os.path.join(root, fname).replace('\\', '/') for fname in files)

	return sorted(col)

def col_rel_file(path):
	path_res = config.PATH_RES
	all_file = col_all_file(path)

	return sorted(set([fname.split(path_res)[1] for fname in all_file]))

def col_ext_file(path, ext):
	col = set()
	fexp = '*.%s' % (ext, )

	for fname in fnmatch.filter(col_all_file(path), fexp):col.add(fname)

	return sorted(col)

def col_ext_file_mul(path, ext_mul):
	col = set()
	for ext in ext_mul:col.update(col_ext_file(path, ext))

	return sorted(col)

def col_all_ext(path):
	ext_col = set()
	for fname in col_all_file(path):
		ext = os.path.splitext(fname)[1]
		if ext == '' or len(ext) <= 1:continue

		ext_col.add(ext[1:])

	return sorted(ext_col)

################################################################################
###
################################################################################

def chk_fnm(path):
	for symf in col_all_file(path):
		if _chk_fnm_one(symf):continue

		debug.pr_fname(symf_relname(symf))

	return

def _chk_fnm_one(symf):
	body, ext = os.path.splitext(symf)

	if ' ' in symf or ext.lower() != ext or body.lower() != body or len(ext) <= 1:return False

	return True

################################################################################
###
################################################################################

def chk_file(path_src):
	debug.pr_march('check_hard_file:大写、空格、无后缀名\t%s' % (path_src, ))

	for path in path_src:chk_fnm(path)

	return

################################################################################
###
################################################################################

def col_src_hard(path_mul):
	for path in path_mul:
		file_hard = col_all_file(path)
		art._file_hard_.update(file_hard)

	write_file_hard(art._file_hard_)

	return art._file_hard_

################################################################################
###
################################################################################

def init_output_path(path):
	if not os.path.isdir(path):os.mkdir(path)

	return

################################################################################
###
################################################################################

def write_file_hard(file_hard):
	debug.pr_march('col_hard_file\t%s %d' % (config.PATH_RES, len(file_hard), ))

	objf_hard = open(config.PATH_FILE_HARD, 'w+')
	for symf in sorted(file_hard):objf_hard.write('%s\n' % (symf_relname(symf), ))

	objf_hard.close()

	debug.pr_info('所有的资源文件(hard)在 %s 中' % (config.PATH_FILE_HARD, ))

	return

def write_xml_ref():
	write_file_soft(art._file_soft_)
	write_err_lack_soft(art._file_hard_, art._file_soft_)
	write_err_lack_hard(art._err_src_, art._err_xml_)
	write_file_chain(art._ref_chain_)

	return

def write_file_soft(file_soft):
	objf_soft = open(config.PATH_FILE_SOFT, 'w+')
	for symf in sorted(file_soft):objf_soft.write('%s\n' % (symf_relname(symf), ))

	objf_soft.close()

	debug.pr_info('使用的资源文件(soft)在 %s 中' % (config.PATH_FILE_SOFT, ))

	return

def write_err_lack_soft(file_hard, file_soft):
	file_lack_soft = set(file_hard) - set(file_soft)
	objf_lack_soft = open(config.PATH_ERR_LACK_SOFT, 'w+')

	for symf in sorted(file_lack_soft):objf_lack_soft.write('%s\n' % (symf_relname(symf), ))

	objf_lack_soft.close()

	debug.pr_info('未使用的资源文件(lack_soft)在 %s 中' % (config.PATH_ERR_LACK_SOFT, ))

	return

def write_err_lack_hard(err_src, err_ref):
	objf_err = open(config.PATH_ERR_LACK_HARD, 'w+')

	for fname in sorted(err_src.iterkeys()):
		for err in sorted(err_src[fname]):objf_err.write('%s\t-->\t%s\n' % (fname, err, ))

	objf_err.write('\n')

	for symf in sorted(err_ref.iterkeys()):
		for symr in sorted(err_ref[symf]):
			if 'aid_builder' in symr:continue
			objf_err.write('%s\t-->\t%s\n' % (symf_relname(symf), symf_relname(symr), ))

	objf_err.close()

	debug.pr_info('错误的引用编号或文件(lack_hard)在 %s 中' % (config.PATH_ERR_LACK_HARD, ))

	return

def write_file_chain(file_chain):
	objf_cross = open(config.PATH_XML_REF_CROSS, 'w+')
	for fname, ref in sorted(file_chain.iteritems(), key=lambda t:t[0]):
		for r in sorted(ref):objf_cross.write('%s\n' % (r, ))

	objf_cross.close()

	debug.pr_info('资源的相互引用关系(cross)在 %s 中' % (config.PATH_XML_REF_CROSS, ))

	return

################################################################################
###
################################################################################
