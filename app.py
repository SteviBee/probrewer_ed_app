import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from forms import 
from models import db, connect_db, Course, Question, SubModule, User, ListOfPossibleAns
from forms import UserAddForm, LoginForm, UserEditForm

CURR_USER_KEY = "curr_user"
app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///beer_education'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

toolbar = DebugToolbarExtension(app)

connect_db(app)

# **************** User signup/login/logout/update ****************************
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user by deleting their flask session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    flash("You have successfully logged out.", 'success')
    return redirect("/login")

@app.route('/signup', methods=["GET", "POST"])
def user_signup():
    """Handles user signup"""

    # delete current session if there is a user
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def user_login():
    """Display user login and authenticate user."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route("/users/edit", methods=["GET", "POST"])
def profile():
    """display edit form and then update profile of user"""

    # Checking for Authorization 
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        # Authenticates user by using bcrypt's check_password_hash on the backend
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.image_url = form.image_url.data or "/static/images/logo.png"

            db.session.commit()
            return redirect(f"/users/{user.id}")

        flash("Wrong password, please try again.", 'danger')
    
    return render_template('users/edit.html', form=form, user_id=user.id)

@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")



# ****************************  MAIN ROUTES:  ****************************
@app.route('/')
def index():
    """displays homepage"""

    question = Question.query.first()
    user = User.query.first()
    course = Course.query.first()
    sub = SubModule.query.first()
    lst= ListOfPossibleAns.query.first()

    return render_template('index.html', question=question, user=user, c=course, sub=sub, lst=lst)

# HERHERHEHRHEHREH - 2/17 - NExt is to show next question or maybe redirect, then corrispond
# API call and then, counter / Total correct vs attempted ?, then maybe look at making
# a query-int to pick which course
@app.route('/course', methods=["GET", "POST"])
def show_course():
    """Populated selected course with first question and controls submitions"""

    # populate course 
    question = Question.query.first()
    course = Course.query.first()
    all_subs = SubModule.query.filter_by(course_id=course.id).all()
    lst= ListOfPossibleAns.query.all()

    # Creating list of submodules, filters out repeats
    submods = []
    for item in all_subs:
        if item.name in submods:
            continue
        else:
            submods.append(item.name)
    print("SUB MODULES -------------------", submods)

    # Creating list of possible answers
    possible = []
    for item in lst:
        possible.append(item)

    # TODO - delete this if too complex?
    # if request.method == "POST":
    #     if question.check_answer(int(request.form.get(f"{question.answer_multi_choice}")), question.answer_multi_choice):
    #         print("true FRIST!__________________________", request.form["2"])
    #         flash("Correct!", "success")
    #         return redirect("/course")
    #     else: 
    #         return redirect("/")
    
    # Checking if answer is correct or not
    if request.method == 'POST':
        if request.form.get(f"{question.answer_multi_choice}") == None:
            flash("Incorrect", "info")
            return redirect('/course')
        elif int(request.form.get(f"{question.answer_multi_choice}")) == question.answer_multi_choice:
            flash("Correct!", "success")
            return redirect("/course")
        else:
            # TODO - validate if I want this or not
            flash("Error", "danger")
            return redirect("/")

    return render_template('course/course_details.html', question=question, course=course, sub=submods, pq=possible)


@app.route('/about')
def about():
    """Takes user to about section"""
      
    return render_template('about.html')

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    """display user profile"""

    user = User.query.get_or_404(user_id)

    return render_template("users/profile.html", user=user)

@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404

# ****************************  COURSE & API ROUTES:  ****************************
