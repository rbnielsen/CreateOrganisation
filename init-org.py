#!/usr/bin/env python3

from pprint import pprint
import os, time, sys
import requests

MAX_RETRIES = 5

api_key = os.environ['MERAKI_API_KEY']
apiVersion = 'v1'
baseURL = 'https://elera.dl/api.meraki.com/api/'+apiVersion

# Claim devices into Organization inventory
def claimDevicesFromOrder(orgID,orderNo):
    ...

# Adds Admin to Organization with full access
def addAdminToOrg(orgID,name,email,orgAccess='full'):
    meraki_post(f'/organizations/{orgID}/admins',
        data = {
            'email': email,
            'name': name,
            'orgAccess': orgAccess
        }
    )
    print(f'Admin {name!r} added successfully.')
# Creates organisation, and returns OrgID
def createOrg(orgName): 
    r = meraki_post(f'/organization',
        data={
            'name': orgName,
        }
    )
    print('Organisation created succesfully.')
    return r.headers["id"]

def meraki_post(sub_url, data, max_retries=MAX_RETRIES):
    for _ in range(max_retries):   
        r = requests.post(
            baseURL+sub_url,
            headers={
                'X-Cisco-Meraki-API-Key': api_key,
                'Content-Type': 'application/json'
            },
            data=data
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
def main():
    orgID = createOrg(input('Name of Organisation: '))

    name = input('Name of Admin: ')
    email = input('Email of Admin: ')
    addAdminToOrg(orgID,name,email)

    claimDevicesFromOrder(orgID,input('Enter Meraki Order no: '))
if __name__ == '__main__':
    main()