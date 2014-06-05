#!/usr/bin/env python3
import unittest
import itertools
import numpy

try:
    import unittest.mock as mock
except:
    import mock

import backend



# Backend tests
class TestBackend(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        mock_images = [numpy.load('test_files/image{}.npy'.format(i)) for i in range(1,3)]
        mock_get_image = mock.patch('backend.get_image', autospec=True).start()
        mock_get_image.return_value = itertools.cycle(mock_images)

        self.motion_generator = backend.get_motion_data()
        self.motion = next(self.motion_generator)
        self.correctly_formatted_motion_data = [[375, 85],
                                                [405, 305],
                                                [565, 105]]

        self.tile_width = 10
        self.tile_height = 10
        self.tile_area = self.tile_width * self.tile_height
        self.tile_centre = [self.tile_width/2, self.tile_height/2]
        self.tile_motion = 1
        self.complete_motion_tile = numpy.ones(
                (self.tile_height, self.tile_width), dtype=numpy.bool)
        self.zero_motion_tile = numpy.zeros(
                (self.tile_height, self.tile_width), dtype=numpy.bool)
        self.half_motion_tile = numpy.ones(
                (self.tile_height, self.tile_width), dtype=numpy.bool)
        self.half_motion_tile[0:10, 0:5] = self.zero_motion_tile[0:10, 0:5]

    def test_get_motion_returns_correct_type(self):
        '''get_motion should return list'''
        self.assertEqual(type(self.motion),
                         type(self.correctly_formatted_motion_data))

    def test_get_motion_returns_list_of_lists(self):
        '''get_motion should return list of lists'''
        list_type = type(self.correctly_formatted_motion_data[0])

        for i in self.motion:
            self.assertEqual(list_type, type(i))

    def test_get_motion_returns_valid_data(self):
        '''get_motion should return list of lists of integers'''
        for value in self.motion:
            self.assertEqual(type(value[0]), type(1))
            self.assertEqual(type(value[1]), type(1))


    def test_motion_coordinates_correct_for_complete_motion(self):
        '''tile with 100% motion should return coordinates of tile centre'''
        valid_coordinates = [self.tile_centre]
        coordinates = backend.motion_coordinates(self.complete_motion_tile,
                                                 self.tile_width,
                                                 self.tile_height,
                                                 self.tile_motion)
        self.assertEqual(valid_coordinates, coordinates)

    def test_motion_coordinates_correct_for_no_motion(self):
        '''tile with 0% motion should return empty list'''
        valid_coordinates = []
        coordinates = backend.motion_coordinates(self.zero_motion_tile,
                                                 self.tile_width,
                                                 self.tile_height,
                                                 self.tile_motion)
        self.assertEqual(valid_coordinates, coordinates)

    def test_motion_coordinates_correct_for_partial_motion(self):
        '''tile with partial motion should be dependent on `tile_motion`'''

        for i in range(11):
            self.tile_motion = 0.1*i
            if self.tile_motion <= 0.5:
                message = ('motion coordinates should be found when '
                           'tile contains 50% motion and '
                           '`tile_motion == {:.2f}`.'.format(self.tile_motion))
                valid_coordinates = [self.tile_centre]
                coordinates = backend.motion_coordinates(
                        self.half_motion_tile,
                        self.tile_width,
                        self.tile_height,
                        self.tile_motion)
                self.assertEqual(
                        valid_coordinates,
                        coordinates,
                        msg = message)

            else:
                message = ('motion coordinates should not be found when '
                           'tile contains 50% motion and '
                           '`tile_motion == {:.2f}`.'.format(self.tile_motion))
                valid_coordinates = []
                coordinates = backend.motion_coordinates(
                        self.half_motion_tile,
                        self.tile_width,
                        self.tile_height,
                        self.tile_motion)
                self.assertEqual(
                        valid_coordinates,
                        coordinates,
                        msg = message)





if __name__ == '__main__':
    unittest.main(verbosity=2)
