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

    #@mock.patch('backend.get_image' autospec=True)
    #def test_get_motion_data(self, mock_get_image):
    #    mock_images = [numpy.load('image{}.npy'.format(i)) for i in range(1,3)]
    #    mock_get_image.return_value = itertools.cycle(mock_images)

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


if __name__ == '__main__':
    unittest.main(verbosity=2)
