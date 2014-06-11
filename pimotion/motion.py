#!/usr/bin/env python3

import logging
import json
import time
import queue
import threading
import argparse
import requests


def write_config(config, config_file):
    '''
    Convert config to json and write to file.
    '''
    with open('config.json', 'w') as file:
        file.write(json.dumps(config))


def get_config(default_config, config_file):
    '''
    Read config from file.

    Return config, using default config for any missing values.
    '''
    try:
        with open(config_file, 'r') as file:
            local_config = json.load(file)

        default_config.update(local_config)

    except ValueError:
        logging.error('Settings file contains JSON error. Exiting program.')
        raise KeyboardInterrupt
    except IOError:
        logging.error('Config file not found. Exiting program.')
        raise KeyboardInterrupt

    return default_config


def upload_background_image(config, background_image):
    # Local import to save time on startup.
    logging.info('Uploading background image to server...')

    api_data = {'apikey': config['apikey']}
    image_data = {'image': ('image.png', background_image)}

    response = requests.post(
        config['image_url'],
        data=api_data,
        files=image_data)

    logging.info('Upload complete.')
    logging.debug(response.text)


def collate_and_send_data(data_queue, config, running):
    '''
    Group data into packet format, convert to json and send.
    '''
    import random
    packet = {'apikey': config['apikey'],
              'tile': config['tile'],
              'frames': []}
    packet_interval = config['packet_interval']
    url = config['url']

    send_time = time.time() + packet_interval
    while running.is_set():
        try:
            data = data_queue.get(timeout=0.1)
            packet['frames'].append(data)
        except queue.Empty:
            pass

        if packet['frames'] and time.time() >= send_time:
            json_data = json.dumps(packet)
            pretty_json_data = json.dumps(packet, sort_keys=False, indent=4)
            logging.debug(''.join(['JSON data: ', pretty_json_data]))
            logging.info('Uploading data...')
            response = requests.post(url, json_data)
            logging.debug(response.text)
            packet['frames'] = []

            # A random interval is added to avoid clobbering the network.
            send_time = time.time() + packet_interval + random.uniform(-1, 1)


def main():
    try:
        # Create flag to notify threads of running state.
        running = threading.Event()
        running.set()

        default_config = {
            'url': '',
            'image_url': '',
            'apikey': '',
            'packet_interval': 5,
            'tile': 20,
            'threshold': 10,
            'resolution': [640, 480],
            'tile_motion': 0.5}

        pretty_json_default_config = json.dumps(
            default_config,
            sort_keys=False,
            indent=4)

        epilog_text = '\n'.join([
            'The config file should contain the following JSON:\n',
            pretty_json_default_config,
            '(The empty fields should be populated...)',
            ''])

        # Parse command line arguments.
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Simple motion dectection client.',
            epilog=epilog_text)
        parser.add_argument(
            '-v', '--verbose', action='count', default=0,
            help='Increase verbosity (-v, -vv, etc)')
        parser.add_argument(
            '-c', '--config', default='config.json',
            metavar='FILE', type=str,
            help='Specify path to config file (default: %(default)s)')
        args = parser.parse_args()

        # Set log level.
        log_level = logging.WARNING
        if args.verbose >= 2:
            log_level = logging.DEBUG
        elif args.verbose >= 1:
            log_level = logging.INFO

        logging.basicConfig(
            format='%(levelname)s: %(message)s', level=log_level)

        # Local import to save time at startup.
        # (We want to parse the command line options as quickly as possible,
        # just in case the user is just trying to get --help, etc.)
        import backend

        # Load config.
        config = get_config(default_config, args.config)

        # Upload background image to server.
        background_image = backend.get_png_image(
            resolution=config['resolution'])
        upload_background_image(config, background_image)

        # Start thread to upload data.
        data_queue = queue.Queue()
        send_data_thread = threading.Thread(
            target=collate_and_send_data,
            args=(data_queue, config, running))

        send_data_thread.start()

        # Get motion data forever.
        for motion in backend.get_motion_data(
                resolution=config['resolution'],
                threshold=config['threshold'],
                tile_dimensions=(config['tile'], config['tile']),
                tile_motion=config['tile_motion']):

            if motion:
                data = {'captured': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'movements': motion}
                data_queue.put(data)

    except KeyboardInterrupt:
        pass
    finally:
        running.clear()
        logging.info('Waiting for threads to exit...')
        print('\nGoodbye!')


if __name__ == '__main__':
    main()
