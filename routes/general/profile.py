import datetime
import uuid
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from app import app, db
from model import User, Region, TeachersStudents
from utils.ResetPasswordMailSender import send_reset_email
from utils.decorator import has_authority


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    regions = Region.query.all()
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    rows_in_ts = TeachersStudents.query.filter(TeachersStudents.student_id == current_user.id)
    teachers = []
    for row in rows_in_ts:
        teachers.append(User.query.filter(User.id == row.teacher_id).first())

    return render_template("user/profile.html", regions=regions, link=link, teachers=teachers)


@app.route('/profile/reset-password', methods=['GET'])
@login_required
def profile_reset_password():
    if current_user.last_password_reset is not None and abs(
            (current_user.last_password_reset - datetime.datetime.now()).total_seconds()) < 60:
        flash("Повторите попытку позже. Примерно через " + str(round(
            60 - abs((current_user.last_password_reset - datetime.datetime.now()).total_seconds()))) + " секунд")
        return redirect(url_for('profile'))

    current_user.reset_code = uuid.uuid4()
    current_user.last_password_reset = datetime.datetime.now()
    db.session.commit()
    send_reset_email(current_user)
    flash("Письмо для изменения пароля успешно отправлено")
    return redirect(url_for('profile'))


@app.route('/change-profile', methods=['POST'])
@login_required
def change_profile():
    User.query.filter(User.id == current_user.id).update({
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'city_id': request.form.get('city_id'),
        'src': request.form.get('imgSrc')
    })
    flash('Данные успешно сохранены')
    db.session.commit()
    return redirect(url_for('profile'))
