from typing import List


from SmartCI.common.dao.project_dependencies_dao_factory import ProjectDependenciesDaoFactory


class EffectedFilesExtractor:

    def __init__(self, config):
        self._project_dependencies_dao = ProjectDependenciesDaoFactory.get_dao(config)

    def extract(self, changed_files) -> List[str]:
        effected_files = set()
        for changed_file in changed_files:
            effected_nodes = self._project_dependencies_dao.get_test_dependencies(changed_file)
            effected_files.update([self._project_dependencies_dao.extract_node_module_name(node) for node in effected_nodes])

        return list(effected_files)
