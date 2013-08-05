# -*- coding: utf-8 -*-
import datetime
from flask import url_for
from iLife.models import db

__all__ = ['Article', 'Feed', 'Mark']

CATE = ((1, '情感'),
        (2, '互联网'),
        (3, '美女'),
        (4, '程序员'),
        (5, '笑话'),
        (6, '设计'),
        (7, '两性'),
        (8, '科技'),
        (9, '生活'))


class Article(db.Document):
    title = db.StringField(max_length=255)
    link = db.URLField(required=True, unique=True)
    desc = db.StringField(required=True)
    pubDate = db.StringField(max_length=255)
    createTime = db.DateTimeField(default=datetime.datetime.now, required=True)
    slug = db.StringField(max_length=255, required=True)
    cate = db.IntField(required=True, choices=CATE)
    author = db.StringField(max_length=255, required=True)
    avatar = db.StringField(max_length=255, required=True)

    def get_cate(self):
        cate_map = dict(CATE)
        return cate_map[self.cate]
        
class Feed(db.Document):
    cate = db.IntField(verbose_name='分类:', required=True, choices=CATE)
    avatar = db.StringField(verbose_name='头像链接:', max_length=255, required=True)
    author = db.StringField(verbose_name='作者:', max_length=255, required=True)
    source = db.URLField(verbose_name='RSS链接:', required=True, unique=True)
    slug = db.StringField(max_length=255, required=True)

    def get_cate(self):
        cate_map = dict(CATE)
        return cate_map[self.cate]

class Mark(db.Document):
    key = db.StringField(max_length=255, required=True)
    markTime = db.DateTimeField(default=datetime.datetime.now, required=True)
