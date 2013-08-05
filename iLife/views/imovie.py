"""
This view is used for movies
"""
from flask import Module
imovie = Module(__name__)
from flask import render_template
from flask import request, redirect, url_for
from flask.ext.mongoengine.wtf import model_form
from iLife.models import client

@imovie.route('/movies')
def index():
    return render_template('imovie/index.html')
