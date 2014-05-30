#!/usr/bin/env python3

import picamera
import numpy

# temporary import for mocking up functions...
from mock_backend import *

def get_motion():
    '''
    Return list of dictionaries of coordinates of motion.
    '''

    return mock_get_motion()


if __name__ == '__main__':
    print("You aren't supposed to run this directly!")
