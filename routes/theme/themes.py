import json
import traceback
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, QuestionType, QuestionInfo, Question, FirstScoreTestScore, Theme, Material, Test
from utils.decorator import has_authority


@app.route('/subject/<subject_id>/themes', methods=['GET'])
def themes(subject_id):
    subject = Subject.query.filter(Subject.id == subject_id).first()
    all_themes = Theme.query.filter(Theme.subject_id == subject_id).all()

    return render_template("theme/themes.html", themes=all_themes, subject=subject)


@app.route('/subject/<subject_id>/theme/<theme_id>', methods=['GET'])
def theme(subject_id, theme_id):
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc


    subject = Subject.query.filter(Subject.id == subject_id).first()
    curr_theme = Theme.query.filter(Theme.id == theme_id).first()

    materials_for_curr_theme = Material.query.filter(Material.theme_id == curr_theme.id).all()

    tests_for_curr_theme = Test.query.filter(Test.theme_id == curr_theme.id).all()

    return render_template("theme/theme.html", theme=curr_theme, subject=subject, link=link,
                           materials_for_curr_theme=materials_for_curr_theme, tests_for_curr_theme=tests_for_curr_theme)


