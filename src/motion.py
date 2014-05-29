#!/usr/bin/env python

# Python standard library imports
import json

# Local imports
import backend
import postdata

def write_default_settings(default_settings):
    with open('settings.json', 'w') as file:
        file.write(json.dumps(default_settings))

def get_settings(settings_file='settings.json'):
    settings = {'url':'http://home.padman.id.au:8080/m2m/public/movements',
                        'apikey':'a8a8f30fdd8249b1e51aa9118f15205708f652db'}

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
