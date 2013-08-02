"""
This view is used for blogs
"""
from flask import Module
iblog = Module(__name__)
from flask import render_template
from flask import request, redirect, url_for
from iLife.models.iblog import *
from flask.ext.mongoengine.wtf import model_form
from iLife.models import client

@iblog.route('/posts')
def post_list():
    posts = Post.objects.all()
    return render_template('iblog/post_list.html', posts = posts)


@iblog.route('/post/<slug>')
def post_detail(slug):
    commentForm = model_form(Comment, exclude=['created_at'])
    post = Post.objects.get_or_404(slug=slug)
    form = commentForm(request.form)
    return render_template('iblog/post_detail.html', post = post, form=form)
    

@iblog.route('/comment/<slug>', methods=['POST', 'GET'])
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

        return redirect(url_for('iblog.post_detail', slug=slug))

    return render_template('iblog/post_detail.html', **context)


@iblog.route('/post/create', methods=['POST', 'GET'])
def add_post():
    postForm = model_form(Post, exclude=['slug', 'created_at', 'comments'])
    if request.form:
        form = postForm(request.form)
        if form.validate():
            counter = client.ilife.command('findandmodify', 'counter', 
               query={'key':'post'}, update={'$inc':{'count':1}}, new='true')
            post = Post()
            form.populate_obj(post)
            slug = str(counter['value']['count'])
            post.slug = slug
            post.save()
            return redirect(url_for('iblog.post_detail', slug=slug))
    else:
        form = postForm()

    return render_template('iblog/add_post.html', form=form)

    
def check_auth(username, password):
    """This function is called to check if a username password combination is\
    valid.
    """
    return username == 'admin' and password == 'root'


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return "Please log in... Log in page"


def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return wrapper
