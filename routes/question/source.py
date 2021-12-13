from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Source
from utils.decorator import has_authority


@app.route('/source', methods=['GET'])
@login_required
@has_authority('Teacher')
def source():
    name = request.args.get('name')

    if name is not None:
        sources = Source.query.filter(Source.name.ilike("%{}%".format(name))).order_by(
            Source.name.asc()).all()
    else:
        sources = Source.query.order_by(Source.name.asc()).all()
    return render_template("question/source.html", sources=sources)


@app.route('/source', methods=['POST'])
@login_required
@has_authority('Teacher')
def add_source():
    name = request.form.get('name')
    link = request.form.get('link')
    src = Source(
        name=name,
        link=link
    )
    db.session.add(src)
    db.session.commit()
    return redirect(url_for('source'))


@app.route('/delete-source', methods=['POST'])
@login_required
@has_authority('Teacher')
def delete_source():
    source_id = request.form.get('source_id')
    try:
        src = Source.query.filter(Source.id == source_id).first()
        db.session.delete(src)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный источник.')
        return redirect(url_for('source'))

    return redirect(url_for('source'))


@app.route('/change-source', methods=['POST'])
@login_required
@has_authority('Teacher')
def change_source():
    source_id = request.form.get('source_id')
    Source.query.filter(Source.id == source_id).update({
        'name': request.form.get('name'),
        'link': request.form.get('link')
    })
    db.session.commit()
    return redirect(url_for('source'))
