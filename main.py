"""
This file is for proofs of concept for different parts of the overall program.
    - Getting web requests to work
    - Calculating minimums/maximums of functions
    - Etc.
"""

"""
General notes:
    - How to identify a card in Yugioh:
        * ID

    - How to identify a card in MTG:
        * Name and Set

    - Determinants of price (for classiciation):
        * Grade
        * Condition (might only be in item description)
        * Multiplicity
        * Common alterations (e.g. "Altered art")
"""

import requests

#
# api.ebay.com/buy/browse/v1/item/{item_id}
#




#
# Get the client credentials.
#

url = 'https://api.sandbox.ebay.com/identity/v1/oauth2/token'

with open('Client ID.txt', 'r') as theFile:
    clientID = theFile.read().replace('\n', '')

with open('Client Secret.txt', 'r') as theFile:
    clientSecret = theFile.read().replace('\n', '')

auth = clientID + ':' + clientSecret

headers = {'Content-Type'  : 'application/x-www-form-urlencoded', \
           'Authorization' : 'Basic ' + auth}

with open('Redirect URI.txt', 'r') as theFile:
    redirectURI = theFile.read().replace('\n', '')

#
# These are the only scopes allowed for client (i.e. not user) authentication:
#     - https://api.ebay.com/oauth/api_scope
#     - https://api.ebay.com/oauth/api_scope/buy.guest.order
#     - https://api.ebay.com/oauth/api_scope/buy.item.feedS
#     - https://api.ebay.com/oauth/api_scope/buy.marketing
#
scope = 'https://api.ebay.com/oauth/api_scope' # "View public data from eBay"

body = {'grant_type'   : clientID, \
        'redirect_uri' : redirectURI, \
        'scope'        : scope}




# Try to log things.
import requests
import logging

# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True




print('\n\n\nSending a POST request to URL:')
print(url)
print('With headers:')
print(headers)
print('And data:')
print(body)
print('\n\n\n')

r = requests.post(url, headers=headers, data=body)

print(r)
print(type(r))
from pprint import pprint
pprint(vars(r))

# r = requests.get('https://api.ebay.com/buy/browse/v1/item/v1|272940054280|0')
# print(r)
# print(type(r))
