from app import db, Dates, MyCourses, CalendarTable, Courses

# print all the courses from the Dates table

print(Dates.query.all())
print(MyCourses.query.all())
print(CalendarTable.query.all())

