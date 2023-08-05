import os
from typing import List, Tuple

from unidiff import PatchSet

from SmartCI.common.dao.project_dependencies_dao_factory import ProjectDependenciesDaoFactory
from SmartCI.common.git_providers.git_accessor import GitAccessor
from SmartCI.planner.types.commit_changes import CommitChanges
from SmartCI.planner.types.moved_file import MovedFile
from SmartCI.planner.config import Config
from SmartCI.planner.types.git_diff_level import GitDiffLevel


class CommitExtractor:
    def __init__(self, config: Config):
        self.project_root_path = config.git_project_path
        self.project_relative_path = config.project_path.replace(self.project_root_path + '/', '') + '/'
        self.git_accessor = GitAccessor(self.project_root_path, source_branch=config.source_development_branch)
        self._project_dependencies_dao = ProjectDependenciesDaoFactory.get_dao(config)

    def get_files_from_commit(self, diff_level=GitDiffLevel.Commit) -> CommitChanges:
        differences = self.git_accessor.get_last_commit_differences(diff_level)
        new_files = self._get_new_files_from_differences(differences)
        modified_files, moved_files = self._get_modified_files_from_differences(differences)
        commit_changes = CommitChanges(new_files=new_files, modified_file=modified_files, moved_files=moved_files)
        return commit_changes

    def extract_file_nodes_from_commit(self, commit_changes: CommitChanges):
        return self._project_dependencies_dao.get_node_by_file_path(commit_changes.get_file_paths())

    def _get_new_files_from_differences(self, differences: PatchSet) -> List[str]:
        added_files_path = []
        for add_file in differences.added_files:
            if self.project_relative_path not in add_file.path:
                print(f'changed file not as part of the project path: {add_file.path} skipping')
                continue
            if '__pycache__' not in add_file.path:
                added_files_path.append(os.path.join(self.project_root_path, add_file.path))

        return added_files_path

    def _get_modified_files_from_differences(self, differences: PatchSet) -> Tuple[List[str], List[MovedFile]]:
        modified_files_path = []
        moved_files = []
        for modified_file in differences.modified_files:
            # if self.project_relative_path not in modified_file.path:
            #     print(f'changed file not as part of the project path: {modified_file.path} skipping')
            #     continue
            if '__pycache__' not in modified_file.path:
                target_file = os.path.join(self.project_root_path, modified_file.path)
                normalized_source_path = modified_file.source_file.replace('a/', '')
                normalized_target_path = modified_file.target_file.replace('b/', '')
                if normalized_source_path == normalized_target_path:
                    modified_files_path.append(target_file)
                else:
                    full_normalized_source_path = os.path.join(self.project_root_path, normalized_source_path)
                    full_normalized_target_path = os.path.join(self.project_root_path, normalized_target_path)
                    moved_files.append(MovedFile(full_normalized_source_path, full_normalized_target_path))
        return modified_files_path, moved_files
