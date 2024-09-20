import json
import urllib.parse
from psycopg.rows import class_row
from dataclasses import dataclass
import falcon


@dataclass
class NodeDTO:
    """
    General definition of a dto from the database
    """
    value: str
    description: str 
    tag:str 
    parents: list[str]

    def to_dict(self):
        """
        map that value to a dict so it may be returned in a JSON
        """
        return self.__dict__


class Resolver:
    """
    Abstract class for all api processing instances 
    """
    def __init__(self, pool):
        """
        Builds a new resolver using a db pool
        """
        self.pool = pool 

    def normalize(self, value:str) -> str:
        """
        Given a string parameter, parses it
        """
        return urllib.parse.unquote(value).strip().lower()

    def load(self, value:str) -> list[NodeDTO]:
        """
        Given a value to search for, get all matching results as node dto
        """
        result = list()
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(NodeDTO)) as cursor:
                for matching in cursor.execute("select * from entities.load_entity(%s)", [value]):
                    result.append(matching)
        return result
    
    

class TagSolver(Resolver):
    """
    Falcon interface to look for a value bounded by a tag
    """
    def __init__(self, pool):
        super().__init__(pool)

    def on_get(self, req, resp, value, tag):
        """
        Query returns matches for value that is an instance of a given tag (transitive) 
        """
        query = self.normalize(value)
        boundaries = self.normalize(tag)
        matches = self.load(query)
        if len(matches) == 0:
            resp.status = falcon.HTTP_404
        else:
            result = []
            resp.status = falcon.HTTP_200
            for node in matches:
                parents = [parent.lower() for parent in node.parents]
                parents.append(boundaries)
                if boundaries in parents:
                    result.append(node.to_dict())
            resp.media = json.dumps(result)