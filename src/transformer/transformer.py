import ast
from typing import Dict, FrozenSet


class AssignmentsTransformer(ast.NodeTransformer):
    def __init__(self, assignments_ids_values_map: Dict[str, str]):
        self.assignments_ids_values_map: Dict[str, str] = assignments_ids_values_map
        self.assignments_ids: FrozenSet = frozenset(assignments_ids_values_map)

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if node.targets[0].id in self.assignments_ids:
            node.value.value = self.assignments_ids_values_map[node.targets[0].id]
        return node
