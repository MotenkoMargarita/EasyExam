from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Requirement, Subject, Criteria
from utils.decorator import has_authority


@app.route('/question-requirement/subject/<subject_id>/question-number/<question_number>', methods=['GET'])
@login_required
def show_req(subject_id, question_number):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    question_requirement = Requirement.query.filter(Requirement.subject_id == subject_id).filter(Requirement.number == question_number).first()
    return render_template("question/showRequirement.html", question_requirement=question_requirement,subject=subject,question_number=question_number)


@app.route('/question-requirement', methods=['GET'])
@login_required
@has_authority('Admin')
def question_req():
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    subjects = Subject.query.all()

    subject_id = request.args.get('subject_id')
    number = request.args.get('number')
    text = request.args.get('text')

    question_requirements = Requirement.query
    if text is not None and text != '':
        question_requirements = question_requirements.filter(Requirement.text.ilike("%{}%".format(text)))
    if number is not None and number != '':
        question_requirements = question_requirements.filter(Requirement.number == number)
    if subject_id is not None and subject_id != '0':
        question_requirements = question_requirements.filter(Requirement.subject_id == subject_id)

    return render_template("question/questionRequirements.html", question_requirements=question_requirements.all(),
                           subjects=subjects,
                           link=link)


@app.route('/question-requirement', methods=['POST'])
@login_required
@has_authority('Admin')
def add_question_req():
    criteria_count = request.form.get('criteriaCount')

    number = request.form.get('number')
    text = request.form.get('text')

    print(repr(text))

    subject_id = request.form.get('subject_id')

    req = Requirement(
        number=number,
        text=text,
        subject_id=subject_id,
    )
    db.session.add(req)
    db.session.commit()

    for i in range(1, int(criteria_count) + 1):
        curr_text = request.form.get('text' + str(i))
        curr_value = request.form.get('value' + str(i))
        criteria = Criteria(
            text=curr_text,
            value=curr_value,
            requirement_id=req.id

        )
        db.session.add(criteria)
        db.session.commit()

    return redirect(url_for('question_req'))


@app.route('/delete-question-requirement/<question_req_id>', methods=['GET'])
@login_required
@has_authority('Admin')
def delete_question_req(question_req_id):
    try:
        req = Requirement.query.filter(Requirement.id == question_req_id).first()

        for curr in req.criteria:
            cr = Criteria.query.filter(Criteria.id == curr.id).first()
            db.session.delete(cr)
            db.session.commit()

        db.session.delete(req)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный тип вопроса.')
        return redirect(url_for('question_req'))

    return redirect(url_for('question_req'))


@app.route('/change-question-requirement', methods=['POST'])
@login_required
@has_authority('Admin')
def change_question_req():
    question_req_id = request.form.get('question_req_id')

    subject_id = request.form.get('subject_id')
    number = request.form.get('number')
    text = request.form.get('text')

    print(text)

    subject = Subject.query.filter(Subject.id == subject_id).first()

    if subject.question_count <= int(number):
        flash('У данного предмета нет такого количества вопросов')
        return redirect(url_for('question_req'))

    Requirement.query.filter(Requirement.id == question_req_id).update({
        'subject_id': subject_id,
        'number': number,
        'text': text
    })
    db.session.commit()

    req = Requirement.query.filter(Requirement.id == question_req_id).first()

    for curr in req.criteria:
        Criteria.query.filter(Criteria.id == curr.id).update({
            'text': request.form.get('text' + str(curr.id)),
            'value': request.form.get('value' + str(curr.id)),
        })
        db.session.commit()

    return redirect(url_for('question_req'))
