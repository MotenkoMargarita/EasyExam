from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, Test, Question, TestType
from utils.decorator import has_authority


@app.route('/show-test/<test_id>', methods=['GET'])
@login_required
@has_authority('Teacher')
def show_test(test_id):
    test = Test.query.filter(Test.id == test_id).first()
    subject = Subject.query.filter(Subject.id == test.subject_id).first()
    test_type = TestType.query.filter(TestType.id == test.testType_id).first()
    return render_template("test/showTest.html", test=test, subject=subject, test_type=test_type)
