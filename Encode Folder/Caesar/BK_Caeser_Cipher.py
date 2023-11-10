import os
import string
from collections import Counter
import wordninja

os.system("Clear")

line = ''
dashes = ""
cFile = 'Caesar_Cipher.txt'
aFile = "BK_Caesar_Analysis.txt"
alphabet = string.ascii_uppercase
top5FQ = 'ETAOI'

# Get the cipher
with open(cFile, "r") as f:
    msg = f.read()
    f.close()

# Get english words
with open('english_words.txt') as word_file:
    valid_words = set(word_file.read().split())


def shift(key):
    return alphabet[key:] + alphabet[0:key]


def decode(codeset):
    cipher = ''
    for letter in msg:
        if letter not in alphabet:
            cipher += letter
        else:
            pos = codeset.find(letter)
            cipher += alphabet[pos]

    return cipher


def word_count(sentence):
    cnt = 0

    for word in valid_words:
        word = word.upper()
        if word in words:
            cnt += 1

    return cnt


# Start building this mess
line += '\n\nCaesar Cipher Analysis\n'
line += f'\nInput message\n{msg}'

char_cnt = Counter(msg)
char_cnt = dict(char_cnt)
char_cnt = sorted(char_cnt.items(), key=lambda x: x[1], reverse=True)

# Using the letter frequency, take the top five frequency and see
# if we can guess the key.
line += f'\n\nFrequency distribution evaluation'
line += f'\n{char_cnt}\n'
line += f'\nTop five frequency key search.\n'

for i in range(5):
    top_letter = list(char_cnt)[i][0]
    top_letter_pos = alphabet.find(top_letter) + 1
    FQ_pos = alphabet.find(top5FQ[i]) + 1
    key = top_letter_pos - FQ_pos

    if key < 0:
        nkey = key + 26
        line += f'\nEntry #{i+1} Cipher letter: {top_letter} for {top5FQ[i]} Calculation: ({top_letter_pos} - {FQ_pos} = {key}) Key: {key} ({nkey})'
    else:
        line += f'\nEntry #{i+1} Cipher letter: {top_letter} for {top5FQ[i]} Calculation: ({top_letter_pos} - {FQ_pos} = {key}) Key: {key}'

    codeSet = shift(key=key)
    cipher = decode(codeset=codeSet)
    line += f'\nCode set: {codeSet}\n{cipher}\n'

    words = wordninja.split(cipher)

    cnt = word_count(words)

    if cnt > 2:
        line += "\n*** Possible words found:\n"
        x = ' '.join(words)
        line += (f'{x}\n')

# Try brute force
line += (f"\n\nBrute Force evaluation\n")

for x in range(1, 26):
    codeSet = shift(key=x)
    cipher = decode(codeset=codeSet)
    words = wordninja.split(cipher)
    line += (f"\nCode set key using key {x}: {codeSet}\n{cipher}\n")

    cnt = word_count(words)

    if cnt > 2:
        line += "\n*** Possible words found:\n"
        x = ' '.join(words)
        line += (f'{x}\n')

# Write the file
with open(aFile, "w") as f:
    f.write(line)
    f.close()

print(f'\nAnalysis file {aFile} saved.\n')
