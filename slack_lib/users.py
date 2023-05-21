import requests
import logging
import json


def get_all_users(token, headers):
    users = []
    nc = None

    while True:
        rstring = 'https://slack.com/api/users.list?token=%s' % token
        if nc is not None:
            rstring = rstring + '&cursor=%s' % (nc)

        logging.info("Requesting: %s with header %s" % (rstring, json.dumps(headers)))
        response = requests.get(rstring, headers=headers).json()
        users.extend(response['members'])

        if response.get('response_metadata', None) is not None and response.get('response_metadata').get('next_cursor', None) is not None:
            nc = response.get('response_metadata').get('next_cursor', None)
            if nc == '':
                break
        else:
            break
        
    return users

