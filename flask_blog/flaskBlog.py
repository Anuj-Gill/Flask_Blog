from flask import Flask, render_template, url_for
from forms import RegistrationForm,LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '8d9a018d01741fc317ce5e4050ee3740'

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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html',form=form,title='register')

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html',form=form,title='Login')

if __name__ == "__main__":
    app.run(debug=True)