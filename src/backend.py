#!/usr/bin/env python3

import picamera
import numpy
import io
import time

def get_image(resolution=(640, 480)):
    '''
    Yield an image of specified resolution to a byte stream.
    '''
    width, height = resolution
    pixels = width * height
    image_stream = io.BytesIO()

    with picamera.PiCamera() as camera:
        camera.resolution = resolution
        camera.start_preview()
        time.sleep(2)  # Let the camera 'warm up'.

        while True:
            camera.capture(image_stream, format='yuv', use_video_port=True)
            image_stream.seek(0)
            image_bytes = image_stream.read(pixels)
            image = numpy.fromstring(image_bytes, count=pixels,
                                     dtype=numpy.int8)
            image = image.reshape((height, width))[:height, :width]
            yield image
            image_stream.seek(0)

        camera.stop_preview()


def difference_image(image1, image2, threshold):
    height, width = image1.shape
    return abs(image1 - image2).astype(numpy.uint8) > threshold


def motion_coordinates(difference_image, tile_width, tile_height, tile_motion):
    """
    Split the image into tiles with dimensions 
    ``tile_width`` * ``tile_height``.

    Return the coordinates of the centre of each tile where the area of
    motion within a tile / area of tile > ``tile_motion``
    """
    height, width = difference_image.shape
    tile_area = tile_height * tile_width
    centre_offset_x, centre_offset_y = tile_width//2, tile_height//2

    coordinates = [[x + centre_offset_x, y + centre_offset_y]
                   for x in range(0, width, tile_width)
                   for y in range(0, height, tile_height) 
                   if difference_image[y:y+tile_height, x:x+tile_width].sum()
                   >= tile_motion]
    return coordinates


def get_motion_data(resolution=(640, 480), threshold=32,
                    tile_dimensions=(40, 40), tile_motion=1):
    '''
    Return list of lists of coordinates of motion.
    '''
    width, height = resolution
    tile_width, tile_height = tile_dimensions
    threshold = threshold * numpy.ones((height, width), dtype=numpy.uint8)

    image_generator = get_image(resolution=resolution)
    image1 = next(image_generator)
    while True:
        image2 = next(image_generator)
        difference = difference_image(image1, image2, threshold)
        motion = motion_coordinates(difference, tile_width,
                                    tile_height, tile_motion)
        yield motion
        image1 = image2


if __name__ == '__main__':
    print("You aren't supposed to run this directly!")
