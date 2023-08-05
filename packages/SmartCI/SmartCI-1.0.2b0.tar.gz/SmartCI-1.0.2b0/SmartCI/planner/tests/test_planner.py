from SmartCI.common.database.enums.db_types import DBTypes
from SmartCI.planner.ci_planner import CiPlanner
from SmartCI.planner.config import Config

if __name__ == '__main__':
    config = Config('Archiver', '/Users/yoavalroy/src/archiver', '/Users/yoavalroy/src/archiver/archiving', DBTypes.Neo4j)
    ci_planner = CiPlanner()
    tests_files_to_run = ci_planner.plan(config, effected_filed_only=True)
    print(tests_files_to_run)