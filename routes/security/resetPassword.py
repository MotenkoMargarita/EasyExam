import uuid

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user
from werkzeug.security import generate_password_hash

from app import app, db
from model import User
import datetime
from utils.ResetPasswordMailSender import send_reset_email


@app.route('/find-user-to-reset-password', methods=['GET'])
def find_user_to_reset_password():
    return render_template("security/passwordResetConfirmEmail.html")


@app.route('/find-user-to-reset-password', methods=['POST'])
def find_user_to_reset_password_send_email():
    email = request.form.get('email')
    curr_user = User.query.filter(User.email == email).first()

    if curr_user is not None and curr_user.is_active:
        if curr_user.last_password_reset is not None and abs(
                (curr_user.last_password_reset - datetime.datetime.now()).total_seconds()) < 60:
            flash("Повторите попытку позже. Примерно через " + str(round(
                60 - abs((curr_user.last_password_reset - datetime.datetime.now()).total_seconds()))) + " секунд")
            return redirect(url_for('find_user_to_reset_password'))
        curr_user.reset_code = uuid.uuid4()
        curr_user.last_password_reset = datetime.datetime.now()
        db.session.commit()
        send_reset_email(curr_user)
        flash("Письмо для сброса пароля успешно отправлено")
    else:
        flash("Пользователь с таким email не найден")
    return redirect(url_for('find_user_to_reset_password'))


@app.route('/reset-password/<email>/<code>', methods=['GET'])
def show_reset_password(email, code):
    user = User.query.filter(User.email == email).first()
    if user.reset_code == code:
        user.reset_code = None
        db.session.commit()
        return render_template("security/passwordReset.html", email=email)
    else:
        flash("Код восстановления не верный. Запросите новое письмо.")
        return redirect(url_for('find_user_to_reset_password'))


@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 != password2:
        flash("Пароли не совпадают!")
        return redirect(url_for('reset_password'))
    else:
        new_hash_password = generate_password_hash(password1)
        curr_user = User.query.filter(User.email == email).first()
        curr_user.password = new_hash_password
        db.session.commit()
        flash("Пароль успешно изменен")
        logout_user()
        return redirect(url_for('login'))
