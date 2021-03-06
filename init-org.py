#!/usr/bin/env python3

from pprint import pprint
import os, time, sys
import argparse
import requests
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

# Claim devices into Organization inventory
def claimDevicesFromOrder(orgID,orderNo):
    r = meraki_post(f'/organizations/{orgID}/claim',
        payload = {
            'orders': orderNo,
        }
    )
    print(f'Meraki Order {json.loads(r.content["orders"])} claimed successfully.')

# Adds Admin to Organization with full access
def addAdminToOrg(orgID,name,email,orgAccess='full'):
    r = meraki_post(f'/organizations/{orgID}/admins',
        payload = {
            'email': email,
            'name': name,
            'orgAccess': orgAccess,
        }
    )
    print(f'Admin {json.loads(r.content)["name"]} added successfully.')
# Creates organisation, and returns OrgID
def createOrg(orgName): 
    r = meraki_post(f'/organizations',
        payload = {
            'name': orgName,
        }
    )
    print(f'Organisation {json.loads(r.content)["id"]} created succesfully.')
    return json.loads(r.content)["id"]

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
    
# Main routine function
def main(key): 
    env_key = os.environ.get('MERAKI_API_KEY', None) 
    if key is None and env_key is None:
        raise SystemExit('Please set environment variable MERAKI_API_KEY')
    if key is not None:
        print('Warning: Passing a key as an argument is unsafe. Consider using the environment variable MERAKI_API_KEY instead.')
        api_key = key
    else:
        api_key = env_key
    

    orgID = createOrg(input('Name of Organisation: '))
    print()
    name = input('Name of Admin: ')
    email = input('Email of Admin: ')
    addAdminToOrg(orgID,name,email)
    print()
    merakiOrderNo = True
    while (merakiOrderNo):
        claimDevicesFromOrder(orgID,input('Enter a single Meraki Order no: '))
        ans = input("Do you have more Orders?[y/n]: ")
        if ans == "nN":
            return 0
        else:
            merakiOrderNo = False
    print(f'Customer has been created in Meraki Dashboard')
    
def run(args):
    parser = argparse.ArgumentParser()

    parser.add_argument('-k', '--key', help='Meraki API Key')
    parser.add_argument('', '--dry-run', help='Dry-run')

    options = parser.parse_args(sys.argv[1:])
    main(**vars(options))

if __name__ == "__main__":
    #main()
    run(sys.argv[1:])