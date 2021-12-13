import json
import traceback

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, QuestionType, QuestionInfo, Question, FirstScoreTestScore
from utils.decorator import has_authority


@app.route('/subjects', methods=['GET'])
def subjects():
    all_subjects = Subject.query.order_by(Subject.name.asc())

    return render_template("subject/subjects.html", subjects=all_subjects.all())

