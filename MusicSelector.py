#!/usr/bin/python3

'''
- v 1.1.2
    -- Fixing bugs with TopTen box
- v 1.1.1
    -- Adding Ability to add more wallboxes to existing RPi.
    -- Adding ability to display current wallbox and song being played
'''

import gpiozero as io
from signal import pause
from subprocess import call
import vlc, os, random, pygame
from station import Station

# -- This is for the picture display --
pygame.init()

display_h = 600
display_w = 1024

gameDisplay = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#gameDisplay = pygame.display.set_mode((display_w,display_h))

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
toptenStation = Station(25,'/media/pi/SOLOTONE/TopTen', False,True, wallbox = 3)

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
