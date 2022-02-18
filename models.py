"""SQLAlchemy models for Beer Education."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Question(db.Model):
    "Questions and answers"

    __tablename__ = 'questions'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    # The key here is linking the answer to the table ID of the possible answers
    answer_multi_choice = db.Column(
        db.Integer,
        nullable=True,
        unique=False,
    )

    answer_text = db.Column(
        db.Text,
        nullable=True,
        unique=False,
    )

    list_questions = db.relationship('ListOfPossibleAns', backref="question")

    # TODO - Check if i should delete this
    @classmethod
    def check_answer(cls, answer, selected):
        """checks if the selected question's answer matches the DB answer and returns true"""

        if answer == selected:
            return True
        else:
            return False

class ListOfPossibleAns(db.Model):
    "referece table for possible answer to each question"

    __tablename__ = 'listofpossibleanswers'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='CASCADE'),
        nullable=True,
    )

    possible_ans = db.Column(
        db.Text,
        nullable=True,
    )



class User(db.Model):
    "User information and coursework"

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/profile.jpg"
    )    

    total_correct_answers = db.Column(
        db.Integer,
        nullable=True,
    )

    # use to record the users current spot so they can resume - TODO - Test this
    current_question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='CASCADE'),
        nullable=True,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, password, image_url):
        """Sign up user. Hashes password, adds user to system, and then returns for use"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Course(db.Model):
    "Courses for brewing education"

    __tablename__ = "courses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )    

    title = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    # Setting up a "through" relationship to connect questions to courses
    questions = db.relationship(
        "Question",
        secondary="submodules",
        backref="course"
    )


class SubModule(db.Model):
    """junction table for courses and questions"""

    __tablename__ = "submodules"

    id = db.Column(
        db.Integer,
        primary_key=True
    )  

    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id', ondelete='cascade')
    )

    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id', ondelete='cascade')
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )





def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)