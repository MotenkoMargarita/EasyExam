from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import QuestionType
from utils.decorator import has_authority


@app.route('/question-type', methods=['GET'])
@login_required
@has_authority('Admin')
def question_type():
    name = request.args.get('name')

    if name is not None:
        question_types = QuestionType.query.filter(QuestionType.name.ilike("%{}%".format(name))).order_by(
            QuestionType.name.asc()).all()
    else:
        question_types = QuestionType.query.order_by(QuestionType.name.asc()).all()
    return render_template("question/questionType.html", questionTypes=question_types)


@app.route('/question-type', methods=['POST'])
@login_required
@has_authority('Admin')
def add_question_type():
    name = request.form.get('name')
    qt = QuestionType(
        name=name
    )
    db.session.add(qt)
    db.session.commit()
    return redirect(url_for('question_type'))


@app.route('/delete-question-type', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_question_type():
    question_type_id = request.form.get('question_type_id')
    try:
        reg = QuestionType.query.filter(QuestionType.id == question_type_id).first()
        db.session.delete(reg)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный тип вопроса.')
        return redirect(url_for('question_type'))

    return redirect(url_for('question_type'))


@app.route('/change-question-type', methods=['POST'])
@login_required
@has_authority('Admin')
def change_question_type():
    question_type_id = request.form.get('question_type_id')
    QuestionType.query.filter(QuestionType.id == question_type_id).update({'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('question_type'))
