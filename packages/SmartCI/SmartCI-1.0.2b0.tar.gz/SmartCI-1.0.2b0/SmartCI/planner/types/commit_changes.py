from typing import List

from SmartCI.planner.types.moved_file import MovedFile


class CommitChanges:

    def __init__(self,
                 modified_file: List[str],
                 new_files: List[str],
                 moved_files: List[MovedFile]):
        self.moved_files = moved_files
        self.new_files = new_files
        self.modified_files = modified_file

    def get_file_paths(self):
        return self.modified_files + self.new_files + [moved_file.new_name for moved_file in self.moved_files]
