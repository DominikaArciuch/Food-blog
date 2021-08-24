from app import app
from flask import render_template, request, redirect, flash, url_for
from .forms import RegisterForm, LoginForm


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        return 'We confirm your registration!'
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login user {}, remember me {}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('log_in.html', form=form)


@app.route('/foodsearch')
def food_search():
    return render_template('food_search.html')