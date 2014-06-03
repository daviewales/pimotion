#!/usr/bin/env python

# Python standard library imports
import json
import datetime

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
    motion_generator = backend.get_motion_data()

    while True:
        motion = next(motion_generator)
        if motion:
            current_time = datetime.datetime.now()
            iso_time = current_time - datetime.timedelta(
                    microseconds=current_time.microsecond)
            iso_time = str(iso_time)

            data = {'apikey': settings['apikey'],
                    'tile': settings['tile'],
                    'frames': [{'captured': iso_time,
                                'movements': motion}]
                   }

            response = postdata.post_json(settings['url'], data)
            print(json.dumps(data, sort_keys=False, indent=4))
            print(response)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
