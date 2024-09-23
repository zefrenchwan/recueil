from dao import Dao
import os
from parsers import TreeParser
import json 


class Bootstrapper:
    """
    When starting the project, some files are provided to feed initial data
    """
    def __init__(self, dao: Dao, logger):
        self.dao = dao 
        self.logger = logger 

    def load(self, dir: str):
        """
        Given a directory, parses it and 
        """
        # first, find files to process
        hierarchy = []
        data = []
        # expected is one csv and multiple json 
        for root, dir, files in os.walk(dir):
            for file in files:
                path = os.path.join(root, file)
                if file.endswith(".csv"):
                    hierarchy.append(path)
                elif file.endswith(".json"):
                    data.append(path)
        # then, find hierarchies
        ontology_parser = TreeParser()
        for file in hierarchy:
            with open(file, "r") as h:
                line = h.readline()
                while line is not None and len(line) != 0:
                    ontology_parser.add(line)
                    line = h.readline()
        for value in ontology_parser.expand():
            parent = value[0]
            child = value[1] if len(value) == 2 else None 
            if child is None:
                self.logger.info(f"adding tag {parent}")
                self.dao.add_tag(parent)
            else:
                self.logger.info(f"linking {child} to {parent}")
                self.dao.add_link(child, parent)
        del ontology_parser
        # parse the data content
        for file in data:
            with open(file, "r") as d:
                contents = json.load(d)
                for content in contents:
                    token_content = content["token"]
                    attributes = json.dumps(content["content"])
                    tag = content["tag"]
                    self.logger.info(f"flagging {token_content} as {tag}")
                    self.dao.add_node(token_content, attributes, tag)

