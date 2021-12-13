from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from sqlalchemy import func

from app import app, db
from model import City, Region
from utils.decorator import has_authority


@app.route('/cities/<region_id>', methods=['GET'])
def cities_json(region_id):
    reg = Region.query.filter(Region.id == region_id).first()
    if reg is None:
        return jsonify(dict())
    cities_in_region = City.query.filter(City.region_id == reg.id).order_by(City.name.asc()).all()
    result = dict()
    for c in cities_in_region:
        result[c.name] = c.id

    return jsonify(result)


@app.route('/city', methods=['GET'])
@login_required
@has_authority('Admin')
def city():
    reg = request.args.get('region')
    cty = request.args.get('city')

    cities = City.query
    if reg is not None and reg != '':
        r = Region.query.filter(Region.name == reg).first()
        if r is not None:
            cities = cities.filter(City.region_id == r.id)
        else:
            cities = cities.filter(City.region_id == -1)
    if cty is not None and cty != '':
        cities = cities.filter(City.name.ilike("%{}%".format(cty)))

    all_cities = City.query.all()

    regions = Region.query.order_by(Region.name.asc()).all()
    return render_template("location/city.html", cities=cities.all(), regions=regions, all_cities=all_cities)


@app.route('/city', methods=['POST'])
@login_required
@has_authority('Admin')
def add_city():
    region_name = request.form.get('region_name')
    name = request.form.get('name')
    reg = Region.query.filter(func.lower(Region.name) == func.lower(region_name)).first()

    if reg is None:
        flash('Данный субъект федерации не найден')
        return redirect(url_for('city'))

    cty = City(
        name=name,
        region_id=reg.id
    )
    db.session.add(cty)
    db.session.commit()
    return redirect(url_for('city'))


@app.route('/delete-city', methods=['POST'])
@login_required
@has_authority('Admin')
def delete_city():
    city_id = request.form.get('city_id')
    try:
        cty = City.query.filter(City.id == city_id).first()
        db.session.delete(cty)
        db.session.commit()
    except Exception:
        flash('Невозможно удалть данный населенный пункт.')
        return redirect(url_for('city'))

    return redirect(url_for('city'))


@app.route('/change-city', methods=['POST'])
@login_required
@has_authority('Admin')
def change_city():
    region_name = request.form.get('region_name')
    name = request.form.get('name')
    reg = Region.query.filter(func.lower(Region.name) == func.lower(region_name)).first()

    if reg is None:
        flash('Данный субъект федерации не найден')
        return redirect(url_for('city'))

    city_id = request.form.get('city_id')
    City.query.filter(City.id == city_id).update({
        'name': name,
        'region_id': reg.id
    })
    db.session.commit()
    return redirect(url_for('city'))
