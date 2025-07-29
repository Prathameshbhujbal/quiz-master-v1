from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy import Column, TIMESTAMP
from datetime import datetime
import pytz

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(64))
    qualification = db.Column(db.String(64))
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    scores = db.relationship('Score', backref='user', lazy=True)

class Subject(db.Model):
    subject_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))

    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

class Chapter(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.subject_id'))
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(256))
    
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')

class Quiz(db.Model):
    quiz_id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.chapter_id'))
    date_of_quiz = db.Column(db.Date)
    time_duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text)
    
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade='all, delete-orphan')
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')

class Question(db.Model):
    question_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text, nullable=False)
    option4 = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)
    

ist_tz = pytz.timezone('Asia/Kolkata')

class Score(db.Model):
    score_id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.quiz_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    time_stamp_of_attempt = db.Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(ist_tz))
    total_score = db.Column(db.Integer)


with app.app_context():
    db.create_all()
    # if admin exists, else create admin
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        password_hash = generate_password_hash('admin')
        admin = User(username='admin', passhash=password_hash, name='Admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()
