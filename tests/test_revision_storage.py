import pytest

from src.revision_storage import RevisionItem, RevisionStorage


@pytest.fixture
def r_item_root():
    return {"revision": "root", "original_filepath": "some/root"}

@pytest.fixture
def r_item_A():
    return {"revision": "A", "down_revision": "root", "original_filepath": "some/root"}

@pytest.fixture
def r_item_B():
    return {"revision": "B", "down_revision": "A", "original_filepath": "some/root"}

@pytest.fixture
def r_item_C():
    return {"revision": "C", "down_revision": "A", "original_filepath": "some/root"}

@pytest.fixture
def r_item_D():
    return {"revision": "D", "down_revision": "B", "original_filepath": "some/root"}


class TestRevisionStorage:
    def test_root_adding(self, r_item_root):
        storage = RevisionStorage()
        storage.add(**r_item_root)

        assert storage.root_revision == r_item_root["revision"]
        assert storage.orphans == []
        assert storage.get(r_item_root["revision"]).revision == r_item_root["revision"]

    def test_ordered_adding(self, r_item_root, r_item_A):
        storage = RevisionStorage()
        storage.add(**r_item_root)
        storage.add(**r_item_A)

        assert storage.get(r_item_A["revision"]).revision == r_item_A["revision"]
        assert storage.get(r_item_root["revision"]).children == [r_item_A["revision"]]
        assert storage.orphans == []

    def test_multiple_children_adding(self, r_item_root, r_item_A, r_item_B, r_item_C):
        storage = RevisionStorage()
        storage.add(**r_item_root)
        storage.add(**r_item_A)
        storage.add(**r_item_B)
        storage.add(**r_item_C)

        assert storage.get(r_item_A["revision"]).children == [r_item_B["revision"], r_item_C["revision"]]

    def test_unordered_adding(self, r_item_root, r_item_A, r_item_B, r_item_D):
        storage = RevisionStorage()
        storage.add(**r_item_root)
        storage.add(**r_item_D)

        assert storage.get(r_item_D["revision"]).revision == r_item_D["revision"]
        assert storage.orphans == [r_item_D["revision"],]

        storage.add(**r_item_B)

        assert storage.orphans == [r_item_B["revision"],]

        storage.add(**r_item_A)

        assert storage.orphans == []

    def test_find_first_multiparent(self, r_item_root, r_item_A, r_item_B, r_item_C):
        storage = RevisionStorage()
        storage.add(**r_item_root)
        storage.add(**r_item_A)
        storage.add(**r_item_B)
        storage.add(**r_item_C)

        assert storage._find_first_multiparent() == r_item_A["revision"]
