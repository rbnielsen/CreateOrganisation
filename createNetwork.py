#!/usr/bin/env python3

from pprint import pprint
import os, time, sys
import argparse
import requests
from requests import Session
import json
import csv

MAX_RETRIES = 5
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

# Write to file
def WriteToCsvFile(p_filename,p_data):
    ...

def CreateNetworks(p_filename):
    return 0

# Get list of networks
def GetNetworkList(p_apiKey,p_orgID):
    if p_orgID is not None:
        for _ in range(MAX_RETRIES):
            try:
                r = session.get(
                    baseURL+"/organizations/"+p_orgID+"/networks",
                    headers = {
                        'Authorization': f'Bearer {p_apiKey}',
                        'Content-Type': 'application/json',
                        "Accept": "application/json",
                    }
                )
                if r.status_code == 200:
                    return r              
                elif r.status_code == 429:
                    print(f'Rate limited - Retrying after {r.headers["Retry-After"]}.')
                    time.sleep(int(r.headers['Retry-After']))
                    continue
                else:
                    raise SystemExit(f'Unexpected status code: {r.status_code} returned from server')
            except Exception as e:
                pprint(e)
                return ""

def GetOrgs(p_apiKey):
    for _ in range(MAX_RETRIES):
        try: 
            r = session.get(
                baseURL+'/organizations',
                headers = {
                    'Authorization': f'Bearer {p_apiKey}',
                    'Content-Type': 'application/json',
                    "Accept": "application/json",
                }
            )
            if r.status_code == 200:
                return r
            elif r.status_code == 429:
                print(f'Rate limited - Retrying after {r.headers["Retry-After"]}.')
                time.sleep(int(r.headers['Retry-After']))
                continue
            else:
                raise SystemExit(f'Unexpected status code: {r.status_code} returned from server.')
            
        except Exception as e:
            pprint(e)

# Main routine function
def main(arg_org_id,arg_get_nw,arg_create_nw): 
    #arg_org_id = "409192" # ND Testnet
    #arg_org_id = "785083" # Redmark
    print(locals())
    print()
    API_KEY = os.environ.get('MERAKI_API_KEY', None) 
    if API_KEY is None:
        raise SystemExit('Please set environment variable MERAKI_API_KEY')
    else:
        API_KEY = os.environ['MERAKI_API_KEY']

    if arg_org_id is not None and arg_get_nw is not None:
        print('Getting list of ntworks...')
        r = GetNetworkList(API_KEY,arg_org_id)
        rjson = r.json()
        print('Success!')
        print(f'Writing list to {arg_get_nw}...')
        # with open (a_get_nw,'w') as csvfile:
        #     csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        #     for _ in rjson:
        #         csvwriter.writerow([_['organizationId'],_['id'],_['name']])
        pprint(rjson)
        print("Done!")
        return
    elif arg_org_id is not None and arg_create_nw is not None:
        print(f'Creating networks for org id {arg_org_id}...')
        result = CreateNetworks(arg_create_nw)
        if result == 0:
            print('Networks Created!')
            return 0
        else:
            print(f'Error: {result}')
            return result




    # if a_org_id is None and a_get_nw is not None:
    #     org = GetOrgs(API_KEY)
    #     orgjson = org.json()
    #     orgs = []
    #     for _ in orgjson:
    #         orgs.append({_['id']: _['name']})
    #     pprint(orgs)
    #     a_org_id = input("Please enter org id: ")
    #     print(a_org_id)
    #     return
    #     #raise SystemExit("Organisation ID not specified.")
    # if a_org_id is not None and a_get_nw is None:
    #     print(a_get_nw)
    #     r = GetNetworkList(API_KEY,a_org_id)
    #     rjson = r.json()
    #     # with open (a_get_nw,'w') as csvfile:
    #     #     csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"')
    #     #     for _ in rjson:
    #     #         csvwriter.writerow([_['organizationId'],_['id'],_['name']])
    #     pprint(rjson)
    #     return
    # if a_org_id is not None and a_get_nw is not None:
    #     print("HEY")
    # if a_org_id is not None and a_create_nw is not None:
    #     print("Network created")
    #     #CreateNetworks(a_create_nw)
    #     return
    

def run(args):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    parser.add_argument('-o', '--org-id', dest='arg_org_id', help='Set the Organisation ID')
    group.add_argument('-n', '--get-networks', dest='arg_get_nw', help='Get Networks')
    group.add_argument('-c', '--create-networks', dest='arg_create_nw', help='Get Networks')
    
    options = parser.parse_args(sys.argv[1:])
    main(**vars(options))

if __name__ == "__main__":
    run(sys.argv[1:])