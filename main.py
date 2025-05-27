from teacher import *
from administrator import *




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
                assignment_names = obtain_assignment_names(grade_infos)

                # separate gradeInfos into each class
                assignment_grades = parse_grades_into_assignments(grade_infos, assignment_names)

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


