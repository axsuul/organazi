import os
import re
import urllib
import mechanize
import subprocess
import glob
import shutil
import mimetypes
from organazi.music import Track
from beautifulsoup.BeautifulSoup import BeautifulSoup

class RadioShow():
    def __init__(self, pathToRadioShow):
        self.path = pathToRadioShow
        self.baseName = os.path.splitext(os.path.basename(self.path))[0]
        self.artist = None
        self.episode = None
        self.showName = None
        self.pathToCue = None
        self.pathToTracks = []
       
        self.identify()
        self.outputRoot = os.path.join('M:', 'Radio Shows')
        self.outputDirectory = os.path.join(self.outputRoot, self.showName, self.episode)
        
        # make sure output directory is empty and create it
        if os.path.isdir(self.outputDirectory):
            shutil.rmtree(self.outputDirectory)
            
        try:
            os.mkdir(self.outputDirectory)
            
        except WindowsError:
            # try again
            os.mkdir(self.outputDirectory)
            
    def identify(self):
        def show(artist, showName, showShortName, albumArt, cueNationFolder, regExs):
            for regEx in regExs:
                match = re.search(re.compile(regEx, re.I), self.baseName)
            
                if match:
                    self.artist = artist
                    self.episode = match.group(1)
                    self.showName = showName
                    self.showShortName = showShortName
                    self.albumArt = albumArt
                    self.cueNationFolder = cueNationFolder
                    break
                    
        show("Above & Beyond",
             "Trance Around the World", 
             "TATW",
             "tatw.jpg",
             "http://cuenation.com/?page=cues&folder=tatw",
             ['Trance_Around_the_World_([0-9]+)'])
             
        show("Armin van Buuren",
             "A State of Trance", 
             "ASOT",
             "asot.jpg",
             "http://cuenation.com/?page=cues&folder=asot",
             ['A_State_of_Trance(?:_Episode)?_([0-9]+)'])
             
        show(None,
             "Anjunabeats Worldwide",
             "AW",
             "aw.jpg",
             "http://cuenation.com/?page=cues&folder=anjunabeats",
             ['Anjunabeats_Worldwide_([0-9]+)'])
             
        show("Will Holland",
             "Enhanced Sessions",
             "Enhanced Sessions",
             "enhanced.jpg",
             "http://cuenation.com/?page=cues&folder=enhancedrecordingsshow",
             ['Enhanced_Sessions_([0-9]+)'])
             
        show("Jaytech",
             "Jaytech Music",
             "Jaytech Music",
             "jaytech.jpg",
             "http://cuenation.com/?page=cues&folder=jaytechmusic",
             ['jaytechmusicpodcast([0-9]+)'])
             
        if not self.showName:
            raise Exception("Could not identify radio show!")
        
    def downloadCue(self):
        cueNation = "http://cuenation.com/"
        
        if self.showName:
            url = self.cueNationFolder
            html = BeautifulSoup(urllib.urlopen(url).read())
            episodeLinkHtml = html.find('a', text=re.compile(self.showName + ' (?:Podcast\s)?(?:Episode\s)?' + self.episode, re.I)).parent
            
            if episodeLinkHtml:
                 # if every show is different artist (like anjuneabts worldwide) try to determine it from the link
                if not self.artist:
                    self.artist = episodeLinkHtml.string.split("-")[0].strip()
            
                # parse the html to get the cue filename
                episodeLink = episodeLinkHtml['href']
                
                html = BeautifulSoup(urllib.urlopen(cueNation + episodeLink))
                cueLink = html.find('a', text="Download Cuesheet!").parent['href']
                cueFileName = cueLink.split("=")[-1]
                self.pathToCue = os.path.join(self.outputDirectory, cueFileName)
                
                # use browser to open link cause of referer shit
                browser = mechanize.Browser()
                browser.open(cueNation + episodeLink)
                req = browser.click_link(text='Download Cuesheet!')
                browser.open(req)
                
                cue = open(self.pathToCue, 'w')
                cue.write(browser.response().read())

                return self.pathToCue
                
            else:
                raise Exception("No cue found!")
       
    def isMp3(self):
        (type, encoding) = mimetypes.guess_type(self.path)
        return type in ['audio/x-mpg']
       
    def convertToMp3(self):
        ffmpeg = os.path.join('bin', 'ffmpeg', 'ffmpeg.exe')
      
        if not self.isMp3():    # if not mp3
            pathToMp3 = os.path.join(os.path.dirname(self.path), os.path.splitext(os.path.basename(self.path))[0] + '.mp3')
            subprocess.call([ffmpeg, '-y', '-i', self.path, pathToMp3])
            os.remove(self.path)
            self.path = pathToMp3
          
    def split(self):
        """split the radio show into multiple mp3"""
        subprocess.call([os.path.join('bin', 'mp3splt', 'mp3splt.exe'), 
                         '-c', 
                         self.pathToCue, 
                         self.path,
                         '-o',
                         '@n. @p - @t',
                         '-d',
                         self.outputDirectory,
                         '-q'])

        for pathToTrack in glob.glob(os.path.join(self.outputDirectory, '*.mp3')):
            self.pathToTracks.append(pathToTrack)
        
    def fixTags(self):
        album = "{0} {1}".format(self.showShortName, self.episode) 
        
        for pathToTrack in self.pathToTracks:
            track = Track(pathToTrack)
            track.fixTags()
            track.setAlbum(album)
            track.setAlbumArtist(self.artist)
            track.setAlbumArt(os.path.join('albumart', self.albumArt))
            
    def renameFromTags(self):
        """rename the tracks according to the tags"""
        newPathToTracks = []
        
        for pathToTrack in self.pathToTracks:
            track = Track(pathToTrack)
            track.renameFromTags("%tracknumber%. %artist% - %title%")
            
            newPathToTracks.append(track.getPath())
            
        self.pathToTracks = newPathToTracks
        
    def addToFoobar2000Playlist(self, playlist):
        foobar = os.path.join('C:/', 'Program Files (x86)', 'foobar2000', 'foobar2000.exe')
    
        for pathToTrack in self.pathToTracks:
            process = subprocess.Popen('"{0}" {1} "{2}"'.format(foobar, '/runcmd-files="Edit Other/Add to Playlist/{0}"'.format(playlist), pathToTrack))
            
            # wait until it adds
            process.wait()
                
    def remove(self):
        os.remove(self.path)
