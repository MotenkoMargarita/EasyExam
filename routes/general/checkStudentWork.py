import os
import uuid

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db
from model import Result, Test, Subject, TestType, QuestionInfo, ResultQuestion, \
    FirstScoreTestScore
from routes.general.fileUpload import allowed_file


@app.route('/student-work', methods=['POST'])
@login_required
def student_work():
    result_id = request.form.get('result_id')

    result = Result.query.filter(Result.id == result_id).first()
    test = Test.query.filter(Test.id == result.test_id).first()
    subject = Subject.query.filter(Subject.id == test.subject_id).first()

    res_questions = ResultQuestion.query.filter(ResultQuestion.result_id == result_id).all()

    question_id_answer = dict()
    question_id_comment = dict()
    question_id_mark = dict()

    for res_question in res_questions:
        question_id_answer[res_question.question.id] = res_question.user_answer
        question_id_comment[res_question.question.id] = res_question.commentary
        question_id_mark[res_question.question.id] = res_question.mark

    comment = result.commentary

    test_type = TestType.query.filter(TestType.id == test.testType_id).first()
    question_number_question_info = dict()
    for i in range(1, subject.question_count + 1):
        question_number_question_info[i] = QuestionInfo.query.filter(
            QuestionInfo.subject_id == subject.id).filter(
            QuestionInfo.number == i).first()

    return render_template("teacher/checkStudentWork.html", test=test, result=result, question_id_answer=question_id_answer,
                           subject=subject, test_type=test_type, question_id_comment=question_id_comment,
                           question_number_question_info=question_number_question_info, comment=comment,
                           question_id_mark=question_id_mark)


@app.route('/student-work-save', methods=['POST'])
@login_required
def student_work_save():
    result_id = request.form.get('result_id')

    result = Result.query.filter(Result.id == result_id).first()
    test = Test.query.filter(Test.id == result.test_id).first()
    subject = Subject.query.filter(Subject.id == test.subject_id).first()

    res_questions = ResultQuestion.query.filter(ResultQuestion.result_id == result_id).all()

    try:
        path_for_teacher_file = None
        file = request.files['teacher_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + '_' + filename
            path = os.path.join(app.config['UPLOAD_FOLDER_FOR_SOLUTIONS'], filename)
            file.save(path)
            path_for_teacher_file = path
            result.teacher_file = path_for_teacher_file
            db.session.commit()
    except Exception as e:
        print(e)

    mark_for_c_part = 0

    for res_question in res_questions:
        comment_for_question = request.form.get('comment' + str(res_question.question_id))
        mark_question = request.form.get('mark' + str(res_question.question_id))
        if comment_for_question:
            res_question.commentary = comment_for_question
            db.session.commit()
        if mark_question:
            res_question.mark = int(mark_question)
            mark_for_c_part += int(mark_question)
            db.session.commit()
    result.commentary = request.form.get('comment')
    db.session.commit()
    result_first_mark = result.first_part_first_mark + mark_for_c_part
    result.result_first_mark = result_first_mark
    db.session.commit()
    result_test_mark = int(
        FirstScoreTestScore.query.filter(FirstScoreTestScore.first_score == result_first_mark).first().test_score)
    result.result_test_mark = result_test_mark
    db.session.commit()
    result.is_checked = True
    db.session.commit()

    flash("Результат сохранен")

    return redirect(url_for('teacher_panel'))
