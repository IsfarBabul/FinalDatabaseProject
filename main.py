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

            elif option == 2:
                print("Your overall grade is: " + str(round(get_student_overall_grade(id_num), 2)))

            elif option == 3:
                results = get_student_schedule(id_num)
                chosen_period = select_period()

                print_student_grades(results, id_num, chosen_period)

            if option != 4:
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

            print("")
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
            elif option == 2:
                chosen_period = select_period()

                grade_infos = get_class_grades(id_num, chosen_period)  # desc: grade, assignment_name, student_name, course_name

                # obtain names of each assignment
                assignment_names = obtain_assignment_names(grade_infos)

                # prints assignments in the course offering
                print_assignments(grade_infos, assignment_names)

                # separate gradeInfos into each class
                assignment_grades = parse_grades_into_assignments(grade_infos, assignment_names)

                # specify an assignment the user wants
                select_assignment_option = select_assignment(grade_infos)

                # prints grades of each student that has this assignment
                print_grades(grade_infos, select_assignment_option, assignment_grades)
            elif option == 3:
                chosen_period = select_period()

                grade_infos = get_class_grades(id_num, chosen_period)

                # obtain names of each assignment
                assignment_names = obtain_assignment_names(grade_infos)

                # prints assignments in the course offering
                print_assignments(grade_infos, assignment_names)

                # separate gradeInfos into each class
                assignment_grades = parse_grades_into_assignments(grade_infos, assignment_names)

                # specify an assignment the user wants
                select_assignment_option = select_assignment(grade_infos)

                # prints grades of each student that has this assignment
                print_grades(grade_infos, select_assignment_option, assignment_grades)

                # the pieces for updating the grade are below
                select_course_offering_id = grade_infos[select_assignment_option][6]  #PIECE 1/4

                select_assignment_id = grade_infos[select_assignment_option][4]      # PIECE 2/4

                select_student_id = select_student(grade_infos[select_assignment_option])    # PIECE 3/4

                updated_grade = prompt_new_grade()      # PIECE 4/4

                # updates the grade accordingly
                update_grade(select_student_id, select_course_offering_id, select_assignment_id, updated_grade)
            elif option == 4:
                chosen_period = select_period()

                grade_infos = get_class_grades(id_num, chosen_period)




            if option != 5:
                option = 0
            else:
                print("Goodbye, " + teacher_name + "!")
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

            if option != 4:
                option = 0
            else:
                print("Goodbye, administrator!")

