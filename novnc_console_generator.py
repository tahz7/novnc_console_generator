#!/usr/bin/python

import requests
import json
import sys
import re
import argparse

class txt_colors:
    BLUE = '\033[94m'
    RED = '\033[31m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[35m'
    ORANGE = '\033[33m'
    LIGHTRED = '\033[91m'
    CYAN = '\033[36m'
    PINK = '\033[95m'
    HEADER = '\033[95m'
    BOLD = '\033[01m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def user_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='Enter your http://mycloud.rackspace.com user', type=str, required=True)
    parser.add_argument('-k', help='Enter your api key', type=str, required=True)
    parser.add_argument('-s', help='Enter your server ID', type=str, required=True)
    args = parser.parse_args()
    user = args.u
    key = args.k
    server_id = args.s

    return user, key, server_id

def user_input():
    sys.stdin = open('/dev/tty')

    if len(sys.argv) > 1:
        user, key, server_id = user_arg()
    else:
        while True:
            user = str(raw_input(txt_colors.YELLOW + 'Please enter account username: ' + txt_colors.ENDC))
            key = str(raw_input(txt_colors.YELLOW +'Please enter authentication key: '+ txt_colors.ENDC))
            server_id = str(raw_input(txt_colors.YELLOW +'Please enter the server ID: '+ txt_colors.ENDC))

            if all([user, key, server_id]):
                break
            else:
                print txt_colors.LIGHTRED + '\nPlease do not leave any fields blank \n' + txt_colors.ENDC

    token, ddi, default_region = get_token(user, key)

    if default_region == 'LON':
        region_list = ['lon']
    else:
        region_list = set(["iad", "ord", "hkg", "syd", "dfw"])

    return token, ddi, region_list, server_id


def get_token(user, key):
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
            }

    data = '{"auth": {"RAX-KSKEY:apiKeyCredentials": {"username":"%s", "apiKey":"%s"}}}' % (user, key)

    try:
        auth_api_url = 'https://identity.api.rackspacecloud.com/v2.0/tokens'
        auth_api_post = requests.post(auth_api_url, timeout=15, verify=True, headers=headers, data=data)
        result_dump = json.dumps(auth_api_post.json())
        result_loads = json.loads(result_dump)
    except:
        print ("Timed out to Rackspace API (auth_api)")

    if 'unauthorized' in result_loads:
        print txt_colors.LIGHTRED + result_loads['unauthorized']['message'] + txt_colors.ENDC
        sys.exit()
    elif 'badRequest' in result_loads:
        print txt_colors.LIGHTRED + result_loads['badRequest']['message'] + txt_colors.ENDC
        sys.exit()
    else:
        token = result_loads['access']['token'][ u'id']
        ddi =  result_loads['access']['token'][u'tenant'][u'id']
        default_region = result_loads['access']['user']['RAX-AUTH:defaultRegion']

    return token, ddi, default_region



def generate_novnc_link(token, dc, ddi, server_id):
    headers = {
    'X-Auth-Token': token,
    'Content-type': 'application/json',
        }

    data = '{"os-getVNCConsole": {"type":"novnc"}}'

    try:
        novnc_api_url = 'https://{0}.servers.api.rackspacecloud.com/v2/{1}/servers/{2}/action'.format(dc, ddi, server_id)
        novnc_api_post = requests.post(novnc_api_url, timeout=15, verify=True, headers=headers, data=data)
        result_dump = json.dumps(novnc_api_post.json())
        result_loads = json.loads(result_dump)
    except:
        print ("Timed out to Rackspace API (novnc_api)")

    if u'console' in result_loads:
        generate_novnc_link = result_loads[u'console'][u'url']
    elif 'itemNotFound' in result_loads:
        print txt_colors.LIGHTRED + result_loads['itemNotFound']['message'] + txt_colors.ENDC
        sys.exit()
    else:
        generate_novnc_link = None

    return generate_novnc_link


def get_novnc_link():
    token, ddi, region_list, server_id = user_input()

    for dc in region_list:
        novnc_link = generate_novnc_link(token, dc, ddi, server_id)
        if novnc_link:
            return novnc_link


def print_results():
    novnc_link = get_novnc_link()
    print txt_colors.GREEN + novnc_link + txt_colors.ENDC


def main():
    print_results()

    try:
        sys.stdout.close()
    except:
        pass
    try:
        sys.stderr.close()
    except:
        pass


if __name__ == "__main__":
    main()
