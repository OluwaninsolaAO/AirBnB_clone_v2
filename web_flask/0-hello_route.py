#!/usr/bin/python3
"""A simple web application using flask"""

from flask import Flask

app = Flask(__name__)

@app.route('/', strict_slashes=False)
def index():
    """a simple index page for my web application"""
    return "Hello HBNB!"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
