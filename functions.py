import os.path
import xml.etree.ElementTree as ET
import requests
import json
import sys
import io
import yaml

## This is the function that generates a payload for the -p (path) tag.

def payload_builder(path, branch, payload):
        for root, dirs, files in os.walk(path):
            seperator = os.sep
            dir_name = root.split(seperator)[-2]
            for next_file in files:
                acceptable = ['input.xml', "unit.xml"]
                if next_file in acceptable:
                    new_resource = {
                        "path" : "",
                        "branch" : "",
                        "revision" : "",
                        "content" : ""
                    }
                    with open(os.path.join(path + next_file)) as stream:
                        try:
                            content = stream.read()
                            tree = ET.fromstring(content)
                            new_resource["path"] = dir_name + "/" + next_file
                            new_resource["branch"] = branch
                            new_resource["content"] = content
                            payload["resources"].append(new_resource)
                        except ET.ParseError as exc:
                            print(exc, "This XML document is invalid.")

                else:
                    continue

## This function allows us to generate an API Fortress security token based on the provided u/p combo.

def get_token(credentials, hook):
    user_creds = credentials.split(":")
    auth_req = requests.get(hook + '/login', auth=(user_creds[0], user_creds[1]))
    access_token = auth_req.content
    parsed_token = json.loads(access_token.decode("utf-8"))
    if not "access_token" in parsed_token:
        print("Invalid credentials!")
        sys.exit(1)
        return None
    else:
        auth_token = parsed_token['access_token']
        return auth_token

## This function allows us to traverse through the filesystem past a given path and find all of the pertinent files for the -r tag.

def traverser(route, branch, payload):
    for root, dirs, files in os.walk(route):
        seperator = os.sep
        dir_name = root.split(seperator)[-1]
        for next_file in files:
            acceptable = ['input.xml', "unit.xml"]
            if next_file in acceptable:
                new_resource = {
                        "path" : "",
                        "branch" : "",
                        "revision" : "",
                        "content" : ""
                    }
                
                with open(os.path.abspath(os.path.join(root + "/" + next_file))) as stream:
                    try:
                        content = stream.read()
                        tree = ET.fromstring(content)
                        new_resource["path"] = dir_name + "/" + next_file
                        new_resource["branch"] = branch
                        new_resource["content"] = content
                        payload["resources"].append(new_resource)
                    except ET.ParseError as exc:
                            print(exc, "This XML document is invalid.")

def bool_return(json):
    if type(json) is list:
        for result in json:
            if result["failuresCount"] > 0:
                return False
            else:
                return True
    else:
        if json['failuresCount'] > 0:
            return False
        else:
            return True

def request_executor(webhook, auth_token, params, sync, format, output):
    headers = {}
    body = {}
    if auth_token:
        headers = {'Authorization': 'Bearer ' + auth_token}
    if params:
        body = json.dumps({'params': params}).encode('utf-8')
    req = requests.post(webhook, headers=headers, data=body)
    print(req.request.body)
    if sync:
        if format == "bool":
            parsed_json = json.loads(req.content)
            print(bool_return(parsed_json))
            sys.exit(1)
        if not output:
            if req.headers["Content-Type"].startswith('application/json'):
                parsed_json = json.loads(req.content)
                print(json.dumps(parsed_json, indent=4))
            else:
                print(req.content)
    else:
        if req.status_code==200:
            print("APIF: OK")
        else:
            print("APIF: " +str(req.status_code)+ " error")
    return req
    