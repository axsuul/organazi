import wx
import mimetypes
import os
import subprocess
import glob
import re
import urllib, urllib2
import shutil
import time
from organazi.radioshow import RadioShow
from organazi.nfo import Nfo
from organazi.music import Track
from organazi.crawler import BeatportCrawler
from agw.multidirdialog import MultiDirDialog
from api import discogs

class ReleaseDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, "Choose Release")
        

class LogWindow(wx.TextCtrl):
    def __init__(self, parent):
        wx.TextCtrl.__init__(self, parent, style=wx.TE_MULTILINE|wx.TE_READONLY)
        
    def add(self, line):
        self.AppendText(line)
        self.ShowPosition(self.GetLastPosition()) 
        
    def addParent(self, line):
        self.AppendText(line)
        self.ShowPosition(self.GetLastPosition()) 
        
    def addChild(self, line, level = 1):
        indent = ""
    
        for i in range(0, level):
            indent += "\t\t"
        
        self.AppendText(indent + line)
        self.ShowPosition(self.GetLastPosition()) 
        
    def clear(self):
        self.SetValue("")
        self.Clear()

class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        
        divider = wx.BoxSizer(wx.HORIZONTAL)
        
        self.logWindow = LogWindow(self)
        divider.Add(self.logWindow, 1, wx.EXPAND)
        
        self.SetSizer(divider)
        
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Organazi", size=(900, 500))
        
        self.createMenuBar()
        self.createMainPanel()
        
        
        self.Show()
        
    def createMenuBar(self):
        fileMenu = wx.Menu()
        self.menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit", "Exit the program")
        
        radioShowMenu = wx.Menu()
        self.menuBrowseRadioShow = radioShowMenu.Append(wx.NewId(), "&Browse")
        
        releaseMenu = wx.Menu()
        self.menuBrowseRelease = releaseMenu.Append(wx.NewId(), "&Browse")
        
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(releaseMenu, "R&eleases")
        menuBar.Append(radioShowMenu, "R&adio Shows")
        
        self.Bind(wx.EVT_MENU, self.onRadioShowBrowse, self.menuBrowseRadioShow)
        self.Bind(wx.EVT_MENU, self.onReleaseBrowse, self.menuBrowseRelease)
        self.Bind(wx.EVT_MENU, self.onExit, self.menuExit)
        
        self.SetMenuBar(menuBar)
        
    def createMainPanel(self):
        self.mainPanel = MainPanel(self)
        
    def getLogWindow(self):
        return self.mainPanel.logWindow
        
    def onExit(self, event):
        self.Close(True)

    def onReleaseBrowse(self, event):
        dirDialog = MultiDirDialog(self, message="Choose Release Folder(s)", defaultPath=os.path.join('X:/', 'Usenet', 'Music'))
        dirDialog.SetSize(wx.Size(1000, 750))
        
        if dirDialog.ShowModal() == wx.ID_OK:
            self.getLogWindow().clear()
            jobCount = len(dirDialog.GetPaths())
            job = 0
            
            for path in dirDialog.GetPaths():
                job += 1
                timeStart = time.clock()
                
                self.getLogWindow().addParent("{0} of {1}: \t\t{2}\n".format(job, jobCount, path))

                albumArtist = None
                album = None
                genre = None
                label = None
                catalogNumber = None
                releaseDate = None
                albumArtUrl = None
                albumArtSource = None
                pathToAlbumArt = None
                
                # check if nfo in this folder
                globNfo = glob.glob(os.path.join(path, '*.nfo'))
                if len(globNfo) > 0:
                    pathToNfo = globNfo[0]
                    
                else:
                    pathToNfo = None
                    self.getLogWindow().addChild("FATAL: Could not find nfo!\n")
                    continue    # skip
                    
                # parse the nfo and obtain useful info
                if pathToNfo:
                    nfo = Nfo(pathToNfo)
                    (albumArtist, album, genre, label, catalogNumber, releaseDate) = nfo.parse()
                    
                # sanitize album, make sure it doesn't contain any (Incl bullshit)
                inclAlbumMatch = re.search(r'\s\(Incl.? [^)]+\)', album)
                
                if inclAlbumMatch:
                    album = album.replace(inclAlbumMatch.group(0), "")
                    
                # crawl websites and use apis and verify information and obtain album art
                # first crawl beatport for info mainly
                beatportCrawler = BeatportCrawler()
                results = beatportCrawler.crawl(albumArtist, album, releaseDate)
                beatportAlbumArtUrl = None
                
                self.getLogWindow().addChild("BEATPORT CRAWL: ")
                    
                if results:
                    (beatportAlbum, beatportLabel, beatportCatalogNumber, beatportReleaseDate, beatportAlbumArtUrl) = results
                        
                    # use beatport's info instead
                    if beatportAlbum:
                        album = beatportAlbum
                        
                    if beatportLabel:
                        label = beatportLabel
                        
                    if beatportCatalogNumber:
                        catalogNumber = beatportCatalogNumber
                        
                    if beatportReleaseDate:
                        releaseDate = beatportReleaseDate
                
                    self.getLogWindow().add("Success!\n")
                    self.getLogWindow().addChild("ALBUM: " + beatportAlbum + "\n", 2)
                    self.getLogWindow().addChild("LABEL: " + beatportAlbum + "\n", 2)
                    self.getLogWindow().addChild("CATALOG NUMBER: " + beatportCatalogNumber + "\n", 2)
                    self.getLogWindow().addChild("RELEASE DATE: " + beatportReleaseDate + "\n", 2)
                    self.getLogWindow().addChild("ALBUM ART: " + beatportAlbumArtUrl + "\n", 2)
                    
                else:
                    self.getLogWindow().add("Failed!\n")
                
                self.getLogWindow().addChild("DISCOGS SEARCH: ")
                
                # crawl discogs because we want their album artist and their album art is preferred, but they don't always have
                try:
                    discogsSearch = discogs.Search("{0} {1}".format(albumArtist, album))
                    discogsRelease = discogsSearch.results()[0]
                    
                    if discogsRelease.title == album:
                        self.getLogWindow().add("Success!\n")
                        discogsImages = discogsRelease.data.get('images')
                        
                        discogsAlbumArtists = discogsRelease.data.get('artists')
                        
                        if len(discogsAlbumArtists) == 1:
                            discogsAlbumArtist = discogsAlbumArtists[0]['name']
                            
                        elif len(discogsAlbumArtists) == 2:
                            discogsAlbumArtist = discogsAlbumArtists[0]['name'] + " & " + discogsAlbumArtists[1]['name']
                            
                        elif len(discogsAlbumArtists) == 3:
                            discogsAlbumArtist = "{0}, {1} & {2}".format(discogsAlbumArtists[0]['name'], discogsAlbumArtists[1]['name'], discogsAlbumArtists[2]['name'])
                        
                        self.getLogWindow().addChild("ALBUM ARTIST: {0}\n".format(discogsAlbumArtist), 2)
                        
                        # use discogs' album artist!
                        # get rid of (#) if its at the end of the line of the artist, Discogs likes to put it there 
                        # when there are duplicates
                        duplicateMatch = re.search(r'\s\([0-9]+\)$', discogsAlbumArtist)
                        
                        if duplicateMatch:
                            discogsAlbumArtist = discogsAlbumArtist.replace(duplicateMatch.group(0), "")
                        
                        albumArtist = unicode(discogsAlbumArtist)
                        
                        # check if there's album art, if so use it
                        if len(discogsImages) > 0:
                            albumArtSource = "Discogs.com"
                            discogsAlbumArt = discogsImages[0]['uri']
                            albumArtUrl = discogsAlbumArt
                            self.getLogWindow().addChild("ALBUM ART: {0}\n".format(discogsAlbumArt), 2)
                            
                            # fetch album art and save it
                            headers = { 'User-Agent' : 'Organazi/1.33.7 +http://at.home' }
                            request = urllib2.Request(albumArtUrl, '', headers)
                            response = urllib2.urlopen(request).read()
                            
                            pathToAlbumArt = os.path.join(path, 'albumart.jpg')
                            image = open(pathToAlbumArt, 'wb')
                            image.write(response)
                            image.close()
                            
                    else:
                        self.getLogWindow().add("Failed!\n")
                        
                except discogs.DiscogsAPIError:
                    self.getLogWindow().add("Failed!\n")
                    
                # alter other stuff
                genre = genre.capitalize()
                    
                # if still no album art yet, use beatport's (if it even exists, but usually does)
                if not albumArtUrl:
                    if beatportAlbumArtUrl:
                        albumArtSource = "Beatport"
                        
                        # first modify the album art url cause we want a bigger size
                        albumArtUrl = beatportAlbumArtUrl.replace("212x212", "1000x1000")
                        
                        #fetch album art and save it
                        response = urllib.urlopen(albumArtUrl).read()
                        
                        pathToAlbumArt = os.path.join(path, 'albumart.jpg')
                        image = open(pathToAlbumArt, 'wb')
                        image.write(response)
                        image.close()
                        
                # set the output directory
                if albumArtist and album:
                    artistDirectory = os.path.join('M:\\', 'Music', albumArtist)
                    outputDirectory = os.path.join(artistDirectory, album.replace("/", "_").replace(":", "_"))
                    
                    # do some checks, make sure we have everything before proceeding
                    if os.path.exists(outputDirectory):
                        self.getLogWindow().addChild("FATAL: This release has already been organazied!\n")
                        continue
                
                else:
                    self.getLogWindow().addChild("FATAL: This release is missing some vital information and cannot proceed!\n")
                    continue
                    
                self.getLogWindow().addChild(u"ARTIST: {0}\n".format(albumArtist.decode('utf-8')))
                self.getLogWindow().addChild(u"RELEASE: {0}\n".format(album))

                if genre:
                    self.getLogWindow().addChild("GENRE: {0}\n".format(genre))
                    
                if releaseDate:
                    self.getLogWindow().addChild("DATE: {0}\n".format(releaseDate))
                    
                if label:
                    self.getLogWindow().addChild("LABEL: {0}\n".format(label))
                    
                if catalogNumber:
                    self.getLogWindow().addChild("CATALOG NUMBER: {0}\n".format(catalogNumber))
                
                if pathToAlbumArt:
                    self.getLogWindow().addChild("ALBUM ART SOURCE: {0}\n".format(albumArtSource))
                    
                # loop through the mp3s
                for pathToTrack in glob.glob(os.path.join(path, '*.mp3')):
                    track = Track(pathToTrack)
                    track.setAlbum(album)
                    track.setAlbumArtist(albumArtist)
                    
                    if genre:
                        track.setGenre(genre)
                    
                    if label:
                        track.setLabel(label)
                        
                    if catalogNumber:
                        track.setCatalogNumber(catalogNumber)

                    if releaseDate:
                        track.setReleaseDate(releaseDate)
                        
                    track.fixTags()
                    
                    if pathToAlbumArt:
                        track.setAlbumArt(pathToAlbumArt)
                    
                    track.renameFromTags()
                    
                    # create artist directory if it doesn't exist
                    if not os.path.exists(artistDirectory):
                        os.mkdir(artistDirectory)
                    
                    # create output directory if it doesn't exist
                    if not os.path.exists(outputDirectory):
                        os.mkdir(outputDirectory)
                        
                    # move to output directory
                    newPath = os.path.join(outputDirectory, track.getFileName())
                    shutil.move(track.getPath(), newPath)
                    self.getLogWindow().addChild("MOVED: {0}\n".format(newPath))
                    
                # remove source directory (only if album art has been added)
                try:
                    if pathToAlbumArt:
                        pass
                        #shutil.rmtree(path)
            
                except WindowsError as error:
                    self.getLogWindow().addChild("ERROR: Couldn't remove source folder!\n")
            
                self.getLogWindow().addChild("FINISHED: {0} seconds!\n".format(round(time.clock() - timeStart), 2))
        dirDialog.Destroy()
        
    def onRadioShowBrowse(self, event):
        fileDialog = wx.FileDialog(self, message="Choose Radio Show", wildcard="*.mp3;*.m4a", style=wx.OPEN)
        
        if fileDialog.ShowModal() == wx.ID_OK:
            self.pathToRadioShow = fileDialog.GetPath()
            
            #try:
            self.mainPanel.logWindow.clear()
            
            self.mainPanel.logWindow.addParent("Identifying show... ")
            radioShow = RadioShow(self.pathToRadioShow)
            self.mainPanel.logWindow.addParent(radioShow.showName + " " + radioShow.episode + "\n")
            
            self.mainPanel.logWindow.addParent("Downloading cue file... ")
            radioShow.downloadCue()
            self.mainPanel.logWindow.addParent("done!\n")
            
            if not radioShow.isMp3():
                self.mainPanel.logWindow.addParent("Converting to mp3... ")
                radioShow.convertToMp3()
                self.mainPanel.logWindow.addParent("done!\n")
            
            self.mainPanel.logWindow.addParent("Splitting into tracks... ")
            radioShow.split()
            radioShow.fixTags()
            radioShow.renameFromTags()
            self.mainPanel.logWindow.addParent("done!\n")
            
            self.mainPanel.logWindow.addParent("Adding to Foobar2000... ")
            radioShow.addToFoobar2000Playlist("Radio Shows")
            self.mainPanel.logWindow.addParent("done!\n")
            
            self.mainPanel.logWindow.addParent("Cleaning up... ")
            radioShow.remove()
            self.mainPanel.logWindow.addParent("done!")
            
            wx.MessageBox("{0} is ready!".format(radioShow.showName), "Done!")
                
            #except Exception as error:
            self.mainPanel.logWindow.addParent(error.message)

        else:
            self.pathToRadioShow = None
            
        fileDialog.Destroy()
        
app = wx.App(False)
MainFrame()
app.MainLoop()
        