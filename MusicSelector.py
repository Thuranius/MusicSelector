#!/usr/bin/python3

'''
- v 1.1.0
    -- Adding Ability to add more wallboxes to existing RPi.
    -- Adding ability to display current wallbox and song being played

*1 :: Added 4/10/2020
'''

import gpiozero as io
from signal import pause
from subprocess import call
import vlc, os, random, pygame

pygame.mixer.init()

led = io.LED(12)

# LED switch
def turnOnLight():
    led.on()
    print("Turning on the light")
def turnLightOff():
    for n in range(100):
        led.value = (1 - n/100)
    print("Turning off the light")

lightButton = io.Button(4, pull_up=False)
lightButton.when_pressed = turnOnLight
lightButton.when_released = turnLightOff

# -- *1 --
# These will be the 'LED' GPIO pins that go back to the relay to switch them off and on
soloRelay = io.LED(8)
meloRelay = io.LED(7)

# -- */1 --

# -- Station Class: Build individual stations from this class -- #
class Station:
    track = 0
    active = False

    # -- *1 --
    def solotone(self):
        # For the future: Will need to add variable information here to send to webserver to display the correct info on screen
        print("This will print stuff for the solotone")
        soloRelay.off()
        meloRelay.off()

    def melodylane(self):
        print("This is the melodylane")
        soloRelay.on()
        meloRelay.on()

    def topten(self):
        print("Top ten here!")
        soloRelay.on()
        meloRelay.off()

    switcher = {
        1: solotone,
        2: melodylane,
        3: topten
    }
    # -- */1 --

    def queueManager(self):
        while self.active:
            if int(pygame.mixer.music.get_pos()) == -1:
                if self.track == len(self.playlist)-1:
                    self.track = 0
                else:
                    self.track += 1
                pygame.mixer.music.load(self.songLocation + '/' + self.playlist[self.track])
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                print("Now Playing: " + self.playlist[self.track])

    def activateStation(self):
        self.active = True
        self.func() # -- *1 --
        print("Pin " + str(self.pin) + " is active")
        if self.iRadio:
            self.player = vlc.MediaPlayer(self.songLocation)
            self.player.play()
        else:
            if self.shuffleOnActivation:
                random.shuffle(self.playlist)
            print(self.playlist)
            pygame.mixer.music.load(self.songLocation + '/' + self.playlist[self.track])
            pygame.mixer.music.play(0)
            print("Now Playing: " + self.playlist[self.track])
            self.queueManager()

    def deactivateStation(self):
        self.active = False
        print("Pin " + str(self.pin) + " has been deactivated")
        if self.iRadio:
            self.player.stop()
        else:
            pygame.mixer.music.stop()

    def __init__(self, pin, songLocation, iRadio, shuffle = True, shuffleOnActivation = False, wallbox = 1):
        self.pin = pin
        self.shuffleOnActivation = shuffleOnActivation
        self.button = io.Button(pin, pull_up=False) #bounce_time=0.2
        self.songLocation = songLocation
        self.iRadio = iRadio
        self.button.when_held = self.activateStation
        self.button.when_released = self.deactivateStation
        self.func = self.switcher.get(wallbox, lambda: "Not a valid box") # -- *1 --
        if iRadio == False:
            self.playlist = os.listdir(songLocation)
            if shuffle:
                random.shuffle(self.playlist)
        if self.button.is_active:
            self.activateStation()

# -- Shutdown function -- #
def shutdown():
    call("sudo poweroff", shell=True)

# -- Creating shutdown button and overriding the when_held function -- #
shutdownButton = io.Button(21, hold_time=3)
shutdownButton.when_held = shutdown

# -- Adding stations from class -- #
# -- Blueprint for stations:
# -- <station name> = Station(<pin number>, <Station URL/Song Folder Location>, <Is this station internet radio?>, <Do you want to shuffle the tracks?>, <Do you want to shuffle on every activation?>)
station01 = Station(17,'/media/pi/SOLOTONE/Station One', False, False)
station02 = Station(27,'http://uk6.internet-radio.com:8465', True)
station03 = Station(22,'http://71.125.37.66:8000/stream', True)
station04 = Station(10,'http://71.125.37.66:8000/stream', True)
station05 = Station(9,'/media/pi/SOLOTONE/Station Five', False, True, True)
station06 = Station(11,'/media/pi/SOLOTONE/Station Six', False, True, True)
station07 = Station(5,'/media/pi/SOLOTONE/Station Seven', False, True, True)
station08 = Station(6,'/media/pi/SOLOTONE/Station Eight', False, True, True)
station09 = Station(13,'/media/pi/SOLOTONE/Station Nine', False, True, True)
station10 = Station(19,'/media/pi/SOLOTONE/Station Ten', False, True, True)
station11 = Station(26,'/media/pi/SOLOTONE/Station Eleven', False, True,True)
station12 = Station(18,'/media/pi/SOLOTONE/Station Twelve', False, True, True)
station13 = Station(23,'/media/pi/SOLOTONE/Station Thirteen', False, True, True)
station14 = Station(24,'/media/pi/SOLOTONE/Station Fourteen', False, True, True)

# -- *1 --
melodyStation = Station(25,'/media/pi/melodylane', False,True, wallbox = 2)
toptenStation = Station(16,'/media/pi/topten', False,True, wallbox = 3)
# -- */1 --




pause()

'''
-- *1 --
Future plan: adding monitor to display song and wallbox information.
 - Option 1: Look into webserver/opening website to localhost to display information
    -- This path would entail sockets communicating to the webserver with the appropriate info.
 - Option 2: Get a GUI involved.
    -- This may benefit from more than likely being able to keep everything in one program
'''
