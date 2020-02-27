#!/usr/bin/env python3
from optparse import OptionParser
import requests


def get_results():
    # call naar backend voor ophalen result info
    response = requests.get('http://server.arne.tech:82/user/{}'.format(username))
    results = response.json()

    result = 'test'
    # result += results  # of iets in deze aard

    if file:
        # kijk of file al bestaat, indien nee maak aan, indien ja, open vorige
        # schrijf opgehaalde info in file
        try:
            f = open("results.txt", "x")
        except IOError:
            f = open("results.txt", "w")
        finally:
            f.write(result)
            f.close()
    else:
        # print resultaten
        print(result)


# startup parameters ###################################################################################################
parser = OptionParser()
parser.add_option("-f", "--file", action="store_true", dest="file", default=False,
                  help="place the output in a file")
parser.add_option("-u", "--github_username", dest="username", help="your GitHub username")

(options, args) = parser.parse_args()
file = options.file
username = options.username
# username = ''

get_results()
