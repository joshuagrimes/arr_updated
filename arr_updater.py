import requests
import json
import time
import win32serviceutil
import argparse

sonarr_base_url = 'http://192.168.50.194:8989/api/v3'
sonarr_4k_base_url = 'http://192.168.50.194:8990/api/v3'
radarr_base_url = ''
radarr_4k_base_url = ''

updates_api = '/update'
command_api = '/command'
shutdown_api = '/system/shutdown'

sonarr_api = 'aec8dc19263d4d54a18cd0d3b9b0b897'
sonarr_4k_api = '24c8fb1b0f7240f7b1b0e9e58cb80752'
radarr_api = ''
radarr_4k_api = ''

parser = argparse.ArgumentParser()
parser.add_argument('--arr_app', dest='arr_app', type=str, help='Specify sonarr or radarr')
args = parser.parse_args()

arr_app = args.arr_app

if arr_app == 'sonarr':
    api_key = sonarr_api
    api_key_4k = sonarr_4k_api
    base_url = sonarr_base_url
    base_url_4k = sonarr_4k_base_url
    service_name = 'Sonarr-4K'
elif arr_app == 'radarr':
    api_key = radarr_api
    api_key_4k = radarr_4k_api
    base_url = radarr_base_url
    base_url_4k = radarr_4k_base_url
    service_name = 'Radarr-4K'

def check_for_updates(url=updates_api, api_key=api_key):
    headers = {
        "Accpet": "*/*",
        "X-Api-Key": api_key
    }
    
    full_url = base_url + url
    
    resp = requests.get(url=full_url,headers=headers).json()

    updates = [update for update in resp if update['latest']==True]

    return updates[0]['installed']

def update_arr(url=command_api, api_key=api_key):
    arr_command_url = ''

    headers = {
        "Accept": "application/json, text/javascript, */*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "X-Api-Key": api_key
    }

    params = {
        "Name": "ApplicationUpdate"
    }
    data = f' {{ "Name": "ApplicationUpdate" }}'

    full_url = base_url + url
    
    resp = requests.post(url=full_url, headers=headers,data=data)
    return resp.json()

def shutdown_arr(url=shutdown_api, api_key=api_key_4k):
    arr_command_url = ''
    
    headers = {
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "X-Api-Key": api_key_4k
    }

    full_url = base_url_4k + url

    resp = requests.post(url=full_url, headers=headers)

    return resp

up_to_date = check_for_updates()

if up_to_date == False:
    shutdown_arr()
    update_arr()
    time.sleep(300)
    win32serviceutil.StartService(serviceName=service_name)