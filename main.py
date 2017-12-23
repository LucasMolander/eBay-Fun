"""
This file is for proofs of concept for different parts of the overall program.
	- Getting web requests to work
	- Calculating minimums/maximums of functions in
	- Etc.
"""

import requests

r = requests.get('https://api.github.com/events')

print(r)
