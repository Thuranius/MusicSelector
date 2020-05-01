#!/usr/bin/python3

'''
- v 1.1.0
    -- Adding Ability to add more wallboxes to existing RPi.
    -- Adding ability to display current wallbox and song being played
'''

import gpiozero as io
from signal import pause
from subprocess import call
import vlc, os, random, pygame, webbrowser

# -- This is for the picture display --
pygame.init()

display_h = 600
display_w = 1024

#gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((display_w,display_h))

picToUse = pygame.image.load('/media/pi/SOLOTONE/Images/Cover.jpg')

font = pygame.font.SysFont('comicsansms', 60)
npText = font.render("", True, (225,225,225))
text = font.render('', True, (225,225,225))

pygame.mixer.init()
# --------------------------------

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

# These will be the 'LED' GPIO pins that go back to the relay to switch them off and on
ttRelay = io.LED(2)
meloRelay = io.LED(3)

ttRelay.off()
meloRelay.off()

# -- Station Class: Build individual stations from this class -- #
class Station:
    track = 0
    active = False

    def solotone():
        print("This will print stuff for the solotone")
        ttRelay.off()
        meloRelay.off()

    def melodylane():
        print("This is the melodylane")
        ttRelay.on()
        meloRelay.on()

    def topten():
        # This one is momentary and will not not stay activated consistantly
        print("Top ten here!")
        ttRelay.on()
        meloRelay.off()

    switcher = {
        1: solotone,
        2: melodylane,
        3: topten
    }

    def queueManager(self):
        while self.active:
            if int(pygame.mixer.music.get_pos()) == -1:
                if self.track == len(self.playlist)-1:
                    if self.wallbox == 3:
                        self.wallbox = -1
                        self.deactivateStation()
                        return
                    else:
                        self.track = 0
                else:
                    self.track += 1
                pygame.mixer.music.load(self.songLocation + '/' + self.playlist[self.track])
                pygame.mixer.music.set_volume(1.0)
                pygame.mixer.music.play()
                print("Now Playing: " + self.playlist[self.track])
                global text, npText
                npText = font.render("Now Playing:", True, (225,225,225))
                text = font.render(self.playlist[self.track].replace('.mp3', ''), True, (225,225,225))

    def activateStation(self):
        self.active = True
        self.func()
        global picToUse
        picToUse = pygame.image.load(self.pic)
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
            global text,npText
            npText = font.render("Now Playing:", True, (225,225,225))
            text = font.render(self.playlist[self.track].replace('.mp3', ''), True, (225,225,225))
            self.queueManager()
        
    def deactivateStation(self):
        if self.wallbox != 3:
            self.active = False
            ttRelay.off()
            meloRelay.off()
            print("Pin " + str(self.pin) + " has been deactivated")
            global picToUse
            picToUse = pygame.image.load('/media/pi/SOLOTONE/Images/Cover.jpg')
            if self.iRadio:
                self.player.stop()
            else:
                pygame.mixer.music.stop()
                global text, npText
                npText = font.render("", True, (225,225,225))
                text = font.render('', True, (225,225,225))

    def __init__(self, pin, songLocation, iRadio, shuffle = True, shuffleOnActivation = False, wallbox = 1):
        self.pin = pin
        self.shuffleOnActivation = shuffleOnActivation
        self.button = io.Button(pin, pull_up=False) #bounce_time=0.2
        self.songLocation = songLocation
        self.iRadio = iRadio
        self.button.when_held = self.activateStation
        self.button.when_released = self.deactivateStation
        self.func = self.switcher.get(wallbox, lambda: "Not a valid box") # -- *1 --
        self.wallbox = wallbox
        if(wallbox == 1):
            self.pic = "/media/pi/SOLOTONE/Images/SolotonePicNew2.jpg"
        elif(wallbox == 2):
            self.pic = "/media/pi/SOLOTONE/Images/MelodyPicNew.jpg"
        elif(wallbox == 3):
            self.pic = "/media/pi/SOLOTONE/Images/TopTenPicNew2.jpg"
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
# || Solotone Stations
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

# || Stations for the two new wallboxes
melodyStation = Station(16,'/media/pi/SOLOTONE/Melodylane', False,True, wallbox = 2)
toptenStation = Station(25,'/media/pi/SOLOTONE/TopTen', False,False, wallbox = 3)

print('Music player is ready for use!')

black = (0,0,0)

running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False    
    gameDisplay.fill(black)
    gameDisplay.blit(picToUse, (0,0))
    gameDisplay.blit(npText, (((display_w / 2)-(npText.get_width()/2)),(display_h * 0.7)-npText.get_height()))
    gameDisplay.blit(text, (((display_w / 2)-(text.get_width()/2)),display_h * 0.7))
    pygame.display.update()

pygame.quit()
