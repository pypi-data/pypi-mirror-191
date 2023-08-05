from SmartCI.scanner.accessors.pydeps_accessor import PydepsAccessor
from SmartCI.scanner.dependencies_parser import DependenciesParser
from common.database.enums.db_types import DBTypes
from planner.config import Config

if __name__ == '__main__':
    config = Config('Archiver', '/Users/yoavalroy/src/archiver', '/Users/yoavalroy/src/archiver/archiving', DBTypes.Neo4j)
    parser = DependenciesParser(config)
    parser.parse(dependencies)