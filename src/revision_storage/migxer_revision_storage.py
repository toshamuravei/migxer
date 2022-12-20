from datetime import datetime
from typing import List, Optional, Union

from .revision_item import RevisionItem


class ParentNotFoundException(Exception):
    pass


class FixIsImpossible(Exception):
    pass


class RevisionStorage(dict):
    def add(
        self, rev_item: Optional[RevisionItem] = None,
        revision: Optional[str] = None, down_revision: Optional[str] = None,
        revision_date: Optional[datetime] = None,
        original_filepath: Optional[str] = None
    ):
        if not rev_item:
            rev_item = RevisionItem(
                revision=revision,
                parent_revision=down_revision,
                revision_date=revision_date,
                original_filepath=original_filepath
            )
        self._add(rev_item)

    def _add(self, revision_item: RevisionItem):
        if len(self) == 0:
            self.root_revision = revision_item.revision
            self.__setitem__(revision_item.revision, revision_item)
            self.orphans = []
            return
        self.__setitem__(revision_item.revision, revision_item)
        self._update_parent(revision_item)
        self._check_orphans(revision_item)

    def _update_parent(self, revision_item: RevisionItem):
        parent = self.get(revision_item.parent_revision)
        if not parent:
            self.orphans.append(revision_item.revision)
        else:
            parent.children.append(revision_item.revision)

    def _check_orphans(self, new_parent: RevisionItem):
        _adopted_idxs = []
        for orphan_idx in range(0, len(self.orphans)):
            orphan = self.orphans[orphan_idx]
            orphan_item = self.get(orphan)
            if orphan_item.parent_revision == new_parent.revision:
                new_parent.children.append(orphan)
                _adopted_idxs.append(orphan_idx)

        for child_idx in _adopted_idxs:
            del self.orphans[child_idx]

    def get_conflict_place_str(self, multiparent: Optional[str] = None) -> str:
        if not multiparent:
            multiparent = self.find_first_multiparent()

        result_string = ""
        upper_child, lower_child = self[multiparent].children
        upper_child = str(self[upper_child])
        lower_child = str(self[lower_child])

        PREFIX_STR = "<...> - "
        UPPER_BRANCH_STR = " / "
        LOWER_BRANCH_STR = " \ " # noqa
        NEWLINE = "\n"
        SPACE = " "

        upper_row = SPACE * (
            len(PREFIX_STR) + len(UPPER_BRANCH_STR) + len(multiparent)
        )
        upper_row += upper_child
        result_string += (upper_row + NEWLINE)

        upper_delimiter_row = SPACE * (len(PREFIX_STR) + len(multiparent))
        upper_delimiter_row += UPPER_BRANCH_STR
        result_string += (upper_delimiter_row + NEWLINE)

        center_row = PREFIX_STR + multiparent
        result_string += (center_row + NEWLINE)

        lower_delimiter_row = SPACE * (len(PREFIX_STR) + len(multiparent))
        lower_delimiter_row += LOWER_BRANCH_STR
        result_string += (lower_delimiter_row + NEWLINE)

        lower_row = SPACE * (
            len(PREFIX_STR) + len(LOWER_BRANCH_STR) + len(multiparent)
        )
        lower_row += lower_child
        result_string += (lower_row + NEWLINE)

        return result_string

    def find_first_multiparent(self) -> Union[str, None]:
        current_revision = self.root_revision
        while current_revision:
            item = self[current_revision]
            children_len = len(item.children)
            if children_len == 0:
                return

            if children_len > 1:
                return current_revision

            current_revision = item.children[0]

    FixWasMaden = bool

    def fix_revision_conflict(
        self, multiparent: Optional[str] = None
    ) -> FixWasMaden:
        # TODO: actualy, infinite children from multiparent can be fixed
        # in such (date comparison) manner and all we need to do this - sort'em
        # and sequentially add this branches to eachother. Same as here, but
        # with sorting. This would be much more nice & abstract way of
        # datetime-based fixing.

        multiparent = multiparent or self.find_first_multiparent()
        if not multiparent:
            return False

        left_child, right_child = self[multiparent].children
        elder_child, younger_child = None, None
        multiparent = self[multiparent]

        if left_child == right_child:
            raise FixIsImpossible()

        if left_child > right_child:
            elder_child, younger_child = right_child, left_child
            del multiparent.children[0]
        else:
            elder_child, younger_child = left_child, right_child
            del multiparent.children[1]

        elder_child, younger_child = self[elder_child], self[younger_child]
        self.revision_to_rewrite = younger_child

        last_descendant_of_elder_child = self._get_last_descendant(
            elder_child.revision
        )
        younger_child.parent_revision = last_descendant_of_elder_child.revision
        last_descendant_of_elder_child.children.append(younger_child.revision)
        return True

    def _get_last_descendant(self, ancestor: str) -> RevisionItem:
        current = self[ancestor]
        while current.children:
            current = self[current.children[0]]
        return current

    def get_revisions_line(self) -> List[str]:
        revisions = [self.root_revision, ]
        current = self[self.root_revision]
        while current.children:
            current = self[current.children[0]]
            revisions.append(current.revision)
        return revisions

    def wtite_fix_to_file(self):
        revision_to_rewrite: Optional[RevisionItem] = getattr(
            self, "revision_to_rewrite"
        )
        if not revision_to_rewrite:
            return

        revision_to_rewrite.serialize_to_revision_file()
