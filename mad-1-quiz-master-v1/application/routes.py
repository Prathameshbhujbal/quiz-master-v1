from flask import render_template, request, redirect, url_for, flash, session
from app import app
from application.models import db, User, Subject, Chapter, Quiz, Question, Score
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta


@app.route("/")
def signin():
    return render_template('login.html')

@app.route("/", methods=["POST"])
def sigin_post():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        flash("Username and Password cannot be empty.")
        return redirect(url_for("signin"))

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.passhash, password):
        flash("Username or password is incorrect.")
        return redirect(url_for("signin"))

    session["user_id"] = user.user_id
    flash("LogIn successful :)")
    return redirect(url_for("user"))

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    name = request.form.get("name")

    if not username or not password or not confirm_password or not name:
        flash("Please fill out all the fields.")
        return redirect(url_for("signup"))


    if password != confirm_password:
        flash("Passwords do not match.")
        return redirect(url_for("signup"))

    user = User.query.filter_by(username=username).first()

    if user:
        flash("Username already exists. Please pick another username.")
        return redirect(url_for("signup"))

    pass_hash = generate_password_hash(password)

    new_user = User(name=name, username=username, passhash=pass_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("signin"))

@app.route("/logout")
def logout():
    session.pop("user_id")
    flash("You have been successfully logged out.")
    return redirect(url_for("signin"))


# ------------ Decorator function for authentication ------------

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if "user_id" in session:
            return func(*args, **kwargs)
        else:
            flash("Please sign in first.")
            return redirect(url_for("signin"))
    return inner


def admin_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if not "user_id" in session:
            flash("Please sign in first.")
            return redirect(url_for("signin"))
        
        user = User.query.get(session["user_id"])
        if not user.is_admin:
            flash("You are not authorised to access this page.")
            return redirect(url_for("user"))
        return func(*args, **kwargs)
    return inner


 
# ------------ Admin pages ------------

@app.route("/admin")
@admin_required
def admin():
    user = User.query.get(session["user_id"])

    parameter = request.args.get("parameter")
    query = request.args.get("query")

    subjects = Subject.query.all()

    if parameter == "subject_name":
        subjects = Subject.query.filter(Subject.name.ilike(f'%{query}%')).all()
        return render_template("admin.html", subjects=subjects, user=user)
    
    elif parameter == "ch_name":
        return render_template("admin.html", subjects=subjects, user=user, 
                               param=parameter, query=query)
    
    elif parameter == "username":
        user_list = User.query.filter(User.name.ilike(f'%{query}%')).all()
        return render_template("user_list.html", user=user, user_list=user_list)

    return render_template("admin.html", subjects=subjects, user=user)


@app.route("/admin/user_list")
@admin_required
def user_list():
    user = User.query.get(session['user_id'])
    user_list = User.query.all()
    return render_template("user_list.html", user_list=user_list, user=user)

@app.route("/admin/subject/add")
@admin_required
def add_subject():
    user = User.query.get(session['user_id'])
    return render_template("subject/add.html", user=user)

@app.route("/admin/subject/add", methods=["POST"])
@admin_required
def add_subject_post():
    name = request.form.get("name")
    description = request.form.get("description")

    if not name:
        flash("Subject name cannot be empty")
        return redirect(url_for("add_subject"))
    if not description:
        flash("Description name cannot be empty")
        return redirect(url_for("add_subject"))

    subject = Subject.query.filter_by(name=name).first()

    if subject:
        flash("This subject already exists")
        return redirect(url_for("add_subject"))
    
    new_subject = Subject(name=name, description=description)
    db.session.add(new_subject)
    db.session.commit()

    return redirect(url_for("admin"))

@app.route("/admin/subject/<int:subject_id>/edit")
@admin_required
def edit_subject(subject_id):
    user = User.query.get(session['user_id'])
    subject = Subject.query.get(subject_id)
    if not subject:
        flash("Subject does not exist")
        return redirect(url_for("admin"))
    return render_template("subject/edit.html", user=user, subject=subject)

@app.route("/admin/subject/<int:subject_id>/edit", methods=["POST"])
@admin_required
def edit_subject_post(subject_id):
    name = request.form.get("name")
    description = request.form.get("description")

    if not name:
        flash("Subject name cannot be empty")
        return redirect(url_for("edit_subject", subject_id=subject.subject_id))
    if not description:
        flash("Description cannot be empty")
        return redirect(url_for("edit_subject", subject_id=subject.subject_id))

    subject = Subject.query.get(subject_id)

    
    subject.name = name
    subject.description = description
    db.session.commit()

    return redirect(url_for("admin"))

@app.route("/admin/subject/<int:subject_id>/delete", methods=["GET","POST"])
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get(subject_id)
    if not subject:
        flash("The subject does not exist")
        return redirect(url_for("admin"))
    
    db.session.delete(subject)
    db.session.commit()
    flash("Subject deleted successfully")
    return redirect(url_for("admin"))
    

@app.route("/admin/chapter/<int:subject_id>/add")
@admin_required
def add_chapter(subject_id):
    user = User.query.get(session["user_id"])
    subject = Subject.query.filter_by(subject_id=subject_id).first()
    return render_template("chapter/add.html", subject=subject, user=user)


@app.route("/admin/chapter/<int:subject_id>/add", methods=["POST"])
@admin_required
def add_chapter_post(subject_id):
    name = request.form.get("name")
    description = request.form.get("description")

    if not name:
        flash("Subject name cannot be empty")
        return redirect(url_for("add_chapter"))
    if not description:
        flash("Description cannot be empty")
        return redirect(url_for("add_chapter"))

    chapter = Chapter.query.filter_by(name=name).first()

    if chapter:
        flash("This subject already exists")
        return redirect(url_for("add_chapter"))
    
    new_chapter = Chapter(name=name, description=description, subject_id=subject_id)
    db.session.add(new_chapter)
    db.session.commit()
    flash("New Chapter added successfully")
    return redirect(url_for("admin"))


@app.route("/admin/chapter/<int:chapter_id>/edit")
@admin_required
def edit_chapter(chapter_id):
    user = User.query.get(session["user_id"])
    chapter = Chapter.query.get(chapter_id)
    return render_template("chapter/edit.html", chapter=chapter, user=user)

@app.route("/admin/chapter/<int:chapter_id>/edit", methods=["POST"])
@admin_required
def edit_chapter_post(chapter_id):
    name = request.form.get("name")
    description = request.form.get("description")
    

    if not name:
        flash("Chapter name cannot be empty")
        return redirect(url_for("add_chapter"))
    if not description:
        flash("Description cannot be empty")
        return redirect(url_for("add_chapter"))

    chapter = Chapter.query.get(chapter_id)
    
    chapter.name = name
    chapter.description = description
    db.session.commit()
    flash("Chapter edited successfully")
    return redirect(url_for("admin"))


@app.route("/admin/chapter/<int:chapter_id>/delete", methods=["GET","POST"])
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    if not chapter:
        flash("The subject does not exist")
        return redirect(url_for("admin"))
    
    db.session.delete(chapter)
    db.session.commit()
    flash("Chapter deleted successfully")
    return redirect(url_for("admin"))

@app.route("/admin/quiz")
@admin_required
def quiz():
    user = User.query.get(session["user_id"])
    quizzes = Quiz.query.all()
    return render_template("quiz/quiz.html",  user=user, quizzes=quizzes)

@app.route("/admin/quiz/add")
@admin_required
def add_quiz():
    user = User.query.get(session["user_id"])
    return render_template("quiz/add.html", user=user)

@app.route("/admin/quiz/add", methods=["POST"])
@admin_required
def add_quiz_post():
    user = User.query.get(session["user_id"])
    chap_id = request.form.get("chapter_id")
    date = request.form.get("date")
    duration = request.form.get("duration")

    if not chap_id or not date or not duration:
        flash("All inputs fields are required.")
        return redirect(url_for("add_quiz"))
    
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except:
        flash("Invalid date format")
        return redirect(url_for("add_quiz"))
    
    quiz = Quiz(chapter_id=chap_id, date_of_quiz=parsed_date, time_duration=duration)
    db.session.add(quiz)
    db.session.commit()
    
    flash("Quiz added successfully")
    return redirect(url_for("quiz"))

@app.route("/admin/quiz/<int:quiz_id>/edit")
@admin_required
def edit_quiz(quiz_id):
    user = User.query.get(session["user_id"])
    return render_template("quiz/edit.html", user=user)

@app.route("/admin/quiz/<int:quiz_id>/edit", methods=["POST"])
@admin_required
def edit_quiz_post(quiz_id):
    date = request.form.get("date")
    duration = request.form.get("duration")
    quiz = Quiz.query.get(quiz_id)

    if not date and not duration:
        flash("All fields are required to proceed further")
        return redirect(url_for("edit_quiz"))
    
    if not quiz:
        flash("Invalid quiz")
        return redirect(url_for("edit_quiz"))
    
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
    except:
        flash("Invalid date format")
        return redirect(url_for("edit_quiz"))
    
    quiz.date_of_quiz=parsed_date 
    quiz.time_duration=duration
    db.session.commit()

    flash("Quiz edited successfully.")
    return redirect(url_for("quiz"))

@app.route("/admin/quiz/<int:quiz_id>/delete", methods=["GET","POST"])
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        flash("The quiz does not exist")
        return redirect(url_for("admin"))
    
    db.session.delete(quiz)
    db.session.commit()
    flash("Quiz deleted successfully")
    return redirect(url_for("quiz"))

@app.route("/admin/quiz/<int:quiz_id>/question/add")
@admin_required
def add_question(quiz_id):
    user = User.query.get(session["user_id"])
    return render_template("question/add.html", user=user)

@app.route("/admin/quiz/<int:quiz_id>/question/add", methods=["POST"])
@admin_required
def add_question_post(quiz_id):
    statement = request.form.get("statement")
    option1 = request.form.get("option1")
    option2 = request.form.get("option2")
    option3 = request.form.get("option3")
    option4 = request.form.get("option4")
    try:
        correct_option = int(request.form.get("correct_option"))
    except:
        flash("Correct option parameter should be integer")
        return redirect(url_for("add_question", quiz_id=quiz_id))

    if not statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
        flash("All fields are required")
        return redirect(url_for("add_question", quiz_id=quiz_id))
    

    
    question = Question(quiz_id=quiz_id, question_statement=statement, option1=option1, 
                option2=option2, option3=option3, option4=option4, correct_option=correct_option)
    db.session.add(question)
    db.session.commit()

    flash("Question added successfully")
    return redirect(url_for("quiz"))

@app.route("/admin/quiz/<int:quiz_id>/question/edit/<int:question_id>")
@admin_required
def edit_question(quiz_id, question_id):
    user = User.query.get(session["user_id"])
    return render_template("question/edit.html", user=user)

@app.route("/admin/quiz/<int:quiz_id>/question/edit/<int:question_id>", methods=["POST"])
@admin_required
def edit_question_post(quiz_id, question_id):
    question = Question.query.get(question_id)
    statement = request.form.get("statement")
    option1 = request.form.get("option1")
    option2 = request.form.get("option2")
    option3 = request.form.get("option3")
    option4 = request.form.get("option4")
    try:
        correct_option = int(request.form.get("correct_option"))
    except:
        flash("Correct option parameter should be integer")
        return redirect(url_for("edit_question", quiz_id=quiz_id, question_id=question_id))
    
    if not statement or not option1 or not option2 or not option3 or not option4 or not correct_option:
        flash("All fields are required")
        return redirect(url_for("edit_question", quiz_id=quiz_id, question_id=question_id))
    
    question.question_statement = statement
    question.option1 = option1
    question.option2 = option2
    question.option3 = option3
    question.option4 = option4
    question.correct_option = correct_option

    db.session.commit()
    flash("Question edited successfully")
    return redirect(url_for("quiz"))


@app.route("/admin/quiz/<int:quiz_id>/question/delete/<int:question_id>", methods=["GET","POST"])
@admin_required
def delete_question(question_id, quiz_id):
    question = Question.query.get(question_id)
    if not question:
        flash("The question does not exist")
        return redirect(url_for("admin"))
    
    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully")
    return redirect(url_for("quiz"))



# ------------ User pages ------------


@app.route("/user")
@auth_required
def user():
    user = User.query.get(session["user_id"])
    if user.is_admin == True:
        return redirect(url_for("admin"))
    
    quizzes = Quiz.query.all()
    return render_template("user_dashboard.html", user=user, quizzes=quizzes)

@app.route("/user/view_quiz/<int:quiz_id>/<int:chapter_id>")
@auth_required
def view_quiz(quiz_id, chapter_id):
    user = User.query.get(session["user_id"])
    quiz = Quiz.query.get(quiz_id)
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.filter_by(subject_id=Chapter.query.get(chapter_id).subject_id).first()
    questions = Question.query.all()
    return render_template("user_quiz/view.html", user=user, quiz=quiz, 
                           chapter=chapter, subject=subject, questions=questions)


@app.route("/user/start_quiz/<int:quiz_id>")
@auth_required
def start_quiz(quiz_id):
    user = User.query.get(session["user_id"])
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    duration = Quiz.query.get(quiz_id).time_duration
    start_time = datetime.now()
    end_time = start_time + timedelta(minutes=duration)
   
    return render_template("user_quiz/start.html", user=user, quiz=quiz, 
                           questions=questions, end_time=end_time)


@app.route("/user/start_quiz/<int:quiz_id>", methods=["POST"])
@auth_required
def start_quiz_post(quiz_id):
    user = User.query.get(session["user_id"])
    questions = Question.query.filter_by(quiz_id=quiz_id).all()


    score = 0
    total_questions = len(questions)

    for question in questions:
        question_key = f'{question.question_id}'
        user_answer = request.form.get(question_key)
        if user_answer:
            try:
                if int(user_answer) == question.correct_option:
                    score += 1
            except ValueError:
                print("Invalid answer format")
                print(user_answer)
                flash("Something went wrong")
                return redirect(url_for("user"))

    
    perc_score = int((score / total_questions) * 100)
    time = datetime.now()

    total = Score(quiz_id=quiz_id, user_id=user.user_id, 
                  total_score=perc_score, time_stamp_of_attempt=time)
    db.session.add(total)
    db.session.commit()

    flash("Quiz successfully submitted. You can check your score in the 'Score' Tab")
    return redirect(url_for("user"))


@app.route("/user/scores")
@auth_required
def score():
    user = User.query.get(session["user_id"])
    scores = Score.query.filter_by(user_id=user.user_id).all()
    

    return render_template("user_score.html", user=user, scores=scores)


@app.route("/user/summary")
@auth_required
def summary():
    user = User.query.get(session["user_id"])
    scores = [score.total_score for score in Score.query.filter_by(user_id=User.query.get(session["user_id"]).user_id).all()]
    max_score = 0
    total = 0
    for score in scores:
        total += score
        if score > max_score:
            max_score = score

    len_scores = len(scores)
    avg_score = 0
    if len_scores:
        avg_score = total / len_scores
    
    return render_template("summary.html", user=user, len_scores=len_scores, 
                           max_score=max_score, avg_score=avg_score)