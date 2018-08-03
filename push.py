import argparse
import requests
import os.path
import json
import yaml

push_parser = argparse.ArgumentParser(description='Push Test to APIF Platform')
push_parser.add_argument('-P', '--push', const = "potato!", nargs='?', help='I GIEV POTATO')
push_parser.add_argument('-H', '--hook', help="This is your webhook. It's required.")
push_parser.add_argument('-r', '--recursive', help='recursive call?')
push_parser.add_argument('-c', '--config', action='store', type=str, help="path to config file")
push_parser.add_argument('-C', '--credentials',
                    help='user credentials. overrides credentials present in config file <username:password>')
push_parser.add_argument('-p', '--path', action="store", help="this is the path to the files you want to push")

args = push_parser.parse_args()

web_hook = args.hook

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

