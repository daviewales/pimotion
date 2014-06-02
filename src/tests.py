import unittest

import backend

# Backend tests

class TestBackend(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.motion = backend.get_motion_data()
        self.correctly_formatted_motion_data = [[ 375, 85 ], 
                                                [ 405, 305 ], 
                                                [ 565, 105 ]]

    def test_get_motion_returns_correct_type(self):
        self.assertEqual(type(self.motion), type(self.correctly_formatted_motion_data))

    def test_get_motion_returns_list_of_dicts(self):
        dict_type = type(self.correctly_formatted_motion_data[0])

        for i in self.motion:
            self.assertEqual(dict_type, type(i))

    def test_get_motion_returns_valid_data(self):
        for value in self.motion:
            self.assertEqual(type(value['x']), type(1))
            self.assertEqual(type(value['y']), type(1))
            self.assertEqual(type(value['radius']), type(1))
            # Need to find a way to test format of date.
            # Probably see if the value can be converted to datetime
            # and back...


if __name__ == '__main__':
    unittest.main(verbosity=2)
