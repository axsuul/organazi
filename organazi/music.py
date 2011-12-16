import re
import os
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

class Track():
    def __init__(self, path):
        self.setDirectory(os.path.dirname(path))
        self.setPath(path)
        self.tags = EasyID3(self.getPath())
        self.tags.RegisterTXXXKey('albumartist', 'ALBUM ARTIST')    # register the album artist tag
        self.tags.RegisterTXXXKey('catalognumber', 'CATALOGNUMBER')    # register the catalog number tag
        self.tags.RegisterTextKey('comments', "COMM::'eng'")        # comments
        
    def setDirectory(self, directory):
        self.directory = directory
        
    def getDirectory(self):
        return self.directory
        
    def setPath(self, path):
        self.path = path
        self.setFileName(os.path.basename(self.path))
        
    def getPath(self):
        return self.path
        
    def setFileName(self, fileName):
        self.fileName = fileName
        
    def getFileName(self):
        return self.fileName
        
    def fixTags(self):
        """fix the artist, titles, track number and format them a certain way"""
        artist = self.getArtist()
        albumArtist = self.getAlbumArtist()
        title = self.getTitle()
        trackNumber = self.getTrackNumber()
        album = self.getAlbum()
            
        # determine featuring if it exists
        featuringMatch = re.search(r'\sf(?:ea)?t. (.+)$', artist)
        
        if featuringMatch:
            featuring = featuringMatch.group(1).strip()
            artist = artist.replace(featuringMatch.group(0), "")
            
        else:
            # try searching for it in the title
            featuringMatch = re.search(re.compile('\s\(f(?:ea)?t.?\s([^()]+)\)', re.IGNORECASE), title)
            
            if featuringMatch:
                featuring = featuringMatch.group(1).strip()
                title = title.replace(featuringMatch.group(0), "")
                
            else:
                # another variation
                featuringMatch = re.search(re.compile('\sFeat.?\s(.+)$', re.IGNORECASE), artist)
                
                if featuringMatch:
                    featuring = featuringMatch.group(1).strip()
                    artist = artist.replace(featuringMatch.group(0), "")
                    
                else:
                    featuring = None
                    
        # determine presents if it exists
        presentsMatch = re.search(r'pres. (.+)$', artist)
        
        if presentsMatch:
            presents = presentsMatch.group(1)
            artist = artist.replace(presentsMatch.group(0), "")
            
        else:
            presents = None
        
        # get rid of featuring and/or presents in the album artist
        if albumArtist:
            featuringMatch = re.search(r'\sf(?:ea)?t. (.+)$', albumArtist)
            
            if featuringMatch:
                albumArtist = albumArtist.replace(featuringMatch.group(0), "")
            
            else:
                featuringMatch = re.search(re.compile('\sFeat.?\s(.+)$', re.IGNORECASE), albumArtist)
                
                if featuringMatch:
                    albumArtist = albumArtist.replace(featuringMatch.group(0), "")
                    
            presentsMatch = re.search(r'pres. (.+)$', albumArtist)
            
            if presentsMatch:
                albumArtist = albumArtist.replace(presentsMatch.group(0), "")
            
        # get rid of original remix if it exists
        originalRemixMatch = re.search(r'\s\(Original (?:Remix|Mix)\)$', title)
        
        if originalRemixMatch:
            title = title.replace(originalRemixMatch.group(0), "")
            
        # get the remix if it exists
        remixMatch = re.search(r'\s\(([^()]+\s(?:Remix|Mix|Dub|Edit))\)', title)
        
        if remixMatch:
            remix = remixMatch.group(1)
            title = title.replace(remixMatch.group(0), "")
            
        else:
            remix = None
            
        # get special label (for radio shows only usually)
        specialLabelMatch = re.search(r'\s\[([^\]]+)\]$', title)
        
        if specialLabelMatch:
            specialLabel = specialLabelMatch.group(1)
            title = title.replace(specialLabelMatch.group(0), "")
            
        else:
            specialLabel = None
            
        # fix vs. if it exists
        vsMatch = re.search(re.compile('\svs.?\s', re.IGNORECASE), artist)
        
        if vsMatch:
            artist = artist.replace(vsMatch.group(0), " vs. ")
          
        # get rid of Incl in the album title
        albumInclMatch = re.search(re.compile('\s\(Incl.? (?:[^)]+)\)', re.IGNORECASE), album)
        
        if albumInclMatch:
            album = album.replace(albumInclMatch.group(0), "")
          
        # fix track number
        trackTotalMatch = re.search(r'[0-9]+(/[0-9]+)', trackNumber)
        
        if trackTotalMatch:
            trackNumber = trackNumber.replace(trackTotalMatch.group(1), "")
        
        trackNumber = str(int(trackNumber)) # get rid of leading zero
          
        # now format the title
        if featuring:
            title = "{0} (feat. {1})".format(title, featuring)
            
        if remix:
            title = "{0} ({1})".format(title, remix)
            
        if specialLabel:
            title = "{0} [{1}]".format(title, specialLabel)
          
        # now save the tags
        self.setArtist(artist)
        
        if albumArtist:
            self.setAlbumArtist(albumArtist)
            
        self.setTitle(title)
        self.setAlbum(album)
        self.setTrackNumber(trackNumber)
        
    def getArtist(self):
        return self.tags['artist'][0].strip()
        
    def setArtist(self, artist):
        self.tags['artist'] = artist
        self.tags.save()
        
    def getTitle(self):
        return self.tags['title'][0].strip()
        
    def setTitle(self, title):
        self.tags['title'] = title
        self.tags.save()
        
    def getTrackNumber(self):
        return self.tags['tracknumber'][0].strip()
        
    def setTrackNumber(self, trackNumber):
        self.tags['tracknumber'] = trackNumber
        self.tags.save()
        
    def getAlbum(self):
        return self.tags['album'][0].strip()
        
    def setAlbum(self, album):
        self.tags['album'] = album
        self.tags.save()
    
    def getGenre(self):
        return self.tags['genre']
    
    def setGenre(self, genre):
        self.tags['genre'] = genre
        self.tags.save()
    
    def getLabel(self):
        return self.tags['organization']
    
    def setLabel(self, label):
        self.tags['organization'] = label
        self.tags.save()
        
    def getCatalogNumber(self):
        try:
            return self.tags['catalognumber']
        
        except KeyError:
            return ""
            
    def setCatalogNumber(self, catalognumber):
        self.tags['catalognumber'] = catalognumber
        self.tags.save()
        
    def getAlbumArtist(self):
        try:
            return self.tags['albumartist'][0].strip()
        
        except KeyError:
            return None
            
    def setAlbumArtist(self, albumArtist):
        self.tags['albumartist'] = albumArtist
        self.tags['albumartistsort'] = albumArtist
        self.tags.save()
        
    def setAlbumArt(self, pathToAlbumArt):
        """sets album art, do not use this method before fixing tags or the album art will get wiped!"""
        mp3 = MP3(self.getPath(), ID3=ID3)
        
        # add ID3 tag if it doesn't exist
        try:
            mp3.add_tags()  
        except error:
            pass
        
        mp3.tags.add(
            APIC(
                encoding=3, # 3 is for utf-8
                mime='image/jpeg', # image/jpeg or image/png
                type=3, # 3 is for the cover image
                desc=u'Cover',
                data=open(pathToAlbumArt, 'rb').read()
            )
        )
        
        mp3.save()
      
    def getReleaseDate(self):
        return self.tags['date'][0].strip()
        
    def setReleaseDate(self, releaseDate):
        self.tags['date'] = releaseDate
        self.tags.save()
      
    def clearComments(self):
        self.tags['comments'] = ""
        self.tags.save()
        
    def getComments(self):
        try:
            return self.tags['comments'][0].strip()
        
        except KeyError:
            return ""
        
    def setComments(self, comments):
        self.tags['comments'] = comments
        self.tags.save()
        
    def renameFromTags(self, format = "%artist% - %title%"):
        format = format.replace("%artist%", self.getArtist())
        format = format.replace("%title%", self.getTitle())
        format = format.replace("%tracknumber%", "%02s" % self.getTrackNumber())
    
        newPathToTrack = os.path.join(self.getDirectory(), "{0}.mp3".format(format))
        
        try:
            os.rename(self.getPath(), newPathToTrack)
            
        except WindowsError:
            pass
            
        self.setPath(newPathToTrack)