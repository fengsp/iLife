"""
This view is used for learning use
"""
from flask import Module
tumblelog = Module(__name__)
from flask import render_template, Blueprint
from flask import request, redirect, url_for
from iLife.models.tumblelog import *
from flask.ext.mongoengine.wtf import model_form


@tumblelog.route('/posts')
def post_list():
    posts = Post.objects.all()
    return render_template('tumblelog/post_list.html', posts = posts)


@tumblelog.route('/post/<slug>')
def post_detail(slug):
    commentForm = model_form(Comment, exclude=['created_at'])
    post = Post.objects.get_or_404(slug=slug)
    form = commentForm(request.form)
    return render_template('tumblelog/post_detail.html', post = post, form=form)
    

@tumblelog.route('/comment/<slug>', methods=['POST', 'GET'])
def add_comment(slug):
    commentForm = model_form(Comment, exclude=['created_at'])
    post = Post.objects.get_or_404(slug=slug)
    form = commentForm(request.form)
    context = {
        "post": post,
        "form": form
    }
    if form.validate():
        comment = Comment()
        form.populate_obj(comment)

        post.comments.append(comment)
        post.save()

        return redirect(url_for('tumblelog.post_detail', slug=slug))

    return render_template('tumblelog/post_detail.html', **context)
