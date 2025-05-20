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


# -------------PART 1: Read Only Operations-------------------


def get_student_schedule(student_id):       # desc: period, name of course, room, teacher
    statement = "CALL Select_Student('" + student_id + "')"
    return execute_statement(get_database_connection(), statement)


def get_student_grades(student_id, specific_class, period):    # desc: grade, assignment_name, assignment_type, course_type
    student_classes = get_student_class_names(student_id)
    class_found = False
    for student_class in student_classes:
        if specific_class == student_class:
            class_found = True
    if class_found:
        statement = "CALL Select_Grades(" + str(student_id) + ", '" + specific_class + "', " + str(period) + ")"
        return execute_statement(get_database_connection(), statement)
    else:
        return []


def get_student_overall_grade(student_id):
    class_names = get_student_class_names(student_id)   # obtain all class names of a given student
    class_periods = get_student_class_periods(student_id)
    grades_in_each_class = []
    for i in range(len(class_names)):
        grades_in_each_class.append(get_student_grades(student_id, class_names[i], class_periods[i]))      #find all their grades in each class (also contains assignment name and type as well as course type

    average_grades_in_each_class = []
    for grades_in_one_class in grades_in_each_class:
        sum_of_minor_grades = 0
        minor_grades_count = 0
        sum_of_major_grades = 0
        major_grades_count = 0
        avg_minor = 0
        avg_major = 0
        for grade in grades_in_one_class:
            if grade[2].lower() == 'minor':
                minor_grades_count += 1
                sum_of_minor_grades += grade[0]
            else:
                major_grades_count += 1
                sum_of_major_grades += grade[0]
        avg_minor = sum_of_minor_grades / minor_grades_count
        avg_major = sum_of_major_grades / major_grades_count
        average = avg_minor * 0.3 + avg_major * 0.7   # multiply minor by 0.3 and major by 0.7
        if grades_in_one_class[0][3] == "AP":
            average *= 1.1      # AP classes have 110% weighting
        average_grades_in_each_class.append(average)

    overall_grade = 0
    for average_grade in average_grades_in_each_class:
        overall_grade += average_grade
    return overall_grade / len(average_grades_in_each_class)


def get_teacher_schedule(teacher_id):
    statement = "CALL Select_Teacher('" + teacher_id + "')"
    return execute_statement(get_database_connection(), statement)

def get_class_grades(teacher_id, specific_class, assignment_name):
    print("TODO")


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


# -------MAIN PROJECT--------


user_identity = ""
possible_identities = ["student", "teacher", "administrator"]
while not verify_user(user_identity, possible_identities):
    user_identity = input("What is your identity? (teacher, student, or administrator) ")
    user_identity = user_identity.lower()
    print()

if user_identity == "student" or user_identity == "teacher":
    id_num = input("Enter your ID: ")

    if user_identity == "student":
        results = get_student_schedule(id_num)

        for result in results:
            print("Period: ", result[0])
            print("Course: ", result[1])
            print("Room: ", result[2])
            print("Teacher: ", result[3])
            print()

        print("Would you like to look at your grades for a specific course or your overall grade?")
        selection = input("(Type the word 'overall' for your overall grade or your class for a specific grade)")
        select_period = 0
        if selection.lower() != 'overall':
            while select_period < 1 or select_period > 10:
                select_period = int(input("Input the period (in case you have multiple periods of the same class):"))
        print(str(type(select_period)) + str(select_period))  #TEST
        print(str(type(selection)) + selection)     #TEST

        student_classes = []   # get a hold of all class names a student has
        for result in results:
            student_classes.append(result[1])

        while verify_class(student_classes, selection) and selection.lower() == 'overall':
            selection = input("(Type the word 'overall' for your overall grade or your class for specific grades)")

        if selection.lower() == 'overall':
            print("Your overall grade is: " + str(get_student_overall_grade(id_num)))
        else:
            print(id_num)
            print(selection)
            print(select_period)
            gradeInfos = get_student_grades(id_num, selection, select_period)  # desc: grade, assignment name, assignment type, course type
            print()
            print("Course: ", selection)
            sum_of_averages = 0
            for gradeInfo in gradeInfos:
                sum_of_averages += gradeInfo[0]
            course_average = sum_of_averages / len(gradeInfos)
            print("Course Average: ", course_average)
            print("---------")
            for gradeInfo in gradeInfos:
                print(gradeInfo[1], ": ", gradeInfo[0])


    else:
        results = get_teacher_schedule(id_num)
        print()
        print("Welcome " + results[0][0] + "!")
        print()
        for result in results:
            print("Period: ", result[1])
            print("Course: ", result[2])
            print("Room: ", result[3])
            print()





