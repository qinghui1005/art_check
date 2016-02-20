# -*- coding: utf-8 -*-

import os

################################################################################
###
################################################################################

PROCESS_ONE = 1
PROCESS_MUL = 2

################################################################################
###
################################################################################

PATH_ME = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')
PATH_PROJECT = PATH_ME

################################################################################
###
################################################################################

def path_join(pdir, cdir):return os.path.join(pdir, cdir).replace('\\', '/')

PATH_RES = path_join(PATH_PROJECT, 'res_art/')
PATH_CONFG = path_join(PATH_PROJECT, 'script_res/')

PATH_SRC = frozenset((
	PATH_RES,
	PATH_CONFG,
))

PATH_1TH_GUI = path_join(PATH_CONFG, 'newui/')
PATH_1TH_EFFECT = path_join(PATH_RES, 'effect/')
PATH_1TH_MATERIAL = path_join(PATH_RES, 'materials/')
PATH_1TH_MCHAR = path_join(PATH_RES, 'mchar/')
PATH_1TH_SPACE = path_join(PATH_RES, 'space/')

PATH_2TH_FONTS = path_join(PATH_RES, r'system/fonts/')

################################################################################
###
################################################################################

PATH_OUT = path_join(PATH_ME, 'output/')

PATH_FILE_HARD = path_join(PATH_OUT, 'file_hard.txt')
PATH_FILE_SOFT = path_join(PATH_OUT, 'file_soft.txt')

PATH_ERR_LACK_SOFT = path_join(PATH_OUT, 'err_lack_soft.txt')
PATH_ERR_LACK_HARD = path_join(PATH_OUT, 'err_lack_hard.txt')

PATH_XML_REF_CROSS = path_join(PATH_OUT, 'xml2ref_cross.txt')

################################################################################
###
################################################################################

DIR_EXCLUDE = frozenset(('.svn', 'shaders_new', 'shader_editor', ))

EXT_XML = frozenset((
	'chunk', 'chunk2', 'font', 'gui', 'localsettings', 'mfm', 'model',
	'ppchain', 'settings', 'template', 'texanim', 'visual', 'vlo', 'xml',
))

EXT_EXCLUDE = frozenset((
	'anca', 'py', 'swp', 'iml',
))

################################################################################
### gui
################################################################################

TAG_GUI = {
	'gui':{
		'parse_art_com':frozenset((
			'bgres/xml',		#.xml in visualstate
			)),
		'parse_texture_com':frozenset((
			'bgres/image',					#.png
			'.//textureName',				#.png, .dds
			)),
		'parse_art_ref':frozenset((
			'bgres/texanim',	#.texanim
			)),
		'parse_font_system':frozenset((
			'bgres/font',				#.font
			)),
		},
	'xml':{
		},
	}

################################################################################
### effect
################################################################################

TAG_1TH_EFFECT = {
	'mfm':{
		'parse_texture_com':frozenset((
			'property/Texture',		#.dds, .bmp, .tga
			)),
		'parse_visual_fx':frozenset((
			'fx',				#.fx
			)),
		},
	'model':{
		'parse_texture_com':frozenset((
			'dye/tint/material/property/Texture',	#.dds, .bmp, .tga
			)),
		'parse_visual_fx':frozenset((
			'dye/tint/material/fx',		#.fx
			)),
		'parse_model_visual':frozenset((
			'nodelessVisual',		#.visual
			'nodefullVisual',		#.visual
			)),
		'parse_effect_animation':frozenset((
			'animation/nodes',		#auto add .animation
			)),
		},
	'visual':{
		'parse_art_ref':frozenset((
			'renderSet/geometry/primitiveGroup/material/mfm',		#.mfm
			)),
		'parse_visual_fx':frozenset((
			'renderSet/geometry/primitiveGroup/material/fx',		#.fx
			)),
		},
	}

################################################################################
### model
################################################################################

TAG_1TH_MODEL = {
	'model':{
		'parse_texture_com':frozenset((
			'dye/tint/material/property/Texture',	#.dds, .bmp, .tga
			)),
		'parse_model_visual':frozenset((
			'nodelessVisual',		#.visual
			'nodefullVisual',		#.visual
			)),
		'parse_visual_fx':frozenset((
			'dye/tint/material/fx',		#.fx
			)),
		'parse_effect_animation':frozenset((
			'animation/nodes',		#auto add .animation
			)),
		},
	'visual':{
		'parse_texture_com':frozenset((
			'renderSet/geometry/primitiveGroup/material/property/Texture',	#.tag, .bmp, .texanim
			)),
		'parse_art_ref':frozenset((
			'renderSet/geometry/primitiveGroup/material/mfm',		#.mfm
			)),
		'parse_visual_fx':frozenset((
			'renderSet/geometry/primitiveGroup/material/fx',		#.fx,检测.11.fxo 和 .9.fxo,同时存在
			)),
		},
	'texanim':{
		'parse_texture_com':frozenset((
			'texture',			#.bmp, .png, .tag
			)),
		},
	}

################################################################################
### space
################################################################################

TAG_1TH_SPACE = {
	'chunk':{
		'parse_art_com':frozenset((
			'pulseLight/animation',	#.animation
			)),
		'parse_art_ref':frozenset((
			'model/resource',	#.model
			'particles/resource',	#.xml
			)),
		'parse_space_cdata':frozenset((
			'terrain/resource',	#.cdata/terrain2
			'worldNavmesh/resource',#.cdata/worldNavmesh
			'shadowmap/resource',	#.cdata/shadowmap.dds
			)),
		},
	'chunk2':{
		},
	'settings':{
		'parse_texture_com':frozenset((
			'cubeMap',		#.dds
			)),
		'parse_art_ref':frozenset((
			'flora',		#.xml
			'timeOfDay',		#.xml
			'skyGradientDome',	#.xml
			)),
		'parse_spec_visual':frozenset((
			'skyDome',		#.visual
			)),
		},
	'localsettings':{
		},
	'vlo':{
		'parse_texture_com':frozenset((
			'water/foamTexture',		#.dds
			'water/reflectionTexture',	#.dds
			'water/waveTexture',		#.dds
			)),
		},
	}

################################################################################
###
################################################################################

PATH_TAG = {
	PATH_1TH_GUI:TAG_GUI,
	PATH_1TH_EFFECT:TAG_1TH_EFFECT,
	PATH_1TH_MCHAR:TAG_1TH_MODEL,
	PATH_1TH_SPACE:TAG_1TH_SPACE,
}

################################################################################
###
################################################################################
