import json
import traceback

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, QuestionType, QuestionInfo, Question, FirstScoreTestScore
from utils.decorator import has_authority


@app.route('/subject/<subject_id>', methods=['GET'])
@login_required
@has_authority('Admin')
def subject_json(subject_id):
    if int(subject_id) != 0:
        sub = Subject.query.filter(Subject.id == subject_id).first()
        return jsonify(sub.question_count)
    else:
        return ''


@app.route('/subject/<subject_id>/question/<question_id>', methods=['GET'])
@login_required
@has_authority('Admin')
def question_json(subject_id, question_id):
    curr_subject = Subject.query.filter(Subject.id == subject_id).first()
    questions = Question.query \
        .filter(Question.subject_id == curr_subject.id) \
        .filter(Question.number == question_id).all()
    result = dict()
    for question in questions:
        result[question.id] = question.text
    return jsonify(result)


@app.route('/subject', methods=['GET'])
@login_required
@has_authority('Admin')
def subject():
    name = request.args.get('name')

    question_types = QuestionType.query.all()

    result = dict()
    for qt in question_types:
        result[str(qt.id)] = qt.name

    if name is not None:
        subjects = Subject.query.filter(Subject.name.ilike("%{}%".format(name))).order_by(
            Subject.name.asc())
    else:
        subjects = Subject.query.order_by(Subject.name.asc())

    return render_template("subject/subject.html", subjects=subjects.all(), question_types=json.dumps(result))


@app.route('/subject', methods=['POST'])
@login_required
@has_authority('Admin')
def add_subject():
    name = request.form.get('name')
    try:
        time_limit = float(request.form.get('time_limit'))
        question_count = int(request.form.get('question_count'))
    except Exception:
        flash("Введите число")
        return redirect(url_for('subject'))
    sub = Subject(
        name=name,
        time_limit=time_limit,
        question_count=question_count
    )
    db.session.add(sub)
    db.session.commit()
    subject_id = sub.id

    first_score = 0
    try:
        for i in range(1, question_count + 1):
            max_q_mark = float(request.form.get('max_mark' + str(i)))
            first_score += max_q_mark
            question_type_id = request.form.get('questionType_id' + str(i))

            qi = QuestionInfo(
                number=i,
                subject_id=subject_id,
                questionType_id=question_type_id,
                max_mark=max_q_mark
            )
            db.session.add(qi)
            db.session.commit()
    except Exception:
        traceback.print_exc()
        flash("В описании вопросов введены неверные данные")
        db.session.delete(sub)
        db.session.commit()
        return redirect(url_for('subject'))
    try:
        for i in range(0, int(first_score) + 1):
            test_score = int(request.form.get('test_score' + str(i)))

            fsts = FirstScoreTestScore(
                first_score=i,
                test_score=test_score,
                subject_id=subject_id
            )
            db.session.add(fsts)
            db.session.commit()
    except Exception:
        traceback.print_exc()

    return redirect(url_for('subject'))


@app.route('/delete-subject', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_subject():
    subject_id = request.form.get('subject_id')
    try:
        sub = Subject.query.filter(Subject.id == subject_id).first()
        db.session.delete(sub)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный тип вопроса.')
        return redirect(url_for('subject'))

    return redirect(url_for('subject'))


@app.route('/change-subject', methods=['POST'])
@login_required
@has_authority('Admin')
def change_subject():
    subject_id = request.form.get('subject_id')
    Subject.query.filter(Subject.id == subject_id).update({
        'name': request.form.get('name'),
        'time_limit': request.form.get('time_limit'),
        'question_count': request.form.get('question_count')
    })
    db.session.commit()
    return redirect(url_for('subject'))
