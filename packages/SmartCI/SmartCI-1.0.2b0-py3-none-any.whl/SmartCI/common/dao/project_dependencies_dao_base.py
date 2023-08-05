from abc import ABC, abstractmethod
from typing import List

from SmartCI.planner.config import Config


class ProjectDependenciesDao(ABC):

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def create_file_node(self, module_name, file_path, file_type):
        pass

    @abstractmethod
    def connect_nodes(self, src_file_node, dest_file_node):
        pass

    @abstractmethod
    def get_node_by_file_path(self, file_paths: List[str]):
        pass

    @abstractmethod
    def get_test_dependencies(self, changed_file):
        pass

    @abstractmethod
    def extract_node_module_name(self, node):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    @abstractmethod
    def save(self):
        pass
