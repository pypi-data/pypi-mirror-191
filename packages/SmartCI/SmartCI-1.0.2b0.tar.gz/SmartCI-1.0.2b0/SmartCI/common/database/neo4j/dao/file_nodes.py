from dataclasses import dataclass

from common.database.enums.file_types import FileTypes
from common.database.neo4j.dao.base_node import BaseNode


@dataclass
class FileNode(BaseNode):
    module_name: str
    file_path: str
    imports: dict

    def __eq__(self, other):
        return self.module_name == other.module_name

    def __hash__(self):
        return hash(self.module_name)


@dataclass
class InitFileNode(FileNode):
    file_type = FileTypes.INIT

    def __hash__(self):
        return hash(self.module_name)


@dataclass
class CodeFileNode(FileNode):
    file_type = FileTypes.Code

    def __hash__(self):
        return hash(self.module_name)


@dataclass
class TestFileNode(FileNode):
    file_type = FileTypes.Test

    def __hash__(self):
        return hash(self.module_name)


class FileNodeFactory:

    @classmethod
    def create_node(cls, file_node_values) -> FileNode:
        input_type = list(file_node_values.labels)[0].replace('FileNode', '').lower()
        if input_type == FileTypes.Code.value:
            return CodeFileNode(
                file_node_values.id,
                file_node_values.get('module_name'),
                file_node_values.get('file_path'),
                file_node_values.get('imports', {})
            )
        elif input_type == FileTypes.Test.value:
            return TestFileNode(
                file_node_values.id,
                file_node_values.get('module_name'),
                file_node_values.get('file_path'),
                file_node_values.get('imports', {})
            )
        elif input_type == FileTypes.INIT.value:
            return InitFileNode(
                file_node_values.id,
                file_node_values.get('module_name'),
                file_node_values.get('file_path'),
                file_node_values.get('imports', {})
            )
