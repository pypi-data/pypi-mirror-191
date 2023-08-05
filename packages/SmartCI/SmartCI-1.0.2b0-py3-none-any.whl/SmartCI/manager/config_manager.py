import json
import os
from enum import Enum
from typing import Optional

from SmartCI import SMART_CI_PATH
from SmartCI.planner.config import Config


class ConfigKeys(Enum):
    DEFAULT_PROJECT = 'defaultProject'
    PROJECTS = 'projects'

class ProjectConfig(Enum):
    PROJECT_NAME = 'project_name'
    PROJECT_PATH = 'project_path'
    GIT_PATH = 'git_path'


class ConfigManager:

    def add_project(self, project_name: str, git_path: str, project_path: str):
        if not os.path.exists(SMART_CI_PATH):
            self._init_config_file(project_name)

        self._add_project(project_name, git_path, project_path)

    def change_default_project(self, new_default_project_name: str):
        config = self._load_config_file()

        config[ConfigKeys.DEFAULT_PROJECT.value] = new_default_project_name

        self._write_content_to_config_file(config)

    def load_project_config(self, project_name: Optional[str]) -> Config:
        config = self._load_config_file()
        if not project_name:
            project_name = config[ConfigKeys.DEFAULT_PROJECT.value]

        project = config[ConfigKeys.PROJECTS.value][project_name]
        return Config(project_name, project[ProjectConfig.GIT_PATH.value],
                      project[ProjectConfig.PROJECT_PATH.value])

    def _load_config_file(self):
        try:
            with open(f'{SMART_CI_PATH}/config', 'r') as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            config = {}
        return config

    def _init_config_file(self, project_name):
        os.mkdir(SMART_CI_PATH)
        config = {
            ConfigKeys.DEFAULT_PROJECT.value: project_name,
            ConfigKeys.PROJECTS.value: {}
        }
        self._write_content_to_config_file(config)

    def _add_project(self, project_name, git_path, project_path):
        config = self._load_config_file()

        project = {
            ProjectConfig.PROJECT_NAME.value: project_name,
            ProjectConfig.GIT_PATH.value: git_path,
            ProjectConfig.PROJECT_PATH.value: project_path,
        }
        if ConfigKeys.PROJECTS.value in config:
            config[ConfigKeys.PROJECTS.value][project_name] = project
        else:
            config[ConfigKeys.PROJECTS.value] = {
                project_name: project
            }

        self._write_content_to_config_file(config)

    def _write_content_to_config_file(self, config):
        with open(f'{SMART_CI_PATH}/config', 'w') as config_file:
            config_file.write(json.dumps(config))
