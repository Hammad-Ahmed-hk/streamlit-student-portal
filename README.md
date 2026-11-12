# 🎓 EduSphere Smart Portal

A student management web app built with [Streamlit](https://streamlit.io/). Add students, record marks, calculate grades and GPA, search by ID and review an activity log, behind a login screen.

It is a learning project that applies object-oriented programming (encapsulation, inheritance, abstraction and polymorphism) to a small, practical app.

## Features

- 🔐 Login screen (see [Logging in](#logging-in))
- ➕ Add student records
- 📋 View all students
- 🔎 Search a student by ID
- 📊 Automatic grade and GPA calculation
- 📜 Activity log

## Concepts demonstrated

| Concept | Where |
|---|---|
| Encapsulation | GPA stored as a private attribute |
| Inheritance | `Student` and course classes extend base classes |
| Abstraction | A `Person` base class |
| Polymorphism | Different course types |

## Run it

Requires Python 3.9+.

```bash
git clone https://github.com/Hammad-Ahmed-hk/streamlit-student-portal.git
cd streamlit-student-portal
pip install -r requirements.txt
streamlit run Streamlit-student-portal.py
```

## Logging in

**Demo mode (default).** With no secrets configured, the login page shows a "Demo mode" hint and accepts `admin` / `@1234` or `Hammad` / `edu123`. These are public and protect nothing.

**Your own logins.** Create `.streamlit/secrets.toml` (it is git-ignored). This switches the demo accounts off:

```toml
[users]
alice = "a-strong-password"
```

On Streamlit Community Cloud, paste the same text into **App settings → Secrets**.

## Project structure

```
streamlit-student-portal/
├── Streamlit-student-portal.py   # The app
├── requirements.txt
├── README.md
└── .gitignore
```

## Known limitations

- Student records live in session memory, so they are lost when the session ends.
- Passwords are compared as plain text, so this is not production authentication.

## Ideas for next steps

- Store records in SQLite
- Edit and delete students
- Role-based access (admin and user)
- Charts for class performance

## Author

Hammad Ahmed, [@Hammad-Ahmed-hk](https://github.com/Hammad-Ahmed-hk)
