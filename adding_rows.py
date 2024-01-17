from app import app, db, Courses, Dates, MyCourses
from datetime import datetime
from pathlib import Path
import os
import pytz

# Example entries
course_entry_1 = Courses(
    Code_LV='12345',
    Lecturer='Prof. Max Musterman',
    Title='Introduction to Testing',
    LectureType='Masterseminar',
    Semester='Frühjahrssemester 2024',
    Faculty='Wirtschaftswissenschaft',
    Level='Master',
    ECTS='6',
    Language='Deutsch',
    Prerequisites='An intrinsic motivation to test',
    Link='https://portal.unilu.ch/details?code=FS241601'  
)

course_entry_2 = Courses(
    Code_LV='54321',
    Lecturer='Erika Musterfrau',
    Title='Advanced Testing',
    LectureType='Vorlesung',
    Semester='Herbstsemester 2024',
    Faculty='Wirtschaftswissenschaft',
    Level='Master',
    ECTS='6',
    Language='Deutsch',
    Prerequisites='Introduction to Testing',
    Link='https://portal.unilu.ch/details?code=FS241199'
)


# Example entries
date_entry_1 = Dates(
    Code_LV='12345',
    Lecture_Start=datetime(2024, 1, 15, 8, 0, 0, tzinfo=pytz.utc),
    Lecture_End=datetime(2024, 1, 15, 10, 0, 0, tzinfo=pytz.utc),
    Room='HS 1'
)

date_entry_2 = Dates(
    Code_LV='12345',
    Lecture_Start=datetime(2024, 1, 16, 8, 0, 0, tzinfo=pytz.utc),
    Lecture_End=datetime(2024, 1, 16, 10, 0, 0, tzinfo=pytz.utc),
    Room='HS 1'
)
date_entry_3 = Dates(
    Code_LV='54321',
    Lecture_Start=datetime(2024, 1, 15, 12, 0, 0, tzinfo=pytz.utc),
    Lecture_End=datetime(2024, 1, 15, 2, 0, 0, tzinfo=pytz.utc),
    Room='HS 5'
)
date_entry_4 = Dates(
    Code_LV='54321',
    Lecture_Start=datetime(2024, 1, 16, 12, 0, 0, tzinfo=pytz.utc),
    Lecture_End=datetime(2024, 1, 16, 2, 0, 0, tzinfo=pytz.utc),
    Room='HS 5'
)

# Example entries
mycourse_entry_1 = MyCourses(
    Code_LV='12345'
)
mycourse_entry_2 = MyCourses(
    Code_LV='54321'
)

with app.app_context():
    # Add entries to the database
    db.session.add(course_entry_1)
    db.session.add(course_entry_2)
    db.session.add(date_entry_1)
    db.session.add(date_entry_2)
    db.session.add(date_entry_3)
    db.session.add(date_entry_4)
    db.session.add(mycourse_entry_1)
    db.session.add(mycourse_entry_2)

    # Commit the changes
    db.session.commit()


