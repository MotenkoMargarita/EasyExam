import os
import uuid
from math import trunc

from flask import render_template, request, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app import app, db
from model import Subject, Test, TestType, QuestionInfo, FirstScoreTestScore, \
    TeachersStudents, User, Theme, Result, ResultQuestion
from routes.general.fileUpload import allowed_file


@app.route('/subject/<subject_id>/theme/<theme_id>/test/<test_id>', methods=['GET'])
@login_required
def theme_test(subject_id, theme_id, test_id):
    curr_test = Test.query.filter(Test.id == test_id).first()

    if curr_test is None:
        return abort(404)

    theme = Theme.query.filter(Theme.id == theme_id).first()
    subject = Subject.query.filter(Subject.id == subject_id).first()

    question_number_question_info = dict()
    for i in range(1, subject.question_count + 1):
        question_number_question_info[i] = QuestionInfo.query.filter(
            QuestionInfo.subject_id == subject.id).filter(
            QuestionInfo.number == i).first()

    test_type = TestType.query.filter(TestType.id == curr_test.testType_id).first()

    return render_template("theme/themeTest.html", test=curr_test, subject=subject, test_type=test_type, theme=theme,
                           question_number_question_info=question_number_question_info)


@app.route('/subject/<subject_id>/theme/<theme_id>/test/<test_id>/result', methods=['POST'])
@login_required
def check_theme_test(subject_id, theme_id, test_id):
    curr_test = Test.query.filter(Test.id == test_id).first()
    subject = Subject.query.filter(Subject.id == curr_test.subject_id).first()
    test_type = TestType.query.filter(TestType.id == curr_test.testType_id).first()

    first_part_first_mark = 0

    max_mark = 0.0

    for question in curr_test.questions:
        if is_first_part(curr_test, question):
            answer = request.form.get('question' + str(question.id))
            first_part_first_mark += get_mark_for_question(curr_test, question, answer)
            max_mark += get_max_mark_for_question(curr_test, question)
        else:
            max_mark += get_max_mark_for_question(curr_test, question)

    time_spent = int(request.form.get('timeSpent'))
    result_time_spent = format_time_spent(time_spent)

    path_for_solution_file = ''
    file = request.files['solutionFile']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filename = str(uuid.uuid4()) + '_' + filename
        path = os.path.join(app.config['UPLOAD_FOLDER_FOR_SOLUTIONS'], filename)
        file.save(path)
        path_for_solution_file = path

    first_part_test_mark = round(first_part_first_mark / max_mark, 4) * 100

    res = Result(
        first_part_first_mark=first_part_first_mark,
        result_first_mark=first_part_first_mark,
        first_part_test_mark=first_part_test_mark,
        result_test_mark=first_part_test_mark,
        time_spent=result_time_spent,
        test_id=test_id,
        user_id=current_user.id,
        solution_file=path_for_solution_file
    )

    db.session.add(res)
    db.session.commit()

    # result_questions = list()
    # question_id_answer = dict()
    # for question in curr_test.questions:
    #     if is_first_part(curr_test, question):
    #         answer = request.form.get('question' + str(question.id))
    #         question_id_answer[question.id] = answer
    #         result_questions.append(ResultQuestion(
    #             result_id=res.id,
    #             question_id=question.id,
    #             user_answer=answer
    #         ))
    #     else:
    #         result_questions.append(ResultQuestion(
    #             result_id=res.id,
    #             question_id=question.id,
    #             user_answer=None
    #         ))
    # res.resultQuestions = result_questions
    # db.session.commit()

    curr_test = Test.query.filter(Test.id == test_id).first()

    question_number_question_info = dict()
    for i in range(1, subject.question_count + 1):
        question_number_question_info[i] = QuestionInfo.query.filter(
            QuestionInfo.subject_id == subject.id).filter(
            QuestionInfo.number == i).first()

    rows_in_ts = TeachersStudents.query.filter(TeachersStudents.student_id == current_user.id)
    teachers = []
    for row in rows_in_ts:
        teachers.append(User.query.filter(User.id == row.teacher_id).first())

    result_questions = list()
    question_id_answer = dict()
    for question in curr_test.questions:
        if is_first_part(curr_test, question):
            answer = request.form.get('question' + str(question.id))
            question_id_answer[question.id] = answer
            result_questions.append(ResultQuestion(
                result_id=res.id,
                question_id=question.id,
                user_answer=answer
            ))
        else:
            result_questions.append(ResultQuestion(
                result_id=res.id,
                question_id=question.id,
                user_answer=None
            ))
    res.resultQuestions = result_questions
    db.session.commit()

    return render_template("results/firstResult.html", test=curr_test, result=res, question_id_answer=question_id_answer,
                            subject=subject, test_type=test_type, teachers=teachers,
                            question_number_question_info=question_number_question_info)


# @app.route('/send-to-teacher', methods=['POST'])
# @login_required
# def send_to_teacher():
#     result_id = request.form.get('result_id')
#     teacher_id = request.form.get('teacher_id')
#
#     res = Result.query.filter(Result.id == result_id).first()
#     res.teacher_id = teacher_id
#     db.session.commit()
#
#     return "Работа отправлена учителю на проверку"


def get_max_mark_for_question(curr_test, question):
    qi = find_question_info(curr_test, question)
    return qi.max_mark


def get_mark_for_question(curr_test, question, answer):
    qi = find_question_info(curr_test, question)

    if qi.max_mark > 1:
        separated_correct_answer = list(question.answer)
        separated_user_answer = list(answer)
        correct = 0
        if len(separated_user_answer) == 0:
            return 0
        for i in range(len(separated_correct_answer)):
            try:
                if separated_correct_answer[i] == separated_user_answer[i]:
                    correct += 1
            except Exception:
                pass
        if correct / float(len(separated_correct_answer)) == 1:
            return qi.max_mark
        if correct / float(len(separated_correct_answer)) >= 0.5:
            return int(qi.max_mark / 2)
    else:
        if question.answer == answer:
            return 1

    return 0


def is_first_part(curr_test, question):
    return find_question_info(curr_test, question).questionType_id == 1


def find_question_info(curr_test, question):
    return QuestionInfo.query.filter(QuestionInfo.subject_id == curr_test.subject_id).filter(
        QuestionInfo.number == question.number).first()


def format_time_spent(time_spent):
    hour = time_spent / 60 / 60 % 60
    minutes = time_spent / 60 % 60
    seconds = time_spent % 60

    correct_hours = str(trunc(hour)) if trunc(hour) >= 10 else "0" + str(trunc(hour))
    correct_minutes = str(trunc(minutes)) if trunc(minutes) >= 10 else "0" + str(trunc(minutes))
    correct_seconds = str(trunc(seconds)) if trunc(seconds) >= 10 else "0" + str(trunc(seconds))

    result_time_spent = correct_hours + ":" + correct_minutes + ":" + correct_seconds

    return result_time_spent
