#!/usr/bin/env python3
import time
import ait			# pip install autoit
import keyboard		# pip install keyboard

# Usage: 
# $ python -i autoclick.py

def loop(n, t, s):
	for i in range(n):
		if ait.holding(s):
			break
		ait.click()
		time.sleep(t)

def loop2(t, s):
	while True:
		if ait.holding(s):
			break
		ait.click()
		time.sleep(t)
	

if __name__ == "__main__":
	terminate = 'Q'
	print('Press ctrl + shift + 1 to start clicking for 100 times')
	print('Press ctrl + shift + 2 to start clicking for infinite times')
	print('Press Q to stop')

	keyboard.add_hotkey('ctrl+shift+1', loop, args=(100, 0.1, terminate))
	keyboard.add_hotkey('ctrl+shift+2', loop2, args=(0.1, terminate))

	
