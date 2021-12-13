import datetime
from time import sleep

from flask import render_template

from app import app
from model import User


@app.route('/terms-of-use', methods=['GET'])
def terms_of_use():
    return render_template("termsOfUse.html")
