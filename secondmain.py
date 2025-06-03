import random
from importlib.util import source_hash

from teacher import *
from administrator import *

# update_grade(6270, 4994, 418, 85)

# get_course_offering_ids()


# remove_assignment_grade(17, 34)

# add_class(482, 6, "6N02", 67, 2)

# print(get_all_room_numbers())

# random_integer = random.randint(1, 100)

# print(random_integer)

# get_course_offering_general_info(3)

# arr = get_teacher_course_offering_id(67, 2)

# print(arr[0][0])

arr = get_student_ids_by_class(418)

print(arr)

for ar in arr:
    print(ar[0])


