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



@app.route('/')
def index():
    return redirect(url_for('list'))



@app.route('/entries')
def list():
    list = models.get_list().limit(100)
    return render_template('entries.html', list=list)



@app.route('/details/<id>')
def details(id):
    detail = models.Entry.select().where(models.Entry.id==id).get()
    return render_template('detail.html', detail=detail)



@app.route('/entry', methods=('GET', 'POST'))
def add():
    form = forms.AddEditForm()
    if form.validate_on_submit():
        flash("Entry Saved!", 'success')
        models.Entry.create_entry(
            title = form.title.data,
            date = form.date.data,
            duration = form.duration.data,
            learned = form.learned.data,
            resources = form.resources.data,
            tag1 = form.tag1.data,
            tag2 = form.tag2.data,
        )
        return redirect('/entries')
    return render_template('new.html', form=form)



@app.route('/delete/<id>', methods=('GET', 'POST'))
def delete(id):
    entry_delete = models.Entry.select().where(models.Entry.id==id).get().delete_instance()
    flash("Entry Deleted!", 'success')
    return redirect(url_for('list'))



@app.route('/edit/<id>', methods=('GET', 'POST'))
def edit(id):
    entry_edit = models.Entry.select().where(models.Entry.id==id).get()
    form = forms.AddEditForm(obj=entry_edit)
    if form.validate_on_submit():
        flash("Entry Saved!", 'success')
        models.Entry.create_entry(
            title = form.title.data,
            date = form.date.data,
            duration = form.duration.data,
            learned = form.learned.data,
            resources = form.resources.data,
            tag1 = tag1,
            tag2 = tag2
        )
        entry_delete = models.Entry.select().where(models.Entry.id==id).get().delete_instance()
        return redirect(url_for('list'))
    return render_template('edit.html', form=form, id=id)



@app.route('/tags/<tag>')
def tags(tag):
    tag_entries = models.get_tags(tag)
    return render_template('tags.html', tag_entries=tag_entries)



if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG)
