import machine
import time
led = machine.Pin("LED", machine.Pin.OUT)
led2 = machine.Pin(28, machine.Pin.OUT)

morse_code = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.'}

def to_morse_code(text):
    result = ''
    for char in text:
        if char in morse_code:
            result += morse_code[char] + ' '
        else:
            result += char
    return result

def send_dot():
    led.value(1)
    led2.value(1)
    time.sleep(0.2)
    led.value(0)
    led2.value(0)
    time.sleep(0.2)

def send_dash():
    led.value(1)
    led2.value(1)
    print('-')
    time.sleep(0.5)
    led.value(0)
    led2.value(0)
    time.sleep(0.2)

def send_space():
    led.value(0)
    led2.value(0)
    time.sleep(0.4)
    led.value(0)
    led2.value(0)

morse = to_morse_code('SOS')

while True:
    for symbol in morse:
        if symbol == '.':
            send_dot()
        elif symbol == '-':
            send_dash()
        else:
            send_space()
    time.sleep(1)
