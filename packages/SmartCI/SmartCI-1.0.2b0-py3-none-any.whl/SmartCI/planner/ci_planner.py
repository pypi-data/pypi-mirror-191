from typing import List

from SmartCI.planner.commit_extractor import CommitExtractor
from SmartCI.planner.config import Config
from SmartCI.planner.effected_files_extractor import EffectedFilesExtractor
from SmartCI.planner.tests_files_extractor import TestsFilesExtractor
from SmartCI.scanner.project_scanner import ProjectScanner
from SmartCI.planner.types.git_diff_level import GitDiffLevel


class CiPlanner:

    def plan(self, config: Config, effected_filed_only: bool) -> List[str]:
        project_scanner = ProjectScanner(config)
        commit_extractor = CommitExtractor(config)

        commit_changes = commit_extractor.get_files_from_commit(diff_level=GitDiffLevel.Branch)
        project_scanner.scan(commit_changes)
        files_changed = commit_extractor.extract_file_nodes_from_commit(commit_changes)
        if files_changed:
            if effected_filed_only:
                effected_files_extractor = EffectedFilesExtractor(config)
                effected_files = effected_files_extractor.extract(files_changed)
                return effected_files
            else:
                tests_file_extractor = TestsFilesExtractor(config)
                tests_files_to_run = tests_file_extractor.extract(files_changed)
                return tests_files_to_run
