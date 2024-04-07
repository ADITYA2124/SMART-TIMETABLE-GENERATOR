import mysql.connector
import streamlit as st

host = "127.0.0.1"
user = ""
password = ""           # ENTER YOUR CREDENTIALS
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

class Course:
    def __init__(self, name, code, credit, course_type, semester, duration):
        self.name = name
        self.code = code
        self.credit = credit
        self.course_type = course_type
        self.semester = semester
        self.duration = duration

    def add_course(self):
        data = (self.name, self.code, self.credit, self.course_type, self.semester, self.duration)

        query = """INSERT INTO course
                   (PROGRAM_NAME, COURSE_CODE, COURSE_CREDIT, COURSE_TYPE, COURSE_SEM, COURSE_DURATION)
                   VALUES
                   (%s, %s, %s, %s, %s, %s)"""

        cursor.execute(query, data)
        connection.commit()  # Commit the changes to the database

    def delete_course(self, course_code):
        # Delete from teacher_course_allocation
        query_delete_teacher_course = "DELETE FROM teacher_course_allocation WHERE COURSE_CODE = %s"
        cursor.execute(query_delete_teacher_course, (course_code,))
        connection.commit()

        # Delete from course
        query_delete_course = "DELETE FROM course WHERE COURSE_CODE = %s"
        cursor.execute(query_delete_course, (course_code,))
        connection.commit()

    def edit_course(self, course_code, new_program_name, new_credit, new_course_type, new_semester, new_duration):
        # Update course details
        query = """UPDATE course
                   SET PROGRAM_NAME=%s, COURSE_CREDIT=%s, COURSE_TYPE=%s, COURSE_SEM=%s, COURSE_DURATION=%s
                   WHERE COURSE_CODE=%s"""

        data = (new_program_name, new_credit, new_course_type, new_semester, new_duration, course_code)

        cursor.execute(query, data)
        connection.commit()

    @staticmethod
    def get_all_courses():
        query = "SELECT * FROM course"
        cursor.execute(query)
        return cursor.fetchall()

def add_course_ui():
    st.header("ADD COURSE")
    name = st.text_input("Enter Program Name")
    code = st.text_input("Enter Course Code")
    credit = st.number_input("Enter Course Credit", min_value=1)
    duration = st.number_input("Enter Course Duration (Hours)", min_value=1, max_value=4)
    # Use a radio button for course type
    course_type = st.radio("Select Course Type", ["Theory", "Practical"])

    semester = st.number_input("Enter Course Semester", min_value=1)

    if st.button("Add Course"):
        course_instance = Course(name=name, code=code, credit=credit, course_type=course_type, semester=semester, duration=duration)
        course_instance.add_course()
        st.success("Course added successfully!")

def delete_course_ui():
    st.header("DELETE COURSE")

    # Fetch all available program names from the database
    all_programs = Course.get_all_courses()
    available_programs = list(set([course[1] for course in all_programs]))  # Assuming program name is at index 1

    # Create a selectbox to choose the program name
    selected_program = st.selectbox("Select Program Name", available_programs)

    # Fetch all available semesters for the selected program
    available_semesters = list(set([course[4] for course in all_programs if course[1] == selected_program]))

    # Create a selectbox to choose the semester
    selected_semester = st.selectbox("Select Semester", available_semesters)

    # Filter courses based on the selected program and semester
    program_semester_courses = [course for course in all_programs if course[1] == selected_program and course[4] == selected_semester]
    available_course_codes = [course[0] for course in program_semester_courses]  # Assuming course code is at index 0

    # Create a selectbox to choose the course code
    delete_code = st.selectbox("Select Course Code to Delete", available_course_codes)

    if st.button("Delete Course"):
        course_instance = Course(name="", code="", credit=0, course_type="", semester=0, duration=0)
        course_instance.delete_course(delete_code)
        st.success(f"Course with code {delete_code} deleted successfully!")

def edit_course_ui():
    st.header("EDIT COURSE")

    # Fetch all available program names from the database
    all_programs = Course.get_all_courses()
    available_programs = list(set([course[1] for course in all_programs]))  # Assuming program name is at index 1

    # Create a selectbox to choose the program name
    selected_program = st.selectbox("Select Program Name", available_programs)

    # Fetch all available semesters for the selected program
    available_semesters = list(set([course[4] for course in all_programs if course[1] == selected_program]))

    # Create a selectbox to choose the semester
    selected_semester = st.selectbox("Select Semester", available_semesters)

    # Filter courses based on the selected program and semester
    program_semester_courses = [course for course in all_programs if course[1] == selected_program and course[4] == selected_semester]
    available_course_codes = [course[0] for course in program_semester_courses]  # Assuming course code is at index 0

    # Create a selectbox to choose the course code
    edit_code = st.selectbox("Select Course Code to Edit", available_course_codes)

    # Get the current details of the selected course
    selected_course = [course for course in program_semester_courses if course[0] == edit_code][0]
    current_credit, current_course_type, current_semester, current_duration = selected_course[2:6]

    # Display current details
    st.write(f"Current Course Code: {edit_code}")
    st.write(f"Current Course Credit: {current_credit}")
    st.write(f"Current Course Type: {current_course_type}")
    st.write(f"Current Course Semester: {current_semester}")
    st.write(f"Current Course Duration: {current_duration} hours")

    # Allow user to input new details
    new_credit = st.number_input("Enter New Course Credit", min_value=0, value=current_credit)
    new_duration = st.number_input("Enter New Course Duration (Hours)", min_value=0, value=current_duration)
    # Use a radio button for course type
    new_course_type = st.radio("Select New Course Type", ["Theory", "Practical"], index=0 if current_course_type == "Theory" else 1)
    new_semester = st.number_input("Enter New Course Semester", min_value=0, value=current_semester)

    if st.button("Edit Course"):
        course_instance = Course(name="", code="", credit=0, course_type="", semester=0, duration=0)
        course_instance.edit_course(edit_code, selected_program, new_credit, new_course_type, new_semester, new_duration)
        st.success(f"Course with code {edit_code} edited successfully!")

def run_course():
    st.title("COURSES")

    tabs = ["Add Course", "Edit Course", "Delete Course"]
    current_tab = st.sidebar.selectbox("Select Action", tabs)

    if current_tab == "Add Course":
        add_course_ui()
    elif current_tab == "Edit Course":
        edit_course_ui()
    elif current_tab == "Delete Course":
        delete_course_ui()

if __name__ == "__main__":
    run_course()
