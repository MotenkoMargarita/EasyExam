import json
import traceback

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, QuestionInfo, QuestionType, FirstScoreTestScore
from utils.decorator import has_authority


@app.route('/subject-info/<subject_id>', methods=['GET'])
@login_required
@has_authority('Admin')
def question_info(subject_id):
    curr_subject = Subject.query.filter(Subject.id == subject_id).first()
    questions_info = QuestionInfo.query.filter(QuestionInfo.subject_id == subject_id).all()
    first_score_test_score = FirstScoreTestScore.query.filter(FirstScoreTestScore.subject_id == subject_id).all()
    question_types = QuestionType.query.all()
    return render_template("subject/subjectInfo.html", curr_subject=curr_subject, questions_info=questions_info,
                           question_types=question_types, first_score_test_score=first_score_test_score)


@app.route('/question-info-change/<subject_id>', methods=['POST'])
@login_required
@has_authority('Admin')
def question_info_change(subject_id):
    questions_info = QuestionInfo.query.filter(QuestionInfo.subject_id == subject_id).all()

    for qi in questions_info:
        QuestionInfo.query.filter(QuestionInfo.id == qi.id).update({
            'max_mark': request.form.get('max_mark' + str(qi.id)),
            'questionType_id': request.form.get('questionType_id' + str(qi.id)),
        })
        db.session.commit()

    first_score_test_score = FirstScoreTestScore.query.filter(FirstScoreTestScore.subject_id == subject_id).all()

    for fsts in first_score_test_score:
        FirstScoreTestScore.query.filter(FirstScoreTestScore.id == fsts.id).update({
            'test_score': request.form.get('test_score' + str(fsts.id)),
        })
        db.session.commit()

    return redirect(url_for('question_info', subject_id=subject_id))
