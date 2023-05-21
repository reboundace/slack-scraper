import requests
import logging
import time
import json


def get_channel_messages(c, count_days, token, headers):
    nc = None
    cur_time = time.time()
    messages = []

    while True:
        rstring = 'https://slack.com/api/conversations.history?token=%s&channel=%s&limit=999' % (token, c)
        if nc is not None:
            rstring = rstring + '&cursor=%s' % (nc)

        logging.info("Requesting: %s with header %s" % (rstring, json.dumps(headers)))
        response = requests.get(rstring, headers=headers).json()
        mlist = response['messages']
        messages.extend(mlist)

        if response.get('has_more', None) == True and response.get('response_metadata', None) is not None and response.get('response_metadata').get('next_cursor', None) is not None:
            mtime = float(mlist[-1]['ts'])
            if cur_time - mtime > 86400*int(count_days):
                break
            nc = response.get('response_metadata').get('next_cursor', None)
            if nc == '':
                break
        else:
            break

    return messages

