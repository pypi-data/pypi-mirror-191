from typing import List

from SmartCI.common.dao.project_dependencies_dao_factory import ProjectDependenciesDaoFactory


class TestsFilesExtractor:

    def __init__(self, config):
        self._project_dependencies_dao = ProjectDependenciesDaoFactory.get_dao(config)

    def extract(self, changed_files) -> List[str]:
        test_files = set()
        for changed_file in changed_files:
            self._project_dependencies_dao.get_test_dependencies(changed_file)
            nodes_test_files_to_run = self._project_dependencies_dao.get_test_dependencies(changed_file)
            test_files.update([self._project_dependencies_dao.extract_node_module_name(node) for node in nodes_test_files_to_run])

        return list(test_files)
