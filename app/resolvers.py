import json

class Resolver:

    def __init__(self, pool):
        self.pool = pool 

    def on_get(self, req, resp, value):
        result = {"value": value, "found":False,"types":[]}
        resp.media = json.dumps(result)