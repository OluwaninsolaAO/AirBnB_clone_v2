#!/usr/bin/python3
"""A simple web application using flask"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def index():
    """a simple index page for my web application"""
    return "Hello HBNB!"


@app.route('/hbnb')
def hbnb():
    """a simple additional route to my web application"""
    return "HBNB"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
