import traceback

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user

from app import app, db
from model import TeachersStudents, User
from utils.decorator import has_authority


@app.route('/students', methods=['GET'])
@login_required
@has_authority('Teacher')
def students():
    name = request.args.get('name')
    last = request.args.get('last')
    email = request.args.get('email')

    all_teachers_students = TeachersStudents.query.filter(TeachersStudents.teacher_id == current_user.id).all()

    show = False
    all_users = User.query
    if email and email != '':
        show = True
        all_users = User.query.filter(User.email.ilike("%{}%".format(email)))
    if name and name != '':
        show = True
        all_users = User.query.filter(User.first_name.ilike("%{}%".format(name)))
    if last and last != '':
        show = True
        all_users = User.query.filter(User.last_name.ilike("%{}%".format(last)))

    all_added_students = []
    for ts in all_teachers_students:
        all_added_students.append(User.query.filter(User.id == ts.student_id).first())

    return render_template("teacher/students.html", all_added_students=all_added_students, all_users=all_users.all(), show=show)


@app.route('/students', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_student():
    identifier = request.form.get('identifier')

    student = User.query.filter(User.identifier == identifier).first()

    if student is None:
        flash("Данный пользователь не найден")
        return redirect(url_for('students'))
    ts = TeachersStudents.query.filter(TeachersStudents.student_id == student.id).filter(
        TeachersStudents.teacher_id == current_user.id).first()
    if ts is not None:
        flash("Данный пользователь уже являеться вашим учеником")
        return redirect(url_for('students'))

    stud = TeachersStudents(
        teacher_id=current_user.id,
        student_id=student.id
    )
    db.session.add(stud)
    db.session.commit()

    return redirect(url_for('students'))


@app.route('/students-simple', methods=['POST'])
@login_required
@has_authority('Teacher')
def simple_add_student():
    student_id = request.form.get('student_id')

    student = User.query.filter(User.id == student_id).first()

    ts = TeachersStudents.query.filter(TeachersStudents.student_id == student.id).filter(
        TeachersStudents.teacher_id == current_user.id).first()

    if ts is not None:
        flash("Данный пользователь уже являеться вашим учеником ")
        return redirect(url_for('students'))

    stud = TeachersStudents(
        teacher_id=current_user.id,
        student_id=student.id
    )
    db.session.add(stud)
    db.session.commit()

    return redirect(url_for('students'))


@app.route('/delete-student', methods=['POST'])
@login_required
@has_authority('Teacher')
def delete_student():
    student_id = request.form.get('student_id')
    try:
        ts = TeachersStudents.query.filter(TeachersStudents.student_id == student_id).filter(
            TeachersStudents.teacher_id == current_user.id).first()
        db.session.delete(ts)
        db.session.commit()
    except Exception:
        traceback.print_exc()
        flash('Невозможно удалть данную связь')
        return redirect(url_for('students'))

    return redirect(url_for('students'))
