
from flask import Flask, render_template
app = Flask(__name__)

from application import config
from application import models
from application import routes

if __name__ == "__main__":
    # If someone is importing this file then this code will not run. It will run only if
    # you are running the file.
    app.run(debug=True)