from flask import Flask
from flask import redirect, render_template, url_for
from flask import request

from todo_app.flask_config import Config
from todo_app.trello_api import get_todo_cards, create_todo_card, move_card_to_done_list

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET'])
def index():
    todo_cards = get_todo_cards()
    items = [{'id': card['id'], 'status': 'Not Started', 'title': card['name']} for card in todo_cards]
    sorted_items = sorted(items, key=lambda item: item['status'], reverse=True)
    return render_template("index.html", items=sorted_items)

@app.route('/', methods=['POST'])
def new_item():
    item_title = request.form['item_title']
    create_todo_card(item_title)
    return redirect(url_for('index'))


@app.route('/complete/<item_id>', methods=['POST'])
def complete_item(item_id):
    move_card_to_done_list(item_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
