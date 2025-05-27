import mysql.connector
from student import *


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


def calculate_average(array):
    sum_of_nums = 0
    for element in array:
        sum_of_nums += element
    return sum_of_nums / len(array)

def calculate_course_average(student_id, period):
    gradeInfos = get_student_grades(student_id, period)
    grades = []
    for gradeInfo in gradeInfos:
        grades.append(gradeInfo[0])
    return calculate_average(grades)


def dash_buffer(string):
    dash_buffer = ""
    for i in range(len(string)):
        dash_buffer += "-"
    return dash_buffer