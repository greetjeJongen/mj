#!/usr/bin/env python3
from optparse import OptionParser
import requests


def get_results():
    # API call
    response = requests.get('http://server.arne.tech:83/status/{}'.format(username))
    results = response.json()

    if results[0]["passed"] == 0:
        print("passed: false")
    else:
        print("passed: true")


# startup parameters ###################################################################################################
parser = OptionParser()
parser.add_option("-u", "--github_username", dest="username", help="your GitHub username")

(options, args) = parser.parse_args()
username = options.username
# username = ''

# Check if username given
if username is None:
    raise Exception("You have to provide a repo name")

get_results()
