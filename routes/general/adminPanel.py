import datetime
import uuid
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from app import app, db
from model import User, Region, Role
from utils.BanMailSender import send_ban_email
from utils.ResetPasswordMailSender import send_reset_email
from utils.decorator import has_authority


@app.route('/admin-panel', methods=['GET'])
@login_required
@has_authority('Admin')
def admin_panel():
    roles = Role.query.all()

    email = request.args.get('email')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    status = request.args.get('status')
    role_id = request.args.get('role_id')

    users = User.query
    if email is not None:
        users = users.filter(User.email.ilike("%{}%".format(email)))
    if first_name is not None:
        users = users.filter(User.first_name.ilike("%{}%".format(first_name)))
    if last_name is not None:
        users = users.filter(User.last_name.ilike("%{}%".format(last_name)))

    if status is not None and status != '0':
        if status == 'True':
            users = users.filter(User.active == True)
        else:
            users = users.filter(User.active == False)
    if role_id is not None and role_id != '0':
        users = users.filter(User.role_id == role_id)

    return render_template("admin/adminPanel.html", users=users.all(), roles=roles)


@app.route('/admin-panel-change-role', methods=['POST'])
@login_required
@has_authority('Admin')
def change_user_role():
    role_id = request.form.get('role_id')

    user_id = request.form.get('user_id')
    User.query.filter(User.id == user_id).update({
        'role_id': role_id,
    })
    db.session.commit()

    user = User.query.filter(User.id == user_id).first()

    flash('Роль пользователя ' + user.email + ' успешно изменена')

    return redirect(url_for('admin_panel'))


@app.route('/admin-panel-delete-user', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_user_by_admin():
    user_id = request.form.get('user_id')
    try:
        user = User.query.filter(User.id == user_id).first()
        user_for_email = user
        send_ban_email(user_for_email)
        user_email = user.email
        db.session.delete(user)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данного пользователя')
        return redirect(url_for('admin_panel'))
    flash('Пользователь ' + user_email + ' успешно удален')

    return redirect(url_for('admin_panel'))
