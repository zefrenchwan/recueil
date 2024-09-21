import json
import urllib.parse
from psycopg.rows import class_row, dict_row
from dataclasses import dataclass
from typing import Any


@dataclass
class NodeDTO:
    """
    General definition of a dto from the database
    """
    token_content: str
    attributes: str 
    tags: list[str]

    def to_dict(self):
        """
        map that value to a dict so it may be returned in a JSON
        """
        return self.__dict__

class Dao:
    """
    All database operations 
    """
    def __init__(self, pool, logger):
        """
        Builds a new resolver using a db pool
        """
        self.pool = pool 
        self.logger = logger 

    def check_expected_value(self, v: Any, t: type, none_allowed = False):
        """
        Raise exception to prevent a SQL issue
        """
        if not none_allowed and v is None:
            raise Exception("none type when not null expected")
        if not isinstance(v, t):
            raise Exception("expected {exp}, got {real}".format(exp = str(t), real = str(type(v))))

    def load(self, value:str) -> list[NodeDTO]:
        """
        Given a value to search for, get all matching results as node dto
        """
        result = list()
        with self.pool.connection() as conn, conn.cursor(row_factory=class_row(NodeDTO)) as cursor:
            cursor.execute("select * from entities.load_entity(%s)", [value])
            matches = cursor.fetchall()
            for matching in matches:
                result.append(matching)
        return result
    
    
    def add_node(self, token: str, attributes: str, tag: str):
        """
        Stores a new token with its attributes and tag
        """
        self.check_expected_value(token, str)
        self.check_expected_value(attributes, str)
        self.check_expected_value(tag, str)
        with self.pool.connection() as conn, conn.cursor() as cursor, conn.transaction():
            cursor.execute('call entities.insert_value(%s, %s, %s);', (token, attributes, tag))
