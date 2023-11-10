"""
Program to perform a Caesar encryption. The program will:

Ask the user for the message to be encrypted.

Ask the user for a key.

Build the codeset from the alphabet shifted by the key.

Encode by finding the position of the message character within the alphabet
and then using that position within the codeset for the encoding.

Display the results and create a file of the Caesar cipher.

NOTE: I could have made this simpler by just doing calculations. 
However, I am checking more variables than just a simple encode. This
implementation allows for numbers to be used. Also, currently, it is 
stripping out punctuations.

NOTE: This code was created to help build code breaking programs.
And may change as I expand things out.

"""

import string
import os

os.system("Clear")

# get user inputs
print(f'\nCaesar Cipher\n')
keys = 0
data = input("Enter sentence to be encoded: ")
gotten_key = False

while not gotten_key:
    print('\nEnter a numeric key from 1 to 26')
    keys = input("Enter key: ")

    if keys.isnumeric():
        if int(keys) > 0 and int(keys) < 27:
            gotten_key = True
            keys = int(keys)
        else:
            print(f'\nThe key entered: {keys} is invalid, please try again.')
    else:
        print(f'\nThe key entered: {keys} is invalid, please try again.')

# Setup
alphabet = string.ascii_uppercase
punctuations = string.punctuation
digit = string.digits
cipher = ""

# Clean the input
data = data.upper()
data = data.translate(str.maketrans('', '', punctuations))
data = data.replace(" ", "")

# Shift the alphabet
codeSet = alphabet[keys:] + alphabet[0:keys]

# Encode
for letter in data:
    if letter not in alphabet:
        if letter in digit:
            cipher += letter
        else:
            continue
    else:
        pos = alphabet.find(letter)
        cipher += codeSet[pos]

# Print it out
print(f'\nCodeset: {codeSet}')
print(f"\nCipher text: {cipher}\n")

with open("Caesar_Cipher.txt", "w") as f:
    f.write(cipher)
    f.close()
