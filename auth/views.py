from auth import app
from flask import render_template

@app.route('/login', methods=['GET', 'POST'])
def log():    
   return render_template('login.html')