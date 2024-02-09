from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
import os
import sqlite3

from FDataBase import FDataBase

DATABASE = '/tmp/flsite.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


menu = [{"name": "Installation", "url": "install-flask"},
        {"name": "First app", "url": "first-app"},
        {"name": "Feedback", "url": "contact"}]


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template("index.html", menu=dbase.get_menu(), posts=dbase.get_all_posts())


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.add_post(request.form['name'], request.form['post'])
            if not res:
                flash('Adding post error', category='error')
            else:
                flash('Post added', category='success')
        else:
            flash('Adding post error', category='error')

    return render_template('add_post.html', menu=dbase.get_menu(), title="Adding new post")


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"User: {username}"


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        if len(request.form['username']) > 5:
            flash('Message sent', category='success')
        else:
            flash('Sending Error', category='error')
    db = get_db()
    dbase = FDataBase(db)
    return render_template("contact.html", title="Feedback", menu=dbase.get_menu())


@app.route("/post/<post_id>")
def show_post(post_id):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.get_post(post_id)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.get_menu(), title=title, post=post)


@app.route("/about")
def about():
    return render_template("about.html", title="About this site", menu=menu)


@app.route("/login", methods=["POST", "GET"])
def login():
    if 'userLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == "POST" and request.form['username'] == 'selfedu' and request.form['psw'] == '123':
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))

    return render_template("login.html", title="Sign in", menu=menu)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title="Page not found", menu=menu)


if __name__ == "__main__":
    app.run(debug=True)
