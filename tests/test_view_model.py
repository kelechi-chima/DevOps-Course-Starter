"""Unit tests for ViewModel"""

import pytest
from datetime import datetime, timedelta
from todo_app.view_model import Item, ItemStatus, ViewModel


today = datetime.utcnow().date()
yesterday = today - timedelta(days=1)

@pytest.fixture
def view_model():
    todo_items = [Item('New task', id='3', status=ItemStatus.TODO.value)]
    doing_items = [Item('In progress', id='2', status=ItemStatus.DOING.value)]
    done_items = [
        Item('Completed task 1', id='1', status=ItemStatus.DONE.value, completed_date=today),
        Item('Completed task 2', id='2', status=ItemStatus.DONE.value, completed_date=today),
        Item('Completed task 3', id='3', status=ItemStatus.DONE.value, completed_date=today),
        Item('Completed task 4', id='4', status=ItemStatus.DONE.value, completed_date=yesterday),
        Item('Completed task 5', id='5', status=ItemStatus.DONE.value, completed_date=yesterday),
        Item('Completed task 6', id='6', status=ItemStatus.DONE.value, completed_date=yesterday),
        Item('Completed task 7', id='7', status=ItemStatus.DONE.value, completed_date=yesterday),
    ]
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
    assert len(done_items) == 7
    assert done_items[0].status == ItemStatus.DONE.value

def test_only_recently_done_items_are_to_be_shown(view_model: ViewModel):
    assert view_model.should_show_all_done_items == False

def test_all_done_items_are_to_be_shown():
    view_model = ViewModel([[], [], [Item('Completed task 1', id='1', status=ItemStatus.DONE.value, completed_date=today)]])
    assert view_model.should_show_all_done_items == True

def test_returns_items_completed_today(view_model: ViewModel):
    items_completed_today = view_model.recent_done_items
    assert len(items_completed_today) == 3
    for item in items_completed_today:
        assert item.completed_date == today

def test_returns_items_completed_before_today(view_model: ViewModel):
    items_completed_before_today = view_model.older_done_items
    assert len(items_completed_before_today) == 4
    for item in items_completed_before_today:
        assert item.completed_date < today