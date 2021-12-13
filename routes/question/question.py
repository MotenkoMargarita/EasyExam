from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Question, Subject, QuestionType, Source, Image, QuestionInfo
from utils.decorator import has_authority


@app.route('/question', methods=['GET'])
@login_required
@has_authority('Teacher')
def question():
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    subjects = Subject.query.all()
    question_types = QuestionType.query.all()
    sources = Source.query.all()

    subject_id = request.args.get('subject_id')
    number = request.args.get('number')
    text = request.args.get('text')
    answer = request.args.get('answer')

    questions = Question.query
    if text is not None and text != '':
        questions = questions.filter(Question.text.ilike("%{}%".format(text)))
    if number is not None and number != '':
        questions = questions.filter(Question.number == number)
    if subject_id is not None and subject_id != '0':
        questions = questions.filter(Question.subject_id == subject_id)
    if answer is not None and answer != '':
        questions = questions.filter(Question.answer.ilike("%{}%".format(answer)))

    return render_template("question/questions.html", questions=questions.all(), subjects=subjects, link=link,
                           question_types=question_types, sources=sources)


@app.route('/question/<question_id>', methods=['GET'])
@login_required
def show_question(question_id):
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    curr_question = Question.query.filter(Question.id == question_id).first()

    is_second = QuestionType.query.filter(QuestionType.id == QuestionInfo.query.filter(QuestionInfo.subject_id == Subject.query.filter(Subject.id == curr_question.subject_id).first().id).filter(QuestionInfo.number == curr_question.number).first().questionType_id).first().name == 'C'
    subjects = Subject.query.all()
    sources = Source.query.all()

    return render_template("question/question.html", question=curr_question, subjects=subjects, sources=sources, link=link,is_second=is_second)


@app.route('/question-preview/<question_id>', methods=['GET'])
@login_required
@has_authority('Teacher')
def one_question(question_id):
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    curr_question = Question.query.filter(Question.id == question_id).first()

    subjects = Subject.query.all()
    sources = Source.query.all()

    return render_template("question/oneQuestion.html", question=curr_question, subjects=subjects, sources=sources, link=link)


@app.route('/question', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_question():
    number = request.form.get('number')
    text = request.form.get('text')
    # value = request.form.get('value')
    subject_id = request.form.get('subject_id')
    # question_type_id = request.form.get('question_type_id')
    source_id = request.form.get('source_id')
    if int(source_id) == 0:
        source_id = None
    answer = request.form.get('answer')

    max_image_count = request.form.get('maxImageCount');

    print(max_image_count)

    quest = Question(
        text=text,
        number=number,
        subject_id=subject_id,
        source_id=source_id,
        answer=answer
    )
    db.session.add(quest)
    db.session.commit()

    for i in range(1, int(max_image_count) + 1):
        try:
            question_image_input = request.form.get('questionImageInput' + str(i))

            if question_image_input:
                img = Image(
                    source=question_image_input,
                    question_id=quest.id
                )
                db.session.add(img)
                db.session.commit()
        except Exception as e:
            print(e)

    return redirect(url_for('question'))


@app.route('/delete-question/<question_id>', methods=['GET'])
@login_required
@has_authority('Teacher')
def delete_question(question_id):
    try:
        quest = Question.query.filter(Question.id == question_id).first()

        db.session.delete(quest)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный вопрос.')
        return redirect(url_for('question'))

    return redirect(url_for('question'))


@app.route('/change-question', methods=['POST'])
@login_required
@has_authority('Teacher')
def change_question():
    question_id = request.form.get('question_id')
    subject_id = request.form.get('subject_id')
    # question_type_id = request.form.get('question_type_id')
    source_id = request.form.get('source_id')
    number = request.form.get('number')
    text = request.form.get('text')
    # value = request.form.get('value')
    answer = request.form.get('answer')

    Question.query.filter(Question.id == question_id).update({
        'number': number,
        'text': text,
        # 'max_mark': value,
        'subject_id': subject_id,
        # 'questionType_id': question_type_id,
        'source_id': source_id,
        'answer': answer
    })
    db.session.commit()

    return redirect(url_for('question'))
