import datetime
import uuid
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from app import app, db
from model import User, Region, TeachersStudents, Result
from utils.ResetPasswordMailSender import send_reset_email
from utils.decorator import has_authority


@app.route('/teacher-panel', methods=['GET'])
@login_required
def teacher_panel():
    results = Result.query.filter(Result.teacher_id == current_user.id).all()

    result_id_user = dict()

    for result in results:
        result_id_user[result.id] = User.query.filter(User.id == result.user_id).first()
    return render_template("teacher/teacherPanel.html", results=results, result_id_user=result_id_user)
