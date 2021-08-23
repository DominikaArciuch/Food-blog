from app import app
from flask import render_template, request
from .forms import RegisterForm


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        return 'We confirm your registration!'
    return render_template('registration.html', form=form)
