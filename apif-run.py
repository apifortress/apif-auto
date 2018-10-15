import argparse
import requests
import os.path
import json
import yaml
import sys
from functions import get_token, bool_return, run_request_executor, yaml_parser, query_builder

pull_parser = argparse.ArgumentParser(description='APIF CLI Tool.')
pull_parser.add_argument('method', action="store", type=str, choices=['run-all', 'run-by-id', 'run-by-tag'], help="this is the type of run that you'll be performing.")
pull_parser.add_argument('hook', action="store", type=str, help="This is your webhook. It is required. It can be passed as either a URL, or a key from a configuration file.")
pull_parser.add_argument('-f', '--format', action="store", type=str,
                    help="This is the output format. Default is 'json', other options are 'junit' or 'bool'. REQUIRES SYNC MODE (-S)")
pull_parser.add_argument('-S', '--Sync', const='sync=true', nargs='?',
                    help="Sync mode. Waits for a response from the API route.")
pull_parser.add_argument('-d', '--dry', const='dryrun=true', nargs='?', help='Dry run mode.')
pull_parser.add_argument('-s', '--silent', const='silent=true', nargs='?', help='Silent mode')
pull_parser.add_argument('-o', '--out', action='store', type=str, help="output to directory")
pull_parser.add_argument('-c', '--config', action='store', type=str, help="path to config file. Defaults to ./config.yml")
pull_parser.add_argument('-C', '--credentials',
                    help='user credentials. overrides credentials present in config file <username:password>')
pull_parser.add_argument('-t', '--tag', action="store", type=str, help='a test tag')
pull_parser.add_argument('-i', '--id', action='store', type=str, help='a test id')
pull_parser.add_argument('-e', '--env', action='append', nargs="?", help='Any environmental override variables you wish to pass')

if len(sys.argv) == 1:
    pull_parser.print_help(sys.stderr)
    sys.exit(1)

args = pull_parser.parse_args()

config_key = None

web_hook = None

auth_token = None

params = {}

if args.hook.startswith("http" or "https"):
    web_hook = args.hook
else:
    config_key = args.hook

if args.config:
    config_yaml = yaml_parser(os.path.join(args.config))

if config_key:
    if not args.config:
        config_yaml = yaml_parser()
    for hook in config_yaml['hooks']:
        key = hook['key']
        if key == config_key:
            web_hook = hook['url']
            if not args.credentials:
                if "credentials" in hook:
                    config_credentials = (hook['credentials']['username'] + ":" + hook['credentials']['password'])
                    args.credentials = config_credentials
if not web_hook:
    print("Couldn't find any hook to use. Check your configuration")
    exit(1)

if args.credentials:
    auth_token = get_token(args.credentials, web_hook)

if args.env:
    for env in args.env:
        if ':' in env:
            params[env[0:env.find(':')].strip()] = env[env.find(':')+1:].strip()

if args.method == "run-all":
    web_hook = web_hook + '/tests/run-all'
elif args.method == "run-by-tag":
    if args.tag:
        web_hook = web_hook + '/tests/tag/' + args.tag + "/run"
    else:
        print("Run by tag requires a tag (-t)")
        sys.exit(1)
elif args.method == "run-by-id":
    if args.id:
        web_hook = web_hook + '/tests/' + args.id + "/run"
    else:
        print("Run by ID requires an ID (-i)")
        sys.exit(1)

potential_args = [args.Sync, args.dry, args.silent, args.format]

route_list = query_builder(potential_args)

web_hook += route_list

req = run_request_executor(web_hook, auth_token, params, args.Sync, args.format, args.out)

if args.out:
    file = open(os.path.join(args.out), 'w')
    response_body = req.content
    file.write(response_body.decode('utf-8'))
    if req.status_code==200:
        print("APIF: OK")
    else:
        print("APIF: " +str(req.status_code)+ " error")
