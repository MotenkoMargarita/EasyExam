from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Subject, Theme
from utils.decorator import has_authority


@app.route('/create-theme', methods=['GET'])
@login_required
@has_authority('Teacher')
def create_theme():
    subjects = Subject.query.all()
    themes = Theme.query.all()
    return render_template("theme/createTheme.html", subjects=subjects, themes=themes)


@app.route('/add-theme', methods=['POST'])
@login_required
@has_authority('Admin')
def add_theme():
    name = request.form.get('name')
    description = request.form.get('description')
    subject_id = request.form.get('subject_id')
    theme = Theme(
        name=name,
        description=description,
        subject_id=subject_id
    )
    db.session.add(theme)
    db.session.commit()
    return redirect(url_for('create_theme'))


@app.route('/delete-theme', methods=['POST'])
@login_required
@has_authority('Teacher')
def delete_theme():
    theme_id = request.form.get('theme_id')
    try:
        theme = Theme.query.filter(Theme.id == theme_id).first()
        db.session.delete(theme)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данную тему.')
        return redirect(url_for('create_theme'))

    return redirect(url_for('create_theme'))


@app.route('/change-theme', methods=['POST'])
@login_required
@has_authority('Teacher')
def change_theme():
    theme_id = request.form.get('theme_id')
    Theme.query.filter(Theme.id == theme_id).update({
        'name': request.form.get('name'),
        'description': request.form.get('description')
    })
    db.session.commit()
    return redirect(url_for('create_theme'))
