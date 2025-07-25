from flask import Flask, render_template, request, redirect, url_for, session
from models import db, QuizResult, init_db
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-this-in-production'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'quiz.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)

# Quiz Questions
QUIZ_QUESTIONS = [
    {
        'question': 'Discord.py kütüphanesi ile bot oluştururken hangi decorator kullanılır?',
        'options': ['@bot.command()', '@client.event()', '@discord.command()', '@bot.event()'],
        'correct': 0
    },
    {
        'question': 'Flask web uygulamasında route tanımlamak için hangi decorator kullanılır?',
        'options': ['@app.route()', '@flask.route()', '@web.route()', '@app.path()'],
        'correct': 0
    },
    {
        'question': 'TensorFlow ile yapay zeka modellerinde hangi katman türü en çok kullanılır?',
        'options': ['Dense', 'Convolutional', 'Recurrent', 'Dropout'],
        'correct': 0
    },
    {
        'question': 'Computer Vision projelerinde görüntü işleme için hangi kütüphane yaygın olarak kullanılır?',
        'options': ['OpenCV', 'Pillow', 'ImageAI', 'Hepsi'],
        'correct': 3
    },
    {
        'question': 'BeautifulSoup kütüphanesi ne için kullanılır?',
        'options': ['Web scraping', 'Görüntü işleme', 'Ses işleme', 'Veritabanı işlemleri'],
        'correct': 0
    },
    {
        'question': 'NLTK kütüphanesi hangi alan için geliştirilmiştir?',
        'options': ['Doğal Dil İşleme', 'Makine Öğrenmesi', 'Web Geliştirme', 'Oyun Geliştirme'],
        'correct': 0
    },
    {
        'question': 'Discord bot geliştirmede hangi olay kullanıcı mesajlarını dinler?',
        'options': ['on_message', 'on_user_message', 'on_chat', 'on_text'],
        'correct': 0
    }
]

@app.route('/')
def index():
    # Getting statistics
    all_time_high = QuizResult.get_all_time_high_score()
    user_high = 0
    if 'username' in session:
        user_high = QuizResult.get_user_best_score(session['username'])
    
    return render_template('index.html', all_time_high=all_time_high, user_high=user_high)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    username = request.form.get('username')
    if not username:
        return redirect(url_for('index'))
    
    session['username'] = username
    session['current_question'] = 0
    session['score'] = 0
    session['answers'] = []
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    current_q = session.get('current_question', 0)
    
    if current_q >= len(QUIZ_QUESTIONS):
        return redirect(url_for('result'))
    
    question = QUIZ_QUESTIONS[current_q]
    
    # Getting statistics for header
    all_time_high = QuizResult.get_all_time_high_score()
    user_high = QuizResult.get_user_best_score(session['username'])
    
    return render_template('quiz.html', 
                         question=question, 
                         question_num=current_q + 1,
                         total_questions=len(QUIZ_QUESTIONS),
                         all_time_high=all_time_high,
                         user_high=user_high)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    answer = request.form.get('answer')
    if answer is None:
        return redirect(url_for('quiz'))
    
    current_q = session.get('current_question', 0)
    correct_answer = QUIZ_QUESTIONS[current_q]['correct']
    
    session['answers'].append(int(answer))
    
    if int(answer) == correct_answer:
        session['score'] = session.get('score', 0) + 1
    
    session['current_question'] = current_q + 1
    
    return redirect(url_for('quiz'))

@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('index'))
    
    score = session.get('score', 0)
    total = len(QUIZ_QUESTIONS)
    username = session['username']
    
    # Saving result to database
    result = QuizResult(username=username, score=score, total_questions=total)
    db.session.add(result)
    db.session.commit()
    
    # Getting statistics
    all_time_high = QuizResult.get_all_time_high_score()
    user_high = QuizResult.get_user_best_score(username)
    last_score = score
    
    return render_template('result.html', 
                         score=score, 
                         total=total,
                         percentage=round((score/total)*100, 1),
                         all_time_high=all_time_high,
                         user_high=user_high,
                         last_score=last_score)

@app.route('/restart')
def restart():
    username = session.get('username')
    session.clear()
    if username:
        session['username'] = username
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)