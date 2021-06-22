from flask import Flask
from flask import redirect, render_template, url_for
from flask import request

from todo_app.trello_api import create_todo_item, complete, get_all_items, start
from todo_app.view_model import Item, ViewModel

def create_app():
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')

    @app.route('/', methods=['GET'])
    def index():
        item_view_model = ViewModel(get_all_items())
        return render_template("index.html", view_model=item_view_model)

    @app.route('/', methods=['POST'])
    def new_item():
        new_item = Item(request.form['item_title'])
        create_todo_item(new_item)
        return redirect(url_for('index'))


    @app.route('/start/<item_id>', methods=['POST'])
    def start_item(item_id):
        start(item_id)
        return redirect(url_for('index'))

    @app.route('/complete/<item_id>', methods=['POST'])
    def complete_item(item_id):
        complete(item_id)
        return redirect(url_for('index'))

    return app
