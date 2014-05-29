#!/usr/bin/env python

import urllib2, json

def post_json(url, json_data):
    """
    >>>post_json(url, json_data) --> json_response
    """

    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(request, json_data)

    return response.read()

if __name__ == "__main__":

    url = 'http://home.padman.id.au:8080/m2m/public/movements'
    data = {
        "apikey": "6a3fc5fb928928bdda165ae7c5",
        "movements": {
            "1": {
                "x":1024,
                "y":768,
                "radius": 5,
                "captured": "2014-5-12 09:34:55"
            },
            "2": {
                "x":100,
                "y":123,
                "radius": 4,
                "captured": "2014-5-12 09:34:56"
            }
        }
    }


    json_data = json.dumps(data)

    response = post_json(url, json_data)
    print response
