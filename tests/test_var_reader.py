import ast
import astpretty

from typing import Any, Optional


FILEPATH = "/Users/shabalkov/Projects/migxer/tests/test_script.py"

MIGRATION_FILEPATH = "/Users/shabalkov/Projects/migxer/tests/test_migration.py"

def read_source_file(filename):
    data = ''
    with open(filename, 'r') as source_file:
        data = source_file.read()
    return data


def get_ast(code):
    astpretty.pprint(ast.parse(code), show_offsets=False, indent=2)


class MigxerVisitor(ast.NodeVisitor):
    def __init__(self):
        self.revision_id: Optional[str] = None
        self.revision_constant_name = "revision"

    def visit_Assign(self, node: ast.Assign) -> Any:
        if node.targets[0].id == self.revision_constant_name:
            self.revision_id = node.value.value

if __name__ == "__main__":
    visitor = MigxerVisitor()
    code = read_source_file(MIGRATION_FILEPATH)
    code_parsed = ast.parse(code)
    visitor.visit(code_parsed)
    print(visitor.revision_id)
    #get_ast(code)

