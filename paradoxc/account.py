from data import db_session
from data.user import User
from data.news import News


def check_account(email, password):
    if email == "" or password == "":
        return False

    db_sess = db_session.create_session()
    query = db_sess.query(User).filter(User.email == email, User.hashed_password == password)

    if query.count() > 0:
        return True

    return False


def find_account_by_id(id):
    db_sess = db_session.create_session()
    query = db_sess.query(User).filter(User.id == id)

    if query.count() > 0:
        return query.first()

    return db_sess.query(User).first()


def find_account(name):
    db_sess = db_session.create_session()
    query = db_sess.query(User).filter(User.name == name)

    if query.count() > 0:
        return query.first()

    return db_sess.query(User).first()


def find_account_by_email(email):
    db_sess = db_session.create_session()
    query = db_sess.query(User).filter(User.email == email)

    if query.count() > 0:
        return query.first()

    return db_sess.query(User).first()


def add_account(email, password, username, about_yourself):
    if email == "" or password == "" or username == "":
        return False

    user = User()
    user.name = username
    user.about = about_yourself
    user.email = email
    user.hashed_password = password
    db_sess = db_session.create_session()

    db_sess.add(user)
    db_sess.commit()

    return True


def add_new_post(name, content, user_id):
    news = News()
    news.title = name
    news.content = content
    news.user_id = user_id

    db_sess = db_session.create_session()
    db_sess.add(news)
    db_sess.commit()


def find_post(post_id):
    db_sess = db_session.create_session()
    query = db_sess.query(News).filter(News.id == post_id)

    if query.count() > 0:
        return query.first()

    return False


def get_all_posts():
    db_sess = db_session.create_session()
    return db_sess.query(News).all()


def get_all_user_posts(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(News).filter(News.user_id == user_id)

