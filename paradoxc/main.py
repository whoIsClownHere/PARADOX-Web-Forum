from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from account import add_account
from account import check_account
from account import find_account
from account import find_account_by_email
from account import add_new_post
from account import find_post
from account import find_account_by_id
from account import get_all_posts
from account import get_all_user_posts
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

logged_in = False
all_posts = None
all_user_posts = None
best_authors = None


@app.route('/')
@app.route('/main')
def main():
    global logged_in
    global all_posts
    global best_authors

    all_posts = get_all_posts()

    return render_template('main.html', logged_in=logged_in, all_posts=all_posts)


@app.route('/account/<path:username>')
def account(username):
    global all_user_posts

    user = find_account(username)
    all_user_posts = get_all_user_posts(user.id)
    if user:
        return render_template('profile.html', item=user, logged_in=logged_in, all_posts=all_user_posts)
    return 'NOT FOUND'


@app.route('/new_post', methods=['GET'])
def new_post():
    return render_template('new_post.html')


@app.route('/new_post', methods=['POST'])
def new_post_complete():
    global logged_in

    name = request.form['name']
    content = request.form['content']

    add_new_post(name, content, logged_in.id)
    return redirect(url_for('main'))


@app.route('/post/<path:postid>')
def post_view(postid):
    post = find_post(postid)
    author = find_account_by_id(post.user_id)
    if post:
        return render_template('post.html', item=post, author=author, logged_in=logged_in)
    return 'NOT FOUND'


@app.route('/login', methods=['GET'])
def login():
    return render_template('authorization.html', logged_in=logged_in)


@app.route('/login', methods=['POST'])
def login_complete():
    global logged_in

    email = request.values.get('email')
    password = request.values.get('password')
    if check_account(email, password):
        logged_in = find_account_by_email(email)
        return redirect(url_for('main'))
    return 'не ok'


@app.route('/registration', methods=['GET'])
def registration():
    return render_template('registration.html')


@app.route('/registration', methods=['POST'])
def registration_complete():
    global logged_in

    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    about_yourself = request.form['about_yourself']

    if add_account(email, password, username, about_yourself):
        logged_in = find_account_by_email(email)
        return redirect(url_for('main'))

    return 'не ok'


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(port=8080, host='127.0.0.1')
