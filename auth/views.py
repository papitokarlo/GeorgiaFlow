from datetime import datetime
from auth import app
from flask import render_template, url_for, flash, request, redirect
from .forms import RegistrateForm
from .models import Users
from auth import db

@app.route('/login', methods=['GET', 'POST'])
def log():    
   return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():    
   form = RegistrateForm()
   print(form.email.validators)
   print(form.fullname.data, form.email.data, datetime.utcnow())
   if form.validate_on_submit():
      print(form.fullname.data, form.email.data, datetime.utcnow())
      new_user = Users(form.fullname.data, form.email.data, datetime.utcnow(), form.password.data)
      Users.add_user(new_user)
      flash('register succesfuly')
      print("£here we are")
      return redirect(url_for('login'))
      
    
   return render_template('register.html', form=form)