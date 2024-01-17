# imports
from icalendar import Calendar, Event, vCalAddress, vText
from datetime import datetime
from pathlib import Path
import os
import pytz
from app import app, db, CalendarTable, Courses, Dates, MyCourses
from calendar_creation import create_calendar_table

def create_calendar_table():
    # Create the calendar table
    with app.app_context():
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
    with app.app_context():
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
    with app.app_context():
        CalendarTable.query.delete()
        db.session.commit()