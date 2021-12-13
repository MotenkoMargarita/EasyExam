from collections import OrderedDict
from operator import getitem
from urllib.parse import urlparse

from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required

from app import app, db
from model import Region, User, City
from utils.decorator import has_authority

SCORE_FOR_READ_MATERIAL = 50


@app.route('/rating', methods=['GET'])
def rating():
    o = urlparse(request.base_url)
    link = o.scheme + "://" + o.netloc

    regions = Region.query.all()
    return render_template('results/rating.html', link=link, regions=regions)


@app.route('/get-rating', methods=['GET'])
def get_rating():
    reg_id = request.args.get('region')
    city_id = request.args.get('city')

    users = User.query

    user_list = list()

    if city_id != "-1" and city_id:
        users = users.filter(User.city_id == city_id).all()
        user_list.extend(users)
    else:
        if reg_id and reg_id != "0":
            region = Region.query.filter(Region.id == reg_id).first()
            for region_cities in region.cities:
                for user in region_cities.users:
                    user_list.append(user)

    if len(user_list) == 0:
        user_list.extend(users.all())

    user_score = dict()
    for user in user_list:
        users_city = City.query.filter(City.id == user.city_id).first()
        users_region = Region.query.filter(Region.id == users_city.region_id).first()
        user_score[user.id] = {
            "score": calc_user_score(user), "first_name": user.first_name, "last_name": user.last_name,
            "city": users_city.name,
            "region": users_region.name
        }

    return jsonify(user_score)


def calc_user_score(user):
    score = 0

    for material in user.materials:
        score += SCORE_FOR_READ_MATERIAL
    for result in user.results:
        score += result.result_test_mark

    return score
