#!/usr/bin/env python
#
# test_midiin_poll.py
#
"""Show how to receive MIDI input by polling an input port."""

from __future__ import print_function

import logging
import sys
import time

from rtmidi.midiutil import open_midiinput
import keyboard
from time import sleep


log = logging.getLogger('midiin_poll')
logging.basicConfig(level=logging.DEBUG)


# Mapping
keyboard_map = {
	'41': ['1', 'a'],
	'42': ['1', 'w'],
	'43': ['1', 's'],
	'44': ['1', 'e'],
	'45': ['1', 'd'],
	'46': ['1', 'r'],
	'47': ['1', 'f'],
	'48': ['1', 'g'],
	'49': ['1', 'y'],
	'50': ['1', 'h'],
	'51': ['1', 'u'],
	'52': ['1', 'j'],
	'53': ['2', 'a'],
	'54': ['2', 'w'],
	'55': ['2', 's'],
	'56': ['2', 'e'],
	'57': ['2', 'd'],
	'58': ['2', 'r'],
	'59': ['2', 'f'],
	'60': ['2', 'g'],
	'61': ['2', 'y'],
	'62': ['2', 'h'],
	'63': ['2', 'u'],
	'64': ['2', 'j'],
	'65': ['3', 'a'],
	'66': ['3', 'w'],
	'67': ['3', 's'],
	'68': ['3', 'e'],
	'69': ['3', 'd'],
	'70': ['3', 'r'],
	'71': ['3', 'f'],
	'72': ['3', 'g'],
	'73': ['3', 'y'],
	'74': ['3', 'h'],
	'75': ['3', 'u'],
	'76': ['3', 'j'],
	'77': ['3', 'i']
}
octave = '2'


# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Entering main loop. Press Control-C to exit.")
try:
    timer = time.time()
    while True:
        msg = midiin.get_message()

        if msg:
            message, deltatime = msg
            timer += deltatime
            print("[%s] @%0.6f %r" % (port_name, timer, message))

            # If key in map
            if str(message[1]) in keyboard_map.keys():

            	# Release key
            	if message[2] == 0:
            		keyboard.release(keyboard_map[str(message[1])][1])
            		print("Tecla levantada {}".format(keyboard_map[str(message[1])][1]))
            	else:

            		# Change octave if necessary
            		if octave != keyboard_map[str(message[1])][0]:
            			keyboard.press_and_release(keyboard_map[str(message[1])][0])
            			sleep(0.16)
            			octave = keyboard_map[str(message[1])][0]

            		keyboard.press(keyboard_map[str(message[1])][1])
            		print("Tecla presionada {}".format(keyboard_map[str(message[1])][1]))



        time.sleep(0.01)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin