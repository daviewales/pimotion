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
        #camera.ISO = 200
        #camera.awb_mode = 'off'
        ##camera.awb_gains = 1
        #camera.brightness = 50
        #camera.contrast = 0
        #camera.exposure_mode = 'antishake'
        #camera.meter_mode = 'spot'
        #camera.video_stabilization = True
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
    Get the coordinates of motion from a difference_image.

    Split the image into tiles with dimensions
    tile_width * tile_height.

    Return the coordinates of the centre of each tile where the sum of 
    motion pixels within the tile is >= tile_motion * tile_area.
    """
    height, width = difference_image.shape
    tile_area = tile_height * tile_width
    centre_offset_x, centre_offset_y = tile_width//2, tile_height//2

    coordinates = [[x + centre_offset_x, y + centre_offset_y]
                   for x in range(0, width, tile_width)
                   for y in range(0, height, tile_height)
                   if difference_image[y:y+tile_height, x:x+tile_width].sum()
                   >= tile_motion * tile_area]
                   # tile_motion * tile_area gives the total number of 
                   # changed pixels within a given tile required for
                   #motion to be registered.
    return coordinates


def get_motion_data(resolution=(640, 480), threshold=32,
                    tile_dimensions=(40, 40), tile_motion=0.5):
    '''
    Return list of lists of coordinates of motion.

    resolution is a tuple containing the dimensions of the image:
    resolution = (width, height).

    threshold is a number specifying the minimum change in pixel intensity
    required for motion to be registered.

    tile_dimensions is a tuple containing the dimensions of the tiles
    which the image will be divided into to check for motion.
    tile_dimensions = (width, height).
    
    tile_motion is the fraction of a given tile which must contain motion
    for motion to be registered. For instance, if we are using 20x20 tiles,
    then the total number of pixels contained in a given tile is 400 pixels.
    If tile_motion == 1, then a tile will not be registerred as containing motion
    if < 400 pixels within the tile contain motion.
    However, if tile_motion == 0.5, then only half the tile must contain motion
    in order for the tile to be registered as motion.
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
