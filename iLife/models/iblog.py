# -*- coding: UTF-8 -*-
import datetime
from flask import url_for
from iLife.models import db

__all__ = ['Post', 'Comment', 'Counter']


class Post(db.Document):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(verbose_name="标题:", max_length=255, required=True)
    slug = db.StringField(max_length=255, required=True)
    body = db.StringField(verbose_name="内容:", required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))

    def get_absolute_url(self):
        return url_for('iblog.post_detail', slug =  self.slug)

    def __unicode__(self):
        return self.title

    meta = {
        'allow_inheritance': True,
        'indexed': ['-created_at', 'slug'],
        'ordering': ['-created_at']
    }


class Comment(db.EmbeddedDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="你的看法:", required=True)
    author = db.StringField(verbose_name="留个名吧:", max_length=255, required=True)


class Counter(db.Document):
    key = db.StringField(required=True)
    count = db.IntField(min_value=10000, required=True)
