from flask import (Flask, g, render_template, flash, redirect, url_for,
abort, request)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user, login_required,
current_user)

import forms
import models

DEBUG = True

app = Flask(__name__)
app.secret_key = 'oir5489th09ubgij432'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    """Close database connection after each request."""
    g.db.close()
    return response

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Thanks for registering!", 'success')
        models.User.create_user(
            username=form.username.data,
            password=form.password.data
        )
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.username == form.username.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for('add'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", 'success')
    return redirect(url_for('login'))



@app.route('/')
def index():
    return redirect(url_for('login'))



@app.route('/entries')
@login_required
def list():
    list = current_user.get_entries().limit(100)
    user = current_user
    return render_template('entries.html', list=list)



@app.route('/details/<id>')
@login_required
def details(id):
    detail = models.Entry.select().where(models.Entry.id==id).get()
    return render_template('detail.html', detail=detail)



@app.route('/entry', methods=('GET', 'POST'))
@login_required
def add():
    form = forms.AddEditForm()
    if form.validate_on_submit():
        flash("Entry Saved!", 'success')
        models.Entry.create(
            user=g.user._get_current_object(),
            title = form.title.data,
            date = form.date.data,
            duration = form.duration.data,
            learned = form.learned.data,
            resources = form.resources.data,
            tag1 = form.tag1.data,
            tag2 = form.tag2.data,
        )
        return redirect(url_for('list'))
    return render_template('new.html', form=form)



@app.route('/delete/<id>', methods=('GET', 'POST'))
@login_required
def delete(id):
    entry_delete = models.Entry.select().where(models.Entry.id==id).get().delete_instance()
    flash("Entry Deleted!", 'success')
    return redirect(url_for('list'))



@app.route('/edit/<id>', methods=('GET', 'POST'))
@login_required
def edit(id):
    entry_edit = models.Entry.select().where(models.Entry.id==id).get()
    form = forms.AddEditForm(obj=entry_edit)
    if form.validate_on_submit():
        flash("Entry Saved!", 'success')
        models.Entry.create(
            user=g.user._get_current_object(),
            title = form.title.data,
            date = form.date.data,
            duration = form.duration.data,
            learned = form.learned.data,
            resources = form.resources.data,
            tag1 = form.tag1.data,
            tag2 = form.tag2.data
        )
        entry_delete = models.Entry.select().where(models.Entry.id==id).get().delete_instance()
        return redirect(url_for('list'))
    return render_template('edit.html', form=form, id=id)



@app.route('/tags/<tag>')
@login_required
def tags(tag):
    tag_entries = current_user.get_tags(tag).limit(100)
    user = current_user
    return render_template('tags.html', tag_entries=tag_entries)



if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='keddy',
            password='password',
        )
    except ValueError:
        print("That user already exists.")
    app.run(debug=DEBUG)
