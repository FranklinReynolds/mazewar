#! /bin/python3

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello world'

@app.route('/status')
def index():
    return 'Hello world: from status'

@app.route('/shoot')
def index():
    return 'Hello world: from shoot'

@app.route('/turn')
def index():
    return 'Hello world: from turn'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
