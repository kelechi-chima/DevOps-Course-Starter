from flask import Flask
from flask import redirect, render_template, url_for
from flask import request

from todo_app.flask_config import Config
from todo_app.data.session_items import *

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", items=get_items())

@app.route('/', methods=['POST'])
def new_item():
    item_title = request.form['item_title']
    add_item(item_title)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
