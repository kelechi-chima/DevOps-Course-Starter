from enum import Enum
from typing import List

class ItemStatus(Enum):
    TODO = 'To Do'
    DOING = 'Doing'
    DONE = 'Done'

class Item:
    def __init__(self, title, id='', status=ItemStatus.TODO.value):
        self.title = title
        self.id = id
        self.status = status

class ViewModel:
    def __init__(self, items):
        self._todo_items = items[0]
        self._doing_items = items[1]
        self._done_items = items[2]
    
    @property
    def todo_items(self):
        return self._todo_items
    
    @property
    def doing_items(self):
        return self._doing_items

    @property
    def done_items(self):
        return self._done_items