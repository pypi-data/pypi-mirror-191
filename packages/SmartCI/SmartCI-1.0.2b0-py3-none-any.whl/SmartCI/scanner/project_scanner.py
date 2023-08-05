import os

from SmartCI.common.dao.project_dependencies_dao_factory import ProjectDependenciesDaoFactory
from SmartCI.planner.config import Config
from SmartCI.planner.types.commit_changes import CommitChanges
from SmartCI.scanner.accessors.pydeps_accessor import PydepsAccessor
from SmartCI.scanner.dependencies_parser import DependenciesParser


class ProjectScanner:

    def __init__(self, config: Config):
        self.parser = DependenciesParser(config)
        self.project_path = config.project_path
        self._project_dependencies_dao = ProjectDependenciesDaoFactory.get_dao(config)

    def scan(self, commit_changes: CommitChanges):
        self._update_projects(commit_changes)
        self._scan_projects(commit_changes)

    def _scan_projects(self, commit_changes):
        if self._should_scan_project():
            self._full_project_scan()
        else:
            self._relative_project_scan(commit_changes)

    def _full_project_scan(self):
        for file_descriptor in os.listdir(self.project_path):
            if self._should_skip_dir(file_descriptor):
                continue
            self._scan_directory(file_descriptor)

    def _relative_project_scan(self, commit_changes):
        paths_to_scan = self._get_paths_from_commit_to_scan(commit_changes)
        for file_descriptor in paths_to_scan:
            self._scan_directory(file_descriptor)

    def _scan_directory(self, file_descriptor):
        dependencies = PydepsAccessor.create_dependencies_graph(self.project_path, file_descriptor)
        self.parser.parse(dependencies)

    def _should_scan_project(self):
        return self._project_dependencies_dao.is_empty()

    def _update_projects(self, commit_changes: CommitChanges):
        self.parser.update_graph(commit_changes.moved_files)

    def _should_skip_dir(self, file_descriptor):
        if file_descriptor.startswith('__') or file_descriptor.startswith('tmp') or file_descriptor.startswith('.'):
            return True
        return False

    def _get_paths_from_commit_to_scan(self, commit_changes):
        paths_to_scan = []
        paths_to_scan.extend(self._get_paths(commit_changes.new_files))
        paths_to_scan.extend(self._get_paths(commit_changes.modified_files))
        return list(set(paths_to_scan))

    def _get_paths(self, files):
        paths = set()
        for file in files:
            path = '/'.join(file.replace(self.project_path + '/', '').split('/')[:-1])
            paths.add(path)
        return list(paths)
