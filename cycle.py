import collections
import mraa
import time

# Map GPIO block pins to MRAA pin numbers
# Reference: https://learn.sparkfun.com/tutorials/installing-libmraa-on-ubilinux-for-edison
pins = collections.OrderedDict()
pins["GP44"] = 31
pins["GP45"] = 45
pins["GP46"] = 32
pins["GP47"] = 46

# Initialize LED controls
leds = collections.OrderedDict()
leds["G"] = mraa.Gpio(pins["GP44"])
leds["R"] = mraa.Gpio(pins["GP45"])
leds["W"] = mraa.Gpio(pins["GP46"])
leds["Y"] = mraa.Gpio(pins["GP47"])

LED_ON = 1
LED_OFF = 0
def toggle(led, state):
    led.write(state)

def ledOn(led, duration):
    toggle(led, LED_ON)
    time.sleep(duration)

def ledOff(led, duration):
    toggle(led, LED_OFF)
    time.sleep(duration)

def allLedsOff(leds):
    for color in leds:
        toggle(leds[color], LED_OFF)

def main():
    # Set direction of LED controls to out
    for color in leds:
        leds[color].dir(mraa.DIR_OUT)

    while True:
        for color in leds:
            ledOn(leds[color], 1)
            ledOff(leds[color], 0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard interrupt received. Cleaning up..."
        allLedsOff(leds)
