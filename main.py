import mysql.connector

# -------------PART 0: Utility Functions-------------------


def get_database_connection():
    connection = mysql.connector.connect(user='isfarb2',
                                   password='222499881',
                                   host='10.8.37.226',
                                   database='isfarb2_db')
    return connection


def execute_statement(connection, statement):
    cursor = connection.cursor()
    cursor.execute(statement)
    results = []

    for row in cursor:
        results.append(row)

    cursor.close()
    connection.close()

    return results


# check if the user inputted a correct identity
def verify_user(claimed_identity, possible_identities):
    for possible_identity in possible_identities:
        if claimed_identity == possible_identity:
            return True
    return False


def get_student_class_names(student_id):
    student_schedules = get_student_schedule(student_id)
    student_classes = []  # ensures only these classes are selected and returns false otherwise
    for student_schedule in student_schedules:
        student_classes.append(student_schedule[1])
    return student_classes


def get_student_class_periods(student_id):
    student_schedules = get_student_schedule(student_id)
    class_periods = []  # ensures only these classes are selected and returns false otherwise
    for student_schedule in student_schedules:
        class_periods.append(student_schedule[0])
    return class_periods


def verify_class(student_classes, selection):
    for student_class in student_classes:
        if student_class == selection:
            return True
    return False


def calculate_average(array):
    sum_of_nums = 0
    for element in array:
        sum_of_nums += element
    return sum_of_nums / len(array)


def dash_buffer(string):
    dash_buffer = ""
    for i in range(len(string)):
        dash_buffer += "-"
    return dash_buffer


def get_student_name(student_id):
    statement = "CALL Get_Student_Name(" + str(student_id) + ")"
    return execute_statement(get_database_connection(), statement)


def get_teacher_name(teacher_id):
    statement = "CALL Get_Teacher_Name(" + str(teacher_id) + ")"
    return execute_statement(get_database_connection(), statement)


# -------------PART 1: Read Only Operations-------------------


def get_student_schedule(student_id):       # desc: period, name of course, room, teacher
    statement = "CALL Select_Student('" + student_id + "')"
    return execute_statement(get_database_connection(), statement)


def get_student_grades(student_id, period):    # desc: grade, assignment_name, assignment_type, course_type
    statement = "CALL Select_Grades(" + str(student_id) + ", " + str(period) + ")"
    return execute_statement(get_database_connection(), statement)

def calculate_course_average(student_id, period):
    gradeInfos = get_student_grades(student_id, period)
    grades = []
    for gradeInfo in gradeInfos:
        grades.append(gradeInfo[0])
    return calculate_average(grades)

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


# -------------PART 2: Update Operations for Teachers-------------------
def update_grade(student_id, specific_class, assignment_name):
    print("TODO")


def add_assignment(specific_class):
    print("TODO")

# -------------PART 3: Update Operations for Administrators-------------------

def add_student(specific_class):
    print("TODO")


def remove_assignment(specific_class):
    print("TODO")


def add_class():
    print("WARNING: THIS IS MEGA HARD")


# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------
# -------MAIN PROJECT-------------------------------------------------------------------------


user_identity = ""
possible_identities = ["student", "teacher", "administrator"]
while not verify_user(user_identity, possible_identities):
    user_identity = input("What is your identity? (teacher, student, or administrator) ")
    user_identity = user_identity.lower()
    print()

if user_identity == "student" or user_identity == "teacher":
    id_num = input("Enter your ID: ")

    if user_identity == "student":
        student_name = get_student_name(id_num)[0][0]

        print()
        print("Welcome, " + student_name + "!")
        print()

        option = 0

        while option != 4:

            print("Main Menu")
            print("1: View your schedule")
            print("2: View your overall grade")
            print("3: View your grades for a specific class")
            print("4: Quit the program")
            print("")
            while option < 1 or option > 4:
                option = int(input("Choose an Option: "))
            print()

            if option == 1:
                results = get_student_schedule(id_num)
                for result in results:
                    print("Period: ", result[0])
                    print("Course: ", result[1])
                    print("Room: ", result[2])
                    print("Teacher: ", result[3])
                    print("Course Average: ", round(calculate_course_average(id_num, result[0]), 2))
                    print()
                option = 0
            elif option == 2:
                print("Your overall grade is: " + str(round(get_student_overall_grade(id_num), 2)))
                print()
                option = 0
            elif option == 3:
                results = get_student_schedule(id_num)
                select_period = -1
                while select_period < 0 or select_period > 10:
                    select_period = int(input("Input the period of the class to inspect: "))
                print()
                print("Course: ", results[select_period - 1][1])

                course_average = calculate_course_average(id_num, select_period)
                print("Course Average: ", round(course_average, 2))
                print("----------------" + dash_buffer(str(round(course_average, 2))))
                grade_infos = get_student_grades(id_num,
                                                 select_period)  # desc: grade, assignment name, assignment type, course type
                grade_infos.reverse()

                for gradeInfo in grade_infos:
                    print(gradeInfo[1], ": ", gradeInfo[0])
                print()
                option = 0
            else:
                print("Goodbye, " + student_name + "!")
    elif user_identity == "teacher":
        teacher_name = get_teacher_name(id_num)[0][0]

        print()
        print("Welcome, " + teacher_name + "!")
        print()

        option = 0

        while option != 5:

            print("Main Menu")
            print("1: View your schedule")
            print("2: View your student's grades")
            print("3: Update a grade")
            print("4: Add an assignment")
            print("5: Quit the program")
            print("")
            while option < 1 or option > 5:
                option = int(input("Choose an Option: "))
            print()

            if option == 1:
                results = get_teacher_schedule(id_num)
                for result in results:
                    print("Period: ", result[1])
                    print("Course: ", result[2])
                    print("Room: ", result[3])
                    print()
                option = 0
            elif option == 2:
                select_period = -1
                while select_period < 1 or select_period > 10:
                    select_period = int(input("Input the period of the class you want to look at the grades for: "))

                grade_infos = get_class_grades(id_num, select_period)  # desc: grade, assignment_name, student_name, course_name

                print("Course Name: " + grade_infos[0][3])
                print("-------------" + dash_buffer(grade_infos[0][3]))

                # obtain names of each assignment
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

                # separate gradeInfos into each class
                assignment_grades = []
                for i in range(len(assignment_names)):
                    assignment_grades.append([])

                for grade_info in grade_infos:
                    for i in range(len(assignment_names)):
                        if assignment_names[i] == grade_info[1]:
                            assignment_grades[i].append(grade_info)

                for i in range(len(assignment_names)):
                    print(str(i + 1) + ": " + assignment_names[i])
                print()

                select_assignment_option = 0
                while select_assignment_option < 1 or select_assignment_option > len(grade_infos):
                    select_assignment_option = int(
                        input("Input the number of the assignment you want to look at your student's grades for: "))
                select_assignment_option -= 1

                print("Assignment Name: " + grade_infos[select_assignment_option][1])
                print("-----------------" + dash_buffer(grade_infos[select_assignment_option][1]))

                for grade_info in assignment_grades[select_assignment_option]:
                    print(grade_info[2], ": ", grade_info[0])
                option = 0
    else:
        print()
        print("Welcome, administrator!")
        print()

        option = 0

        while option != 4:

            print("Main Menu")
            print("1: Add a student")
            print("2: Remove a student")
            print("3: Create a new class")
            print("4: Quit the program")
            print("")
            while option < 1 or option > 4:
                option = int(input("Choose an Option: "))
            print()


