from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import desc

from app import app, db
from model import Subject, Test, Question, TestType, FirstScoreTestScore
from utils.decorator import has_authority


@app.route('/create-test', methods=['GET'])
@login_required
@has_authority('Teacher')
def create_test():
    subjects = Subject.query.all()
    test_types = TestType.query.all()
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc
    return render_template("test/createTest.html", subjects=subjects, test_types=test_types, link=link)


@app.route('/create-test', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_test():
    subject_id = request.form.get('subject_id')
    testType_id = request.form.get('testType_id')

    curr_subject = Subject.query.filter(Subject.id == subject_id).first()

    fsts = FirstScoreTestScore.query.filter(FirstScoreTestScore.subject_id == curr_subject.id).order_by(
        desc(FirstScoreTestScore.first_score)).limit(1).first()
    first_score = fsts.first_score

    test = Test(
        subject_id=subject_id,
        testType_id=testType_id,
        max_first_score=first_score
    )
    db.session.add(test)
    db.session.commit()

    questions = []

    for i in range(1, curr_subject.question_count + 1):
        question_id = request.form.get('question' + str(i))
        question = Question.query.filter(Question.id == question_id).first()
        questions.append(question)
    test.questions = questions
    db.session.commit()

    return redirect(url_for('show_test', test_id=test.id))
