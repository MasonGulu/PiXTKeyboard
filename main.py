import RPi.GPIO as GPIO
from time import sleep
import keyboard

GPIO.setmode(GPIO.BCM)

clockpin = 27
datapin = 17

GPIO.setup(datapin, GPIO.OUT)
GPIO.setup(clockpin, GPIO.OUT, initial=GPIO.HIGH)

transmitting = False

scancodes = {
    "1": 2,
    "2": 3,
    "3": 4,
    "4": 5,
    "5": 6,
    "6": 7,
    "7": 8,
    "8": 9,
    "9": 10,
    "0": 11,
    "-": 12,
    "=": 13,
    "a": 30,
    "b": 48,
    "c": 46,
    "d": 32,
    "e": 18,
    "f": 33,
    "g": 34,
    "h": 35,
    "i": 23,
    "j": 36,
    "k": 37,
    "l": 38,
    "m": 50,
    "n": 49,
    "o": 24,
    "p": 25,
    "q": 16,
    "r": 19,
    "s": 31,
    "t": 20,
    "u": 22,
    "v": 47,
    "w": 17,
    "x": 45,
    "y": 21,
    "z": 44,
    "enter": 28,
    "ctrl": 29,
    "shift": 42,
    "\\": 43,
    ";": 39,
    "'": 40,
    "`": 41,
    ",": 51,
    ".": 52,
    "/": 53,
    "*": 55,
    "alt": 56,
    "space": 57,
    "caps lock": 58,
    "num lock": 69,
    "scroll lock": 70,
    "esc": 1,
    "backspace": 14,
    "del": 83,
    "up": 72,
    "down": 80,
    "left": 75,
    "right": 77,
    "f1": 59,
    "f2": 60,
    "f3": 61,
    "f4": 62,
    "f5": 63,
    "f6": 64,
    "f7": 65,
    "f8": 66,
    "f9": 67,
    "f10": 68

}

def outputBit(bit):
    GPIO.output(datapin, bit)
    GPIO.output(clockpin, False)
    GPIO.output(clockpin, True)


def outputByte(byte):
    mask = 0b00000001
    outputBit(True)
    for i in range(0, 8):
        if ((byte & mask) > 0):
            # True
            outputBit(True)
        else:
            outputBit(False)
        mask = mask << 1


def keyPressed(key):
    global transmitting
    while (transmitting):
        sleep(0.1)
    transmitting = True
    outputByte(scancodes[key])
    transmitting = False


def keyReleased(key):
    global transmitting
    while (transmitting):
        sleep(0.1)
    transmitting = True
    outputByte(scancodes[key] | 0b10000000)
    transmitting = False



doPost = True
clockinpin = 22


if doPost:
    GPIO.setup(clockinpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    while (GPIO.input(clockinpin)):
        pass
        # wait for pin to be pulled low
    print("Pulled low")
    while (not GPIO.input(clockinpin)):
        pass
        # wait for input to go high
    print("Went high, sending data")
    outputByte(0xAA)

activeKeys = []



GPIO.setup(clockpin, GPIO.OUT)
while True:
    key = keyboard.read_key()
    if key in activeKeys and not keyboard.is_pressed(key):
        # Key has been released
        keyReleased(key)
        activeKeys.remove(key)
    elif not key in activeKeys and keyboard.is_pressed(key):
        # First time pressed
        keyPressed(key)
        activeKeys.append(key)

GPIO.cleanup()