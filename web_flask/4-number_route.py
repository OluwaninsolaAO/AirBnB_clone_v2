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


@app.route('/c/<text>')
def c_is_fun(text):
    """a simple dynamic route handling on my web application"""
    return "C {}".format(text.replace('_', ' '))


@app.route('/python')
@app.route('/python/<text>')
def python_is_cool(text="is cool"):
    """a simple dynamic route with optional parameter"""
    return "Python {}".format(text.replace('_', ' '))


@app.route('/number/<int:n>')
def is_number(n):
    """a dynamic route that checks for number"""
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
