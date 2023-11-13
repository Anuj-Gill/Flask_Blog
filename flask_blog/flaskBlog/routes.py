from flaskBlog.models import User, Post
from flask import render_template, url_for,flash, redirect, request
from flaskBlog.forms import RegistrationForm,LoginForm
from flaskBlog import bcrypt,app,db
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        
        'author' : 'Sahil Shangloo',
        'title' : 'Release of My New Song',
        'date' : '01/11/2023',
        'content' : "Hello everyone, this is Sahil Shangloo from Jammu. I am happy to announce the release of my new Rap before you. The song will be availabel on Spotify from 3rd of November!"
    },
    {
        
        'author' : 'Om Alve',
        'title' : 'Neural Network',
        'date' : '28/10/2023',
        'content' : "Hello everyone, this is Om Alve from Thane. I am happy to announce the release of my new Rap before you. The song will be availabel on Spotify from 3rd of November!"
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts = posts,title = "Welcome")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods=['GET','POST']) #methods is used to specify that this specific route can accept these methods
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please login now','success')
        return redirect(url_for('login'))
    # else:
    #     flash
    return render_template('register.html',form=form,title='Register')

@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user,remember=form.remember.data)
          next_page = request.args.get('next')
          flash('Loged In!','success')
          return redirect(next_page) if next_page else  redirect(url_for('home'))
        else:
             flash('Login Unseccessful. Please check email and password','danger')
    return render_template('login.html',form=form,title='Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')