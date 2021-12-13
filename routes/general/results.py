from flask import render_template, abort
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import app
from model import Result, Test, Subject, TestType, QuestionInfo, ResultQuestion, \
    FirstScoreTestScore


@app.route('/results', methods=['GET'])
@login_required
def show_user_results():
    results = Result.query.filter(Result.user_id == current_user.id).all()

    result_id_subject = dict()
    subject_set = set()
    for curr_result in results:
        curr_test = Test.query.filter(Test.id == curr_result.test_id).first()
        curr_subject = Subject.query.filter(Subject.id == curr_test.subject_id).first()
        subject_set.add(curr_subject)
        result_id_subject[curr_result.id] = curr_subject

    subject_id_max_marks = dict()
    for curr_subject in subject_set:
        fsts = FirstScoreTestScore.query.filter(FirstScoreTestScore.subject_id == curr_subject.id).order_by(
            desc(FirstScoreTestScore.first_score)).limit(1).first()
        subject_id_max_marks[curr_subject.id] = fsts

    result_id_test = dict()
    for curr_result in results:
        test_id = curr_result.test_id
        test = Test.query.filter(Test.id == test_id).first()
        result_id_test[curr_result.id] = test

    return render_template("results/results.html", results=results, result_id_subject=result_id_subject,
                           subject_id_max_marks=subject_id_max_marks, result_id_test=result_id_test)


@app.route('/result/<result_id>', methods=['GET'])
@login_required
def result(result_id):
    result = Result.query.filter(Result.id == result_id).first()

    if result.user_id != current_user.id:
        return abort(403)

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

    return render_template("results/result.html", test=test, result=result, question_id_answer=question_id_answer,
                           subject=subject, test_type=test_type, question_id_comment=question_id_comment,
                           question_number_question_info=question_number_question_info, comment=comment,
                           question_id_mark=question_id_mark)
