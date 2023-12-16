import pygame.mixer as mxr
from random import choice

# SOUND PREFS
PL = 1
DE = 2
START = 0
HOORAY = 1
FAIL = 2
GUN = 3
TOWER = 4
TRACK = 5
READY = 6


class SoundLoader:
    def __init__(self):
        self.polish_gun = ['sounds/pl/Armaty.wav',
                           'sounds/pl/Armaty2.wav']
        self.german_gun = ['sounds/de/geschuetz1.wav',
                           'sounds/de/geschuetz2.wav',
                           'sounds/de/geschuetz3.wav']
        self.polish_hooray = ['sounds/pl/poczuw.wav',
                              'sounds/pl/dziesiantka.wav',
                              'sounds/pl/Mam wiecej.wav']
        self.german_hooray = ['sounds/de/wirkung1.wav',
                              'sounds/de/wirkung2.wav',
                              'sounds/de/wirkung3.wav']
        self.polish_start = ['sounds/pl/do boju.wav',
                             'sounds/pl/do roboty.wav',
                             'sounds/pl/Jazda.wav']
        self.german_start = ['sounds/de/bewegung1.wav',
                             'sounds/de/bewegung2.wav',
                             'sounds/de/bewegung3.wav']
        self.polish_tower = ['sounds/pl/wieza zablokowana.wav',
                             'sounds/pl/Wieza zablokowana 2.wav']
        self.german_tower = ['sounds/de/Turm1.wav']
        self.polish_track = ['sounds/pl/Stoimy.wav']
        self.german_track = ['sounds/de/kette1.wav',
                             'sounds/de/kette2.wav']
        self.polish_fail = ['sounds/pl/prawie.wav',
                            'sounds/pl/bylo blisko.wav']
        self.german_fail = ['sounds/de/nicht1.wav',
                            'sounds/de/nicht2.wav']
        self.polish_ready = ['sounds/pl/gotow1.wav',
                             'sounds/pl/gotow2.wav',
                             'sounds/pl/gotow3.wav']
        self.german_ready = ['sounds/de/aus1.wav',
                             'sounds/de/aus2.wav',
                             'sounds/de/aus3.wav']

        mxr.music.load(choice(self.polish_start))
        mxr.music.queue(choice(self.german_start))
        mxr.music.play()

    def play_sound(self, sound, language):
        if language == DE:
            if sound == FAIL:
                mxr.music.load(choice(self.german_fail))
            elif sound == HOORAY:
                mxr.music.load(choice(self.german_hooray))
            elif sound == TOWER:
                mxr.music.load(choice(self.german_tower))
            elif sound == TRACK:
                mxr.music.load(choice(self.german_track))
            elif sound == GUN:
                mxr.music.load(choice(self.german_gun))
            elif sound == READY:
                mxr.music.load(choice(self.german_ready))
        elif language == PL:
            if sound == FAIL:
                mxr.music.load(choice(self.polish_fail))
            elif sound == HOORAY:
                mxr.music.load(choice(self.polish_hooray))
            elif sound == TOWER:
                mxr.music.load(choice(self.polish_tower))
            elif sound == TRACK:
                mxr.music.load(choice(self.polish_track))
            elif sound == GUN:
                mxr.music.load(choice(self.polish_gun))
            elif sound == READY:
                mxr.music.load(choice(self.polish_ready))
        mxr.music.play()
