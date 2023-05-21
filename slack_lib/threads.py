import os
import sys
import requests
import logging
import json
from time import sleep


def get_channel_thread(c, tid, token, headers):
    nc = None
    retries = 0
    messages = []

    while True:
        rstring = 'https://slack.com/api/conversations.replies?token=%s&channel=%s&limit=999&ts=%s' % (token, c, tid)
        if nc is not None:
            rstring = rstring + '&cursor=%s' % (nc)

        logging.info("Requesting: %s with header %s" % (rstring, json.dumps(headers)))
        response = requests.get(rstring, headers=headers).json()

        mlist = response.get('messages')
        if not mlist:
            retries += 1
            if retries < 3:
                logger.warn ("Retrying loading thread %s %s .. retrying" % (tid, json.dumps(response)) )
                sleep(0.5 * retries)
                continue
            else:
                logger.error ("Unable to load thread %s %s" % (tid, json.dumps(response)) )
                break
                
        messages.extend(mlist)
        break

        '''
        if response.get('has_more', None) == True and response.get('response_metadata', None) is not None and response.get('response_metadata').get('next_cursor', None) is not None:
            nc = response.get('response_metadata').get('next_cursor', None)
            if nc == '':
                break
        else:
            break
        '''

    return mlist
