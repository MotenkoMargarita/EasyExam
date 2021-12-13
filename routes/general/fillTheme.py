import os
import uuid
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db
from model import Subject, Theme, Material, Image, TestType, Test, Question, QuestionInfo
from routes.general.fileUpload import allowed_file
from utils.decorator import has_authority


@app.route('/fill-theme/<theme_id>', methods=['GET'])
@login_required
@has_authority('Teacher')
def show_theme_content(theme_id):
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    test_types = TestType.query.all()

    theme = Theme.query.filter(Theme.id == theme_id).first()
    subject = Subject.query.filter(Subject.id == theme.subject_id).first()

    curr_materials = Material.query.filter(Material.theme_id == theme.id).all()
    curr_tests = Test.query.filter(Test.theme_id == theme.id).all()

    return render_template("theme/fillTheme.html", theme=theme, subject=subject, curr_materials=curr_materials, link=link,
                           test_types=test_types, curr_tests=curr_tests)


@app.route('/add_test_to_theme', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_test_to_theme():
    max_question_count = request.form.get('maxQuestionCount')
    theme_id = request.form.get('theme_id')
    number_in_order = request.form.get('number_in_order')
    description = request.form.get('description')

    theme = Theme.query.filter(Theme.id == theme_id).first()
    subject = Subject.query.filter(Subject.id == theme.subject_id).first()
    test_type_id = request.form.get('testType_id')

    questions = []
    max_question_mark_sum = 0
    for i in range(1, int(max_question_count) + 1):
        question_id = request.form.get('qs' + str(i))
        if question_id:
            question = Question.query.filter(Question.id == question_id).first()
            question_info = QuestionInfo.query.filter(QuestionInfo.number == question.number)\
                .filter(QuestionInfo.subject_id == question.subject_id).first()
            max_question_mark_sum = max_question_mark_sum + question_info.max_mark
            questions.append(question)

    test_for_theme = Test(
        max_first_score=max_question_mark_sum,
        subject_id=subject.id,
        testType_id=test_type_id,
        theme_id=theme.id,
        number_in_order=number_in_order,
        is_for_theme=True,
        description=description
    )
    db.session.add(test_for_theme)
    db.session.commit()

    test_for_theme.questions = questions
    db.session.commit()

    return redirect(url_for('show_theme_content', theme_id=theme_id))


@app.route('/add_to_theme', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_to_material_theme():
    try:
        name = request.form.get('name')
        text = request.form.get('text')
        description = request.form.get('description')
        number_in_order = request.form.get('number_in_order')
        theme_id = request.form.get('theme_id')

        if number_in_order is None or number_in_order == '':
            number_in_order = 1

        material = Material(
            name=name,
            text=text,
            number_in_order=number_in_order,
            theme_id=theme_id,
            description=description
        )
        db.session.add(material)
        db.session.commit()

        try:
            path_for_material_file = None
            file = request.files['material_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filename = str(uuid.uuid4()) + '_' + filename
                path = os.path.join(app.config['UPLOAD_FOLDER_FOR_SOLUTIONS'], filename)
                file.save(path)
                path_for_material_file = path
                material.file = path_for_material_file
                db.session.commit()
        except Exception as e:
            print(e)

        max_image_count = int(request.form.get('maxImageCount'))
        for i in range(1, max_image_count + 1):
            if request.form.get('materialImageInput' + str(i)):
                img = Image(source=request.form.get('materialImageInput' + str(i)), material_id=material.id)
                db.session.add(img)
                db.session.commit()
    except Exception as e:
        flash('Ошибка при добавленнии')
        print(e)

    return redirect(url_for('show_theme_content', theme_id=theme_id))


@app.route('/delete-material-del', methods=['POST'])
@login_required
@has_authority('Teacher')
def delete_material_del():
    material_id = request.form.get('material_id')
    theme_id = request.form.get('theme_id')
    try:
        material = Material.query.filter(Material.id == material_id).first()
        db.session.delete(material)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный материал.')
        return redirect(url_for('show_theme_content', theme_id=theme_id))

    return redirect(url_for('show_theme_content', theme_id=theme_id))


@app.route('/delete-test-del', methods=['POST'])
@login_required
@has_authority('Teacher')
def delete_test_del():
    test_id = request.form.get('test_id')
    theme_id = request.form.get('theme_id')
    try:
        Test.query.filter(Test.id == test_id).update({
            'theme_id': None,
        })
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный тест.')
        return redirect(url_for('show_theme_content', theme_id=theme_id))

    return redirect(url_for('show_theme_content', theme_id=theme_id))


@app.route('/change-material', methods=['POST'])
@login_required
@has_authority('Teacher')
def change_material():
    material_id = request.form.get('material_id')
    Material.query.filter(Material.id == material_id).update({
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'text': request.form.get('text'),
        'number_in_order': request.form.get('number_in_order'),
    })
    db.session.commit()
    theme_id = request.form.get('theme_id')
    return redirect(url_for('show_theme_content', theme_id=theme_id))


@app.route('/change-test', methods=['POST'])
@login_required
@has_authority('Teacher')
def change_test():
    test_id = request.form.get('test_id')
    Test.query.filter(Test.id == test_id).update({
        'number_in_order': request.form.get('number_in_order'),
    })
    db.session.commit()
    theme_id = request.form.get('theme_id')
    return redirect(url_for('show_theme_content', theme_id=theme_id))
