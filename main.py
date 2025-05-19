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


# -------------PART 1: Read Only Operations-------------------
def get_student_schedule(student_id):
    statement = "CALL Select_Student('" + student_id + "')"
    return execute_statement(get_database_connection(), statement)

def get_student_grades(student_id, specific_class):
    print("TODO")

def get_student_overall_grade(student_id):
    print("TODO; multiply major assessments by 0.7; multiply minor assessments by 0.3; multiply AP class grades by 1.1")

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





