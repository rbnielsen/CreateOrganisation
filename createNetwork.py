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

def meraki_post(sub_url, payload, max_retries=MAX_RETRIES):
    for _ in range(max_retries):   
        r = session.post(
            baseURL+sub_url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            },
            json=payload
        )
        if r.status_code == 201:
            return r
        elif r.status_code == 429:
            print(f'Rate limited activated - Retrying after {r.headers["Retry-After"]}.')
            time.sleep(int(r.headers['Retry-After']))
            continue
        else: 
            raise SystemExit(f'Unexpected status code: {r.status_code} returned from server')
    raise SystemExit('Aborted due to too many retries')

def meraki_get(p_sub_url, p_orgID, max_retries=MAX_RETRIES):
    for _ in range(max_retries):   
        r = session.post(
            baseURL+p_sub_url,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
            }
        )
        if r.status_code == 200:
            return r
        elif r.status_code == 429:
            print(f'Rate limited activated - Retrying after {r.headers["Retry-After"]}.')
            time.sleep(int(r.headers['Retry-After']))
            continue
        else: 
            raise SystemExit(f'Unexpected status code: {r.status_code} returned from server')
    raise SystemExit('Aborted due to too many retries')

def GetNetworkList(p_orgID):
    networks = None
    if p_orgID is not None:
        for p_org in p_orgID:
            try:
                networks = session.get(
                    baseURL+"/organisations/"+p_org+"/networks",
                    headers={
                        'Authorization': f'Bearer {api_key}',
                        'Content-Type': 'application/json',
                    }
                )
                if networks.status_code == 200:
                    with open('networks.txt','w') as nwlist:
                        #TODO: Add, orgID, nwID, Name
                        #csv_writer = csv_writer(nwlist, delimiter=',')

                    
                elif networks.status_code == 429:
                    print(f'Rate limited - Retrying after {r.headers["Retry-After"]}.')
                    time.sleep(int(r.headers['Retry-After']))
                    continue
                else:
                    raise SystemExit(f'Unexpected status code: {r.status_code} returned from server')
            except Exception as e:
                pprint(e)
                return ""


# Main routine function
def main(opts): 
    env_key = os.environ.get('MERAKI_API_KEY', None) 
    if env_key is None:
        raise SystemExit('Please set environment variable MERAKI_API_KEY')
    else:
        api_key = env_key

    if opts in ("-o", "--get-org-id"):
        r = meraki_get(f'/organizations',orgID)
        print(r)
    else:
        print("Fail")
    



def run(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-o', '--get-org-id', help='Get the Organisation ID')
    #parser.add_argument('-g', '--get', help='Get list of networks')
    #parser.add_argument('-p', '--post', help='Post list of networks')

    options = parser.parse_args(sys.argv[1:])
    main(**vars(options))

if __name__ == "__main__":
    
    run(sys.argv[1:])