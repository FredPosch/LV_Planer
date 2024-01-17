from app import app, db, Courses, Dates, MyCourses, CalendarTable
from datetime import datetime

def print_courses():
    # display the names of the first 4 courses in the course table in the terminal
    with app.app_context():
        courses = Courses.query.all()
        for course in courses:
            print(course.Code_LV)
            print(course.Lecturer)
            print(course.Title)
            print(course.LectureType)
            print(course.Semester)
            print(course.Faculty)
            print(course.Level)
            print(course.ECTS)
            print(course.Language)
            print(course.Prerequisites)
            print(course.Link)
            print("\n")
        dates = Dates.query.all()
        for date in dates:
            print(date.Code_LV)
            print(date.Lecture_Start)
            print(date.Lecture_End)
            print(date.Room)
            print("\n")
        mycourses = MyCourses.query.all()
        for mycourse in mycourses:
            print(mycourse.Code_LV)
            print("\n")
        calendartable = CalendarTable.query.all()
        for calendarentry in calendartable:
            print(calendarentry.Code_LV)
            print(calendarentry.Lecture_title)
            print(calendarentry.Lecture_Start)
            print(calendarentry.Lecture_End)
            print(calendarentry.Room)
            print("\n")

if __name__ == "__main__":
    print_courses()