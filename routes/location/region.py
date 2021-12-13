from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Region
from utils.decorator import has_authority


@app.route('/regions', methods=['GET'])
def regions_json():
    regions = Region.query.order_by(Region.name.asc()).all()
    regs = list()
    for r in regions:
        regs.append(r.name)
    return jsonify(regs)


@app.route('/region', methods=['GET'])
@login_required
@has_authority('Admin')
def region():
    name = request.args.get('name')

    if name is not None:
        regions = Region.query.filter(Region.name.ilike("%{}%".format(name))).order_by(Region.name.asc()).all()
    else:
        regions = Region.query.order_by(Region.name.asc()).all()
    return render_template("location/region.html", regions=regions)


@app.route('/region', methods=['POST'])
@login_required
@has_authority('Admin')
def add_region():
    name = request.form.get('name')
    reg = Region(
        name=name
    )
    db.session.add(reg)
    db.session.commit()
    return redirect(url_for('region'))


@app.route('/delete-region', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_region():
    region_id = request.form.get('region_id')
    try:
        reg = Region.query.filter(Region.id == region_id).first()
        db.session.delete(reg)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный регион.')
        return redirect(url_for('region'))

    return redirect(url_for('region'))


@app.route('/change-region', methods=['POST'])
@login_required
@has_authority('Admin')
def change_region():
    region_id = request.form.get('region_id')
    Region.query.filter(Region.id == region_id).update({'name': request.form.get('name')})
    db.session.commit()
    return redirect(url_for('region'))
