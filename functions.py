import os.path
from lxml import etree
import requests
import json

def payload_builder(path, branch, payload):
        for root, dirs, files in os.walk(path):
            dir_name = root.split('/')[-2]
            print(dir_name)
            print(files)
            for filename in files:
                print(filename)
                if filename == "unit.xml" or "input.xml":
                    new_resource = {
                        "path" : "",
                        "branch" : "",
                        "revision" : "",
                        "content" : ""
                    }
                    with open(os.path.join(path + filename)) as stream:
                        try:
                            tree = etree.parse(stream)
                            xml_string = etree.tostring(tree)
                        except etree.ParseError as exc:
                            print(exc)
                    new_resource["path"] = dir_name + "/" + filename
                    new_resource["branch"] = branch
                    new_resource["content"] = xml_string
                    payload["resources"].append(new_resource)
                else:
                    continue

def get_token(credentials, hook):
    user_creds = credentials.split(":")
    username = user_creds[0]
    password = user_creds[1]
    auth_req = requests.get(hook + '/login', auth=(username, password))
    access_token = auth_req.content
    parsed_token = json.loads(access_token)
    auth_token = parsed_token['access_token']
    return auth_token