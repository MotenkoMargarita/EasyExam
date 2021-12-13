from flask import render_template, redirect, url_for, flash

from app import app


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@app.errorhandler(401)
def page_not_found(e):
    flash('Для продолжения нужно войти')
    return redirect(url_for('login'))
    # return render_template('error/401.html'), 401


@app.errorhandler(403)
def page_not_found(e):
    return render_template('error/403.html'), 403


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error/500.html'), 500


