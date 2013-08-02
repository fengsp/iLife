# -*- encoding: utf-8 -*-
"""
The view is for news...
"""
import httplib
import urllib
import xml.etree.ElementTree as ET
from urlparse import urlparse
import datetime

from flask import Module
inews = Module(__name__)
from flask import render_template, request, redirect
from flask.ext.mongoengine.wtf import model_form
from flask import flash, get_flashed_messages, url_for

from iLife.models.inews import *
from iLife.models import client
from mongoengine import NotUniqueError
import feedparser

@inews.route('/news')
def news_list():
    articles = Article.objects(createTime__gt=Mark.objects.get(key='news').markTime)
    return render_template('inews/news_list.html', articles=articles)

@inews.route('/feed/add', methods=['POST', 'GET'])
def add_feed():
    feedForm = model_form(Feed, exclude=['slug'])
    feeds = Feed.objects
    if request.form:
        form = feedForm(request.form)
        if form.validate():
            feed = Feed()
            form.populate_obj(feed)
            try:
                counter = client.ilife.command('findandmodify', 'counter',
                 query={'key':'feed'}, update={'$inc':{'count':1}}, new='true')
                feed.slug = str(counter['value']['count'])
                feed.save()
            except NotUniqueError:
                flash('此源已经存在')
                return render_template('inews/add_feed.html', form=form, feeds=feeds)
                
            return redirect(url_for('inews.news_list'))
    else:
        form = feedForm()

    return render_template('inews/add_feed.html', form=form, feeds=feeds)

@inews.route('/feed/delete/<slug>')
def delete_feed(slug):
    try:
        Feed.objects.get(slug=slug).delete()
    except:
        pass
    return redirect(url_for('inews.add_feed'))
            
@inews.route('/feed/update')
def update():
    for feed in Feed.objects:
        root = feedparser.parse(feed.source)
        for item in root.entries:
            if not Article.objects(link=item.link).count():
                article = Article()
                counter = client.ilife.command('findandmodify', 'counter',
                 query={'key':'post'}, update={'$inc':{'count':1}}, new='true')
                article.slug = str(counter['value']['count'])
                article.author = feed.author
                article.cate = feed.cate
                article.avatar = feed.avatar
                try:
                    article.title = item.title
                    article.link = item.link
                    article.desc = item.description
                except:
                    continue
                try:
                    article.pubDate = item.published
                except AttributeError:
                    article.pubDate = datetime.datetime.now().strftime("\
                                      %d. %B  %I:%M%p")
                try:
                    article.save()
                except:
                    continue
    
    return redirect(url_for('inews.news_list'))

@inews.route('/feed/mark')
def mark():
    news_mark = Mark.objects.get(key='news').update(set__markTime=datetime.datetime.now())
    return redirect(url_for('inews.news_list'))
