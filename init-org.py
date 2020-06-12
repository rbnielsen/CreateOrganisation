#!/usr/bin/env python3

from pprint import pprint
import os, time, sys
import requests

api_key = os.environ['MERAKI_API_KEY']

apiVersion = "v1"

baseURL = "https://api.meraki.com/api/"+apiVersion

# Claim devices into Organization inventory
def claimDevicesFromOrder(orgID,orderNo):
    ...

# Adds Admin to Organization with full access
def addAdminToOrg(orgID,name,email,orgAccess="full"):
    try:
        r = requests.post(
            baseURL+"/organizations/"+orgID+"/admins",
            headers = {
                "X-Cisco-Meraki-API-Key": api_key,
                "Content-Type": "application/json"
            },
            data = {
                "email": email,
                "name": name,
                "orgAccess": orgAccess
            }
        )
        if r.status_code == 201:
            pprint("Admin '"+name+"' added successfully.\n")
            return 0
        elif r.status_code == 429:
            pprint("Rate limited activated - Retry after "+r.headers["Retry-After"]+".\n")
            time.sleep(int(r.headers["Retry-After"]))
        else:
            pprint(r.status_code)
    except Exception as e:
        pprint(e)

# Creates organisation, and returns OrgID
def createOrg(orgName): 
    try:
        # r = {
        #     "status_code": 200
        # }
        r = requests.post(
            baseURL+"/organisation",
            headers={
                "X-Cisco-Meraki-API-Key": api_key,
                "Content-Type": "application/json"
            },
            data={
                "name": orgName,
            },
        )
        if r.status_code == 200:
            print("Organisation created succesfully.\n")
            return r.headers["id"]
        elif r.status_code == 429:
            print("Rate limited activated - Retry after "+r.headers["Retry-After"]+".\n")
            time.sleep(int(r.headers["Retry-After"]))
        else: 
            pprint(r.status_code)
    except Exception as e:
        pprint(e)

# Main routine function
def main():
    try:
        orgID = createOrg(input("Name of Organisation: "))
        
        name = input("Name of Admin: ")
        email = input("Email of Admin: ")
        addAdminToOrg(orgID,name,email)
        
        claimDevicesFromOrder(orgID,input("Enter Meraki Order no: "))
    except Exception as e:
        pprint(e)

if __name__ == "__main__":
    main()
