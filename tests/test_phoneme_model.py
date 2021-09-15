import unittest
import os
from xml.etree import ElementTree
from models.phoneme import (
    Phoneme,
    PhonemeLists,
    )
from math import ceil

class TestPhonemeModel(unittest.TestCase):

    def test_xml_load(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../resources/PhonemeFrequency.xml')
        tree = ElementTree.parse(filename)
        root = tree.getroot()
        self.assertEqual(root.tag, "phonemes")

    def test_load_phonemes(self):
        expected_phonemes = 40
        expected_vowels = 17
        expected_consonants = 40-17
        percentage = 0

        phonemeLists = PhonemeLists.load_phonemes()

        self.assertEqual(len(phonemeLists.all_phonemes), expected_phonemes, f"Should contain {expected_phonemes} phonemes")
        self.assertEqual(len(phonemeLists.vowels), expected_vowels, f"Should contain {expected_vowels} vowel phonemes")
        self.assertEqual(len(phonemeLists.consonants), expected_consonants, f"Should contain {expected_consonants} consonant phonemes")

        self.assertEqual(ceil(sum([phoneme.frequency for phoneme in phonemeLists.all_phonemes.phonemes])), 100)

    def test_bad_phoneme_type(self):
        with self.assertRaises(TypeError) as typeError:
            Phoneme("foo", "bar", "baz", 100.0)

    def test_weights_list(self):
        """Expect instantiated PhonemeList to have weight lists matching 1-to-1 with phoneme list"""
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, 'resources/test_phonemes.xml')
        phoneme_lists = PhonemeLists.load_phonemes(path)

        expected_vowels = [
            {"name":"i", 'frequency':9.9},
            {"name":"ee", 'frequency':5.0},
            {"name":"er", 'frequency':3.4},
        ]

        expected_consonants = [
            {"name":"n", 'frequency':7.8},
            {"name":"s", 'frequency':6.8},
            {"name":"t", 'frequency':6.8},
        ]

        vowels = phoneme_lists.vowels
        for index, vowel in enumerate(vowels.phonemes):
            self.assertEqual(vowel.id, expected_vowels[index]['name'])
            self.assertEqual(vowel.frequency, expected_vowels[index]['frequency'])
            self.assertEqual(vowels.weights[index], expected_vowels[index]['frequency'])

        consonants = phoneme_lists.consonants
        for index, consonant in enumerate(consonants.phonemes):
            self.assertEqual(consonant.id, expected_consonants[index]['name'])
            self.assertEqual(consonant.frequency, expected_consonants[index]['frequency'])
            self.assertEqual(consonants.weights[index], expected_consonants[index]['frequency'])

    def test_get_choice(self):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, 'resources/test_phonemes.xml')
        phoneme_lists = PhonemeLists.load_phonemes(path)

        random_phoneme = phoneme_lists.vowels.get_random()
        self.assertTrue(random_phoneme)
        print(f"Random phoneme was: {random_phoneme.id}")
