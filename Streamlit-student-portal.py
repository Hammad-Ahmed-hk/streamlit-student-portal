import streamlit as st
import pandas as pd

st.set_page_config(page_title="EduSphere Portal", page_icon="🎓", layout="wide")

# -------------------------------
# SESSION DATABASE
# -------------------------------

if "students_db" not in st.session_state:
    st.session_state.students_db = {}

if "logs" not in st.session_state:
    st.session_state.logs = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# -------------------------------
# USER AUTHENTICATION DATABASE
# -------------------------------

users = {
    "admin": "@1234",
    "Hammad": "edu123"
}


# -------------------------------
# COURSE CLASSES (INHERITANCE)
# -------------------------------

class Course:

    def __init__(self, course_name):
        self.course_name = course_name

    def get_course(self):
        return self.course_name


class StemCourse(Course):

    def __init__(self, course_name, lab_required=True):
        super().__init__(course_name)
        self.lab_required = lab_required

    def course_info(self):
        return f"{self.course_name} (STEM Course, Lab Required: {self.lab_required})"


# -------------------------------
# PERSON CLASS (ABSTRACTION)
# -------------------------------

class Person:

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id


# -------------------------------
# STUDENT CLASS (INHERITANCE)
# -------------------------------

class Student(Person):

    def __init__(self, name, student_id, course, marks):
        super().__init__(name, student_id)

        self.course = course
        self.marks = marks
        self.__gpa = None     # Encapsulation
        self.__grade = None   # FIX: store grade as well

    def set_gpa(self, gpa):
        self.__gpa = gpa

    def get_gpa(self):
        return self.__gpa

    def set_grade(self, grade):
        self.__grade = grade

    def get_grade(self):
        return self.__grade


# -------------------------------
# GRADE CALCULATOR
# -------------------------------

def calculate_grade(marks):

    match marks:

        case m if m >= 80:
            return "A", 4.0

        case m if m >= 65:
            return "B", 3.0

        case m if m >= 50:
            return "C", 2.0

        case _:
            return "D", 1.0


# -------------------------------
# LOGIN SYSTEM
# -------------------------------

def login():

    st.title("🎓 EduSphere Smart Portal")

    st.subheader("Login to Continue")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username] == password:

            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()

        else:
            st.error("Invalid Credentials")


# -------------------------------
# ADD STUDENT
# -------------------------------

def add_student():

    st.header("➕ Add Student")

    name = st.text_input("Student Name")

    student_id = st.text_input("Student ID")

    course_type = st.selectbox(
        "Course Category",
        ["STEM Course", "General Course"]
    )

    course_name = st.text_input("Course Name")

    marks = st.number_input("Marks", 0, 100)

    if st.button("Add Student"):

        if student_id in st.session_state.students_db:

            st.error("Student already exists")

        else:

            if course_type == "STEM Course":

                course = StemCourse(course_name)

            else:

                course = Course(course_name)

            student = Student(name, student_id, course.get_course(), marks)

            grade, gpa = calculate_grade(marks)

            student.set_gpa(gpa)
            student.set_grade(grade)   # FIX: save grade to student object

            st.session_state.students_db[student_id] = student

            st.session_state.logs.append((student_id, name))

            st.success("Student Added Successfully")


# -------------------------------
# VIEW STUDENTS  ✅ FIXED
# -------------------------------

def view_students():

    st.header("📋 Student Records")

    if len(st.session_state.students_db) == 0:

        st.warning("No students found. Please add students first.")

    else:

        table_data = []

        for sid in st.session_state.students_db:

            student = st.session_state.students_db[sid]

            table_data.append({
                "Student ID": student.student_id,
                "Name": student.name,
                "Course": student.course,
                "Marks": student.marks,
                "Grade": student.get_grade(),   # FIX: now shows grade
                "GPA": student.get_gpa()
            })

        # FIX: use pandas DataFrame with st.dataframe() for reliable rendering
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

        # Summary stats
        st.markdown("---")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Students", len(table_data))

        with col2:
            avg_marks = round(sum(s["Marks"] for s in table_data) / len(table_data), 2)
            st.metric("Average Marks", avg_marks)

        with col3:
            avg_gpa = round(sum(s["GPA"] for s in table_data) / len(table_data), 2)
            st.metric("Average GPA", avg_gpa)


# -------------------------------
# SEARCH STUDENT
# -------------------------------

def search_student():

    st.header("🔎 Search Student")

    search_id = st.text_input("Enter Student ID")

    if st.button("Search"):

        keys = list(st.session_state.students_db.keys())

        found = False

        for i in range(len(keys)):

            sid = keys[i]

            if sid == search_id:

                student = st.session_state.students_db[sid]

                st.success("Student Found")

                st.write("Name:", student.name)
                st.write("Course:", student.course)
                st.write("Marks:", student.marks)
                st.write("Grade:", student.get_grade())
                st.write("GPA:", student.get_gpa())

                found = True

        if not found:

            st.error("Student Not Found")


# -------------------------------
# GRADE CALCULATOR PAGE
# -------------------------------

def grade_page():

    st.header("📊 Grade Calculator")

    marks = st.number_input("Enter Marks", 0, 100)

    if st.button("Calculate"):

        grade, gpa = calculate_grade(marks)

        st.success(f"Grade: {grade}")

        st.info(f"GPA: {gpa}")


# -------------------------------
# DATA LOGS
# -------------------------------

def show_logs():

    st.header("📜 Student Logs")

    if len(st.session_state.logs) == 0:

        st.warning("No logs available")

    else:

        for log in st.session_state.logs:

            st.write("Student ID:", log[0], "| Name:", log[1])


# -------------------------------
# DASHBOARD
# -------------------------------

def dashboard():

    st.sidebar.title("🎓 EduSphere Menu")

    menu = st.sidebar.selectbox(
        "Navigation",
        [
            "Add Student",
            "View Records",
            "Search Student",
            "Calculate Grades",
            "Logs"
        ]
    )

    match menu:

        case "Add Student":
            add_student()

        case "View Records":
            view_students()

        case "Search Student":
            search_student()

        case "Calculate Grades":
            grade_page()

        case "Logs":
            show_logs()


# -------------------------------
# MAIN PROGRAM
# -------------------------------

if not st.session_state.logged_in:

    login()

else:

    dashboard()