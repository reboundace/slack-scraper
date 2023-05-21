#!/bin/env python


import os
import sys
import traceback
import logging
import json
from optparse import OptionParser

from slack_lib import channels,messages,threads,users

class ParseError(Exception):
    def __init__(self, message, usage):
        Exception.__init__(self, message)
        self.usage = usage


usage_str = (
    "Usage: slack-scraper.py [options] <channel_name>\n")
    

def usage(parser=None):
    if parser is None:
        sys.stderr.write(usage_str)
    else:
        parser.print_help()
    sys.exit(1)

        
def main():
    optparser = OptionParser(usage=usage_str)
    optparser.add_option("--token", dest="token",
                         default=os.getenv('SLACK_API_TOKEN'),
                         help="api token for accessing Slack. must be specified via command line or passed in via environment variable SLACK_API_TOKEN")

    optparser.add_option("--dcookie", dest="dcookie",
                         default=os.getenv('SLACK_API_DCOOKIE'),
                         help="Value of D cookie ")
    
    optparser.add_option("-v", dest="verbose", action="store_true",
                         default=False,
                         help="verbose mode - info level logging")
    
    optparser.add_option("--vv", dest="chatty", action="store_true",
                         default=False,
                         help="very verbose mode - debug level logging")
    
    optparser.add_option("--no_replies", dest="no_replies", action="store_true",
                         default=False,
                         help="Only fetch direct messages from Slack and not the threaded replies")

    optparser.add_option("--days", dest="days", type=int,
                         default=31,
                         help="Number of days over which to get messages for")

    optparser.add_option("--mode", dest="mode", 
                         default='messages',
                         help="Mode - 'messages' or 'users'")


    optparser.disable_interspersed_args()
    (options, args) = optparser.parse_args()

    if options.chatty:
        logging.basicConfig(level=logging.DEBUG)
    elif options.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)

    if options.token is None:
        sys.stderr.write("No Slack API Token provided\n")
        usage(optparser)

    token = options.token
    headers = {}
    if options.dcookie is not None:
        headers = {'cookie': 'd='+ options.dcookie}


    if options.mode == 'users':
        ulist = users.get_all_users(token, headers)
        for u in ulist:
            print(json.dumps(u))

        return
            
        

    if len(args) < 1:
        sys.stderr.write("Missing first argument: channel_name\n")
        usage(optparser)

    cname = args.pop(0)

    c = channels.get_channel(cname, token, headers)
    if c is None or c.get('id') is None:
        sys.stderr.write("Unable to find channel: " + cname)
        sys.exit(1)

    cid = c['id']
    mlist = messages.get_channel_messages(cid, options.days, token, headers)
    for m in mlist:

        print(json.dumps(m))

        if options.no_replies:
            continue
        
        if (m.get('thread_ts') == m['ts']):
            rlist = threads.get_channel_thread(cid, m['ts'], token, headers)
            for r in rlist:
                print(json.dumps(r))
    

if __name__ == '__main__':
    try:
        sys.exit(main())
    except ParseError as e:
        sys.stderr.write("Error: %s\n" % str(e))
        sys.stderr.write("Usage: %s\n" % e.usage)
        sys.exit(2)
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(3)
