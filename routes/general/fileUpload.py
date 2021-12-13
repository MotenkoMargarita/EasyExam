import os
import uuid

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import func
from werkzeug.utils import secure_filename

from app import app, db, ALLOWED_PROFILE_IMAGE_EXTENSIONS
from model import City, Region
from utils.decorator import has_authority


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_PROFILE_IMAGE_EXTENSIONS


@app.route('/upload/image', methods=['POST'])
def upload_profile_photo():
    try:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + '_' + filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return path
        else:
            return 'Выбирите другой формат файла'
    except Exception:
        return 'Проблемы при загрузке файла'


@app.route('/upload/file', methods=['POST'])
def upload_file():
    try:
        file = request.files['photo']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + '_' + filename
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return path
        else:
            return 'Выбирите другой формат файла'
    except Exception:
        return 'Проблемы при загрузке файла'
