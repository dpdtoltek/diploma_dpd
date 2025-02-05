from flask import Flask, render_template, g, request, redirect
from wtforms import Form, StringField, PasswordField, SubmitField, IntegerField, validators
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from forms import *
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'dpd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artshop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


buyers_arts = db.Table('buyers_arts',
                       db.Column('buyer_id', db.Integer, db.ForeignKey('buyers.id'), primary_key=True),
                       db.Column('art_id', db.Integer, db.ForeignKey('arts.id'), primary_key=True))


class Buyer(db.Model):
    __tablename__ = 'buyers'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    balance = db.Column(db.Float(precision=2), default=0)
    age = db.Column(db.Integer, nullable=False)
    arts = db.relationship('Buyer', secondary=buyers_arts, backref=db.backref('buyer', lazy='dynamic'))

    def __str__(self):
        return self.username


class Art(db.Model):
    __tablename__ = 'arts'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    cost = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text, nullable=False)
    age_limited = db.Column(db.Boolean, default=False)
    buyers = db.relationship('Buyer', secondary=buyers_arts, backref=db.backref('art', lazy='dynamic'))

    def __str__(self):
        return self.title


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.title


class BuyerAdmin(ModelView):
    form_columns = ['username', 'password', 'balance', 'age']


class ArtAdmin(ModelView):
    form_columns = ['title', 'cost', 'description', 'age_limited']


class NewsAdmin(ModelView):
    form_columns = ['title', 'content', 'date']


admin = Admin(app)
admin.add_view(BuyerAdmin(Buyer, db.session))
admin.add_view(ArtAdmin(Art, db.session))
admin.add_view(NewsAdmin(News, db.session))


@app.before_request
def set_global_variables():
    g.site_title = "Art shop"


@app.route('/', methods=['GET', 'POST'])
def sign_up():
    users = Buyer.query.all()
    usernames = [user.username for user in users]
    form = UserRegister(request.form)
    header = 'Страница регистрации'
    content = ''
    context = {'header': header, 'content': content}
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        repeat_password = form.repeat_password.data
        age = form.age.data
        if password == repeat_password and username not in usernames:
            new_user = Buyer(username=request.form['username'],
                             password=request.form['password'],
                             age=request.form['age'])
            db.session.add(new_user)
            db.session.commit()
            context['content'] = f'{username} успешно зарегистрирован!'
            return render_template('index.html', **context)
        elif password != repeat_password:
            context['content'] = 'Пароли не совпадают'
            return render_template('registration_page.html', **context)
        elif username in usernames:
            context['content'] = 'Пользователь уже существует'
            return render_template('registration_page.html', **context)
    return render_template('registration_page.html', **context)


@app.route('/index')
def index():
    header = 'Главная страница'
    context = {
        'header': header
    }
    return render_template('index.html', **context)


@app.route('/arts')
def arts():
    header = 'Магазин'
    arts_all = Art.query.all()
    context = {
        'header': header,
        'arts_all': arts_all
    }
    return render_template('arts.html', **context)


@app.route('/cart')
def cart():
    header = 'Корзина'
    content = 'Извините, Ваша корзина пуста'
    context = {
        'header': header,
        'content': content
    }
    return render_template('cart.html', **context)


@app.route('/news')
def news():
    header = 'Новости'
    news_all = News.query.all()
    context = {
        'header': header,
        'news_all': news_all
    }
    return render_template('news.html', **context)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
