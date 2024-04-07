from datetime import timedelta

import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    e = Budget(plan=100, duration=timedelta(days=84))
    assert e.plan == 100
    assert e.duration == timedelta(days=84)


def test_create_brief():
    e = Budget(duration=timedelta(days=84))
    assert e.duration == timedelta(days=84)
    assert e.plan == 1000
