"""
This view is the home
"""
from flask import Module
ilife = Module(__name__)
from flask import render_template


@ilife.route('/')
def index():
    return render_template('ilife/index.html')
