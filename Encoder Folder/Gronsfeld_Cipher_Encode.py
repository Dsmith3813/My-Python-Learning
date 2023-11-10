import string
import wordninja
import os


def Gronsfeld_Cipher_Encode(data, keys, decode=False):
    # Gronsfeld Cipher encoding. While, this encryption by itself isn't
    # much these days, however, this implementation is different.
    #
    # We are using a set of numeric key values; ex: [1,2,3,4].
    # Loop thru the plain text and extract a letter
    # Then cycle thru the key set and shift the codeset by the key value
    # Substitute the letter with the corresponding codeset character.
    # Add substituted value to the cipher text.
    # The shifted codeset is then used as input for the next shift.
    # There is no limit to the number of keys that can be used.
    # There is a limit to the key value to fall between 1 and 26 inclusive.
    # There is no restriction to repeating keys values. Ex: [1,3,3,13,13] is
    #  a valid sequence.

    codeSet = alphabet
    data = data.upper()

    # Set the keys to negative when decoding.
    if decode:
        keys = [-1 * int(k) for k in keys]

    ks = len(keys)
    cipher = ""

    print('\nPrinting shifted code sets.\n')

    # Loop to apply the Vigenere encryption/decryption using
    # Gronsfeld Cipher encoding.
    for i in range(len(data)):
        letter = data[i]            # Grab a letter from plain text

        if letter not in alphabet:  # Only alphabetics
            char = letter           # Keep all else as is
        else:
            k = keys[i % ks]      # cycle thru the keys

            # shift the codeset by this key value
            codeSet = codeSet[int(k):] + codeSet[0:int(k)]
            print(f'Codeset: {codeSet}')

            char = codeSet[ord(letter) - 65]  # Substitute

        cipher += char      # Add to cipher

    return cipher


os.system("Clear")

print(f'\nGronsfeld Cipher\n')
keys = []
num_keys = 0
gotten_key = False

alphabet = string.ascii_uppercase
punctuations = string.punctuation
digit = string.digits

# Decide what we are doing here, encoding or decoding.
Q = input("What function to perform; E for encoding, D for decoding? ")
Q = Q.upper()

if Q not in 'ED':
    print(f'Invalid input, input not E or D, defaulting to Encoding.\nInput given: {Q}')
    Q = 'E'

# Get message to be processed.
if Q == 'E':
    data = input("\nEnter sentence to be encoded: ")
else:
    data = input("\nEnter sentence to be decoded: ")

# Clean the input
data = data.upper()
data = data.translate(str.maketrans('', '', punctuations))
data = data.replace(" ", "")

print("\nEnter numeric keys values from 1 to 26. Enter 'x' to end sequence")

while not gotten_key:
    x = ''
    x = input("Enter key: ")

    if x == 'x':
        gotten_key = True
    elif x.isnumeric():
        if int(x) > 0 and int(x) < 27:
            keys.append(int(x))
        else:
            print(f'\nThe key entered: {x} is invalid, please try again.')
    else:
        print(f'\nThe key entered: {x} is invalid, please try again.')

print(f'\nKeys used for encoding: {keys}')

if Q == 'E':
    cipher = Gronsfeld_Cipher_Encode(data=data, keys=keys, decode=False)
    print(f'\nEncoded message:\n{cipher}\n')
else:
    cipher = Gronsfeld_Cipher_Encode(data=data, keys=keys, decode=True)
    cipher = wordninja.split(cipher)
    cipher = ' '.join(cipher)
    print(f'\nDecoded message:\n{cipher}\n')
