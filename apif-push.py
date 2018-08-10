import argparse
import requests
import os.path
import json
import yaml
import sys
from functions import payload_builder, get_token, traverser

push_parser = argparse.ArgumentParser(description='Push Test to APIF Platform')
push_parser.add_argument('-P', '--push', const="/tests/push", nargs="?", help='This command executes a push to APIF')
push_parser.add_argument('-H', '--hook', help="This is your webhook. It's required.")
push_parser.add_argument('-r', '--recursive', nargs="?", action='append', help='Recursive file-getter')
push_parser.add_argument('-c', '--config', action='store', type=str, help="path to config file")
push_parser.add_argument('-C', '--credentials',
                    help='user credentials. overrides credentials present in config file <username:password>')
push_parser.add_argument('-p', '--path', type=str, nargs="?", action='append', help="this is the path to the files you want to push")
push_parser.add_argument('-k', '--key', action='store', type=str,
                    help='A key from a configuration file. Pulls the related configuration data.')
push_parser.add_argument('-b', '--branch', action='store', type=str, help="The specific branch")

if len(sys.argv) == 1:
    push_parser.print_help(sys.stderr)
    sys.exit(1)

args = push_parser.parse_args()

web_hook = args.hook

auth_token = None

branch = "master"

payload = {
    "resources": []
}

if args.branch:
    branch = args.branch

if args.path:
    for path in args.path:
        payload_builder(path, branch, payload)

if args.config:
    with open(os.path.join(args.config)) as stream:
        try:
            config_yaml = (yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)

if args.recursive:
    for recursion in args.recursive:
        traverser(recursion, branch, payload)


if args.key:
    for hook in config_yaml['hooks']:
        key = hook['key']
        if key == args.key:
            if not args.hook:
                web_hook = hook['url']
            if not args.credentials:
                config_credentials = (hook['credentials']['username'] + ":" + hook['credentials']['password'])
                args.credentials = config_credentials

if args.credentials:
    user_creds = args.credentials.split(":")
    auth_req = requests.get(web_hook + '/login', auth=(user_creds[0], user_creds[1]))
    access_token = auth_req.content
    parsed_token = json.loads(access_token)
    if not access_token in parsed_token: 
        print("Invalid credentials!")
    else:
        auth_token = parsed_token['access_token']

if args.push:
    web_hook = web_hook + args.push

if auth_token:
    headers = {'Authorization': 'Bearer ' + auth_token}
    req = requests.post(web_hook, headers=headers, data=json.dumps(payload).encode('utf-8'))
    if req.status_code==200:
        print("APIF: OK")
    else:
        print("APIF: " + str(req.status_code) + " error")
