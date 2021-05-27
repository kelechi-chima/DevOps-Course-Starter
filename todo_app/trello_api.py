import os
import requests
import sys

base_query = { 'key': os.environ.get('TRELLO_API_KEY'), 'token': os.environ.get('TRELLO_API_TOKEN') }
board_name = 'Task Manager'
todo_list_name = 'To Do'
done_list_name = 'Done'

# Set up initial board with a to do list and a done list.
def init_boards():
    board_id = create_board(board_name)
    create_list(board_id, todo_list_name)
    create_list(board_id, done_list_name)

# Create board if it doesn't exist.
def create_board(board_name):
    board_id = find_board(get_boards(), board_name)
    if board_id != '':
        return board_id
    url = 'https://api.trello.com/1/boards/'
    query = dict(base_query)
    query['name'] = board_name
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

def get_boards():
    url = 'https://api.trello.com/1/members/me/boards'
    query = dict(base_query)
    query['fields'] = 'id,name'
    response = requests.get(url, params=query)
    return response.json()

def find_board(boards, name):
    if len(boards) > 0:
        for board in boards:
            if board['name'] == name:
                return board['id']
    return ''

# Create list if it doesn't exist in given board.
def create_list(board_id, list_name):
    lists = get_lists(board_id)
    list_id = find_list(lists, list_name)
    if list_id != '':
        return list_id
    url = f'https://api.trello.com/1/boards/{board_id}/lists'
    query = dict(base_query)
    query['name'] = list_name
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

def get_todo_list():
    board_id = find_board(get_boards(), board_name)
    return find_list(get_lists(board_id), todo_list_name)

def get_done_list():
    board_id = find_board(get_boards(), board_name)
    return find_list(get_lists(board_id), done_list_name)

# Get all the lists in the board with the given id.
def get_lists(board_id):
    url = f'https://api.trello.com/1/boards/{board_id}/lists'
    query = dict(base_query)
    query['fields'] = 'id,name'
    resp = requests.get(url, params=query)
    return resp.json()

def find_list(lists, name):
    for list in lists:
        if list['name'] == name:
            return list['id']
    return ''

# Get all the cards in the to do list.
def get_todo_cards():
    board_id = find_board(get_boards(), board_name)
    lists = get_lists(board_id)
    todo_list_id = find_list(lists, todo_list_name)
    return get_cards_in_list(todo_list_id)

def get_cards_in_list(list_id):
    url = f'https://api.trello.com/1/lists/{list_id}/cards'
    response = requests.get(url, params=base_query)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Create a new card with the given name in the to do list.
def create_todo_card(card_name):
    list_id = get_todo_list()
    url = 'https://api.trello.com/1/cards'
    query = dict(base_query)
    query['idList'] = list_id
    query['name'] = card_name
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

# Update the card with the given id to be in the done list.
def move_card_to_done_list(card_id):
    list_id = get_done_list()
    url = f'https://api.trello.com/1/cards/{card_id}'
    move_card_query = dict(base_query)
    move_card_query['idList'] = list_id
    response = requests.put(url, params=move_card_query)