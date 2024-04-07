import mysql.connector
import streamlit as st
from COURSE import Course  # Assuming COURSE is the name of the Python program that contains the Course class

host = "127.0.0.1"
user = ""                       # ENTER YOUR CREDENTIALS
password = ""
database = "TT"

# Establish a database connection
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
# Create a cursor
cursor = connection.cursor()

class Teacher:
    def __init__(self, name, working):
        self.name = name
        self.working = working

    def add_teacher(self):
        data = (self.name, self.working)

        query = """INSERT INTO teacher
                   (TEACHER_NAME, TEACHER_WORKING)  
                   VALUES
                   (%s, %s)"""

        cursor.execute(query, data)
        connection.commit()  # Commit the changes to the database

    def delete_teacher(self, teacher_name):
        # Delete from teacher_course_allocation
        query_delete_teacher_course = "DELETE FROM teacher_course_allocation WHERE TEACHER_NAME = %s"
        cursor.execute(query_delete_teacher_course, (teacher_name,))
        connection.commit()

        # Delete from teacher
        query_delete_teacher = "DELETE FROM teacher WHERE TEACHER_NAME = %s"
        cursor.execute(query_delete_teacher, (teacher_name,))
        connection.commit()

    def assign_course(self, teacher_name, course_code):
        query = """INSERT INTO teacher_course_allocation
                   (TEACHER_NAME, COURSE_CODE)
                   VALUES
                   (%s, %s)"""
        cursor.execute(query, (teacher_name, course_code))
        connection.commit()

    def edit_teacher(self, old_name, new_working):
        query_update_teacher = """UPDATE teacher
                                  SET TEACHER_WORKING=%s
                                  WHERE TEACHER_NAME=%s"""

        data = (new_working, old_name)

        cursor.execute(query_update_teacher, data)
        connection.commit()

    @staticmethod
    def get_all_teachers():
        query = "SELECT * FROM teacher"
        cursor.execute(query)
        return cursor.fetchall()

def add_teacher_ui():
    st.header("ADD TEACHER")
    name = st.text_input("Enter Teacher Name")
    work = st.number_input("Enter Total Weekly Classes", max_value=30)
    # Fetch all courses from the COURSE program
    courses = Course.get_all_courses()
    course_options = [course[0] for course in courses]
    
    # Allow the user to select multiple courses
    selected_courses = st.multiselect("Select Courses", course_options)

    if st.button("Add Teacher"):
        # Create a teacher instance
        teacher_instance = Teacher(name=name, working=work)

        # Add the teacher to the database
        teacher_instance.add_teacher()

        # Assign the selected courses to the teacher using the teacher's name
        for course_code in selected_courses:
            teacher_instance.assign_course(name, course_code)

        st.success("Teacher added successfully!")

def delete_teacher_ui():
    st.header("DELETE TEACHER")

    # Fetch all available teacher names from the database
    all_teachers = Teacher.get_all_teachers()
    available_teacher_names = [teacher[0] for teacher in all_teachers]  # Assuming teacher name is at index 0

    # Create a selectbox to choose the teacher name
    delete_name = st.selectbox("Select Teacher Name to Delete", available_teacher_names)

    if st.button("Delete Teacher"):
        teacher_instance = Teacher(name="", working=0)  
        teacher_instance.delete_teacher(delete_name)
        st.success(f"Teacher with name {delete_name} deleted successfully!")

def edit_teacher_ui():
    st.header("EDIT TEACHER")

    # Fetch all available teacher names from the database
    all_teachers = Teacher.get_all_teachers()
    available_teacher_names = [teacher[0] for teacher in all_teachers]  # Assuming teacher name is at index 0

    # Create a selectbox to choose the teacher name
    edit_name = st.selectbox("Select Teacher Name to Edit", available_teacher_names)

    # Get the current details of the selected teacher
    selected_teacher = [teacher for teacher in all_teachers if teacher[0] == edit_name][0]
    current_working = selected_teacher[1]

    # Display current details
    st.write(f"Teacher Name: {edit_name}")
    st.write(f"Current Total Weekly Classes: {current_working}")

    # Allow user to input new details
    new_working = st.number_input("Enter New Total Weekly Classes", max_value=30, value=current_working)

    if st.button("Edit Teacher"):
        teacher_instance = Teacher(name="", working=0)  
        teacher_instance.edit_teacher(edit_name, new_working)
        st.success(f"Teacher with name {edit_name} edited successfully!")

def run_teacher():
    st.title("TEACHERS")

    tabs = ["Add Teacher", "Edit Teacher", "Delete Teacher"]
    current_tab = st.sidebar.selectbox("Select Action", tabs)

    if current_tab == "Add Teacher":
        add_teacher_ui()
    elif current_tab == "Edit Teacher":
        edit_teacher_ui()
    elif current_tab == "Delete Teacher":
        delete_teacher_ui()

if __name__ == "__main__":
    run_teacher()
