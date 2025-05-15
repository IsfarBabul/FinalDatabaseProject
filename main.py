import mysql.connector


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


def get_student_schedule(student_id):
    statement = "CALL Select_Student('" + student_id + "')"
    return execute_statement(get_database_connection(), statement)


def get_teacher_schedule(teacher_name):
    statement = "CALL Select_Teacher('" + teacher_name + "')"
    return execute_statement(get_database_connection(), statement)


userIdentity = ""
while userIdentity != "student" and userIdentity != "teacher":
    userIdentity = input("What is your identity? (teacher or student)")
    userIdentity = userIdentity.lower()
    print()

if userIdentity == "student":
    student_id = input("Enter a student ID: ")
    results = get_student_schedule(student_id)

    for result in results:
        print("Period: ", result[0])
        print("Course: ", result[1])
        print("Room: ", result[2])
        print("Teacher: ", result[3])
        print()
else:
    teacher_name = input("Enter a teacher name: ")
    results = get_teacher_schedule(teacher_name)
    for result in results:
        print("Period: ", result[0])
        print("Course: ", result[1])
        print("Room: ", result[2])
        print()





