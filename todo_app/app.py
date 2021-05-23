from flask import Flask
from flask import redirect, render_template, url_for
from flask import request

from todo_app.flask_config import Config
from todo_app.data.session_items import add_item, get_item, get_items, save_item

import os
import requests

app = Flask(__name__)
app.config.from_object(Config)

base_query = { 'key': os.environ.get('TRELLO_API_KEY'), 'token': os.environ.get('TRELLO_API_TOKEN') }

@app.route('/', methods=['GET'])
def index():
    init_boards()
    #sorted_items = sorted(get_items(), key=lambda item: item['status'], reverse=True)
    sorted_items = []
    return render_template("index.html", items=sorted_items)

@app.route('/', methods=['POST'])
def new_item():
    item_title = request.form['item_title']
    add_item(item_title)
    return redirect(url_for('index'))


@app.route('/complete', methods=['POST'])
def complete_item():
    completed = request.form.getlist('completed')
    for c in completed:
        item = get_item(c)
        item['status'] = 'Completed'
        save_item(item)
    return redirect(url_for('index'))


def init_boards():
    board_id = create_board()
    todo_list_id = create_list(board_id, 'To Do')
    done_list_id = create_list(board_id, 'Done')

def create_board(board_name):
    url = 'https://api.trello.com/1/boards/'
    query = dict(base_query)
    query['name'] = board_name
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

def create_list(board_id, list_name):
    url = f'https://api.trello.com/1/boards/{board_id}/lists'
    query = dict(base_query)
    query['name'] = list_name
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

def get_cards_in_list(list_id):
    url = f'https://api.trello.com/1/lists/{list_id}/cards'
    response = requests.get(url, params=base_query)
    result = response.json()

def create_new_card_in_list(list_id, card_name):
    url = 'https://api.trello.com/1/cards'
    query = dict(base_query)
    query['idList'] = list_id
    query['name'] = card_name
    response = requests.post(url, params=query)
    result = response.json()
    return result['id']

def move_card_to_list(card_id, list_id):
    url = f'https://api.trello.com/1/cards/{card_id}'
    move_card_query = dict(base_query)
    move_card_query['idList'] = list_id
    response = requests.put(url, params=move_card_query)

if __name__ == '__main__':
    app.run()
