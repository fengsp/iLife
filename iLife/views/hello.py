"""
This view is used for learning use
"""
from flask import Module
hello = Module(__name__)
from flask import render_template
from flask import request
from flask import session, redirect, url_for, escape
from flask import flash, get_flashed_messages


@hello.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'


@hello.route('/hello/')
@hello.route('/hello/<name>')
def helloWorld(name=None):
    return render_template('hello/hello.html', name=name)


@hello.route('/flash')
def flash_demo():
    flash('flash message 1')
    flash('flash message 2')
    return str(get_flashed_messages())


@hello.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return """
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        """
        

@hello.route('/logout')
def logout():
    # remote the uesrname from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@hello.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username


@hello.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@hello.route('/dump_request/')
def dump_request():
    import StringIO
    tmp = StringIO.StringIO()
    from pprint import pprint
    import sys
    sys.stdout = tmp
    pprint(request.__dict__)
    sys.stdout = sys.__stdout__
    return tmp.getvalue()
