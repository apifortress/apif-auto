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
push_parser.add_argument('p', '--path', action="store", help="this is the path to the files you want to push")

args = push_parser.parse_args()

web_hook = args.hook