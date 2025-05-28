
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

                select_student_id = select_student()    # PIECE 3/4

                updated_grade = prompt_new_grade()      # PIECE 4/4

                print("reached")

                print(f"{select_assignment_id} {select_student_id} {select_course_offering_id} {updated_grade}")

                # updates the grade accordingly
                update_grade(select_student_id, select_course_offering_id, select_assignment_id, updated_grade)
            elif option == 4:
                chosen_period = select_period()

                grade_infos = get_class_grades(id_num, chosen_period)

                existing_assignment_ids = []

                # create a pool of existing assignment_ids
                for grade_info in grade_infos:
                    found = False    # tracks if we find the same id in our pool of existing ids
                    for existing_assignment_id in existing_assignment_ids:
                        if existing_assignment_id == grade_info[4]:      # we don't add the same id so if found then we add nothing
                            found = True
                    if not found:
                        existing_assignment_ids.append(grade_info[4])     # if not found then we know the appending id is different from all others

                new_assignment_id = 0                # PIECE 1/4 once the below code runs
                found = True
                while found:
                    new_assignment_id += 1
                    identified = False    # tracks if we located same course_offering_id
                    for grade_info in grade_infos:
                        for existing_assignment_id in existing_assignment_ids:
                            if existing_assignment_id == new_assignment_id:     # compare if a certain existing id matches with a new id we're attempting to use
                                identified = True     # if located then found remains True
                    if not identified:
                        found = False    # if not located then found is false which breaks the loop

                new_assignment_name = ""  # PIECE 2/4
                while new_assignment_name == "":
                    new_assignment_name = input("What will the name of this assignment be? ")

                new_assignment_type_id = 0    # PIECE 3/4
                while new_assignment_type_id != 1 and new_assignment_type_id != 2:
                    new_grade = int(input("Input 1 for minor assignment or 2 for major assignment: "))


                course_offering_id = grade_infos[0][6]  # PIECE 4/4      the use of 0 as the index is arbitrary but there has to be at least one grade info if we're here so it's the best candidate to use

                add_assignment(new_assignment_id, new_assignment_name, new_assignment_type_id, course_offering_id)

                # THE BELOW LOGIC IS TO GET THE STUDENT IDS OF AN ASSIGNMENT ASSUMING ALL ASSIGNMENTS GET THE SAME NUMBER OF GRADES FOR EACH STUDENT
                # obtain names of each assignment
                assignment_names = obtain_assignment_names(grade_infos)

                # prints assignments in the course offering
                print_assignments(grade_infos, assignment_names)

                # separate gradeInfos into each class
                assignment_grades = parse_grades_into_assignments(grade_infos, assignment_names)

                student_ids = []
                for grade_info in assignment_grades[0]: # again 0 is arbitrary but is the best number to use since there has to be at least 1 assignment
                    student_ids.append(grade_info[5])

                for student_id in student_ids:
                    add_assignment_grade(student_id, new_assignment_id)





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

