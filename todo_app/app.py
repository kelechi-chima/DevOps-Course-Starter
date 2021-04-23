from flask import Flask
from flask import redirect, render_template, url_for
from flask import request

from todo_app.flask_config import Config
from todo_app.data.session_items import *

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index():
    sorted_items = sorted(get_items(), key=lambda item: item['status'], reverse=True)
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

if __name__ == '__main__':
    app.run()
