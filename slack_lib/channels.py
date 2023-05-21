import os
import sys
import requests
import logging
import json

def get_all_channels(cname, token, headers):
    channels = []
    nc = None

    while True:
        rstring = 'https://slack.com/api/conversations.list?token=%s&types=%s&limit=999&exclude_archived=true' % (token, 'public_channel,private_channel')
        if nc is not None:
            rstring = rstring + '&cursor=%s' % (nc)

        logging.info("Requesting: %s with header %s" % (rstring, json.dumps(headers)))
        response = requests.get(rstring, headers=headers).json()

        clist = response.get('channels')
        if clist is not None:
            channels.extend(response['channels'])
        else:
            raise Exception('Channels missing in response: ' + json.dumps(response))

        if response.get('response_metadata', None) is not None and response.get('response_metadata').get('next_cursor', None) is not None:
            nc = response.get('response_metadata').get('next_cursor', None)
            if nc == '':
                break
        else:
            break

    return channels

def get_channel(cname, token, headers):
    for c in get_all_channels(cname, token, headers):
        if 'name' in c and c['name'] == cname:
            return c

    return None
