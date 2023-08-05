from SmartCI.common.dao.project_dependencies_dao_memory import ProjectDependenciesDaoMemory
from SmartCI.common.database.enums.db_types import DBTypes
from SmartCI.common.dao.project_dependencies_dao_neo4j import ProjectDependenciesDaoNeo4j


class ProjectDependenciesDaoFactory:

    @classmethod
    def get_dao(cls, config):
        dao = None
        if config.db_class == DBTypes.Neo4j:
            dao = ProjectDependenciesDaoNeo4j(config)
        elif config.db_class == DBTypes.InMemory:
            dao = ProjectDependenciesDaoMemory(config)
        return dao
