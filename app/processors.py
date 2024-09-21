import json
import urllib.parse
import falcon

from dao import *


class Processor:
    """
    Abstract class for all api processing instances 
    """
    def __init__(self, dao:Dao, logger):
        self.dao = dao 
        self.logger = logger 

    def normalize(self, value:str) -> str:
        """
        Given a string parameter, parses it
        """
        return urllib.parse.unquote(value).strip().lower()

    
class TokenStats(Processor):
    """
    Displays counters for stats
    """
    def __init__(self, dao, logger):
        super().__init__(dao, logger)

    def on_get(self, req, resp):
        values = self.dao.dump()
        resp.media = json.dumps(values)
        resp.status = falcon.HTTP_200



class TagSolver(Processor):
    """
    Falcon interface to look for a value bounded by a tag
    """
    def __init__(self, dao, logger):
        super().__init__(dao, logger)

    def on_get(self, req, resp, value, tag):
        """
        Query returns matches for value that is an instance of a given tag (transitive) 
        """
        token = self.normalize(value)
        boundaries = self.normalize(tag)
        self.logger.info(f"resolve {token} as {boundaries}")
        matches = []
        try:
            matches = self.dao.load(token)
        except Exception as e:
            self.logger.error("failed to load token " + str(token) + ":" + str(e))
            resp.status = falcon.HTTP_500 
            return
        if len(matches) == 0:
            self.logger.info(f"No match for {token}")
            resp.status = falcon.HTTP_404
        else:
            result = []
            resp.status = falcon.HTTP_200
            for node in matches:
                parents = [parent.lower() for parent in node.tags]
                parents.append(boundaries.lower())
                if boundaries in parents:
                    result.append(node.to_dict())
            resp.media = json.dumps(result)
            resp.status = falcon.HTTP_200



class ValuesAppender(Processor):
    """
    Given a tagged token and a description, adds it to the database
    """
    def __init__(self, dao, logger):
        super().__init__(dao, logger)

    def on_post(self, req, resp, value, tag):
        token = self.normalize(value)
        tag = self.normalize(tag)
        self.logger.info(f"adding {token} as {tag}")
        doc = dict()
        if req.content_length:
            doc = json.load(req.stream)
        payload = json.dumps(doc)
        try:
            self.dao.add_node(token, payload, tag)
            resp.status = falcon.HTTP_200 
        except Exception as e:
            self.logger.error("failed to save token " + str(token) + ":" + str(e))
            resp.status = falcon.HTTP_500 
                