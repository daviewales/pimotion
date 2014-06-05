#!/usr/bin/env python3

# Python standard library imports
import json
import time
import queue
import threading

# Local imports
import backend
import postdata

default_settings = {'url': '',
                    'apikey': '',
                    'tile': 20,
                    'packet_interval': 5}


def write_settings(settings=default_settings):
    '''Convert settings to json and write to file.'''
    with open('settings.json', 'w') as file:
        file.write(json.dumps(settings))


def get_settings(settings_file='settings.json', settings=default_settings):
    '''
    Read settings from file.

    Return settings, using default settings for any missing values.
    '''
    with open(settings_file, 'r') as file:
        local_settings = json.load(file)

    settings.update(local_settings)
    return settings


def collate_and_send_data(data_queue, settings, running):
    '''
    Group data into packet format, convert to json and send.
    '''
    packet = {'apikey': settings['apikey'],
              'tile': settings['tile'],
              'frames': []}
    packet_interval = settings['packet_interval']
    url = settings['url']

    send_time = time.time() + packet_interval
    while running.is_set():
        try:
            data = data_queue.get(timeout=0.1)
            packet['frames'].append(data)
        except queue.Empty:
            pass

        if packet['frames'] and time.time() >= send_time:
            print(json.dumps(packet, sort_keys=False, indent=4))
            response = postdata.post_json(url, packet)
            print(response)
            packet['frames'] = []
            send_time = time.time() + packet_interval


def main():
    try:
        settings = get_settings(settings_file='settings.json')
        data_queue = queue.Queue()
        running = threading.Event()
        running.set()
        send_data_thread = threading.Thread(target=collate_and_send_data,
                                            args=(data_queue, settings,
                                                  running))
        send_data_thread.start()

        for motion in backend.get_motion_data():
            if motion:
                data = {'captured': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'movements': motion}
                data_queue.put(data)

    except KeyboardInterrupt:
        running.clear()
        print('\nWaiting for threads to exit...')
        print('\nGoodbye!')
    finally:
        running.clear()


if __name__ == '__main__':
    main()
