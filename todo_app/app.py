from flask import Flask, request, render_template # needed to specify explicitly to use this
from todo_app.flask_config import Config
from todo_app.data.session_items import * # reference file with CRUD functions

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
     # call function from session_items.py to retrieve predefined item list
     # and render index html page
    return render_template("index.html", items = get_items()) 

@app.route('/items', methods=['POST'])
def add_newitem():
    #read form data - newItem - submitted in the POST request
    newItem = request.form['newItem']
    # call function from session_items.py to add the new item to the existing item list
    add_item(title = newItem)
    # re-call the function from session_items.py to retrieve predefined item list with newly added item
    # and 'redirect' back to the index html page   
    return render_template("index.html", items = get_items())

if __name__ == '__main__':
    app.run()
