from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Criteria
from utils.decorator import has_authority


@app.route('/criteria', methods=['GET'])
@login_required
@has_authority('Admin')
def criteria():
    text = request.args.get('text')

    if text is not None:
        all_criteria = Criteria.query.filter(Criteria.text.ilike("%{}%".format(text))).order_by(
            Criteria.text.asc()).all()
    else:
        all_criteria = Criteria.query.order_by(Criteria.text.asc()).all()
    return render_template("question/criteria.html", all_criteria=all_criteria)


@app.route('/criteria', methods=['POST'])
@login_required
@has_authority('Admin')
def add_criteria():
    text = request.form.get('text')
    try:
        value = int(request.form.get('value'))
    except Exception:
        flash('Введите целое число')
        return redirect(url_for('criteria'))
    qt = Criteria(
        text=text,
        value=value
    )
    db.session.add(qt)
    db.session.commit()
    return redirect(url_for('criteria'))


@app.route('/delete-criteria', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_criteria():
    criteria_id = request.form.get('criteria_id')
    try:
        ct = Criteria.query.filter(Criteria.id == criteria_id).first()
        db.session.delete(ct)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный критерий.')
        return redirect(url_for('criteria'))

    return redirect(url_for('criteria'))


@app.route('/change-criteria', methods=['POST'])
@login_required
@has_authority('Admin')
def change_criteria():
    criteria_id = request.form.get('criteria_id')
    Criteria.query.filter(Criteria.id == criteria_id).update({
        'text': request.form.get('text'),
        'value': request.form.get('value')
    })
    db.session.commit()
    return redirect(url_for('criteria'))
