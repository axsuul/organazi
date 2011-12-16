from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from organazi.nfo import Nfo
from organazi.music import Track
from organazi.crawler import BeatportCrawler
import os
import glob
import re

import api.discogs as discogs

nfo = Nfo('test.nfo')
print nfo.parse()
#crawler = BeatportCrawler()
#print crawler.crawl("Andain", "Promises", "2011-06-13")