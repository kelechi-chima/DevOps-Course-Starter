from datetime import datetime
from enum import Enum
from typing import List

class ItemStatus(Enum):
    TODO = 'To Do'
    DOING = 'Doing'
    DONE = 'Done'

class Item:
    def __init__(self, title, id='', status=ItemStatus.TODO.value, completed_date=''):
        self.title = title
        self.id = id
        self.status = status
        if completed_date == '':
            self._completed_date = None
        else:
            self._completed_date = datetime.fromisoformat(completed_date.replace('Z', '+00:00')).date()

    @property
    def completed_date(self):
        return self._completed_date

class ViewModel:
    def __init__(self, items):
        self._todo_items = items[0]
        self._doing_items = items[1]
        self._done_items = items[2]
        if len(self._done_items) < 5:
            self._should_show_all_done_items = True
        else:
            self._should_show_all_done_items = False
    
    @property
    def todo_items(self):
        return self._todo_items
    
    @property
    def doing_items(self):
        return self._doing_items

    @property
    def done_items(self):
        return self._done_items

    @property
    def should_show_all_done_items(self):
        return self._should_show_all_done_items
    
    @property
    def recent_done_items(self):
        today = datetime.utcnow().date()
        return [item for item in self.done_items if item.completed_date == today]

    @property
    def older_done_items(self):
        today = datetime.utcnow().date()
        return [item for item in self.done_items if item.completed_date < today]