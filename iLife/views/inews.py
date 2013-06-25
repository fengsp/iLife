# -*- encoding: utf-8 -*-
"""
The view is for news...
"""
from flask import Module
inews = Module(__name__)
from flask import render_template, request, redirect
from flask.ext.mongoengine.wtf import model_form
from iLife.models.inews import *
from iLife.models.iblog import Counter
from mongoengine import NotUniqueError
from flask import flash, get_flashed_messages, url_for
import httplib
import urllib
import xml.etree.ElementTree as ET
from urlparse import urlparse

@inews.route('/news')
def news_list():
    articles = Article.objects
    return render_template('inews/news_list.html', articles=articles)

@inews.route('/feed/add', methods=['POST', 'GET'])
def add_feed():
    feedForm = model_form(Feed)
    if request.form:
        form = feedForm(request.form)
        if form.validate():
            feed = Feed()
            form.populate_obj(feed)
            try:
                feed.save()
            except NotUniqueError:
                flash('此源已经存在')
                return render_template('inews/add_feed.html', form=form)
                
            return redirect(url_for('inews.news_list'))
    else:
        form = feedForm()

    return render_template('inews/add_feed.html', form=form)
            
@inews.route('/feed/update')
def update():
    for feed in Feed.objects:
        o = urlparse(feed.source)
        conn = httplib.HTTPConnection(o.hostname)
        conn.request("GET", o.path)
        response = conn.getresponse()
        if response.status != 200:
            continue
        
        data = response.read()
        root = ET.fromstring(data)
        root = root.find('channel')
        for item in root.findall('item'):
            if not Article.objects(link=item.find('link').text).count():
                article = Article()
                Counter.objects(key='news').update_one(inc__count=1)
                article.slug = str(Counter.objects(key='news')[0].count)
                article.author = feed.author
                article.cate = feed.cate
                article.avatar = feed.avatar
                article.title = item.find('title').text
                article.link = item.find('link').text
                article.desc = item.find('description').text
                article.pubDate = item.find('pubDate').text
                article.save()
    
    return redirect(url_for('inews.news_list'))
