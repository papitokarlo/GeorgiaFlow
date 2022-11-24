from view import app
from flask import render_template


@app.route('/')
def index():
    print("new here")
    return render_template('index.html')