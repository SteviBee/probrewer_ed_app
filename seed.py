"""Seed database with sample data"""
from turtle import title
from app import db
from models import Course, Question, SubModule, User, ListOfPossibleAns

db.drop_all()
db.create_all()

Course.query.delete()
Question.query.delete()
SubModule.query.delete()
User.query.delete()

# Add sample data:
q1 = Question(question="If roses are red what are violets? (multichoice)", answer_multi_choice=2)
q2 = Question(question="Testing word responses?", answer_text="yes")
q3 = Question(question="What is one plus two? (multichoice)", answer_multi_choice=3)
u1 = User(username="billybob", password="12321324234", total_correct_answers=2)
c1 = Course(title="Introduction To Brewing Science", description="Great overview of beer making process")
db.session.add_all([q1, q2, q3, u1, c1])
db.session.commit()

# Idea here is to have one question mapped to one course but showing which submodule
# TODO - validate question_id and course_id are unique (2/17/22) They should be as they are FK
s1 = SubModule(course_id=c1.id, question_id=q1.id, name="Water")
s2 = SubModule(course_id=c1.id, question_id=q2.id, name="Water")
s3 = SubModule(course_id=c1.id, question_id=q3.id, name="Malt")
db.session.add_all([s1, s2, s3])
db.session.commit()

l1 = ListOfPossibleAns(question_id=q1.id, possible_ans="purple")
l2 = ListOfPossibleAns(question_id=q1.id, possible_ans="SELECTME")
l3 = ListOfPossibleAns(question_id=q1.id, possible_ans="red")
l4 = ListOfPossibleAns(question_id=q1.id, possible_ans="blue")

db.session.add_all([l1, l2, l3, l4])
db.session.commit()


