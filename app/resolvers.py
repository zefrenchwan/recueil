import json
import re
from psycopg.rows import class_row
from dataclasses import dataclass
from typing import Optional


@dataclass
class NodeDTO:
    value: str
    description: Optional[str] = None 
    tag:str 
    parents: list[str]


class Resolver:

    def __init__(self, pool):
        self.pool = pool 

    def normalize(self, value:str) -> str|None:
        base = re.sub(r'\s\s+', " ")
        size = len(base)
        base = base.replace("  ",' ')
        while size > len(base):
            size = len(base)
            base = base.replace("  ",' ')
        return base.lower()    

    def load(self, value:str) -> list[NodeDTO]:
        result = list()
        with self.pool.connection() as conn:
            with conn.cursor(row_factory=class_row(NodeDTO)) as cursor:
                for matching in cursor.execute("select * from entities.load_entity(%s)", value):
                    result.append(matching)
        return result