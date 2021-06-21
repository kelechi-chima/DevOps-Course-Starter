"""Unit tests for ViewModel"""

import pytest

from todo_app.view_model import Item, ItemStatus, ViewModel

@pytest.fixture
def view_model():
    todo_items = [Item('New task', id='3', status=ItemStatus.TODO.value)]
    doing_items = [Item('In progress', id='2', status=ItemStatus.DOING.value)]
    done_items = [Item('Completed task', id='1', status=ItemStatus.DONE.value)]
    return ViewModel([todo_items, doing_items, done_items])

def test_returns_only_todo_items(view_model: ViewModel):
    todo_items = view_model.todo_items
    assert len(todo_items) == 1
    assert todo_items[0].status == ItemStatus.TODO.value


def test_returns_only_doing_items(view_model: ViewModel):
    doing_items = view_model.doing_items
    assert len(doing_items) == 1
    assert doing_items[0].status == ItemStatus.DOING.value

def test_returns_only_done_items(view_model: ViewModel):
    done_items = view_model.done_items
    assert len(done_items) == 1
    assert done_items[0].status == ItemStatus.DONE.value  