from SmartCI.common.database.enums.db_types import DBTypes


class Config:
    def __init__(self, project_name: str, git_project_path: str, project_path: str,
                 db_class: DBTypes = DBTypes.InMemory, source_development_branch: str = 'develop'):
        self.project_name = project_name
        self.db_class = db_class
        self.project_path = project_path
        self.git_project_path = git_project_path
        self.source_development_branch = source_development_branch
