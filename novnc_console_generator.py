#!/usr/bin/python

import requests
import json
import sys
import re

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


def user_input():
    sys.stdin = open('/dev/tty')

    # sys args are; -u user -k key -s server
    if len(sys.argv) > 1:
        if sys.argv[1] == str('-u'):
            user = str(sys.argv[2])
        if sys.argv[3] == str('-k'):
            key = str(sys.argv[4])
        if sys.argv[5] == str('-s'):
            server_id = str(sys.argv[6])
    else:
        user = str(raw_input(txt_colors.YELLOW + 'Please enter account username: ' + txt_colors.ENDC))
        key = str(raw_input(txt_colors.YELLOW +'Please enter authentication key: '+ txt_colors.ENDC))
        server_id = str(raw_input(txt_colors.YELLOW +'Please enter the server ID: '+ txt_colors.ENDC))

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
