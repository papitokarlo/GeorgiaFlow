from view import app
from flask import render_template, request, flash, redirect, url_for, Flask


@app.route('/', methods=['GET', 'POST'])
def index():    
   return render_template('index.html')
