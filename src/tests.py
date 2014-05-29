import unittest

import backend

# Backend tests

class TestBackend(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.motion = backend.get_motion()
        self.correctly_formatted_motion_data = {
                                                '1':{
                                                     'x':1024,
                                                     'y':768,
                                                     'radius': 5,
                                                     'captured': '2014-5-12 09:34:55',
                                                    },
                                               }
        self.test_keys = self.motion.keys()
        self.correct_keys = ['1' for i in range(len(self.test_keys))]

    def test_get_motion_returns_correct_type(self):
        self.assertEqual(type(self.motion), type(self.correctly_formatted_motion_data))

    def test_get_motion_returns_dict_with_correct_key_types(self):
        test_key_types = map(type, self.test_keys)
        correct_key_types = map(type, self.correct_keys)

        self.assertEqual(correct_key_types, test_key_types)

    def test_get_motion_returns_dict_with_correct_key_values(self):
        self.assertTrue(i.isdigit() for i in self.test_keys)



if __name__ == '__main__':
    unittest.main(verbosity=2)
