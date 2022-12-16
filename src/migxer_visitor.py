import ast

from dataclasses import dataclass
from typing import List, Optional


class MigxerVisitor(ast.NodeVisitor):
    def __init__(self, sourcefile_path: str):
        self.revision_value: Optional[str] = None
        self.revision_target_id: str = "revision"
        self.down_revision_value: Optional[str] = None
        self.down_revision_target_id: str = "down_revision"
        self._parse_file(sourcefile_path)

    def visit_Assign(self, node: ast.Assign) -> None:
        if node.targets[0].id == self.revision_target_id:
            self.revision_value = node.value.value
        if node.targets[0].id == self.down_revision_target_id:
            self.down_revision_value = node.value.value

    def _parse_file(self, sourcefile):
        with open(sourcefile, 'r') as migration_file:
            _raw_file = migration_file.read()
            _parsed = ast.parse(_raw_file)
            self.visit(_parsed)