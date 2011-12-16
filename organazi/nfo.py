import os
import re
import datetime

class Nfo():
    def __init__(self, pathToNfo):
        self.pathToNfo = pathToNfo
        self.dirName = os.path.basename(os.path.dirname(self.pathToNfo))
        self.group = None
        
    def getValidGroups(self):
        groups = ["PWT",
                  "H3X",
                  "TraX",
                  "sour"]
                  
        return groups
        
    def detectGroup(self):
        groupMatch = re.search(r'-([A-Za-z0-9]+)$', self.dirName)
        
        # attempt to get group from the directory name
        if groupMatch:
            potentialGroup = groupMatch.group(1)
            
            if potentialGroup in self.getValidGroups():
                self.group = potentialGroup
                
        
    def parse(self):
        file = open(self.pathToNfo, 'r')
        
        albumArtist = None
        album = None
        genre = None
        label = None
        catalogNumber = None
        releaseDate = None
        
        for line in file.readlines():
            keyMatch = re.search(r'([A-Za-z\(\)\s]+)\s?.*[:\[]+\s+([A-Za-z0-9&\(\):\-!\'\s]+)', line)
            
            if keyMatch:
                key = keyMatch.group(1).lower().strip()
                value = keyMatch.group(2).strip()
                
                if key == 'artist' or \
                   key == 'artist(s)':
                    albumArtist = value
                    
                elif key == 'title' or \
                     key == 'album':
                    album = value
                    
                elif key == 'genre':  
                    genre = value
                    
                elif key == 'label':
                    label = value
                    
                elif key == 'catalognr' or \
                     key == 'nr':
                    catalogNumber = value
                    
                elif re.search(r'date', key):
                    # normalize the date
                    releaseDateFormat = "%Y-%m-%d"
                    if re.match(r'[A-Za-z]{3,}-[0-9]{2}-[0-9]{4}', value):
                        releaseDate = datetime.datetime.strptime(value.capitalize(), "%b-%d-%Y").strftime(releaseDateFormat)

                    elif re.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value):
                        releaseDate = value
                    
        if album:
            # clean up the album (sometimes it can get messy)
            albumMatch = re.search(r'-?WEB', album)
            
            if albumMatch:
                album = album.replace(albumMatch.group(0), "")
                
            if catalogNumber:
                album = album.replace(catalogNumber, "")
                
            
            
        return (albumArtist, album, genre, label, catalogNumber, releaseDate)
