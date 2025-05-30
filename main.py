
from teacher import *
from administrator import *




user_identity = ""
possible_identities = ["student", "teacher", "administrator", "admin"]
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

                grade_infos = get_class_grades(id_num, chosen_period)  # desc: grade, assignment_name, student_name, course_name, assignment_id

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

                assignment_ids = []
                for grade_info in grade_infos:
                    if len(assignment_ids) != 0:
                        isThere = False
                        for assignment_id in assignment_ids:
                            if assignment_id == grade_info[4]:
                                isThere = True
                        if not isThere:
                            assignment_ids.append(grade_info[4])
                    else:
                        assignment_ids.append(grade_info[4])

                select_assignment_id = assignment_ids[select_assignment_option]  # PIECE 2/4
                print(f"Assignment id: {select_assignment_id}")

                select_student_id = select_student()    # PIECE 3/4

                updated_grade = prompt_new_grade()      # PIECE 4/4

                print("reached")

                print(f"{select_assignment_id} {select_student_id} {select_course_offering_id} {updated_grade}")

                # updates the grade accordingly
                update_grade(select_assignment_id, select_student_id, select_course_offering_id, updated_grade)
            elif option == 4:
                chosen_period = select_period()

                grade_infos = get_class_grades(id_num, chosen_period)

                existing_assignment_ids = []

                unparsed_assignment_ids = get_assignment_ids()
                for unparsed_assignment_id in unparsed_assignment_ids:
                    existing_assignment_ids.append(unparsed_assignment_id[0])

                # print(existing_assignment_ids)
                # print(max(existing_assignment_ids))

                new_assignment_id = max(existing_assignment_ids) + 1

                print(new_assignment_id)

                new_assignment_name = ""  # PIECE 2/4
                while new_assignment_name == "":
                    new_assignment_name = input("What will the name of this assignment be? ")

                new_assignment_type_id = 0    # PIECE 3/4
                while new_assignment_type_id != 1 and new_assignment_type_id != 2:
                    new_assignment_type_id = int(input("Input 1 for minor assignment or 2 for major assignment: "))

                course_offering_id = grade_infos[0][6]  # PIECE 4/4      the use of 0 as the index is arbitrary but there has to be at least one grade info if we're here so it's the best candidate to use
                # TODO: DOES NOT WORK WHEN THERE ARE NO ASSIGNMENTS BECAUSE IT PULLS FROM GRADE INFOS

                add_assignment(new_assignment_id, new_assignment_name, new_assignment_type_id, course_offering_id)

                # THE BELOW LOGIC IS TO GET THE STUDENT IDS OF AN ASSIGNMENT ASSUMING ALL ASSIGNMENTS GET THE SAME NUMBER OF GRADES FOR EACH STUDENT
                # obtain names of each assignment
                assignment_names = obtain_assignment_names(grade_infos)

                # prints assignments in the course offering
                # print_assignments(grade_infos, assignment_names)

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
            print("1: Add a student to a class")
            print("2: Remove a student from a class")
            print("3: Create a new class")
            print("4: Quit the program")
            print("")
            while option < 1 or option > 4:
                option = int(input("Choose an Option: "))
            print()

            if option == 1:

                selected_student_id = input("Input a Student ID: ")

                course_offering_ids = []
                course_names = []
                listed_course_offering_ids = get_course_offering_ids()
                for listed_course_offering_id in listed_course_offering_ids:
                     course_offering_ids.append(listed_course_offering_id[1])
                     course_names.append(listed_course_offering_id[0])

                print()
                for i in range(len(course_offering_ids)):
                    print(f"{i + 1}: {course_names[i]} (id: {course_offering_ids[i]})")
                print()

                # SHOULD PRINT OUT CLASSES STUDENT IS IN
                # TODO: EXCLUDE THESE CLASS PERIODS SINCE THE STUDENT HAS A CLASS THERE ALREADY

                # TODO: FILTER BASED ON PERIOD, COURSE TYPE, COURSE, AND THEN SELECT THE CLASS TO ADD THE STUDENT IN

                course_offering_option = 0
                while course_offering_option < 1 or course_offering_option > len(course_offering_ids):
                    course_offering_option = int(input("Input the number of your target course offering: "))
                course_offering_option -= 1

                # TODO: FIX IT WHEN YOU GET BACK IT BREAKS HERE

                specified_course_offering_id = course_offering_ids[course_offering_option]

                add_student(selected_student_id, specified_course_offering_id)

                for assignment_id in get_course_offering_assignment_ids(specified_course_offering_id):
                    add_assignment_grade(selected_student_id, assignment_id)

            elif option == 2:
                selected_student_id = input("Input a Student ID: ")

                student_course_offerings = get_student_course_offerings(selected_student_id) # desc: course_offering_id, course_name, period

                print("Period| Course Name")
                print()
                for student_course_offering in student_course_offerings:
                    print(f"{student_course_offering[2]}| {student_course_offering[1]}")
                print()

                specified_period = 0

                while specified_period < 1 or specified_period > 10:
                    specified_period = int(input("Input the period of the class you want to remove the student from: "))

                target_course_offering_id = 0
                for student_course_offering in student_course_offerings:
                    if student_course_offering[2] == specified_period:
                        target_course_offering_id = student_course_offering[0]

                remove_student(selected_student_id, target_course_offering_id)

                assignment_ids = get_course_offering_assignment_ids(target_course_offering_id)

                for assignment_id in assignment_ids:
                    print(assignment_id)
                    remove_assignment_grade(selected_student_id, assignment_id[0])

            elif option == 3:
                determined_course_offering_id = 0
                specified_course_id = 0
                determined_course_offering_room = ""
                determined_teacher_id = 0
                specified_period = 0






            if option != 4:
                option = 0
            else:
                print("Goodbye, administrator!")

