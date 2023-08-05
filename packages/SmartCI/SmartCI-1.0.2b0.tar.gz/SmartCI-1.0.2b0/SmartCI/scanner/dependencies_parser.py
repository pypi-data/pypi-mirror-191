import logging
from typing import Dict, List


from SmartCI.common.dao.project_dependencies_dao_factory import ProjectDependenciesDaoFactory
from SmartCI.common.database.enums.file_types import FileTypes
from SmartCI.common.database.neo4j.dao import FileNode
from SmartCI.planner.types.moved_file import MovedFile
from SmartCI.planner.config import Config

logger = logging.getLogger('SmartCI')


class DependenciesParser:
    _PYTHON_MODULE_STRING = '__'
    _LOGGER_PREFIX = 'dependencies_parser'

    def __init__(self, config: Config):
        self._seen_third_party_modules = set()
        self._project_dependencies_dao = ProjectDependenciesDaoFactory.get_dao(config)

    def update_graph(self, moved_files: List[MovedFile]):
        old_paths = [moved_file.old_name for moved_file in moved_files]
        nodes_to_modify = self._project_dependencies_dao.get_node_by_file_path(old_paths)
        for node_to_modify in nodes_to_modify:
            node_to_modify.delete()

    # @db.transaction
    def parse(self, dependencies: dict) -> None:
        if dependencies:
            nodes = self._create_nodes(dependencies)
            self._create_relationships(dependencies, nodes)
            self._project_dependencies_dao.save()

    def _create_nodes(self, dependencies) -> Dict[str, FileNode]:
        nodes = {}
        for module_name, module_value in dependencies.items():
            if self._is_module_belongs_to_python(module_name):
                continue
            if self._is_module_third_party(module_name, module_value):
                continue

            file_type = self._get_file_type(module_name, module_value['path'])
            logger.info(f'{self._LOGGER_PREFIX}: got module name {module_name} creating node from file type {file_type}')

            try:
                file_node = self._project_dependencies_dao.create_file_node(
                    module_name=module_name,
                    file_path=module_value['path'],
                    file_type=file_type
                )
                nodes[module_name] = file_node
            except Exception as e:
                print(f'failed to save node {e}')

        return nodes

    def _is_module_belongs_to_python(self, module_name):
        return (module_name.startswith(self._PYTHON_MODULE_STRING) and module_name.endswith(self._PYTHON_MODULE_STRING))

    def _is_module_third_party(self, module_name, module_value):
        if module_name in self._seen_third_party_modules:
            return True
        elif module_value and module_value.get('path') and 'site-packages' in module_value.get('path'):
            self._seen_third_party_modules.add(module_name)
            return True
        return False

    def _get_file_type(self, module_name, file_path):
        if file_path and '__init__' in file_path:
            return FileTypes.INIT.value
        if 'test' in module_name:
            return FileTypes.Test.value
        return FileTypes.Code.value

    def _create_relationships(self, dependencies, nodes):
        for src_module_name, module_value in dependencies.items():
            if self._is_module_belongs_to_python(src_module_name):
                continue
            if self._is_module_third_party(src_module_name, module_value):
                continue

            src_file_node = nodes.get(src_module_name)
            for dest_module_name in module_value.get('imports', []):
                try:
                    if dest_module_name in self._seen_third_party_modules or src_module_name == dest_module_name:
                        continue
                    logger.info(f'{self._LOGGER_PREFIX}: Connecting modules {src_module_name} and {dest_module_name}')
                    dest_file_node = nodes[dest_module_name]
                    if src_file_node:
                        self._project_dependencies_dao.connect_nodes(src_file_node, dest_file_node)
                except Exception as e:
                    logger.exception(f'{self._LOGGER_PREFIX}: {e}')

