def json_import(filename):
    with open(filename, 'r') as f:
        data = f.read()
    js = json.loads(data)
    return js


def json_export(filename, ldict):
    with open(filename, 'w') as f:
        jstr = json.dumps(ldict)
        f.write(jstr)
