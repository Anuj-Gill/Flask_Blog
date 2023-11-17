from flaskBlog.models import User, Post
from flask import render_template, url_for,flash, redirect, request, abort
from flaskBlog.forms import RegistrationForm,LoginForm, PostForm
from flaskBlog import bcrypt,app,db
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html",title='About')

@app.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html",posts = posts,title = "Home Feed")

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

@app.route('/post/new',methods=["GET","POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post has been created!","success")
        return redirect(url_for('home'))
    return render_template('new_post.html',title="New Post", form=form,legend='New Post')

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title, post=post)

@app.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('new_post.html',title="Update Post", form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))