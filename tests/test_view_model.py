"""Unit tests for ViewModel"""

import pytest

from todo_app.trello_api import Item
from todo_app.view_model import ViewModel

@pytest.fixture
def view_model():
    todo_item = Item('New task', id='3', status='Not Started')
    doing_item = Item('In progress', id='2', status='Doing')
    done_item = Item('Completed task', id='1', status='Done')
    return ViewModel([todo_item, doing_item, done_item])

def test_returns_only_todo_items(view_model: ViewModel):
    todo_items = view_model.todo_items
    assert len(todo_items) == 1
    assert todo_items[0].status == 'Not Started'


def test_returns_only_doing_items(view_model: ViewModel):
    doing_items = view_model.doing_items
    assert len(doing_items) == 1
    assert doing_items[0].status == 'Doing'

def test_returns_only_done_items(view_model: ViewModel):
    done_items = view_model.done_items
    assert len(done_items) == 1
    assert done_items[0].status == 'Done'    