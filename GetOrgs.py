#!/usr/bin/env python3

from pprint import pprint
import os, time, sys
import argparse
#import requests
from requests import Session
import json

MAX_RETRIES = 5

#api_key = os.environ['MERAKI_API_KEY']
api_key = None

apiVersion = 'v1'
baseURL = 'https://api.meraki.com/api/'+apiVersion

class NoRebuildAuthSession(Session):
 def rebuild_auth(self, prepared_request, response):
   '''
   No code here means requests will always preserve the Authorization header when redirected.
   Be careful not to leak your credentials to untrusted hosts!
   '''
session = NoRebuildAuthSession()

def GetOrgs():
    orgs = None

    try: 
        orgs = session.get(
            baseURL+'/organisations',
            headers = {
                'Authorization': f'Bearer: {api_key}',
                'Content-Type': 'application/json',
            }
        )
        orgs = json.loads(orgs.text)
        pprint(orgs)
    except Exception as e:
        pprint(e)

# Main routine function
def main(opts): 
    env_key = os.environ.get('MERAKI_API_KEY', None) 
    if env_key is None:
        raise SystemExit('Please set environment variable MERAKI_API_KEY')
    else:
        api_key = env_key

    if opts is None:
        print("Go go go")
    elif opts in ("-o", "--get-org-id"):
        ...
    else:
        ...
        #GetOrgs()

def run(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--echo", help="Repeating")
    parser.add_argument("-o", "--get-org-id", help='Get the Organisation ID')
    #parser.add_argument('-g', '--get', help='Get list of networks')
    #parser.add_argument('-p', '--post', help='Post list of networks')

    arguments = parser.parse_args(sys.argv[1:])
    if arguments.get_org_id:
        print("haha")
    elif arguments.echo:
        print(arguments.echo)
    else:
        print("Default")
    #main(**vars(options))

if __name__ == "__main__":
    run(sys.argv[1:])