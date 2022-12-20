import ast

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from src.transformer import AssignmentsTransformer


@dataclass
class RevisionItem:
    revision: str
    original_filepath: str
    parent_revision: Optional[str] = None
    revision_date: Optional[datetime] = None
    children: Optional[List[str]] = field(default_factory=list)

    def __str__(self) -> str:
        if self.revision_date:
            date = self.revision_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            date = "date is unknown"
        return f"{self.revision} ({date})"

    @property
    def last_descendant(self) -> 'RevisionItem':
        raise NotImplementedError()

    @property
    def assignments_ids_values_map(self) -> Dict[str, str]:
        return {
            "revision": self.revision,
            "down_revision": self.parent_revision
        }

    def __eq__(self, other):
        if not hasattr(other, "revision_date"):
            return NotImplemented
        return self.revision_date == other.revision_date

    def __lt__(self, other):
        if not hasattr(other, "revision_date"):
            return NotImplemented
        return self.revision_date < other.revision_date

    def serialize_to_revision_file(
        self, transformer: ast.NodeTransformer = AssignmentsTransformer
    ) -> str:
        parsed_tree = None
        transformer = AssignmentsTransformer(self.assignments_ids_values_map)
        with open(self.original_filepath, 'r') as revision_file:
            raw_file = revision_file.read()
            parsed_tree = ast.parse(raw_file)
        new_tree = transformer.visit(parsed_tree)
        new_source_string = ast.unparse(new_tree)

        with open(self.original_filepath, 'w') as revision_file:
            revision_file.write(new_source_string)

        return self.original_filepath
