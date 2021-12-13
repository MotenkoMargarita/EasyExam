import json
import traceback
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify, Response
from flask_login import login_required, current_user

from app import app, db
from model import Subject, QuestionType, QuestionInfo, Question, FirstScoreTestScore, Theme, Material, Test
from utils.decorator import has_authority


@app.route('/subject/<subject_id>/theme/<theme_id>/material/<material_id>', methods=['GET'])
def mark_material(subject_id, theme_id, material_id):

    curr_material = Material.query.filter(Material.id == material_id).first()
    if curr_material not in current_user.materials:
        current_user.materials.append(curr_material)
    else:
        current_user.materials.remove(curr_material)
    db.session.commit()

    return Response(status=200)
