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


@app.route('/hbnb_filters')
def hbnb_index():
    """AirBnB index page for hbnb_web_static"""
    from models.state import State
    from models.amenity import Amenity

    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()

    return render_template('10-hbnb_filters.html', states=states,
                           amenities=amenities)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
