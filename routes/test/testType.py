from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import TestType
from utils.decorator import has_authority


@app.route('/test-type', methods=['GET'])
@login_required
@has_authority('Admin')
def test_type():
    name = request.args.get('name')

    if name is not None:
        test_types = TestType.query.filter(TestType.name.ilike("%{}%".format(name))).order_by(
            TestType.name.asc()).all()
    else:
        test_types = TestType.query.order_by(TestType.name.asc()).all()
    return render_template("test/testType.html", testTypes=test_types)


@app.route('/test-type', methods=['POST'])
@login_required
@has_authority('Admin')
def add_test_type():
    name = request.form.get('name')
    qt = TestType(
        name=name
    )
    db.session.add(qt)
    db.session.commit()
    return redirect(url_for('test_type'))


@app.route('/delete-test-type', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_test_type():
    test_type_id = request.form.get('test_type_id')
    try:
        reg = TestType.query.filter(TestType.id == test_type_id).first()
        db.session.delete(reg)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный тип вопроса.')
        return redirect(url_for('test_type'))

    return redirect(url_for('test_type'))


@app.route('/change-test-type', methods=['POST'])
@login_required
@has_authority('Admin')
def change_test_type():
    test_type_id = request.form.get('test_type_id')
    TestType.query.filter(TestType.id == test_type_id).update({'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('test_type'))
