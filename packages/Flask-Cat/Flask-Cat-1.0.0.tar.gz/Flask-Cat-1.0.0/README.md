# Flask-Cats
*Flask-cats* is a small blueprint which takes all status codes above 399 and returns cat images from httpcats.com<br>
(*Made as a Joke, to learn how to make Flask blueprints*)

# Install
```sh
pip install Flask-Cats
```

# Use
```py
from flask import Flask
import flaskcat

app = Flask(__name__)

app.register_blueprint(flaskcat.cat_blueprint)


@app.get('/')
def root():
    return 'Hello, World.'


app.run()
```