from typing import List, Set

from neo4j import GraphDatabase
from singleton_decorator import singleton

from SmartCI.common.dao.project_dependencies_dao_base import ProjectDependenciesDao
from SmartCI.common.database.neo4j.dao import FileNode, FileNodeFactory
from planner.config import Config


@singleton
class ProjectDependenciesDaoNeo4j(ProjectDependenciesDao):

    def __init__(self, config: Config):
        super().__init__(config)
        self._driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "ownbackup123"))

    def close(self):
        self.driver.close()

    def create_file_node(self, module_name: str, file_path: str, file_type: str) -> FileNode:
        with self._driver.session() as session:
            file_node = session.execute_write(self._find_node_by_file_path, file_path)

            if not file_node:
                file_node = session.execute_write(self._create_file_node, file_path, file_type, module_name)
            file_node_values = file_node.values()[0]
            return FileNodeFactory.create_node(file_node_values)

    @staticmethod
    def _create_file_node(tx, file_path, file_type, module_name):
        query = (f"CREATE (fn:{file_type.capitalize()}FileNode "
                 "{ file_path: $file_path, module_name: $module_name }) "
                 "RETURN fn")
        result = tx.run(query, file_path=file_path, module_name=module_name)
        return result.single()

    def connect_nodes(self, src_file_node: FileNode, dest_file_node: FileNode):
        with self._driver.session() as session:
            session.execute_write(self._connect_nodes, src_file_node.uid, dest_file_node.uid)

    @staticmethod
    def _connect_nodes(tx, src_file_node_id, dest_file_node_id):
        query = ("MATCH (src_fn), (dest_fn) WHERE id(src_fn) = $src_file_node_id AND id(dest_fn) = $dest_file_node_id"
                 " CREATE (src_fn)-[:IMPORTS]->(dest_fn)")
        tx.run(query, src_file_node_id=src_file_node_id, dest_file_node_id=dest_file_node_id)

    def find_node_by_file_path(self, file_path):
        with self._driver.session() as session:
            file_node = session.execute_write(self._find_node_by_file_path, file_path)
            file_node_values = file_node.values()[0]
            return FileNodeFactory.create_node(file_node_values)

    @staticmethod
    def _find_node_by_file_path(tx, file_path):
        try:
            query = "MATCH (fn) WHERE fn.file_path = $file_path RETURN fn"
            result = tx.run(query, file_path=file_path)
            return result.single()
        except Exception:
            pass

    def get_node_by_file_path(self, file_paths: List[str]) -> List[FileNode]:
        with self._driver.session() as session:
            file_nodes = session.execute_write(self._get_node_by_file_path, file_paths)
            file_nodes_entities = []
            for file_node in file_nodes:
                file_node_values = file_node.values()[0]
                file_nodes_entities.append(
                    FileNodeFactory.create_node(file_node_values)
                )
            return file_nodes_entities

    @staticmethod
    def _get_node_by_file_path(tx, file_paths):
        try:
            query = "MATCH (fn) WHERE fn.file_path IN $file_paths RETURN fn"
            results = tx.run(query, file_paths=file_paths)
            return [result for result in results]
        except Exception as e:
            return []

    def get_test_dependencies(self, changed_file: FileNode) -> Set[FileNode]:
        with self._driver.session() as session:
            file_nodes = session.execute_write(self._get_test_dependencies, changed_file.module_name)
            file_nodes_entities = set()
            for file_node in file_nodes:
                file_node_values = file_node.values()[0]
                file_nodes_entities.add(FileNodeFactory.create_node(file_node_values))
            return file_nodes_entities

    @staticmethod
    def _get_test_dependencies(tx, module_name):
        query = "MATCH (fn: CodeFileNode {module_name: $module_name}) MATCH (fn)<-[*1..4]-(b:TestFileNode) RETURN b"
        results = tx.run(query, module_name=module_name)
        return [result for result in results]

    def get_effected_dependencies(self, changed_file: FileNode) -> Set[FileNode]:
        with self._driver.session() as session:
            file_nodes = session.execute_write(self._get_effected_dependencies, changed_file.uid)
            file_nodes_entities = set()
            for file_node in file_nodes:
                file_node_values = file_node.values()
                file_nodes_entities.add(FileNodeFactory.create_node(file_node_values))
            return file_nodes_entities

    @staticmethod
    def _get_effected_dependencies(tx, changed_file_id):
        query = "MATCH (a) WHERE id(a)=$file_node_id MATCH (a)<-[*1..4]-(b:CodeFileNode) RETURN b"
        results = tx.run(query, file_node_id=changed_file_id)
        return [result for result in results]

    def extract_node_module_name(self, node: FileNode) -> str:
        return node.module_name

    def is_empty(self):
        with self._driver.session() as session:
            return not bool(session.execute_write(self._is_empty))

    @staticmethod
    def _is_empty(tx):
        query = "MATCH (fn) RETURN fn"
        results = tx.run(query)
        return results.single()

    def save(self):
        pass
