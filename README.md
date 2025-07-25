Python PRO Quiz Web App
=======================

This is a web-based multiple-choice quiz application built using Flask and SQLAlchemy. It was created as part of the Python PRO DST Teaching Qualification by Arife Dal.

🧠 Features
-----------

- Dynamic question navigation  
- Real-time progress bar that updates with each question  
- Final score display with personalized feedback  
- Clean Bootstrap 5 interface  
- SQLite database to store quiz questions  

📁 Folder Structure
-------------------

/quiz-app/
│
├── app.py                  # Main Flask application  
├── questions.py            # List of quiz questions  
├── quiz.db                 # SQLite database (auto-generated if not found)  
├── /templates/             # HTML templates  
│   ├── base.html  
│   ├── question.html  
│   └── result.html  
├── /static/  
│   ├── style.css           # Custom styles  
│   └── images/             # Optional images or icons  

🚀 How to Run
-------------

1. Install dependencies (if you haven’t yet):  
   `pip install flask sqlalchemy`

2. Run the application:  
   `python app.py`

3. Open in your browser:  
   `http://localhost:5000`

✅ Notes
--------

- Questions are stored in `questions.py`, not directly in the database.  
- Progress is calculated dynamically based on question number.  
- The app was built for educational purposes and is easy to customize.

👩‍💻 Author: Arife Dal
----------------------

Computer Engineer & Python Instructor  
GitHub: https://github.com/arifedal  
