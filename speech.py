import collections
import mraa
import os
import sys
import time

# Import things for pocketsphinx
import pyaudio
import wave
import pocketsphinx as ps
import sphinxbase

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

# Parameters for pocketsphinx
LMD   = "/home/root/led-speech-edison/lm/8484.lm"
DICTD = "/home/root/led-speech-edison/lm/8484.dic"
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2
PATH = 'output'

LED_ON = 1
LED_OFF = 0
def toggle(led, state):
    led.write(state)

def allLedsOn(leds):
    for color in leds:
        toggle(leds[color], LED_ON)

def allLedsOff(leds):
    for color in leds:
        toggle(leds[color], LED_OFF)

def cycleLeds(leds, time_on, num_repeat=1):
    for i in range(num_repeat):
        for color in leds:
            toggle(leds[color], LED_ON)
            time.sleep(time_on)
            toggle(leds[color], LED_OFF)

def triggerLeds(leds, words):
    allLedsOff(leds)

    if "RED" in words:
        toggle(leds["R"], LED_ON)
    if "GREEN" in words:
        toggle(leds["G"], LED_ON)
    if "WHITE" in words:
        toggle(leds["W"], LED_ON)
    if "YELLOW" in words:
        toggle(leds["Y"], LED_ON)
    if "ALL" in words:
        allLedsOn(leds)
    if "TORONTO" in words:
        cycleLeds(leds, 0.05)
    if "CANADA" in words:
        cycleLeds(leds, 0.1, 2)

def decodeSpeech(speech_rec, wav_file):
	wav_file = file(wav_file,'rb')
	wav_file.seek(44)
	speech_rec.decode_raw(wav_file)
	result = speech_rec.get_hyp()
	return result[0]

def main():
    # Set direction of LED controls to out
    for color in leds:
        leds[color].dir(mraa.DIR_OUT)

    if not os.path.exists(PATH):
        os.makedirs(PATH)

    p = pyaudio.PyAudio()
    speech_rec = ps.Decoder(lm=LMD, dict=DICTD)

    while True:
        # Record audio
    	stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    	print("* recording")
    	frames = []
    	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    		data = stream.read(CHUNK)
    		frames.append(data)
    	print("* done recording")
    	stream.stop_stream()
    	stream.close()
    	#p.terminate()

        # Write .wav file
        fn = "o.wav"
    	wf = wave.open(os.path.join(PATH, fn), 'wb')
    	wf.setnchannels(CHANNELS)
    	wf.setsampwidth(p.get_sample_size(FORMAT))
    	wf.setframerate(RATE)
    	wf.writeframes(b''.join(frames))
    	wf.close()

        # Decode speech
    	wav_file = os.path.join(PATH, fn)
    	recognised = decodeSpeech(speech_rec, wav_file)
    	rec_words = recognised.split()

        # Trigger LEDs
    	triggerLeds(leds, rec_words)

        # Playback recognized word
    	cm = 'espeak "'+recognised+'"'
    	os.system(cm)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "Keyboard interrupt received. Cleaning up..."
        allLedsOff(leds)
