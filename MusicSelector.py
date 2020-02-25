#!/usr/bin/python3

import gpiozero as io
from signal import pause
from subprocess import call
import vlc, os, random, pygame

pygame.mixer.init()

# -- Station Class: Build individual stations from this class -- #
class Station:
    track = 0
    active = False
    
    def queueManager(self):
        while self.active:
            if int(pygame.mixer.music.get_pos()) == -1:
                if self.track == len(self.playlist)-1:
                    self.track = 0
                else:                
                    self.track += 1
                pygame.mixer.music.load(self.songLocation + '/' + self.playlist[self.track])
                pygame.mixer.music.play()
    
    def activateStation(self):
        self.active = True
        if self.iRadio:
            self.player = vlc.MediaPlayer(self.songLocation)
            self.player.play()
        else:
            pygame.mixer.music.load(self.songLocation + '/' + self.playlist[self.track])
            pygame.mixer.music.play(0)
            self.queueManager()
    
    def deactivateStation(self):
        self.active = False
        if self.iRadio:
            self.player.stop()
        else:
            pygame.mixer.music.stop()
    
    def __init__(self, pin, songLocation, iRadio, shuffle = True):
        self.button = io.Button(pin, pull_up=False, bounce_time=0.2) 
        self.songLocation = songLocation
        self.iRadio = iRadio
        self.button.when_held = self.activateStation
        self.button.when_released = self.deactivateStation
        if iRadio == False:
            self.playlist = os.listdir(songLocation)
            if shuffle:
                random.shuffle(self.playlist)
        if self.button.is_active:
            self.activateStation()

# -- Shutdown function -- #
def shutdown():
    call("sudo poweroff", shell=True)

# -- Adding stations from class -- #
# -- Blueprint for stations:
# -- <station name> = Station(<pin number>, <Station URL/Song Folder Location>, <Is this station internet radio?>, <Do you want to shuffle the tracks?>)
station01 = Station(17,'/media/pi/solotone/Station One', False, False)
station02 = Station(27,'http://uk6.internet-radio.com:8465', True)
station03 = Station(22,'http://71.125.37.66:8000/stream', True)
station04 = Station(10,'http://71.125.37.66:8000/stream', True)
station05 = Station(9,'/media/pi/solotone/Station Five', False)
station06 = Station(11,'/media/pi/solotone/Station Six', False)
station07 = Station(5,'/media/pi/solotone/Station Seven', False)
station08 = Station(6,'/media/pi/solotone/Station Eight', False)
station09 = Station(13,'/media/pi/solotone/Station Nine', False)
station10 = Station(19,'/media/pi/solotone/Station Ten', False)
station11 = Station(26,'/media/pi/solotone/Station Eleven', False)
station12 = Station(18,'/media/pi/solotone/Station Twelve', False)
station13 = Station(23,'/media/pi/solotone/Station Thirteen', False)
station14 = Station(24,'/media/pi/solotone/Station Fourteen', False)

# -- Creating shutdown button and overriding the when_held function -- #
shutdownButton = io.Button(21, hold_time=3)
shutdownButton.when_held = shutdown

pause()