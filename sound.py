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
        self.polish_gun = ['pl/Armaty.wav',
                           'pl/Armaty2.wav']
        self.german_gun = ['de/geschuetz1.wav',
                           'de/geschuetz2.wav',
                           'de/geschuetz3.wav']
        self.polish_hooray = ['pl/poczuw.wav',
                              'pl/dziesiantka.wav',
                              'pl/Mam wiecej.wav']
        self.german_hooray = ['de/wirkung1.wav',
                              'de/wirkung2.wav',
                              'de/wirkung3.wav']
        self.polish_start = ['pl/do boju.wav',
                             'pl/do roboty.wav',
                             'pl/Jazda.wav']
        self.german_start = ['de/bewegung1.wav',
                             'de/bewegung2.wav',
                             'de/bewegung3.wav']
        self.polish_tower = ['pl/wieza zablokowana.wav',
                             'pl/Wieza zablokowana 2.wav']
        self.german_tower = ['de/Turm1.wav']
        self.polish_track = ['pl/Stoimy.wav']
        self.german_track = ['de/kette1.wav',
                             'de/kette2.wav']
        self.polish_fail = ['pl/prawie.wav',
                            'pl/bylo blisko.wav']
        self.german_fail = ['de/nicht1.wav',
                            'de/nicht2.wav']
        self.polish_ready = ['pl/gotow1.wav',
                             'pl/gotow2.wav',
                             'pl/gotow3.wav']
        self.german_ready = ['de/aus1.wav',
                             'de/aus2.wav',
                             'de/aus3.wav']

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
