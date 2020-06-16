import gpiozero as io
from signal import pause
from subprocess import call
import vlc, os, random, pygame

class Station:
    track = 0
    active = False

    # -- Combination of GPIO pins to control the audio relay --
    def solotone():
        ttRelay.off()
        meloRelay.off()

    def melodylane():
        ttRelay.on()
        meloRelay.on()

    def topten():
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
        if self.wallbox == 3:
            if self.playing:
                return
            else:
                self.playing == True
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
            ttRelay.off()
            meloRelay.off()
            if self.wallbox == -1:
                self.wallbox = 3
                self.playing = False

    def __init__(self, pin, songLocation, iRadio, shuffle = True, shuffleOnActivation = False, wallbox = 1):
        self.pin = pin
        self.shuffleOnActivation = shuffleOnActivation
        self.button = io.Button(pin, pull_up=False) #bounce_time=0.2
        self.songLocation = songLocation
        self.iRadio = iRadio
        self.button.when_held = self.activateStation
        self.button.when_released = self.deactivateStation
        self.func = self.switcher.get(wallbox, lambda: "Not a valid box")
        self.wallbox = wallbox
        if(wallbox == 1):
            self.pic = "/media/pi/SOLOTONE/Images/SolotonePicNew2.jpg"
        elif(wallbox == 2):
            self.pic = "/media/pi/SOLOTONE/Images/MelodyPicNew.jpg"
        elif(wallbox == 3):
            self.pic = "/media/pi/SOLOTONE/Images/TopTenPicNew2.jpg"
            self.button.when_pressed = self.activateStation
            self.playing = False
        if iRadio == False:
            self.playlist = os.listdir(songLocation)
            if shuffle:
                random.shuffle(self.playlist)
        if self.button.is_active:
            self.activateStation()
