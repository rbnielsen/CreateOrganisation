#!/usr/bin/env python3

from pprint import pprint
import os, time, sys
import argparse
import requests as req
from requests import Session
import json

MAX_RETRIES = 5

#api_key = os.environ['MERAKI_API_KEY']
API_KEY = None

apiVersion = 'v1'
baseURL = 'https://api.meraki.com/api/'+apiVersion

class NoRebuildAuthSession(Session):
    def rebuild_auth(self, prepared_request, response):
        '''
        No code here means requests will always preserve the Authorization header when redirected.
        Be careful not to leak your credentials to untrusted hosts!
        '''
session = NoRebuildAuthSession()

def GetOrgs(p_apiKey):
    orgs = None

    try: 
        header = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {p_apiKey}",
            }
        orgs = session.get(
            baseURL+'/organizations',
            headers = header
        )
        if orgs.status_code != req.codes.ok:
            return None
        orgs = orgs.json()
        for _ in orgs:
            return _['id']
        
    except Exception as e:
        pprint(e)

# Main routine function
def main(org_id):
    
    API_KEY = os.environ.get('MERAKI_API_KEY', None) 
    if API_KEY is None:
        raise SystemExit('Please set environment variable MERAKI_API_KEY')
    else:
        ...
        #API_KEY = os.environ['MERAKI_API_KEY']

    if org_id is None:
        org = GetOrgs(API_KEY)
        print(org)


    #print(locals())
    

def run(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--org-id', help='Set the Organisation ID')
    
    options = parser.parse_args(sys.argv[1:])
    main(**vars(options))


if __name__ == "__main__":
    run(sys.argv[1:])