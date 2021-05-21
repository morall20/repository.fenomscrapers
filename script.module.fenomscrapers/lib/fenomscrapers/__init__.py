# -*- coding: UTF-8 -*-

import os
from pkgutil import walk_packages
from fenomscrapers.modules import control
from fenomscrapers.modules import log_utils

debug = control.setting('debug.enabled') == 'true'

def sources(specified_folders=None):
	try:
		sourceDict = []
		sourceFolder = getScraperFolder()
		sourceFolderLocation = os.path.join(os.path.dirname(__file__), sourceFolder)
		sourceSubFolders = [x[1] for x in os.walk(sourceFolderLocation)][0]
		sourceSubFolders = [x for x in sourceSubFolders if  '__pycache__' not in x]
		if specified_folders:
			sourceSubFolders = specified_folders
		for i in sourceSubFolders:
			for loader, module_name, is_pkg in walk_packages([os.path.join(sourceFolderLocation, i)]):
				if is_pkg: continue
				if enabledCheck(module_name):
					try:
						module = loader.find_module(module_name).load_module(module_name)
						sourceDict.append((module_name, module.source()))
					except Exception as e:
						if debug: log_utils.log('Error: Loading module: "%s": %s' % (module_name, e), level=log_utils.LOGWARNING)
		return sourceDict
	except:
		log_utils.error()
		return []

def getScraperFolder():
	try:
		sourceSubFolders = [x[1] for x in os.walk(os.path.dirname(__file__))][0]
		return [i for i in sourceSubFolders if 'fenomscrapers' in i.lower()][0]
	except:
		log_utils.error()
		return 'sources_fenomscrapers'

def enabledCheck(module_name):
	try:
		if control.setting('provider.' + module_name) == 'true': return True
		else: return False
	except:
		log_utils.error()
		return True

def pack_sources():
	return ['bitlord', 'bt4g', 'btdb', 'btscene', 'extratorrent', 'idope', 'kickass2', 'limetorrents', 'magnetdl', 'piratebay',
				'solidtorrents', 'torrentapi', 'torrentdownload', 'torrentfunk', 'torrentgalaxy', 'torrentparadise',
				'torrentz2', 'yourbittorrent', 'zooqle']