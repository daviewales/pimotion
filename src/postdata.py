import urllib2
import json

def post_json(url, data):
    '''
    post_json(url, json_data) --> json_response
    '''

    json_data = json.dumps(data)

    request = urllib2.Request(url)
    request.add_header('Content-Type', 'application/json')

    response = urllib2.urlopen(request, json_data)

    return response.read()

if __name__ == '__main__':
    print("You aren't supposed to run this!!!")
