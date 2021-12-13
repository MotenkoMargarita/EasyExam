import datetime
from time import sleep

from flask import render_template

from app import app
from model import User


@app.route('/', methods=['GET'])
def welcome():
    return render_template("welcome.html")
