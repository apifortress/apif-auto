import argparse
import requests
import os.path
import json
import yaml

pull_parser = argparse.ArgumentParser(description='APIF CLI Tool.')
pull_parser.add_argument('-RA', '--run_all', const='/tests/run-all', nargs='?',
                    help='This will execute all the tests in a chosen project')
pull_parser.add_argument('-RI', '--run_by_id', const='/tests/', nargs='?', help='this will execute a test with a specific id')
pull_parser.add_argument( '-RT', '--run_by_tag', const='/tests/tag/', nargs='?', help='this will run a test by a tag')
pull_parser.add_argument('-H', '--hook', help="This is your webhook. It's required.")
pull_parser.add_argument('-f', '--format', action="store", type=str,
                    help="This is the output format. Options are JSON, JUnit, or Bool")
pull_parser.add_argument('-S', '--Sync', const='?sync=true', nargs='?',
                    help="Sync mode. Waits for a response from the API route.")
pull_parser.add_argument('-d', '--dry', const='&dryrun=true', nargs='?', help='Dry run mode.')
pull_parser.add_argument('-s', '--silent', const='&silent=true', nargs='?', help='Silent mode')
pull_parser.add_argument('-o', '--out', action='store', type=str, help="output to directory")
pull_parser.add_argument('-c', '--config', action='store', type=str, help="path to config file")
pull_parser.add_argument('-C', '--credentials',
                    help='user credentials. overrides credentials present in config file <username:password>')
pull_parser.add_argument('-t', '--tag', action="store", type=str, help='a test tag')
pull_parser.add_argument('-i', '--id', action='store', type=str, help='a test id')
pull_parser.add_argument('-k', '--key', action='store', type=str,
                    help='A key from a configuration file. Pulls the related configuration data.')

args = pull_parser.parse_args()

web_hook = args.hook

auth_token = None

if args.config:
    with open(os.path.join(args.config)) as stream:
        try:
            config_yaml = (yaml.load(stream))
        except yaml.YAMLError as exc:
            print(exc)

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
    username = user_creds[0]
    password = user_creds[1]
    auth_req = requests.get(web_hook + '/login', auth=(username, password))
    access_token = auth_req.content
    parsed_token = json.loads(access_token)
    auth_token = parsed_token['access_token']

if args.run_all:
    web_hook = web_hook + args.run_all

if args.run_by_tag:
    web_hook = web_hook + args.run_by_tag + args.tag + "/run"

if args.run_by_id:
    web_hook = web_hook + args.run_by_id + args.id + "/run"

route_list = []

potential_args = [args.Sync, args.dry, args.silent, args.format]

for arg in potential_args:
    if arg:
        if arg == args.format:
            route_list.append('&format=' + args.format)
        else:
            route_list.append(arg)

for route in route_list:
    web_hook = web_hook + route

if auth_token:
    headers = {'Authorization': 'Bearer ' + auth_token}
    req = requests.get(web_hook, headers=headers)
elif web_hook:
    req = requests.get(web_hook)

if args.out:
    file = open(os.path.join(args.out), 'w')
    response_body = req.content
    file.write(response_body.decode('utf-8'))

if req.status_code==200:
    print("APIF: OK")
else: 
    print("APIF:" +req.status_code+ " error")
