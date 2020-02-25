# MusicSelector
Made for my dad for one of his physical projects

If you are have PulseAudio errors still, install pulse audio with:
sudo apt-get install pulseaudio

You may need to force the audio to come out of the headphone jacks. To do so use:
sudo amixer -c 0 cset numid=3 1

to get the file to start when the pi first boots, use:
