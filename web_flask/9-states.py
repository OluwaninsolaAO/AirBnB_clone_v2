#!/usr/bin/python3
"""An flask web application that lists states"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_storage(exception=None):
    """Closes the current SQLAlchemy session"""
    storage.close()


@app.route('/states')
@app.route('/states/<id>')
def state_list(id=None):
    """Returns a rendered HTML template"""
    from models.state import State
    states = storage.all(State).values()

    state_obj = None
    if id is not None:
        state_obj = storage.all(State).get('State.' + id, 'Nil')

    return render_template('9-states.html', states=states, state_obj=state_obj)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
