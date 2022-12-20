import ast
import os

from typing import List, Optional

import pytest


class SimpleTransformer(ast.NodeTransformer):
    def __init__(self, assignment_id: Optional[str] = None, assignmen_value: Optional[int] = None):
        self.assignment_id: str = assignment_id or "SOME_CONSTANT"
        self.assignment_value_to_replace: int = assignmen_value or 999

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        if node.targets[0].id == self.assignment_id:
            node.value.value = self.assignment_value_to_replace
        return node


class SimpleVisitor(ast.NodeVisitor):
    def __init__(self):
        self.assignment_id_to_read: str = "SOME_CONSTANT"
        self.assignment_value: Optional[int] = None

    def visit_Assign(self, node: ast.Assign) -> None:
        if node.targets[0].id == self.assignment_id_to_read:
            self.assignment_value = node.value.value


class TestClassWithASTFixture():
    @pytest.fixture
    def example_script_parsed_as_ast(self) -> ast.AST:
        filepath = "tests/example_script.py"
        _parsed = None
        with open(filepath, 'r') as example_file:
            _raw_file = example_file.read()
            _parsed = ast.parse(_raw_file)
        return _parsed


class TestTransofrmation(TestClassWithASTFixture):
    def test_transformation(self, example_script_parsed_as_ast):
        transformer = SimpleTransformer()
        new_tree = transformer.visit(example_script_parsed_as_ast)

        visitor = SimpleVisitor()
        visitor.visit(new_tree)
        
        assert visitor.assignment_value == transformer.assignment_value_to_replace


class TestUnparse(TestClassWithASTFixture):
    def test_unparse(self, example_script_parsed_as_ast):
        temp_file = "tests/example_script_changed.py"
        try:
            with open(temp_file, 'w') as tmp:
                transformer = SimpleTransformer()
                new_tree = transformer.visit(example_script_parsed_as_ast)
                new_source_string = ast.unparse(new_tree)
                tmp.write(new_source_string)
                
            with open(temp_file, 'r') as tmp:
                new_source_string_reread = tmp.read()
                new_source_parsed = ast.parse(new_source_string_reread)
                visitor = SimpleVisitor()
                visitor.visit(new_source_parsed)

                assert visitor.assignment_value == transformer.assignment_value_to_replace
        finally:
            os.remove(temp_file)
