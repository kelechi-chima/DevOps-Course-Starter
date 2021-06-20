from typing import List


class ViewModel:
    def __init__(self, items):
        self._items = items
    
    @property
    def items(self):
        return self._items
    
    @property
    def todo_items(self):
        return [item for item in self._items if item.status == 'Not Started']
    
    @property
    def doing_items(self):
        return [item for item in self._items if item.status == 'Doing']

    @property
    def done_items(self):
        return [item for item in self._items if item.status == 'Done']