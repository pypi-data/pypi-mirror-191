import json
import os
from copy import deepcopy
from typing import List

from singleton_decorator import singleton

from SmartCI import SMART_CI_PATH
from SmartCI.common.dao.project_dependencies_dao_base import ProjectDependenciesDao
from SmartCI.common.database.enums.file_types import FileTypes
from SmartCI.planner.config import Config


@singleton
class ProjectDependenciesDaoMemory(ProjectDependenciesDao):
    graph = {}

    def __init__(self, config: Config):
        super().__init__(config)
        self.project_dependencies_file = os.path.join(SMART_CI_PATH, config.project_name)
        try:
            if not self.is_empty():
                with open(self.project_dependencies_file, 'r') as project_graph_file:
                    raw_project_graph = project_graph_file.readline()
                    self.graph = json.loads(raw_project_graph)
        except Exception as e:
            print(f'Failed to load graph file with error {e}, scanning from scratch')

    def create_file_node(self, module_name, file_path, file_type):
        node = {
            'module_name': module_name,
            'file_path': file_path,
            'file_type': file_type,
            'imported_by': []
        }
        self.graph[file_path] = node
        return node

    def connect_nodes(self, src_file_node, dest_file_node):
        dest_file_node['imported_by'].append(deepcopy(src_file_node))

    def get_node_by_file_path(self, file_paths: List[str]):
        nodes = []
        for file_path in file_paths:
            if file_path in self.graph:
                nodes.append(self.graph[file_path])

        return nodes

    def get_test_dependencies(self, changed_file):
        test_files = []
        nodes_to_scan = [changed_file]
        while nodes_to_scan:
            node = nodes_to_scan.pop()
            if self._file_is_test(node['file_path']):
                test_files.append(node)
                continue

            for other_node in node['imported_by']:
                if other_node['file_type'] == FileTypes.Test.value:
                    print(f'Found node! {other_node["module_name"]}')
                    test_files.append(other_node)
                nodes_to_scan.extend(other_node['imported_by'])
        return test_files

    def extract_node_module_name(self, node):
        return node['module_name']

    def is_empty(self):
        return not os.path.exists(self.project_dependencies_file)

    def save(self):
        with open(self.project_dependencies_file, 'w') as project_graph_file:
            project_graph_file.write(json.dumps(self.graph))

    def _file_is_test(self, file_path):
        file_path_parts = file_path.split('/')
        return 'test_' in file_path_parts[-1]
