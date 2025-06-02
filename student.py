from utility import *


def get_student_name(student_id):
    statement = "CALL Get_Student_Name(" + str(student_id) + ")"
    return execute_read_statement(get_database_connection(), statement)


def get_student_class_periods(student_id):
    student_schedules = get_student_schedule(student_id)
    class_periods = []  # ensures only these classes are selected and returns false otherwise
    for student_schedule in student_schedules:
        class_periods.append(student_schedule[0])
    return class_periods


def get_student_schedule(student_id):       # desc: period, name of course, room, teacher
    statement = "CALL Select_Student('" + student_id + "')"
    return execute_read_statement(get_database_connection(), statement)


def get_student_grades(student_id, period):    # desc: grade, assignment_name, assignment_type, course_type
    statement = "CALL Select_Grades(" + str(student_id) + ", " + str(period) + ")"
    # print(execute_statement(get_database_connection(), statement))
    return execute_read_statement(get_database_connection(), statement)

def calculate_course_average(student_id, period):
    grade_infos = get_student_grades(student_id, period)
    grades = []
    for gradeInfo in grade_infos:
        grades.append(gradeInfo[0])
    return calculate_average(grades)


def print_student_grades(results, id_num, chosen_period):   # TODO: FIGURE OUT IF THERE's SOMETHING WRONG HERE
    print("Course: ", results[chosen_period - 1][1])
    course_average = calculate_course_average(id_num, chosen_period)
    print("Course Average: ", round(course_average, 2))
    print("----------------" + dash_buffer(str(round(course_average, 2))))

    grade_infos = get_student_grades(id_num, chosen_period)
    # desc for grade_infos: grade, assignment name, assignment type, course type

    grade_infos.reverse()

    for gradeInfo in grade_infos:
        print(gradeInfo[1], ": ", gradeInfo[0])
    print()