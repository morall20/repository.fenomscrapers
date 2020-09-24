# -*- coding: utf-8 -*-
# (updated 9-20-2020)

'''
	Fenomscrapers Project
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import re

try: from urlparse import urljoin
except ImportError: from urllib.parse import urljoin

from fenomscrapers.modules import cleantitle
from fenomscrapers.modules import client
from fenomscrapers.modules import dom_parser
from fenomscrapers.modules import source_utils


class source:
	def __init__(self):
		self.priority = 31
		self.language = ['en']
		self.domains = ['watchseries.movie', 'watch-series.co']
		self.base_link = 'https://www6.watchseries.movie'
		self.search_link = '/series/%s-season-%s-episode-%s'


	def tvshow(self, imdb, tvdb, tvshowtitle, aliases, year):
		try:
			url = tvshowtitle.replace(" ", "-").lower()
			return url
		except:
			source_utils.scraper_error('WATCHSERIES')
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			url = urljoin(self.base_link, self.search_link % (url, season, episode))
			return url
		except:
			source_utils.scraper_error('WATCHSERIES')
			return


	def sources(self, url, hostDict):
		sources = []
		try:
			if not url: return sources

			result = client.request(url)

			dom = dom_parser.parse_dom(result, 'a', req='data-video')
			urls = [i.attrs['data-video'] if i.attrs['data-video'].startswith('https') else 'https:' + i.attrs['data-video'] for i in dom]

			for url in urls:
				if url in str(sources):
					continue
				valid, host = source_utils.is_host_valid(url, hostDict)
				if not valid:
					continue
				try: url.decode('utf-8')
				except: pass
				sources.append({'source': host, 'quality': 'SD', 'info': '', 'language': 'en', 'url': url, 'direct': False, 'debridonly': True})

			return sources
		except:
			source_utils.scraper_error('WATCHSERIES')
			return sources


	def resolve(self, url):
		return url