from beautifulsoup.BeautifulSoup import BeautifulSoup
import re
import urllib
from htmlentitydefs import name2codepoint

class Crawler():
    def __init__(self):
        pass
        
    def decodeHtml(self, html):
        return html.replace('&amp;', '&') \
                   .replace('&lt;', '<') \
                   .replace('&gt;', '>') \
                   .replace('&quot;', '"') \
                   .replace('&#039;', "'") \
                   .replace('&#39;', "'")

class BeatportCrawler(Crawler):
    def __init__(self):
        self.domain = "http://beta.beatport.com"
        
    def crawl(self, albumArtist, album, releaseDate):
        releaseFound = False
        searchPage = urllib.urlopen("{0}/search?query={1}&facets[]=fieldType:release".format(self.domain, urllib.quote(albumArtist + " " + album))).read()
        searchHtml = BeautifulSoup(searchPage)
        #releaseLinks = searchHtml.findAll('a', { 'name' : 'unit_title' })
        releaseLinks = []
        releases = searchHtml.findAll('li', { 'name' : re.compile('tiles-list_release_[0-9]+') })
        
        for release in releases:
            thisTitle = release.find('a', { 'name' : 'unit_title' })
            thisAlbum = thisTitle.string
            thisUrl = thisTitle['href']
            thisDate = release.find('span', { 'class' : 'itemRenderer-minor' }).contents[1].replace(" | ", "").strip()
            print thisDate
            if releaseDate and releaseDate == thisDate:
                releaseUrl = thisUrl
                beatportAlbum = thisAlbum
                releaseFound = True
                break
                
        if releaseFound:
            # open the release page
            releasePage = urllib.urlopen("{0}{1}".format(self.domain, releaseUrl))
            releaseHtml = BeautifulSoup(releasePage)
            
            # now that we are here, we can obtain some of the release info
            releaseInfoLabels = releaseHtml.findAll('td', { 'class' : 'meta-data-label' })
            
            beatportReleaseDate = releaseInfoLabels[0].nextSibling.string
            beatportLabel = releaseInfoLabels[1].nextSibling.a.string
            beatportCatalogNumber = releaseInfoLabels[2].nextSibling.string
            beatportAlbumArtUrl = releaseHtml.find('img', { 'class' : 'tile-image' })['src']
                
            return (self.decodeHtml(beatportAlbum), 
                    self.decodeHtml(beatportLabel), 
                    self.decodeHtml(beatportCatalogNumber), 
                    self.decodeHtml(beatportReleaseDate), 
                    beatportAlbumArtUrl)
