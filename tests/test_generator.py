import unittest
import generator

class TestGenerator(unittest.TestCase):

    def test_generate_word(self):
        random_word = generator.generate_word(4, 1)
        self.assertTrue(random_word)
        self.assertTrue(len(random_word)>=4)
        self.assertTrue(len(random_word.split("_")), 1)
        print(f"Random word was {random_word}")

    def test_multiple_words(self):
        random_word = generator.generate_word(4, 5)
        self.assertTrue(random_word)
        self.assertTrue(len(random_word)>=(4*5))
        self.assertTrue(len(random_word.split("_")), 5)
        print(f"Random word was {random_word}")

    def test_bad_phoneme_count(self):
        with self.assertRaises(ValueError) as valueError:
            generator.generate_word(0, 5)
        self.assertTrue("phoneme_count" in str(valueError.exception))

        with self.assertRaises(ValueError) as valueError:
            generator.generate_word(-1, 5)
        self.assertTrue("phoneme_count" in str(valueError.exception))

    def test_bad_word_count(self):
        with self.assertRaises(ValueError) as valueError:
            generator.generate_word(1, 0)
        self.assertTrue("word_count" in str(valueError.exception))

        with self.assertRaises(ValueError) as valueError:
            generator.generate_word(1, -1)
        self.assertTrue("word_count" in str(valueError.exception))

    def test_generator_pattern(self):
        random_word = generator.generate_word(pattern="CVVC", with_list=True)
        print(f"Random pattern word is: {random_word}")
        self.assertTrue(generator.phoneme_lists.is_consonant(random_word[1][0]))
        self.assertTrue(generator.phoneme_lists.is_vowel(random_word[1][1]))
        self.assertTrue(generator.phoneme_lists.is_vowel(random_word[1][2]))
        self.assertTrue(generator.phoneme_lists.is_consonant(random_word[1][3]))
