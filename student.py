from utility import execute_statement
from utility import get_database_connection




def get_student_name(student_id):
    statement = "CALL Get_Student_Name(" + str(student_id) + ")"
    return execute_statement(get_database_connection(), statement)


def get_student_class_periods(student_id):
    student_schedules = get_student_schedule(student_id)
    class_periods = []  # ensures only these classes are selected and returns false otherwise
    for student_schedule in student_schedules:
        class_periods.append(student_schedule[0])
    return class_periods


def get_student_schedule(student_id):       # desc: period, name of course, room, teacher
    statement = "CALL Select_Student('" + student_id + "')"
    return execute_statement(get_database_connection(), statement)


def get_student_grades(student_id, period):    # desc: grade, assignment_name, assignment_type, course_type
    statement = "CALL Select_Grades(" + str(student_id) + ", " + str(period) + ")"
    return execute_statement(get_database_connection(), statement)

