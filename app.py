from flask import Flask
from flask import render_template
from flask import request
import json_creator
import map_creator


app = Flask(__name__)


@app.route('/', methods = ['GET'])
def index_html():
    '''
    Builds a map.
    Returns: str
    '''
    return render_template('index.html')


@app.route('/data_pass', methods = ['POST'])
def submit():
    '''
    Receives a post signal from a user.
    Returns: str
    '''
    global submit
    submit = request.form['submit']
    return render_template('index.html')


@app.route('/data_pass/friends_map', methods = ['POST'])
def display():
    '''
    Submits nickname to a server.
    Returns: str
    '''    
    json_creator.create_json(submit)
    map_creator.build_map()
    ip_add = request.remote_user
    return render_template('map.html', user_ip=ip_add)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
