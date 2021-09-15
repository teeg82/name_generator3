import random

from models.phoneme import (
    PhonemeLists,
    )

phoneme_lists = PhonemeLists.load_phonemes()

def generate_word(phoneme_count:int=4, word_count:int=2, pattern:str="", with_list=False):
    if(phoneme_count <= 0):
        raise ValueError("phoneme_count must be greater than 0")

    if(word_count <= 0):
        raise ValueError("word_count must be greater than 0")

    output = []

    if(not pattern):
        pattern = generate_pattern(phoneme_count, word_count)

    for phoneme_type in pattern:
        if phoneme_type == "V":
            phoneme = phoneme_lists.vowels.get_random().id
        elif phoneme_type == "C":
            phoneme = phoneme_lists.consonants.get_random().id
        elif phoneme_type == " ":
            phoneme = " "
        else:
            phoneme = phoneme_type
        output.append(phoneme)

    if with_list:
        return_value = ("".join(output), output)
    else:
        return_value = "".join(output)

    return return_value

def generate_pattern(phoneme_count:int, word_count:int):
    output = []
    for word_index in range(word_count):
        word=[]
        use_vowel = bool(random.getrandbits(1))
        for index in range(phoneme_count):
            if(use_vowel):
                word.append("V")
            else:
                word.append("C")
            use_vowel = not use_vowel
        output.append("".join(word))
    return " ".join(output)

