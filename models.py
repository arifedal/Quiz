from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class QuizResult(db.Model):
    """
    Model to store quiz results for each user
    """
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, index=True)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __init__(self, username, score, total_questions):
        self.username = username
        self.score = score
        self.total_questions = total_questions
        self.percentage = round((score / total_questions) * 100, 2)
    
    def __repr__(self):
        return f'<QuizResult {self.username}: {self.score}/{self.total_questions}>'
    
    @staticmethod
    def get_user_best_score(username):
       
        result = QuizResult.query.filter_by(username=username).order_by(QuizResult.score.desc()).first()
        return result.score if result else 0
    
    @staticmethod
    def get_all_time_high_score():
        
        result = QuizResult.query.order_by(QuizResult.score.desc()).first()
        return result.score if result else 0
    
    @staticmethod
    def get_user_stats(username):
        
        results = QuizResult.query.filter_by(username=username).all()
        if not results:
            return {
                'total_attempts': 0,
                'best_score': 0,
                'average_score': 0,
                'last_score': 0,
                'improvement': 0
            }
        
        scores = [r.score for r in results]
        return {
            'total_attempts': len(results),
            'best_score': max(scores),
            'average_score': round(sum(scores) / len(scores), 1),
            'last_score': results[-1].score,
            'improvement': results[-1].score - (results[-2].score if len(results) > 1 else 0)
        }
    
    @staticmethod
    def get_global_stats():
        
        all_results = QuizResult.query.all()
        if not all_results:
            return {
                'total_attempts': 0,
                'unique_users': 0,
                'highest_score': 0,
                'average_score': 0
            }
        
        scores = [r.score for r in all_results]
        unique_users = len(set(r.username for r in all_results))
        
        return {
            'total_attempts': len(all_results),
            'unique_users': unique_users,
            'highest_score': max(scores),
            'average_score': round(sum(scores) / len(scores), 1)
        }

class QuizQuestion(db.Model):
    """
    Model to store quiz questions
    """
    __tablename__ = 'quiz_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False)  # 0=A, 1=B, 2=C, 3=D
    category = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), default='medium')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizQuestion {self.id}: {self.question_text[:50]}...>'
    
    def to_dict(self):
        """Convert question to dictionary format"""
        return {
            'id': self.id,
            'question': self.question_text,
            'options': [self.option_a, self.option_b, self.option_c, self.option_d],
            'correct': self.correct_answer,
            'category': self.category,
            'difficulty': self.difficulty
        }
    
    @staticmethod
    def get_random_questions(count=7):
        return QuizQuestion.query.filter_by(is_active=True).order_by(db.func.random()).limit(count).all()
    
    @staticmethod
    def get_questions_by_category(category, count=2):
        return QuizQuestion.query.filter_by(category=category, is_active=True).order_by(db.func.random()).limit(count).all()

class UserSession(db.Model):

    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    session_id = db.Column(db.String(200), nullable=False, unique=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    is_completed = db.Column(db.Boolean, default=False)
    current_question = db.Column(db.Integer, default=0)
    current_score = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<UserSession {self.username}: {self.session_id}>'
    
    def mark_completed(self):
        self.is_completed = True
        self.end_time = datetime.utcnow()
        db.session.commit()

# Database initialization functions
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if QuizQuestion.query.count() == 0:
            add_sample_questions()

def add_sample_questions():
    sample_questions = [
        {
            'question_text': 'Discord.py kütüphanesi ile bot oluştururken hangi decorator kullanılır?',
            'option_a': '@bot.command()',
            'option_b': '@client.event()',
            'option_c': '@discord.command()',
            'option_d': '@bot.event()',
            'correct_answer': 0,
            'category': 'Discord Bot Development'
        },
        {
            'question_text': 'Flask web uygulamasında route tanımlamak için hangi decorator kullanılır?',
            'option_a': '@app.route()',
            'option_b': '@flask.route()',
            'option_c': '@web.route()',
            'option_d': '@app.path()',
            'correct_answer': 0,
            'category': 'Flask Web Development'
        },
        {
            'question_text': 'TensorFlow ile yapay zeka modellerinde hangi katman türü temel yapı taşıdır?',
            'option_a': 'Dense',
            'option_b': 'Convolutional',
            'option_c': 'Recurrent',
            'option_d': 'Dropout',
            'correct_answer': 0,
            'category': 'AI Development'
        },
        {
            'question_text': 'Computer Vision projelerinde görüntü işleme için hangi kütüphane yaygın olarak kullanılır?',
            'option_a': 'OpenCV',
            'option_b': 'Pillow',
            'option_c': 'ImageAI',
            'option_d': 'Hepsi',
            'correct_answer': 3,
            'category': 'Computer Vision'
        },
        {
            'question_text': 'BeautifulSoup kütüphanesi ne için kullanılır?',
            'option_a': 'Web scraping',
            'option_b': 'Görüntü işleme',
            'option_c': 'Ses işleme',
            'option_d': 'Veritabanı işlemleri',
            'correct_answer': 0,
            'category': 'Natural Language Processing'
        },
        {
            'question_text': 'NLTK kütüphanesi hangi alan için geliştirilmiştir?',
            'option_a': 'Doğal Dil İşleme',
            'option_b': 'Makine Öğrenmesi',
            'option_c': 'Web Geliştirme',
            'option_d': 'Oyun Geliştirme',
            'correct_answer': 0,
            'category': 'Natural Language Processing'
        },
        {
            'question_text': 'Discord bot geliştirmede hangi olay kullanıcı mesajlarını dinler?',
            'option_a': 'on_message',
            'option_b': 'on_user_message',
            'option_c': 'on_chat',
            'option_d': 'on_text',
            'correct_answer': 0,
            'category': 'Discord Bot Development'
        }
    ]
    
    for q_data in sample_questions:
        question = QuizQuestion(**q_data)
        db.session.add(question)
    
    db.session.commit()
    print("Sample questions added to database!")