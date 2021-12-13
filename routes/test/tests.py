import json
import traceback

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, QuestionType, QuestionInfo, Question, FirstScoreTestScore, Theme, Material, Test
from utils.decorator import has_authority


@app.route('/subject/<subject_id>/tests', methods=['GET'])
def tests(subject_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    all_tests = Test.query.filter(Test.subject_id == subject_id).filter(Test.is_for_theme == False).all()

    return render_template("test/tests.html", tests=all_tests, subject=subject)
