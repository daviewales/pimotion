#!/usr/bin/env python

# Python standard library imports
import json

# Local imports
import backend
import postdata

default_settings = {'url':'',
                    'apikey':''}

def write_settings(settings=default_settings):
    with open('settings.json', 'w') as file:
        file.write(json.dumps(settings))

def get_settings(settings_file='settings.json', settings=default_settings):
    with open(settings_file, 'r') as file:
        local_settings = json.load(file)

    settings.update(local_settings)

    return settings

def main():

    settings = get_settings(settings_file='settings.json')

    while True:
        movements = backend.get_motion()

        data = {'apikey': settings['apikey'],
                'movements': movements}   

        response = postdata.post_json(settings['url'], data)
        print(response)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
