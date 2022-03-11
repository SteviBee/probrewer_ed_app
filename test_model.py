import os
from unittest import TestCase

from models import db, connect_db, Course, Question, SubModule, User, ListOfPossibleAns

# Connect to test-db
os.environ['DATABASE_URL'] = "postgresql:///beer_education_test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test users models."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 12345
        u = User.signup("testing", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic user model work?"""
        
        u = User(
            username="test1",
            password="test1234",
            total_correct_answers=3
        )

        db.session.add(u)
        db.session.commit()

        # User should have no competed questions
        self.assertIsInstance(self.u, User)
        self.assertEqual(u.total_correct_answers, 3)

    def test_questions(self):
        """testing the questions model"""

        q = Question(
            question="what is the meaning of life?",
            answer_multi_choice=1,
            resource="url",
            answer_text="answer",
            api_call={}
        )

        db.session.add(q)
        db.session.commit()
        q1 = Question.query.get(q.id)

        self.assertIsInstance(q, Question)
        self.assertEqual(q.id, q1.id)
        self.assertEqual(q.answer_multi_choice, q1.answer_multi_choice)
        self.assertEqual(q.resource, q1.resource)
        self.assertEqual(q.answer_text, q1.answer_text)
        self.assertEqual(q.api_call, q1.api_call)

    def test_listofpossibleans(self):
        """testing the list of ans model"""
        q2 = Question(
            question="What color is the sky?",
            api_call={}
        )

        db.session.add(q2)
        db.session.commit()

        l = ListOfPossibleAns(
            question_id= q2.id,
            possible_ans="red",
        )

        db.session.add(l)
        db.session.commit()

        l1 = ListOfPossibleAns.query.get(l.id)

        self.assertIsInstance(l, ListOfPossibleAns)
        self.assertEqual(l.id, l1.id)
        self.assertEqual(l.possible_ans, "red")  

    def test_course(self):
        """testing the course model"""

        c = Course(
            title="Art of Code",
            description="Some cool text",
        )

        db.session.add(c)
        db.session.commit()
        c1 = Course.query.get(c.id)

        self.assertIsInstance(c, Course)
        self.assertEqual(c.id, c1.id)
        self.assertEqual(c.title, "Art of Code")
        self.assertEqual(c.description, c1.description)

    def test_junctiontable(self):
        """testing the junction table Submodule"""
        q3 = Question(
            question="The last question is?",
        )

        db.session.add(q3)
        db.session.commit()

        c2 = Course(
            title="Code",
            description="Cool Stuff",
        )

        db.session.add(c2)
        db.session.commit()

        sub = SubModule(
            course_id=q3.id,
            question_id=c2.id,
            name="cool name"
        )

        db.session.add(sub)
        db.session.commit()

        sub1 = SubModule.query.get(sub.id)
        question = Question.query.get(q3.id)
        course = Course.query.get(c2.id)

        self.assertIsInstance(sub1, SubModule)
        self.assertEqual(sub1.question_id, question.id)
        self.assertEqual(sub1.course_id, course.id) 

    def test_valid_authentication(self):
        u = User.authenticate(self.u.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u.username, "badpassword")) 