import os

from flask import current_app, send_from_directory, send_file
from app import app


@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_solution(filename):
    return send_file(filename, as_attachment=True)