from enum import Enum


class DBTypes(Enum):
    Neo4j = 'neo4j'
    InMemory = 'in_memory'