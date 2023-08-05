import os
import subprocess
from typing import List

from pygit2 import Repository, GIT_SORT_TIME, Commit
from unidiff import PatchSet

from SmartCI.planner.types.git_diff_level import GitDiffLevel


class GitAccessor:
    def __init__(self, project_root_path, source_branch):
        self.source_branch = source_branch
        self.project_root_path = project_root_path
        self._repo = Repository(project_root_path)
        self._current_branch_name = None

    @property
    def current_branch_name(self):
        if self._current_branch_name:
            return self._current_branch_name
        self._current_branch_name = self._repo.head.name
        return self._current_branch_name

    def get_commits(self) -> List[Commit]:
        commits = []
        commits_itr = self._repo.walk(self._repo.head.target, GIT_SORT_TIME)
        for commit in commits_itr:
            commits.append(commit)
            break
        return commits

    def get_last_commit_differences(self, diff_level, commit_id=None) -> PatchSet:
        curr_dir = os.getcwd()
        os.chdir(self.project_root_path)
        if diff_level == GitDiffLevel.Commit:
            last_commit = self.get_commits()[0]
            if commit_id:
                cmd = f'git diff {commit_id} {last_commit.id}'
            else:
                cmd = f'git diff {last_commit.id}'
        else:
            cmd = f'git diff {self.current_branch_name}..{self.source_branch}'
        result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
        raw_patch = result.stdout.decode('utf-8')
        patch_set = PatchSet.from_string(raw_patch)
        os.chdir(curr_dir)
        return patch_set
