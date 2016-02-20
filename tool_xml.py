# -*- coding: utf-8 -*-

import sys
import re
import xml.etree.ElementTree as ET

from collections import defaultdict

from debug import pr_error

################################################################################
###
################################################################################

RES_ART_REGEX = re.compile(r'^/*(?P<base>[^:*?<>\\/]+)(/[^:*?<>\\/]+)*\.(?P<ext>\w+)$')

################################################################################
###
################################################################################

def xml_child(sec):return [] if sec is None else [c for c in sec]
def tag_text(ptag, ctag):return  ptag + '/' + ctag 
def xml_replace(symf):
	f = open(symf, 'r')
	text = f.read()
	f.close()

	text = re.sub(r'<!--[^>]*-->',r'',text)

	return text

def verify_art(text):
	if text is None or text.strip() == '':return False

	text = text.strip()
	if not isinstance(text, basestring):return False

	if re.match('[\u4e00-\u9fa5]+', text) is None:return False	#判断汉字

	if len(text.split('.')) == 1:
		if '/' not in text:return False
		if text.replace('/', '').isdigit():return False
	else:
		if text.split('.')[-1] == '':return False
		if not text.split('.')[-1].isalnum():return False
		if text.split('.')[-1][0].isdigit():return False

	return True

################################################################################
###
################################################################################

def xml_iter(etree):return etree.getiterator if sys.version_info < (2, 7) else etree.iter
def xml_root(symf):
	try:
		tree = ET.parse(symf)
	except:
		text = xml_replace(symf)
		try:
			tree = ET.fromstring(text)
		except:
			pr_error('Parse xml error!!! file name is %s' % (symf, ))
			raise

	try:
		return tree.getroot()
	except:
		return tree

def walk_xml(tag, node, depth=None, ret=None):
	if depth == None:depth = [0]
	if ret == None:ret = defaultdict(set)

	depth[0] -= 1
	if verify_art(node.text):ret[tag].add(node.text.strip())

	if depth[0] > 0:
		for child in xml_child(node):
			depth[0] += len(xml_child(child))
			for r in walk_xml(tag_text(tag, child.tag), child, depth=depth, ret=ret):yield r
	else:
		yield ret

################################################################################
###
################################################################################
