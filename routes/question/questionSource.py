from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Source
from utils.decorator import has_authority


@app.route('/question-source', methods=['GET'])
@login_required
@has_authority('Teacher')
def question_source():
    name = request.args.get('name')

    if name is not None:
        question_sources = Source.query.filter(Source.name.ilike("%{}%".format(name))).order_by(
            Source.name.asc())
    else:
        question_sources = Source.query.order_by(Source.name.asc())
    return render_template("question/questionSource.html", question_sources=question_sources.all())


@app.route('/question-source', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_question_source():
    name = request.form.get('name')
    link = request.form.get('link')
    qs = Source(
        name=name,
        link=link
    )
    db.session.add(qs)
    db.session.commit()
    return redirect(url_for('question_source'))


@app.route('/delete-question-source', methods=['POST'])
@login_required
@has_authority('Teacher')
def delete_question_source():
    question_source_id = request.form.get('question_source_id')
    try:
        qs = Source.query.filter(Source.id == question_source_id).first()
        db.session.delete(qs)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный тип вопроса.')
        return redirect(url_for('question_source'))

    return redirect(url_for('question_source'))


@app.route('/change-question-source', methods=['POST'])
@login_required
@has_authority('Teacher')
def change_question_source():
    question_source_id = request.form.get('question_source_id')
    Source.query.filter(Source.id == question_source_id).update(
        {'name': request.form.get('name'), 'link': request.form.get('link')}
    )
    db.session.commit()
    return redirect(url_for('question_source'))
