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
    connection.commit()
    connection.close()

    return results


def execute_read_statement(connection, statement):
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

def select_period():
    period = -1
    while period < 1 or period > 10:
        period = int(input("Input your target period: "))
    return period

def calculate_average(array):
    sum_of_nums = 0
    for element in array:
        sum_of_nums += element
    return sum_of_nums / len(array)




def dash_buffer(string):
    buffer = ""
    for i in range(len(string)):
        buffer += "-"
    return buffer