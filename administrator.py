from utility import *

def add_student(student_id, course_offering_id):
    statement = "CALL Add_Student(" + str(student_id) + ", " + str(course_offering_id) + ")"
    return execute_statement(get_database_connection(), statement)


def remove_student(student_id, course_offering_id):
    statement = "CALL Remove_Student(" + str(student_id) + ", " + str(course_offering_id) + ")"
    return execute_statement(get_database_connection(), statement)


def add_class(course_offering_id, course_id, course_offering_room, teacher_id, period):
    statement = ("CALL Add_Student(" + str(course_offering_id) + ", " + str(course_id) +
                 course_offering_room + str(teacher_id) + str(period) + ")")
    return execute_statement(get_database_connection(), statement)

def get_course_offering_ids():
    statement = "CALL Get_Course_Offering_Ids()"
    return execute_statement(get_database_connection(), statement)

def get_student_schedule_ids(student_id):
    statement = "CALL Get_Student_Schedule( " + str(student_id) + " )"
    return execute_statement(get_database_connection(), statement)


def get_course_offering_assignment_ids(course_offering_id):
    statement = "CALL Get_Assignment_Ids( " + str(course_offering_id) + " )"
    return execute_statement(get_database_connection(), statement)