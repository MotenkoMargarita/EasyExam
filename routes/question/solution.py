import os
import uuid

from flask import render_template, request, redirect, url_for
from flask_login import login_required
from werkzeug.utils import secure_filename

from app import app, db
from model import Image, Solution
from routes.general.fileUpload import allowed_file
from utils.decorator import has_authority


@app.route('/solution', methods=['GET'])
@login_required
@has_authority('Teacher')
def solution():
    question_id = request.args.get('question_id')
    return render_template('question/solution.html', question_id=question_id)


@app.route('/add_solution', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_solution():
    text = request.form.get('text')
    description = request.form.get('description')

    question_id = request.form.get('question_id')

    curr_solution = Solution(
        question_id=question_id,
        text=text,
        description=description
    )
    db.session.add(curr_solution)
    db.session.commit()

    try:
        path_for_material_file = None
        file = request.files['solution_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = str(uuid.uuid4()) + '_' + filename
            path = os.path.join(app.config['UPLOAD_FOLDER_FOR_SOLUTIONS'], filename)
            file.save(path)
            path_for_material_file = path
            curr_solution.file = path_for_material_file
            db.session.commit()
    except Exception as e:
        print(e)

    max_image_count = int(request.form.get('maxImageCount'))
    for i in range(1, max_image_count + 1):
        if request.form.get('solutionImageInput' + str(i)):
            img = Image(source=request.form.get('solutionImageInput' + str(i)), solution_id=curr_solution.id)
            db.session.add(img)
            db.session.commit()

    return redirect(url_for('show_question', question_id=question_id))
