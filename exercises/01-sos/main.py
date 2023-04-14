import time

morse_code = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}

def to_morse_code(text):
    result = ''
    for char in text:
        if char in morse_code:
            result += morse_code[char] + ' '
        else:
            result += char
    return result

morse = to_morse_code('SOS')
for symbol in morse:
    if symbol == '.':
        print('.', end='', flush=True)
        time.sleep(0.2)
    elif symbol == '-':
        print('-', end='', flush=True)
        time.sleep(0.5)
    else:
        print(' ', end='', flush=True)
        time.sleep(0.5)

