import os

from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import urandom
from models import *


app = Flask(__name__)

count = 1

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = urandom(24)


Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# db.init_app(app)


@app.route("/")
def index():
    if 'username' in session:
        message = session['username'] + " you are currently logged in!!!"
        return render_template('success.html',message=message)
    return render_template("index.html")

@app.route("/success",methods=["POST"])
def success():
    global count
    username = request.form.get("username")
    form_password = request.form.get("password")
    button = request.form.get("login")

    if button=="LOGIN":
        user = db.execute("select * from users where name=:username",{"username":username}).fetchone()

        if user == None or user.password != form_password :
            message = "check username or password"
            # session['username'] = None

        elif user.password == form_password:
            print(user.password)
            session['username'] = username
            session['username'] = session['username'].capitalize()
            message = session['username'] +" you are logged in succcusfully!"


    else:
        db.execute("INSERT INTO users (id,name, password) VALUES (:id,:name, :password)",{"id":count,"name": username, "password": form_password})
        db.commit()
        count += 1
        session['username'] = username
        session['username'] = session['username'].capitalize()
        message = session['username'] + " you are registered succcusfully!"
    return render_template('success.html',message=message)


@app.route("/register")
def register():
    return render_template('register.html')


@app.route('/sign_out')
def sign_out():
    session.pop('username')
    return render_template("index.html")