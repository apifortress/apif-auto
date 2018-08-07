import os.path
from lxml import etree

def payload_builder(path, branch, payload):
        for root, dirs, files in os.walk(path):
            dir_name = root.split('/')[-2]
            for filename in files:
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