#!/usr/bin/env python
# Rebuild arbitrary results in fareto-examples with new backend versions, by sending the same profile requests to
# a running backend

import requests
import json
import os
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('result', nargs='+', metavar='RESULT_JSON', help='One or more result JSON files that will be updated')
parser.add_argument('--backend', default='http://localhost:8080', metavar='BACKEND', help='URL of backend server to query (should be running R5Main point')
parser.add_argument('--skip-backup', action='store_true', help='Don\'t back up files before overwriting')
args = parser.parse_args()

for fn in args.result:
    print(fn)
    with open(fn, 'r') as injson:
        orig = json.load(injson)

    result = requests.post(args.backend + '/pareto', data=json.dumps(orig['request']))
    if result.status_code != 200:
        print(f'  Error fetching result for {fn}: status code {result.status_code}:')
        print(result.text)
    else:
        resjson = result.json()
        if not args.skip_backup:
            os.rename(fn, fn + '.b')
        with open(fn, 'w') as outjson:
            json.dump(resjson, outjson, indent=2)