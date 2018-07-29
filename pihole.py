# -*- coding: utf-8 -*-
import json
import time
import os
if __name__ != "__main__":
    from urllib.request import urlopen

url = "http://pi.hole/admin"

status_check = "%s/api.php?status" % url

summary_today = "%s/api.php?summary" % url


def nativejson(data):
    return json.loads(data)


def request(input_url, method='GET'):
    response = urlopen(input_url)
    return nativejson(response.read().decode('utf-8'))


def check_status():
    response = request(status_check)
    return response['status']


def get_summary():
    response = request(summary_today)
    summary = 'Status: ' + response['status'] + '\n' + \
            'Domains being blocked: ' + response['domains_being_blocked'] + '\n' + \
            'Total Queries today: ' + response['dns_queries_today'] + '\n' + \
            'Ads blocked today: ' + response['ads_blocked_today'] + '\n' + \
            'Queries Blocked: ' + response['ads_percentage_today'] + '%'
    return summary


if __name__ == "__main__":
    from urllib2 import urlopen
    response = request(summary_today)
    print(response)
    get_summary()