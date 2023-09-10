from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import LoginForm, RegisterForm, EnrolCareer
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort
 
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///fobework.db"
#postgres://blog:28TUl9nXzhdxkwWec7vJqS4lXrjmG9u8@dpg-chf0keu4dad1jq99ae80-a.oregon-postgres.render.com/blog_1ld7
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(100))
    password = db.Column(db.String(100))
with app.app_context():
    db.create_all()

class Career(UserMixin, db.Model):
    __tablename__ = "career"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    fullname = db.Column(db.String(100))
    tech_stack = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
with app.app_context():
    db.create_all()

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=["POST", "GET"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            flash("You have already signed up with this email, log in instead")
            return redirect(url_for("login"))
        hash_and_salted = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email = form.email.data,
            fullname = form.fullname.data,
            password = hash_and_salted
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for("index"))
    return render_template("signup.html", form=form)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/faq')
def faq():
    return render_template("faq.html")

@app.route('/career')
def career():
    return render_template("career.html")

@app.route('/enrol_career', methods=["POST", "GET"])
def enrol():
    form = EnrolCareer()
    if form.validate_on_submit():
        if Career.query.filter_by(email=form.email.data).first():
            flash("This email is already registered")
            return redirect(url_for("enrol"))
            
        new_career = Career(
            fullname = form.fullname.data,
            email = form.email.data,
            tech_stack = form.tech_stack.data,
            description = form.description.data
        )
        flash("Career Registered successfully")
        db.session.add(new_career)
        db.session.commit()
        return redirect(url_for('career'))
    return render_template('enrol_career.html', form=form)

@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("This email does not exist, please try again")
            return redirect(url_for("login"))

        elif not check_password_hash(user.password, password):
            flash("incorrect password, please try again")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("index"))
    return render_template("login.html", form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)