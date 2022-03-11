"""Seed database with sample data"""

from app import db
from models import Course, Question, SubModule, User, ListOfPossibleAns

db.drop_all()
db.create_all()

Course.query.delete()
Question.query.delete()
SubModule.query.delete()
User.query.delete()

# Add data for intro course:
q1 = Question(question="Watch the short video and answer the following question; the four main typical ingredients of beer are: malt, hops, water, and ______", answer_multi_choice=3, answer_text="https://www.youtube.com/embed/ZMq8Wq-55Ao", api_call="")
# q1 = Question(question="Watch the short video and answer the following question; the four main typical ingredients of beer are: malt, hops, water, and ______", answer_multi_choice=3, api_call={'chart': {'type': 'bar', 'data': {'labels': ['Hello', 'World'],
#                 'datasets': [{'label': 'Foo', 'data': [1, 2]}]}}, 'h': 150, 'w': 250, 'backgroundColor': 'red'})
q2 = Question(question="Read the link above and then based on the mash regime, which typical mash profile is this?", answer_multi_choice=5, api_call={'chart': {'type': 'line', 'data': {'labels': ['0 Min', '15 Min', "30 Min", "45 Min", "60 Min", "75 Min"],
                'datasets': [{'label': 'Temp (F)', "steppedLine": True, 'data': [65, 154, 154, 154, 154, 170]}]}}, 'h': 150, 'w': 250}, resource="https://crispmalt.com/news/the-crisp-guide-to-mashing/")
q3 = Question(question="Read the link above and then based on the hop regime, which typical type of beer is this?", answer_multi_choice=12, api_call={'chart': {'type': 'line', 'data': {'labels': ['0', '15', "30", "45", "60", "Whirlpool", "FT"],
                'datasets': [{'label': 'Total Hop IBU Addition vs. Boil Time (Min)', "steppedLine": True, 'data': [50, 50, 65, 65, 75, 75, 85]}]}}, 'h': 150, 'w': 250}, resource="https://beersmith.com/blog/2008/11/11/best-hop-techniques-for-homebrewing/")
q4 = Question(question="Based on the link above and the water profile, what beer would this be used for?", answer_multi_choice=15, api_call={'chart': {'type': 'bar', 'data': {'labels': ['Ca', 'Mg', "Na", "Cl", "SO4", "HCO3"],
                'datasets': [{'label': 'Salt Profile (PPM)', 'data': [7, 3, 2, 5, 5, 25]}]}}, 'h': 150, 'w': 250}, resource="https://shop.theelectricbrewery.com/pages/water-adjustment#:~:text=Different%20beer%20styles%20will%20call,more%20bitter%2C%20or%20even%20sour.")
q5 = Question(question="Based on the video, what is the primary flavor impact of yeast?", answer_multi_choice=20, answer_text="https://www.youtube.com/embed/TVtqwWGguFk", api_call="")

# Add data masters course:
q6 = Question(question="Watch the short video and answer the following question; what is the type of malt is used to balance IPAs?", answer_multi_choice=23, answer_text="https://www.youtube.com/embed/gh2KHDYjXNU", api_call="")

q7 = Question(question="Please read the link above and then based on the mash regime, which typical mash profile is this?", answer_multi_choice=25, api_call={'chart': {'type': 'line', 'data': {'labels': ['0 Min', '15 Min', "30 Min", "45 Min", "60 Min", "75 Min"],
                'datasets': [{'label': 'Temp (F) v. Mash Time (Min)', "steppedLine": True, 'data': [65, 145, 154, 154, 165, 170]}]}}, 'h': 150, 'w': 250}, resource="https://crispmalt.com/news/the-crisp-guide-to-mashing/")
q8 = Question(question="Please read the link above and then based on the hop regime, which typical type of beer is this?", answer_multi_choice=30, api_call={'chart': {'type': 'line', 'data': {'labels': ['0', '15', "30", "45", "60", "Whirlpool", "FT"],
                'datasets': [{'label': 'Total Hop IBU Addition vs. Boil Time (Min)', "steppedLine": True, 'data': [0, 5, 5, 5, 5, 25, 85]}]}}, 'h': 150, 'w': 250}, resource="https://beersmith.com/blog/2008/11/11/best-hop-techniques-for-homebrewing/")
q9 = Question(question="Based on the link above and the water profile, what beer would this be used for and what should HCO3 be?", answer_multi_choice=36, api_call={'chart': {'type': 'bar', 'data': {'labels': ['Ca', 'Mg', "Na", "Cl", "SO4", "HCO3"],
                'datasets': [{'label': 'Salt Profile (PPM)', 'data': [7, 3, 2, 5, 5, 0]}]}}, 'h': 150, 'w': 250}, resource="https://shop.theelectricbrewery.com/pages/water-adjustment#:~:text=Different%20beer%20styles%20will%20call,more%20bitter%2C%20or%20even%20sour.")
q10 = Question(question="Based on the video, what is the primary compound for apple flavor from yeast?", answer_multi_choice=38, answer_text="https://www.youtube.com/embed/TVtqwWGguFk", api_call="")


c1 = Course(title="Introduction To Brewing Science", description="Great overview of beer making process")
c2 = Course(title="Masters To Brewing Science", description="In-depth education for brewing professionals")
u1 = User(username="billybob", password="12321324234", total_correct_answers=2, current_course=c1.id, current_question=q2.id)
db.session.add_all([q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, u1, c1, c2])
db.session.commit()

# Idea here is to have one question mapped to one course but showing which submodule
# TODO - validate question_id and course_id are unique (2/17/22) They should be as they are FK
s1 = SubModule(course_id=c1.id, question_id=q1.id, name="Raw Material Overview")
s2 = SubModule(course_id=c1.id, question_id=q2.id, name="Malt")
s3 = SubModule(course_id=c1.id, question_id=q3.id, name="Hops")
s4 = SubModule(course_id=c1.id, question_id=q4.id, name="Water")
s5 = SubModule(course_id=c1.id, question_id=q5.id, name="Saccharomyces")

s6 = SubModule(course_id=c2.id, question_id=q6.id, name="Raw Material Selection")
s7 = SubModule(course_id=c2.id, question_id=q7.id, name="Malts")
s8 = SubModule(course_id=c2.id, question_id=q8.id, name="Hops")
s9 = SubModule(course_id=c2.id, question_id=q9.id, name="Water")
s10 = SubModule(course_id=c2.id, question_id=q10.id, name="Saccharomyces")
db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10])
db.session.commit()

l1 = ListOfPossibleAns(question_id=q1.id, possible_ans="Sugar")
l2 = ListOfPossibleAns(question_id=q1.id, possible_ans="Alcohol")
l3 = ListOfPossibleAns(question_id=q1.id, possible_ans="Yeast")
l4 = ListOfPossibleAns(question_id=q1.id, possible_ans="Bacteria")

l5 = ListOfPossibleAns(question_id=q2.id, possible_ans="Infusion mashing")
l6 = ListOfPossibleAns(question_id=q2.id, possible_ans="Decoction mashing")
l7 = ListOfPossibleAns(question_id=q2.id, possible_ans="Temperature-controlled infusion mashing")
l8 = ListOfPossibleAns(question_id=q2.id, possible_ans="Wild mash profile")

l9 = ListOfPossibleAns(question_id=q3.id, possible_ans="American Lager")
l10 = ListOfPossibleAns(question_id=q3.id, possible_ans="Amber Ale")
l11 = ListOfPossibleAns(question_id=q3.id, possible_ans="Stout")
l12 = ListOfPossibleAns(question_id=q3.id, possible_ans="IPA")

l13 = ListOfPossibleAns(question_id=q4.id, possible_ans="Stout")
l14 = ListOfPossibleAns(question_id=q4.id, possible_ans="IPA")
l15 = ListOfPossibleAns(question_id=q4.id, possible_ans="Pilser")
l16 = ListOfPossibleAns(question_id=q4.id, possible_ans="Sour beer")

l17 = ListOfPossibleAns(question_id=q5.id, possible_ans="Cereal / Bready")
l18 = ListOfPossibleAns(question_id=q5.id, possible_ans="Dank / Veggie")
l19 = ListOfPossibleAns(question_id=q5.id, possible_ans="Crisp / Clean")
l20 = ListOfPossibleAns(question_id=q5.id, possible_ans="Estery / Fruity")

# Masters course
l21 = ListOfPossibleAns(question_id=q6.id, possible_ans="Pilsner")
l22 = ListOfPossibleAns(question_id=q6.id, possible_ans="Black Malt")
l23 = ListOfPossibleAns(question_id=q6.id, possible_ans="Caramel Malt")
l24 = ListOfPossibleAns(question_id=q6.id, possible_ans="Wheat Malt")

l25 = ListOfPossibleAns(question_id=q7.id, possible_ans="Hefeweizen")
l26 = ListOfPossibleAns(question_id=q7.id, possible_ans="IPA")
l27 = ListOfPossibleAns(question_id=q7.id, possible_ans="Stout")
l28 = ListOfPossibleAns(question_id=q7.id, possible_ans="Light Lager")

l29 = ListOfPossibleAns(question_id=q8.id, possible_ans="Light Lager")
l30 = ListOfPossibleAns(question_id=q8.id, possible_ans="Hazy IPA")
l31 = ListOfPossibleAns(question_id=q8.id, possible_ans="IPA")
l32 = ListOfPossibleAns(question_id=q8.id, possible_ans="Stout")

l33 = ListOfPossibleAns(question_id=q9.id, possible_ans="Light Lager, 25")
l34 = ListOfPossibleAns(question_id=q9.id, possible_ans="Pilser, 100")
l35 = ListOfPossibleAns(question_id=q9.id, possible_ans="Light Lager, 100")
l36 = ListOfPossibleAns(question_id=q9.id, possible_ans="Pilser, 25")

l37 = ListOfPossibleAns(question_id=q10.id, possible_ans="Sulfurs")
l38 = ListOfPossibleAns(question_id=q10.id, possible_ans="Ethyl Acetate")
l39 = ListOfPossibleAns(question_id=q10.id, possible_ans="Isopropyl Acetate")
l40 = ListOfPossibleAns(question_id=q10.id, possible_ans="Fusel Alcohols")

db.session.add_all([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20, l21, l22, l23, l24, l25, l26, l27, l28, l29, l30, l31, l32, l33, l34, l35, l36, l37, l38, l39, l40])
db.session.commit()


