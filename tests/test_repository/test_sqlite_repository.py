from bookkeeper.bookkeeper.repository.sqlite_repository import SQLiteRepository

import pytest


@pytest.fixture
def custom_class():
    class Custom():
        pk: int = 0
        ID: int = 2
        Name: str = 'orange'
        Value: float = 50

        def __eq__(self, other) -> bool:
            return (self.pk == other.pk
                    and self.ID == other.ID
                    and self.Name == other.Name
                    and self.Value == other.Value)

    return Custom


@pytest.fixture
def custom_obj():
    class Obj():
        pk: int = 0
        ID: int = 2
        Name: str = 'orange'
        Value: float = 50

    return Obj


@pytest.fixture
def custom_db_file():
    db_file = 'db_file.db'

    return db_file


@pytest.fixture
def repo(custom_db_file, custom_class):
    return SQLiteRepository(custom_db_file, custom_class)


def test_crud(repo, custom_class, custom_obj):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo):
    with pytest.raises(ValueError):
        repo.add(0)


def test_cannot_delete_unexistent(repo):
    with pytest.raises(KeyError):
        repo.delete(1)


def test_get_all(repo, custom_class):
    objects = [custom_class() for i in range(5)]
    for o in objects:
        repo.add(o)
    obj = repo.get_all()
    print(objects)
    print(obj)
    assert obj == objects

def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.ID = i
        o.Name = 'test'
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'ID': '0'}) == [objects[0]]
    #repo_get = repo.get_all({'Name': 'test'})
    #print(repo_get)
    #print(objects)
    assert repo.get_all({'Name': 'test'}) == objects
