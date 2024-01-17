from flask import Flask, render_template, url_for, request, redirect, send_file
from icalendar import Calendar, Event, vCalAddress, vText
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pathlib import Path
import os
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class MyCourses(db.Model):
    __tablename__ = 'my_courses'
    id = db.Column(db.Integer, primary_key=True)
    Code_LV = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<MyCourses %r>' % self.id

class CalendarTable(db.Model):
    __tablename__ = 'calendar_table'
    id = db.Column(db.Integer, primary_key=True)
    Code_LV = db.Column(db.String(200), nullable=False)
    Lecture_title = db.Column(db.String(200), nullable=False)
    Lecture_Start = db.Column(db.DateTime, nullable=False)
    Lecture_End = db.Column(db.DateTime, nullable=False)
    Room = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<CalendarTable %r>' % self.id  
    
class Courses(db.Model):
    __tablename__ = 'courses'
    Code_LV = db.Column(db.String(200), primary_key=True)
    Lecturer = db.Column(db.String(200), nullable=False)
    Title = db.Column(db.String(200), nullable=False)
    LectureType = db.Column(db.String(200), nullable=False)
    Semester = db.Column(db.String(200), nullable=False)
    Faculty = db.Column(db.String(200), nullable=False)
    Level = db.Column(db.String(200), nullable=False)
    ECTS = db.Column(db.Integer, nullable=False)
    Language = db.Column(db.String(200), nullable=False)
    Prerequisites = db.Column(db.String(200), nullable=False)
    Link = db.Column(db.String(200), nullable=False)
    

    def __repr__(self):
        return '<Courses %r>' % self.Code_LV
    
class Dates(db.Model):
    __tablename__ = 'dates'
    id = db.Column(db.Integer, primary_key=True)
    Code_LV = db.Column(db.String(200), nullable=False)
    Lecture_Start = db.Column(db.DateTime, nullable=False)
    Lecture_End = db.Column(db.DateTime, nullable=False)
    Room = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Dates %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        my_courses = request.form['Code_LV']
        new_course = MyCourses(Code_LV=my_courses)

        try:
            db.session.add(new_course)
            db.session.commit()
            return redirect('/')
        except:
            'There was an issue adding your task'
    else:
        tasks = MyCourses.query.order_by(MyCourses.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    courses_to_remove = MyCourses.query.get_or_404(id)

    try:
        db.session.delete(courses_to_remove)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error deleting the course'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = MyCourses.query.get_or_404(id)

    if request.method == 'POST':
        task.Code_LV = request.form['Code_LV']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your Course List'
    else:
        return render_template('update.html', task=task)



@app.route('/create_calendar', methods=['POST'])
def create_calendar():
    # Your calendar creation script here
    unique_code_lv_list = db.session.query(MyCourses.Code_LV).distinct().all()

    for code_lv_tuple in unique_code_lv_list:
        code_lv = code_lv_tuple[0]

        # Query the corresponding title from Courses
        course_info = Courses.query.filter_by(Code_LV=code_lv).first()

        if course_info:
            # Query dates for the course from Dates
            dates_list = Dates.query.filter_by(Code_LV=code_lv).all()

            # Insert entries into CalendarTable
            for date_entry in dates_list:
                calendar_entry = CalendarTable(
                    Code_LV=code_lv,
                    Lecture_title=course_info.Title,
                    Lecture_Start=date_entry.Lecture_Start,
                    Lecture_End=date_entry.Lecture_End,
                    Room=date_entry.Room
                )

                db.session.add(calendar_entry)
    db.session.commit()

    # init the calendar
    cal = Calendar()

    # Create a calendar called "MyLectures"
    cal.add('prodid', '-//MyLectures//')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'MyLectures')

    # get all rows in Calendar table
    calendar_rows = CalendarTable.query.all()

    for row in calendar_rows:

        # create inputs
        calevent_title = row.Lecture_title
        calevent_start = row.Lecture_Start
        calevent_end = row.Lecture_End
        calevent_location = row.Room

        # Add subcomponents
        event = Event()
        event.add('summary', calevent_title)
        event.add('dtstart', calevent_start)
        event.add('dtend', calevent_end)
        event['location'] = calevent_location
        
        # Add the event to the calendar
        cal.add_component(event)
    # Convert the calendar to the iCalendar format
    cal_content = cal.to_ical()

    # Write the calendar to a file
    with open('MyLectures.ics', 'wb') as f:
        f.write(cal_content)

    # delete all content in CalendarTable
    CalendarTable.query.delete()
    db.session.commit()
    # After creating the calendar, render the display_calendar.html template
    return render_template('display_calendar.html')


@app.route('/download_calendar')
def download_calendar():
    return send_file('MyLectures.ics', as_attachment=True)

@app.route('/go_to_main_page')
def main_page():
    # Delete all rows from CalendarTable
    CalendarTable.query.delete()
    # Commit the changes to the database
    db.session.commit()

    tasks = MyCourses.query.order_by(MyCourses.date_created).all()
    return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
