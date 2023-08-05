from enum import Enum
from pathlib import Path
from typing import List

from SmartCI.manager import ConfigManager
from SmartCI.planner.ci_planner import CiPlanner


class CliManager:
    HOME = '~'

    def __init__(self):
        self.config_manager = ConfigManager()

    def run(self, command: str, argv: List[str]):
        if command not in AvailableCommands.to_list():
            command = AvailableCommands.HELP.value

        if command == AvailableCommands.HELP.value:
            self._print_help_menu()
        elif command == AvailableCommands.INIT.value:
            self._add_project()
        elif command == AvailableCommands.CHANGE_DEFAULT.value:
            self._change_default_project()
        elif command == AvailableCommands.RUN_TEST.value:
            self._run_test(argv)
        elif command == AvailableCommands.RUN_CHANGES.value:
            self._run_changes(argv)

    def _print_help_menu(self):
        print(f'Available Commands: ')
        print(f'1. init - Connect SmartCI with a project')
        print(f'2. run-changes - On a initiated project get the test files you need to run per your last commit changes')
        print(f'3. run-test - On a initiated project get the test files you need to run per your last commit changes')
        print(f'4. changeDefault - Change default project')
        print(f'5. help - List available commands')

    def _add_project(self):
        project_name = input('Enter Project Name: ')
        git_path = input('Enter Git Path: ')
        project_path = input('Enter Project Path (leave empty for using the same path as Git Path): ')
        git_path = self._normalize_path(git_path)
        if project_path:
            project_path = self._normalize_path(project_path)
        else:
            project_path = git_path

        self._add_to_config_file(project_name, git_path, project_path)
        self._run_planner(project_name)

    def _normalize_path(self, path):
        if '~' in path:
            path = path.replace(self.HOME, str(Path.home()))
        return path

    def _add_to_config_file(self, project_name, git_path, project_path):
        self.config_manager.add_project(project_name, git_path, project_path)

    def _change_default_project(self):
        project_name = input('Enter Project Name: ')
        self.config_manager.change_default_project(project_name)

    def _run_test(self, argv):
        project_name = None
        if argv:
            project_name = argv[0]
        self._run_planner(project_name)

    def _run_changes(self, argv):
        project_name = None
        if argv:
            project_name = argv[0]
        self._run_planner(project_name, effected_filed_only=True)

    def _run_planner(self, project_name, effected_filed_only=False):
        config = self.config_manager.load_project_config(project_name)
        print(f'Running on Project: {config.project_name}')
        ci_planner = CiPlanner()
        tests_files_to_run = ci_planner.plan(config, effected_filed_only=effected_filed_only)
        print(tests_files_to_run)


class AvailableCommands(Enum):
    HELP = 'help'
    INIT = 'init'
    RUN_TEST = 'run-test'
    RUN_CHANGES = 'run-changes'
    CHANGE_DEFAULT = 'changeDefault'

    @classmethod
    def to_list(cls):
        return [cls.HELP.value,
                cls.INIT.value,
                cls.RUN_TEST.value,
                cls.RUN_CHANGES.value,
                cls.CHANGE_DEFAULT.value]