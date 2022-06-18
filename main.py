from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from datetime import timedelta
import os

pjdir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = "#230dec61-fee8-4ef2-a791-36f9e680c9fc"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
                                        os.path.join(pjdir, 'data_register.sqlite')
app.config['SECRET_KEY']='your key'

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

PRODUCTS = {
    'iphone': {
        'name': 'iphone 5s',
        'category': 'iphons',
        'prince': 699,
    },
    'galaxy': {
        'name': 'aaa',
        'category': 'bbb',
        'prince': 699,
    },
    'ipad-air': {
        'name': 'ccc',
        'category': 'ddd',
        'prince': 699,
    }

}


@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form['nm']
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/user')
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        return redirect(url_for("login"))


@app.route('/register', methods=['GET', 'POST'])
def register():
    from model import UserReister
    from form import FormRegister
    form =FormRegister()
    if form.validate_on_submit():
        user = UserReister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return render_template('base.html')

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.debug = True
    app.run()