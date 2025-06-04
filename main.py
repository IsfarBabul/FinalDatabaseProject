import random

from teacher import *
from administrator import *



user_identity = ""
while user_identity != "quit":
    user_identity = ""
    possible_identities = ["student", "teacher", "administrator", "admin", "quit"]
    while not verify_user(user_identity, possible_identities):
        user_identity = input("Verify your identity for login. (teacher, student, or administrator) (Type 'quit' to exit the program) ")
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
                print()
                print("Main Menu")
                print("1: View your schedule")
                print("2: View your overall grade")
                print("3: View your grades for a specific class")
                print("4: Logout")
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
                    print()

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
                print("5: Logout")
                print("")
                while option < 1 or option > 5:
                    option = int(input("Choose an Option: "))
                print()

                if option == 1:      # TODO: ORDER OF SCHEDULES IS INCORRECT WHEN ADDING STUDENT TO A CLASS
                    results = get_teacher_schedule(id_num)
                    for result in results:
                        print("Period: ", result[1])
                        print("Course: ", result[2])
                        print("Room: ", result[3])
                        print()
                elif option == 2:
                    chosen_period = select_period()

                    grade_infos = get_class_grades(id_num, chosen_period)  # desc: grade, assignment_name, student_name, course_name, assignment_id

                    if len(grade_infos) != 0:
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
                    else:
                        print()
                        print("No grades to view!")
                        print()

                elif option == 3:
                    chosen_period = select_period()

                    grade_infos = get_class_grades(id_num, chosen_period)

                    if len(grade_infos) != 0:
                        update_grade_logic(grade_infos)
                    else:
                        print()
                        print("No grades to update!")
                        print()

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

                    course_offering_id = get_teacher_course_offering_id(id_num, chosen_period)[0][0]  # PIECE 4/4

                    add_assignment(new_assignment_id, new_assignment_name, new_assignment_type_id, course_offering_id)

                    # THE BELOW LOGIC IS TO GET THE STUDENT IDS OF AN ASSIGNMENT ASSUMING ALL ASSIGNMENTS GET THE SAME NUMBER OF GRADES FOR EACH STUDENT
                    # obtain names of each assignment
                    assignment_names = obtain_assignment_names(grade_infos)

                    # prints assignments in the course offering
                    # print_assignments(grade_infos, assignment_names)

                    # separate gradeInfos into each class
                    assignment_grades = parse_grades_into_assignments(grade_infos, assignment_names)

                    student_ids = []
                    unparsed_student_ids = get_student_ids_by_class(course_offering_id)
                    for student_id in unparsed_student_ids:
                        student_ids.append(student_id[0])

                    for student_id in student_ids:
                        add_assignment_grade(student_id, new_assignment_id)

                    if len(student_ids) == 0:
                        print()
                        print("Note: No assignments were actually added because there are no students in this class.")
                        print()





                if option != 5:
                    option = 0
                else:
                    print("Goodbye, " + teacher_name + "!")
                    print()

    elif user_identity == "admin" or user_identity == "administrator":
            print()
            print("Welcome, administrator!")
            print()

            option = 0

            while option != 5:

                print()
                print("Main Menu")
                print("1: Add a student to a class")
                print("2: Remove a student from a class")
                print("3: Create a new class")
                print("4: Add a student to the system")
                print("5: Logout")
                print("")
                while option < 1 or option > 5:
                    option = int(input("Choose an Option: "))
                print()

                if option == 1:

                    selected_student_id = input("Input a Student ID: ")

                    results = get_student_schedule(selected_student_id)

                    class_periods = []
                    for result in results:
                        class_periods.append(result[0])

                    if len(class_periods) < 10:

                        print()
                        if len(class_periods) != 0:
                            print("Period| Course Name")
                            for result in results:
                                print(f"{result[0]}| {result[1]}")
                        else:
                            print("This student has no classes yet.")
                        print()

                        specified_period = 0

                        while specified_period < 1 or specified_period > 10:
                            specified_period = int(input("Input a free period you want to add the student to: "))
                            for result in results:
                                if result[0] == specified_period:
                                    specified_period = 0

                        course_offering_ids = []
                        course_names = []
                        listed_course_offering_ids = get_course_offering_ids(specified_period)
                        for listed_course_offering_id in listed_course_offering_ids:
                             course_offering_ids.append(listed_course_offering_id[1])
                             course_names.append(listed_course_offering_id[0])

                        print()
                        for i in range(len(course_offering_ids)):
                            print(f"{i + 1}: {course_names[i]} (id: {course_offering_ids[i]})")
                        print()

                        # SHOULD PRINT OUT CLASSES AND THEIR COURSE_OFFERING_ID THAT THE STUDENT IS IN

                        # COULD FILTER BASED ON PERIOD, COURSE TYPE, COURSE, AND THEN SELECT THE CLASS TO ADD THE STUDENT IN

                        course_offering_option = 0
                        while course_offering_option < 1 or course_offering_option > len(course_offering_ids):
                            course_offering_option = int(input("Input the number of your target course offering: "))
                        course_offering_option -= 1

                        # TODO: FIX IT WHEN YOU GET BACK IT BREAKS HERE

                        specified_course_offering_id = course_offering_ids[course_offering_option]

                        add_student(selected_student_id, specified_course_offering_id)

                        for assignment_id in get_course_offering_assignment_ids(specified_course_offering_id):
                            add_assignment_grade(selected_student_id, assignment_id[0])
                    else:
                        print()
                        print("This student has a full schedule.")
                        print()

                elif option == 2:
                    selected_student_id = input("Input a Student ID: ")

                    student_course_offerings = get_student_course_offerings(selected_student_id) # desc: course_offering_id, course_name, period

                    print()
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
                        remove_assignment_grade(selected_student_id, assignment_id[0])

                elif option == 3:
                    determined_course_offering_id = 0
                    specified_course_id = 0
                    determined_course_offering_room = ""
                    determined_teacher_id = 0
                    specified_period = 0

                    # find the specified period
                    while specified_period < 1 or specified_period > 10:
                        specified_period = int(input("Input the period you want this class to be in: "))    # PIECE 1/5

                    course_offering_infos = get_course_offering_general_info(specified_period) # desc: course_offering_id, course_offering_room, teacher_id

                    # find an available room

                    all_possible_rooms = get_all_room_numbers()

                    all_available_rooms = []

                    all_rooms = ""

                    for room in all_possible_rooms:
                        # print("together forever")
                        room_found = False
                        for course_offering_info in course_offering_infos:
                            if room == course_offering_info[1]:
                                room_found = True
                        if not room_found:
                            all_available_rooms.append(room)

                    random_room_id_index = random.randint(0, len(all_available_rooms) - 1)

                    determined_course_offering_room = all_available_rooms[random_room_id_index]    # PIECE 2/5
                    # print(determined_course_offering_room)

                    # find a random available teacher

                    arrayed_teacher_ids = get_teacher_ids()   # actually comes in array with 1 element arrays

                    all_teacher_ids = []

                    for arrayed_teacher_id in arrayed_teacher_ids:
                        all_teacher_ids.append(arrayed_teacher_id[0])   # picks the only element in each array called arrayed_teacher_id

                    all_available_teachers = []

                    for teacher_id in all_teacher_ids:
                        teacher_found = False
                        for course_offering_info in course_offering_infos:
                            if teacher_id == course_offering_infos[2]:
                                teacher_found = True
                        if not teacher_found:
                            all_available_teachers.append(teacher_id)

                    random_teacher_id_index = random.randint(0, len(all_available_teachers) - 1)   # picks out a random index for all_available_teachers

                    determined_teacher_id = all_available_teachers[random_teacher_id_index]    # PIECE 3/5
                    # print(determined_teacher_id)

                    # determine a new course_offering_id for the class

                    all_existing_course_offering_ids = []

                    all_course_offering_infos = get_all_course_offering_general_info()

                    for course_offering_ids in all_course_offering_infos:
                        all_existing_course_offering_ids.append(course_offering_ids[0])

                    # print(max(all_existing_course_offering_ids))
                    # print(all_existing_course_offering_ids)

                    determined_course_offering_id = max(all_existing_course_offering_ids) + 1   # PIECE 4/5
                    # print(determined_course_offering_id)

                    # ask the user for the name of the course they are adding a class for

                    courses_info = get_courses_info()   # desc: course_id, course_name, course_type_id


                    print()
                    for i in range(len(courses_info)):
                        print(f"{i + 1}: {courses_info[i][1]}")
                    print()

                    specified_course_option = 0

                    while specified_course_option < 1 or specified_course_option > len(courses_info):
                        specified_course_option = int(input("Input the the number next to the name of the course you want to add: "))

                    specified_course_id = courses_info[specified_course_option - 1][0]   # PIECE 5/5
                    # print(specified_course_id)


                    # we will use all five pieces of information we obtained to add the class

                    #             PIECE 4/5                     PIECE 5/5               PIECE 2/5                      PIECE 3/5              PIECE 1/5
                    add_class(determined_course_offering_id, specified_course_id, determined_course_offering_room, determined_teacher_id, specified_period)

                    # get the teacher's name
                    determined_teacher_name = ""
                    for arrayed_teacher_id in arrayed_teacher_ids:
                        if arrayed_teacher_id[0] == determined_teacher_id:
                            determined_teacher_name = arrayed_teacher_id[1]

                    print()
                    print("Class added!")
                    print()
                    print("Class Info")
                    print(dash_buffer("Class Info"))
                    print(f"Course Offering ID: {determined_course_offering_id}")
                    print(f"Course Name: {courses_info[specified_course_option - 1][1]}")
                    print(f"Room: {determined_course_offering_room}")
                    print(f"Teacher: {determined_teacher_name}")
                    print(f"Period: {specified_period}")
                    print()
                elif option == 4:
                    student_name = ""
                    while student_name == "":
                        student_name = input("What is the name of the student you want to add? ")

                    add_student_to_system(student_name)



                if option != 5:
                    option = 0
                else:
                    print("Goodbye, administrator!")
                    print()

