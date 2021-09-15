import os
import random

from enum import Enum
from typing import List
from xml.etree import ElementTree


class PhonemeType(Enum):
    consonant = "CONSONANT"
    vowel = "VOWEL"

    @classmethod
    def has_member_key(cls, key):
        return key in cls.__members__


class Phoneme(object):
    id: str
    alternative_id: str
    type: PhonemeType
    frequency: float

    def __init__(self, id: str, alternative_id: str, type: str, frequency: float):
        if(PhonemeType.has_member_key(type)):
            self.type = PhonemeType[type]
            self.id = id
            self.alternative_id = alternative_id
            self.frequency = frequency
        else:
            raise TypeError(f"'Type' must be a value in {[pt.value for pt in PhonemeType]}")

    def __str__(self):
        output = f"Phoneme for sound {self.id}"
        if(self.alternative_id):
            output += f", Alternate spelling = {self.alternative_id}"
        output += f", Type = {self.type}, sound frequency = {self.frequency}%"
        return output


class PhonemeList(object):
    phonemes: List[Phoneme]
    weights: List[float]

    def __init__(self, phonemes):
        self.phonemes = phonemes
        self.weights = []
        self._set_weights()
        if(len(self.phonemes) != len(self.weights)):
            raise ValueError(f"Size mismatch between list of phonemes ({len(self.phonemes)}) and list of weights ({len(self.weights)})")

    def get_random(self):
        return random.choices(self.phonemes, weights=self.weights)[0]

    def _set_weights(self):
        for phoneme in self.phonemes:
            self.weights.append(phoneme.frequency)

    def __len__(self):
        return len(self.phonemes)


class PhonemeLists(object):
    all_phonemes: PhonemeList
    consonants: PhonemeList
    vowels: PhonemeList

    def __init__(self, phonemes):
        self.all_phonemes = PhonemeList(phonemes)
        self._create_type_lists()

    def _create_type_lists(self):
        consonants = []
        vowels = []

        for phoneme in self.all_phonemes.phonemes:
            if(phoneme.type == PhonemeType.vowel):
                vowels.append(phoneme)
            else:
                consonants.append(phoneme)

        self.consonants = PhonemeList(consonants)
        self.vowels = PhonemeList(vowels)

    def is_consonant(self, target_phoneme):
        for phoneme in self.consonants.phonemes:
            if target_phoneme == phoneme.id:
                return True
        return False

    def is_vowel(self, target_phoneme):
        for phoneme in self.vowels.phonemes:
            if target_phoneme == phoneme.id:
                return True
        return False

    @classmethod
    def load_phonemes(cls, path=None):
        phonemes = []
        if(path == None):
            dirname = os.path.dirname(__file__)
            path = os.path.join(dirname, '../resources/PhonemeFrequency.xml')

        tree = ElementTree.parse(path)
        root = tree.getroot()

        for phoneme in root:
            attributes = phoneme.attrib
            name = attributes['name']
            alternative_id = attributes.get('alternate', "")
            type = attributes['type']
            frequency = float(phoneme.find("frequency").attrib['frequency'])
            phoneme = Phoneme(name, alternative_id, type, frequency)
            phonemes.append(phoneme)

        return PhonemeLists(phonemes)
