from utility import *

def add_student(student_id, course_offering_id):
    statement = "CALL Add_Student(" + str(student_id) + ", " + str(course_offering_id) + ")"
    return execute_statement(get_database_connection(), statement)


def remove_student(student_id, course_offering_id):
    statement = "CALL Remove_Student(" + str(student_id) + ", " + str(course_offering_id) + ")"
    return execute_statement(get_database_connection(), statement)


def add_class(course_offering_id, course_id, course_offering_room, teacher_id, period):
    statement = ("CALL Add_Class(" + str(course_offering_id) + ", " + str(course_id) + ", '" + course_offering_room + "', " + str(teacher_id) + ", " + str(period) + ")")
    print(statement)
    return execute_statement(get_database_connection(), statement)

def get_course_offering_ids():
    statement = "CALL Get_Course_Offering_Ids()"
    return execute_statement(get_database_connection(), statement)

def get_student_course_offerings(student_id):
    statement = "CALL Get_Student_Course_Offerings( " + str(student_id) + " )"
    return execute_statement(get_database_connection(), statement)


def get_course_offering_assignment_ids(course_offering_id):
    statement = "CALL Get_Course_Offering_Assignment_Ids( " + str(course_offering_id) + " )"
    return execute_statement(get_database_connection(), statement)

def get_course_offering_general_info(specified_period):
    statement = "CALL Get_Course_Offering_General_Info(" + str(specified_period) + ")"
    print(statement)
    print("CALL Get_Course_Offering_General_Info(3);")
    return execute_statement(get_database_connection(), statement)

def get_courses_info():
    statement = "CALL Get_Courses_Info()"
    return execute_statement(get_database_connection(), statement)

def get_teacher_ids():
    statement = "CALL Get_All_Teacher_Ids()"
    return execute_statement(get_database_connection(), statement)

def get_all_room_numbers():
    room_wings = ["N", "E", "S", "W"]
    floor_numbers = ["B", "1", "2", "3", "4", "5", "6", "7", "8"]
    all_room_numbers = []

    for floor_number in floor_numbers:
        for room_wing in room_wings:
            for i in range(20):
                zero_pad = ""
                if i + 1 < 10:
                    zero_pad = "0"
                all_room_numbers.append(floor_number + room_wing + zero_pad + str(i + 1))
    return all_room_numbers