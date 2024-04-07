import streamlit as st
from COURSE import run_course
from TEACHER import run_teacher
from TIMETABLE import run_timetable


st.title("SMART TIMETABLE GENERATOR")
st.header("DEVELOPED BY - ADITYA ARORA\n")
# Create a sidebar with navigation links
Introduction = st.empty()
Introduction.markdown("""
    This project is a Streamlit-based application for generating and managing\n
    a university timetable. The project involves interactions with\n
    a MySQL database to fetch course and teacher data, random generation of a\n 
    timetable based on course credits and duration, and allocation of teachers to\n 
    the generated timetable. The generated timetable is displayed through a \n
    Streamlit web interface, and users have the option to save the timetable and\n
    view allocated teachers. Key components include database interaction functions,\n
    timetable generation logic, and a Streamlit user interface. It aims to automate\n
    the timetable creation process for educational institutions while considering\n
    course requirements and teacher availability.""")

def run_main():
    page = st.sidebar.selectbox("Select a page", ["Course", "Teacher","TimeTable"]) 
        # Display the selected page
    if page == "Course":
        run_course()
    elif page == "Teacher":
        run_teacher()
    elif page =="TimeTable":
        run_timetable() 

current=st.sidebar.selectbox("SELECT AN OPTION",["INTRODUCTION", "TIMETABLE GENERATION"])
if current == "INTRODUCTION":
    Introduction.markdown("""
    This project is a Streamlit-based application for generating and managing\n
    a university timetable. The project involves interactions with\n
    a MySQL database to fetch course and teacher data, random generation of a\n 
    timetable based on course credits and duration, and allocation of teachers to\n 
    the generated timetable. The generated timetable is displayed through a \n
    Streamlit web interface, and users have the option to save the timetable and\n
    view allocated teachers. Key components include database interaction functions,\n
    timetable generation logic, and a Streamlit user interface. It aims to automate\n
    the timetable creation process for educational institutions while considering\n
    course requirements and teacher availability.""")
elif current == "TIMETABLE GENERATION":
        Introduction.markdown("""""")
        run_main()


   

