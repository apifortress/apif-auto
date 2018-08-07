import argparse
import requests
import os.path
import json
import yaml
from lxml import etree

push_parser = argparse.ArgumentParser(description='Push Test to APIF Platform')
push_parser.add_argument('-P', '--push', const="/tests/push", nargs="?", help='I GIEV POTATO')
push_parser.add_argument('-H', '--hook', help="This is your webhook. It's required.")
push_parser.add_argument('-r', '--recursive', help='recursive call?')
push_parser.add_argument('-c', '--config', action='store', type=str, help="path to config file")
push_parser.add_argument('-C', '--credentials',
                    help='user credentials. overrides credentials present in config file <username:password>')
push_parser.add_argument('-p', '--path', type=str, help="this is the path to the files you want to push")
push_parser.add_argument('-k', '--key', action='store', type=str,
                    help='A key from a configuration file. Pulls the related configuration data.')
push_parser.add_argument('-b', '--branch', action='store', type=str, help="The specific branch")

args = push_parser.parse_args()

web_hook = args.hook

branch = "master"

payload = {
    "resources": []
}

if args.branch:
    branch = args.branch

if args.path:
    for root, dirs, files in os.walk(args.path):
        for filename in files:
            if filename == "unit.xml" or "input.xml":
                new_resource = {
                    "path" : "",
                    "branch" : "",
                    "revision" : "",
                    "content" : ""
                }
                with open(os.path.join(args.path + filename)) as stream:
                    try:
                        tree = etree.parse(stream)
                        xml_string = etree.tostring(tree)
                    except etree.ParseError as exc:
                        print(exc)
                new_resource["path"] = filename
                new_resource["branch"] = args.branch
                new_resource["content"] = xml_string
                payload["resources"].append(new_resource)

   
        

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

if args.push:
    web_hook = web_hook + args.push


print(payload)