import os
from unittest import TestCase

from models import db, connect_db, Course, Question, SubModule, User, ListOfPossibleAns

# Connect to test-db
os.environ['DATABASE_URL'] = "postgresql:///beer_education_test"

from app import app, CURR_USER_KEY

db.create_all()

class ViewsGeneralTestCase(TestCase):
    """Test all the integrated testing between views"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 12346
        u = User.signup("testing2", "password", None)
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_index(self):
        with self.client as c:
            resp = c.get("/")

            self.assertIn("Courses", str(resp.data))
            self.assertIn("Masters", str(resp.data))
            self.assertIn("Start", str(resp.data))
            # This assertIn is users specific therefore confirms user data is displayed
            self.assertIn("testing2", str(resp.data))
            self.assertIn("Log", str(resp.data))  

    def test_about(self):
        with self.client as c:
            resp = c.get("/about")

            self.assertEqual(resp.status_code, 200)

    def test_404(self):
        with self.client as c:
            resp = c.get("/404")

            self.assertEqual(resp.status_code, 404)     

    def test_user_signup_get(self):
        with self.client as c:
            resp = c.get("/signup")

            self.assertEqual(resp.status_code, 200)   

    def test_user_signup_post(self):
        with self.client as c:
            resp = c.post("/signup", data={"username": "test2", "password":"123456"}, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)  

    def test_user_logout(self):
        with self.client as c:
            resp = c.get("/logout")

            self.assertEqual(resp.status_code, 302) 

    def test_user_login_get(self):
        with self.client as c:
            resp = c.get("/login")

            self.assertEqual(resp.status_code, 200)        

    def test_user_login_post(self):
        with self.client as c:
            resp = c.post("/login", data={"username":"testing2", "password":"password"})

            self.assertEqual(resp.status_code, 200)       
            self.assertIn("testing2", str(resp.data))

    def test_users_edit(self):
        with self.client as c:
            resp = c.get("/users/edit")

            self.assertEqual(resp.status_code, 302)

    def test_users_delete(self):
        with self.client as c:
            resp = c.post("/users/delete")

            self.assertEqual(resp.status_code, 302)

class ViewsCourseTestCase(TestCase):
    """Test all the integrated testing between views for courses"""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 12343
        u = User.signup("testing2", "password", None)
        u.id = self.uid

        db.session.commit()
        
        self.cid = 123467
        self.qid = 7654321

        q2 = Question(question="Read the link above and then based on the mash regime, which typical mash profile is this?", answer_multi_choice=5, api_call={'chart': {'type': 'line', 'data': {'labels': ['0 Min', '15 Min', "30 Min", "45 Min", "60 Min", "75 Min"],
                'datasets': [{'label': 'Temp (F)', "steppedLine": True, 'data': [65, 154, 154, 154, 154, 170]}]}}, 'h': 150, 'w': 250}, resource="https://crispmalt.com/news/the-crisp-guide-to-mashing/")
        c1 = Course(title="Introduction To Brewing Science", description="Great overview of beer making process")
        c1.id = self.cid
        q2.id = self.qid

        db.session.add_all([c1, q2])
        db.session.commit()
     
        s2 = SubModule(course_id=c1.id, question_id=q2.id, name="Malt")
        l5 = ListOfPossibleAns(question_id=q2.id, possible_ans="Infusion mashing")
        l6 = ListOfPossibleAns(question_id=q2.id, possible_ans="Decoction mashing")
        l7 = ListOfPossibleAns(question_id=q2.id, possible_ans="Temperature-controlled infusion mashing")
        l8 = ListOfPossibleAns(question_id=q2.id, possible_ans="Wild mash profile")

        db.session.add_all([s2, l5, l6, l7, l8])
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res    

    def test_course_get(self):
        # c1 = Course.query.get(self.cid)
        # q2 = Question.query.get(self.qid)


        with self.client as c:
            resp = c.get(f"/course/123467/question/7654321")

            self.assertEqual(resp.status_code, 200) 
            self.assertIn("Wild", str(resp.data))           
            self.assertIn("Malt", str(resp.data))           
            self.assertIn("Brewing", str(resp.data))           
            self.assertIn("regime", str(resp.data))           

    def test_course_correct(self):

        with self.client as c:
            resp = c.post(f"/course/123467/question/7654321", data={"answer_multi_choice":5}, follow_redirects=True)          
            self.assertEqual(resp.status_code, 200)
 