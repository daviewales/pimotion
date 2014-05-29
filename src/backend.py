import picamera
import numpy

def get_motion():
    '''
    get_motion() --> return {
                             '1':{
                                  'x':1024,
                                  'y':768,
                                  'radius': 5,
                                  'captured': '2014-5-12 09:34:55',
                                 },

                             '2':{
                                  'x':100,
                                  'y':123,
                                  'radius': 4,
                                  'captured': '2014-5-12 09:34:56',
                                 },
                             }
    '''

    return {
            '1':{
                 'x':1024,
                 'y':768,
                 'radius': 5,
                 'captured': '2014-5-12 09:34:55',
                },

            '2':{
                 'x':100,
                 'y':123,
                 'radius': 4,
                 'captured': '2014-5-12 09:34:56',
                },
            }


if __name__ == '__main__':
    print("You aren't supposed to run this directly!")
