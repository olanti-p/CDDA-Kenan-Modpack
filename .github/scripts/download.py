#!/usr/bin/env python3

import github
import datetime
import json
import os
import time
import requests

repo = 'CleverRaven/Cataclysm-DDA'
target_build = 'linux-tiles-x64'
output_file = 'cata-latest.tar.gz'

def download_asset(download_url):
    print('Downloading from {}', download_url)
    resp = requests.get(download_url)
    print('Status code: {}'.format(resp.status_code))
    if not resp.ok:
        return False
    print('Writing to {}'.format(output_file))
    with open(output_file, mode='wb') as f:
        f.write(resp.content)
    return True

g = github.Github()

print('Current request limit: {}/{}'.format(g.rate_limiting[0], g.rate_limiting[1]))
print('Next limit reset time is {}'.format(datetime.datetime.fromtimestamp(g.rate_limiting_resettime)))

if g.rate_limiting[0] < 10:
    print('Warning: about to hit Guthub''s request limit.')

repo = g.get_repo(repo)

latest_release = repo.get_latest_release()

assets = list(latest_release.get_assets())

for x in assets:
    if target_build in x.name:
        if download_asset(x.browser_download_url):
            print('Success!')
            exit(0)
        else:
            print('Failed to download latest "{}" build.  Try again later.'.format(target_build))
            exit(1)

print('Latest release does not have "{}" build.'.format(target_build))
exit(2)
