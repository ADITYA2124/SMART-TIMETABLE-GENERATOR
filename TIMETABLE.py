import mysql.connector
import streamlit as st
import numpy as np
import os
from tabulate import tabulate
# Declare matrix as a global variable
matrix = np.empty((6, 10), dtype='|U100')

def establish_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="",
        password="",                # ENTER YOUR CREDENTIALS
        database="TT"
    )

def fetch_course_by_name_and_semester(course_name, semester, cursor):
    query = "SELECT c.COURSE_CODE, c.COURSE_TYPE, c.COURSE_CREDIT, c.COURSE_DURATION " \
            "FROM course c " \
            "WHERE c.PROGRAM_NAME = %s AND c.COURSE_SEM = %s"
    cursor.execute(query, (course_name, semester))
    return cursor.fetchall()

def fetch_teachers_by_course_code(course_code, cursor):
    query = "SELECT t.TEACHER_NAME, t.TEACHER_WORKING " \
            "FROM teacher_course_allocation tca " \
            "JOIN teacher t ON tca.TEACHER_NAME = t.TEACHER_NAME " \
            "WHERE tca.COURSE_CODE = %s AND t.TEACHER_NAME IS NOT NULL"
    cursor.execute(query, (course_code,))
    return cursor.fetchall()

def get_courses(cursor):
    query = "SELECT DISTINCT PROGRAM_NAME FROM course"
    cursor.execute(query)
    courses = cursor.fetchall()
    return [course[0] for course in courses]
days = ["MONDAY     ", "TUESDAY    ", "WEDNESDAY  ", "THURSDAY   ", "FRIDAY     ", "SATURDAY   "]

def get_sorted_course_info_list(course_name, semester, cursor):
    result = fetch_course_by_name_and_semester(course_name, semester, cursor)

    course_info_list = [
        {
            "Course Code": row[0],
            "Course Type": row[1],
            "Course Credits": row[2],
            "Course Duration": row[3],
        }
        for row in result
    ]

    teacher_data_list = []
    if result:
        for course in result:
            course_code = course[0]
            teacher_data = fetch_teachers_by_course_code(course_code, cursor)
            teacher_data_list.extend([
                {
                    "Course Code": course_code,
                    "Teacher Name": teacher[0],
                    "Teacher Working": teacher[1]
                }
                for teacher in teacher_data
            ])

    sorted_course_info_list = sorted(course_info_list, key=lambda x: (x["Course Duration"], x["Course Type"] != 'Theory', x["Course Credits"]), reverse=True)

    return sorted_course_info_list, teacher_data_list

def generate_timetable(sorted_course_info_list):
    global matrix
    matrix = np.empty((6, 10), dtype='|U100')
    matrix[:] = ''  # Initialize matrix with empty strings
    for c in range(6):
        matrix[c, 0] = days[c]
        matrix[c, 5] = "BREAK"

    # Split the course list into two parts
    courses_with_duration_gt_1 = [course for course in sorted_course_info_list if course["Course Duration"] > 1]
    remaining_courses = [course for course in sorted_course_info_list if course["Course Duration"] == 1]

    # Fill timetable with courses with duration greater than 1
    for course_teacher_info in courses_with_duration_gt_1:
        course_credit_count = course_teacher_info["Course Credits"]
        course_dur = course_teacher_info["Course Duration"]

        for _ in range(course_credit_count):
            consecutive_result = False
            while not consecutive_result:
                x = np.random.randint(6)
                y = np.random.randint(10 - course_dur + 1)
                temp_indices = [(x, y + i) for i in range(course_dur)]
                consecutive_result = all(matrix[i, j] == '' for i, j in temp_indices)

            for i, j in temp_indices:
                matrix[i, j] = course_teacher_info["Course Code"]

    # Fill remaining courses
    for course_teacher_info in remaining_courses:
        course_credit_count = course_teacher_info["Course Credits"]

        for _ in range(course_credit_count):
            consecutive_result = False
            while not consecutive_result:
                x = np.random.randint(6)
                y = np.random.randint(10)
                if matrix[x, y] == '':
                    matrix[x, y] = course_teacher_info["Course Code"]
                    consecutive_result = True

    return matrix

def allocate_teachers(sorted_course_info_list, teacher_data_list):
    allocated_teachers = []

    for course_teacher_info in sorted_course_info_list:
        course_code = course_teacher_info["Course Code"]
        course_credit_count = course_teacher_info["Course Credits"]
        course_duration = course_teacher_info["Course Duration"]
        
        suitable_teachers = [teacher_info for teacher_info in teacher_data_list if teacher_info["Course Code"] == course_code]
        
        if not suitable_teachers:
            st.warning(f"No teacher found for {course_code}")
        else:
            for teacher_info in suitable_teachers:
                teacher_name = teacher_info["Teacher Name"]
                teacher_hours = teacher_info["Teacher Working"]
                
                if teacher_hours >= course_credit_count * course_duration:
                    new_hours = teacher_hours - course_credit_count * course_duration
                    update_teacher_working_hours_query = "UPDATE teacher SET TEACHER_WORKING = %s WHERE TEACHER_NAME = %s"
                    cursor.execute(update_teacher_working_hours_query, (new_hours, teacher_name))
                    connection.commit()
                    
                    allocated_teachers.append({"Course Code": course_code, "Teacher Name": teacher_name})
                    break
            else:
                st.warning(f"No available teacher for {course_code}")

    return allocated_teachers
connection = establish_connection()
cursor = connection.cursor()
def run_timetable():
    connection = establish_connection()
    cursor = connection.cursor()
    
    course_name_input = st.selectbox("Select Course:", get_courses(cursor))
    semester_input = st.number_input("Enter Semester:", min_value=0, max_value=10, value=3)
    sorted_course_info_list, teacher_data_list = get_sorted_course_info_list(course_name_input, semester_input, cursor)
    
    if st.button("Fetch Course Data"):
        st.write("Fetched Course Data")
        st.table(sorted_course_info_list)
    
    generated_timetable = None
    
    if st.button("Generate Timetable"):
        generated_timetable = generate_timetable(sorted_course_info_list)
        st.write("Generated Timetable:")
        st.table(generated_timetable)
        with open(os.path.expanduser("C:\\Users\\NEW\\OneDrive\\Desktop\\TIMETABLE.txt"), 'w') as txtfile:
            pass
        with open(os.path.expanduser("C:\\Users\\NEW\\OneDrive\\Desktop\\TIMETABLE.txt"), 'w') as txtfile:
            txtfile.write('Time Table \n')
            time_heading = ["DAYS", "8 - 9", "9 - 10", "10 - 11", "11 - 12", "12 - 1", "1 - 2", "2 - 3", "3 - 4", "4 - 5"]
            timetable=tabulate(generated_timetable,headers=time_heading,tablefmt="simple")
            txtfile.write(timetable)
            txtfile.write('\n\n')
    # Ask the user whether to save the timetable and reduce teacher hours
    if st.button("Save Timetable"):
        allocated_teachers = allocate_teachers(sorted_course_info_list, teacher_data_list)
        st.write("Allocated Teachers:\n")
        st.table(allocated_teachers)
        with open(os.path.expanduser("C:\\Users\\NEW\\OneDrive\\Desktop\\TIMETABLE.txt"), 'a') as txtfile:    
            txtfile.write('Allocated Teachers \n')
            teacher_heading = ["Course Code", "Teacher Name"]
            teacher_table=tabulate(allocated_teachers,headers="keys",tablefmt="simple")
            txtfile.write(teacher_table)
            txtfile.write('\n\n')
            os.startfile("C:\\Users\\NEW\\OneDrive\\Desktop\\TIMETABLE.txt")
    # Close the cursor and connection at the end
    cursor.close()
    connection.close()

if __name__ == "__main__":
    run_timetable()


