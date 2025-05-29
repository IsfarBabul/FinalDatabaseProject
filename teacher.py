from student import *
from utility import *


def get_teacher_name(teacher_id):
    statement = "CALL Get_Teacher_Name(" + str(teacher_id) + ")"
    return execute_statement(get_database_connection(), statement)



def get_student_class_names(student_id):
    student_schedules = get_student_schedule(student_id)
    student_classes = []  # ensures only these classes are selected and returns false otherwise
    for student_schedule in student_schedules:
        student_classes.append(student_schedule[1])
    return student_classes




def get_student_overall_grade(student_id):
    class_periods = get_student_class_periods(student_id)
    grades_in_each_class = []
    for i in range(len(class_periods)):
        grades_in_each_class.append(get_student_grades(student_id, class_periods[i]))      #find all their grades in each class (also contains assignment name and type as well as course type

    average_grades_in_each_class = []
    for grades_in_one_class in grades_in_each_class:
        minor_grades = []
        major_grades = []
        for grade in grades_in_one_class:
            if grade[2].lower() == 'minor':
                major_grades.append(grade[0])
            else:
                minor_grades.append(grade[0])
        average = calculate_average(minor_grades) * 0.3 + calculate_average(major_grades) * 0.7
        if grades_in_one_class[0][3] == "AP":
            average *= 1.1      # AP classes have 110% weighting
        average_grades_in_each_class.append(average)

    return calculate_average(average_grades_in_each_class)


def get_teacher_schedule(teacher_id):
    statement = "CALL Select_Teacher('" + teacher_id + "')"
    return execute_statement(get_database_connection(), statement)


def get_class_grades(teacher_id, period):    # ask later: assignment_name_option
    statement = "CALL Select_Assignments(" + str(teacher_id) + ", " + str(period) + ")"
    return execute_statement(get_database_connection(), statement)


def obtain_assignment_names(grade_infos):
    assignment_names = []
    for grade_info in grade_infos:
        if len(assignment_names) != 0:
            isThere = False
            for assignment_name in assignment_names:
                if assignment_name == grade_info[1]:
                    isThere = True
            if not isThere:
                assignment_names.append(grade_info[1])
        else:
            assignment_names.append(grade_info[1])
    return assignment_names


def parse_grades_into_assignments(grade_infos, assignment_names):
    assignment_grades = []
    for i in range(len(assignment_names)):
        assignment_grades.append([])

    for grade_info in grade_infos:
        for i in range(len(assignment_names)):
            if assignment_names[i] == grade_info[1]:
                assignment_grades[i].append(grade_info)
    return assignment_grades


def print_assignments(grade_infos, assignment_names):
    print("Course Name: " + grade_infos[0][3])
    print("-------------" + dash_buffer(grade_infos[0][3]))

    for i in range(len(assignment_names)):
        print(str(i + 1) + ": " + assignment_names[i])
    print()



def select_assignment(grade_infos):
    select_assignment_option = 0
    while select_assignment_option < 1 or select_assignment_option > len(grade_infos):
        select_assignment_option = int(
            input("Input the number of your target assignment: "))
    select_assignment_option -= 1
    return select_assignment_option


def print_grades(grade_infos, select_assignment_option, assignment_grades):
    print("Assignment Name: " + grade_infos[select_assignment_option][1])
    print("-----------------" + dash_buffer(grade_infos[select_assignment_option][1]))

    for grade_info in assignment_grades[select_assignment_option]:
        print(grade_info[2], " (id: " + str(grade_info[5]) + "): ", grade_info[0])

def select_student():   # no clear way to deal with error handling
    selected_student_id = int(input("Input Student ID: "))
    return selected_student_id

def prompt_new_grade():
    new_grade = 0
    while new_grade < 75 or new_grade > 100:
        new_grade = int(input("Input the updated grade (75-100): "))
    return new_grade


def update_grade(assignment_id, student_id, course_offering_id, updated_grade):
    statement = "CALL Update_Grade(" + str(assignment_id) + ", " + str(student_id) + ", " + str(course_offering_id) + ", " + str(updated_grade) + ")"
    print(statement)
    print(f"{assignment_id} {student_id} {course_offering_id} {updated_grade}")
    return execute_statement(get_database_connection(), statement)


def add_assignment(assignment_id, assignment_name, assignment_type_id, course_offering_id):
    statement = "CALL Add_Assignment(" + str(assignment_id) + ", " + assignment_name + ", " + str(assignment_type_id) + ", " + str(course_offering_id) + ")"
    return execute_statement(get_database_connection(), statement)


def add_assignment_grade(student_id, assignment_id):
    statement = "CALL Add_Assignment_Grade(" + str(student_id) + ", " + str(assignment_id) + ")"
    return execute_statement(get_database_connection(), statement)


def get_assignment_ids():
    statement = "CALL Get_Assignment_Ids()"
    return execute_statement(get_database_connection(), statement)