example = {
    "resources": [
        {
            "path": "",
            "branch": "",
            "revision": "",
            "content": ""
        }
    ]
}

paths = ["path1", "path2", "path3"]

result = {
    "resources": []
}

def builder(arr):
    for path in arr:
        result["resources"].append(path)


builder(paths)

print(result)