import traceback
import datetime
import uuid
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user
from werkzeug.security import generate_password_hash

from app import app, db
from model import User, Role, City, Region
from utils.ActivationMailSender import send_activation_email


@app.route('/registration', methods=['GET'])
def registration():
    regions = Region.query.all()

    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    return render_template("security/registration.html", regions=regions, link=link)


@app.route('/registration', methods=['POST'])
def registration_post():
    email = request.form.get('email')
    try:
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')

        city_id = request.form.get('city_id')

        user = User.query.filter(User.email == email).first()

        if user is not None:
            flash("Данный email уже занят!")
            return redirect(url_for('registration'))

        if password1 != password2:
            flash("Пароли не совпадают!")
            return redirect(url_for('registration'))

        hash_password = generate_password_hash(password1)
        new_user = User(
            email=email,
            password=hash_password,
            first_name=first_name,
            last_name=last_name,
            role_id=Role.query.filter(Role.name == 'Student').first().id,
            identifier=uuid.uuid4(),
            activation_code=uuid.uuid4(),
            registration_date=datetime.datetime.now(),
            city_id=city_id
        )
        db.session.add(new_user)
        db.session.commit()
        logout_user()

        send_activation_email(new_user)

    except Exception:
        user = User.query.filter(User.email == email).first()
        db.session.delete(user)
        db.session.commit()
        traceback.print_exc()
        flash("Не удалось зарегестрироваться")

    flash("Письмо для активации отправлено на вашу почту")

    return redirect(url_for('login'))


@app.route('/registration/activate/<email>/<code>', methods=['GET'])
def activation(email, code):
    user = User.query.filter(User.email == email).first()
    if user.activation_code == code:
        user.active = True
        user.activation_code = None
        db.session.commit()
        flash("Аккаунт успешно активированн!")

    return redirect(url_for('login'))
