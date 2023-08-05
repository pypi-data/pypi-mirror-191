import gitlab
from pygit2 import Repository


class GitLabAccessor:
    def __init__(self, config):
        gl = gitlab.Gitlab(config['GITLAB_ACCOUNT_ADDRESS'])
        self.project = gl.projects.get(config['PROJECT_ID'])
        self.repo = Repository(config['PROJECT_REPO_PATH'])
        self._current_branch_name = None

    @property
    def current_branch_name(self):
        if self._current_branch_name:
            return self._current_branch_name
        self._current_branch_name = self.repo.head.name
        return self._current_branch_name

    def get_commits(self):
        commits = self.project.commits.list(ref_name=self._current_branch_name)
        return commits

    def get_last_commit_differences(self):
        last_commit = self.get_commits()[-1]
        return last_commit.diff()