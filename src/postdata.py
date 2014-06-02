#!/usr/bin/env python3

import urllib.request, urllib.error
import json

def post_json(url, data):
    '''
    Convert data to json, encode as bytes, post to specified url, and return response.
    '''

    try:
        json_data = json.dumps(data).encode('utf-8')

        request = urllib.request.Request(url)
        request.add_header('Content-Type', 'application/json')

        response = urllib.request.urlopen(request, json_data)

        return response.read().decode('utf-8')

    except urllib.error.URLError:
    try:
        print("Error: Network lookup failed. Trying again...")
        response = postdata.post_json(settings['url'], data)
    except urllib.error.URLError:
        print("Error: Network lookup failed after retry.",
              "Giving up on this packet.")
        pass

if __name__ == '__main__':
    print("You aren't supposed to run this!!!")
