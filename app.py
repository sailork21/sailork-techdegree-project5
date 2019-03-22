from flask import (Flask, g, render_template, flash, redirect, url_for,
abort)
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
    return 'Hey'


@app.route('/entries')
def list():
    list = models.get_list().limit(100)
    return render_template('entries.html', list=list)



@app.route('/entries/edit')


@app.route('/entries/delete')


@app.route('/entry', methods=('GET', 'POST'))
def add():
    form = forms.AddForm()
    if form.validate_on_submit():
        flash("Entry Saved!", 'success')
        models.Entry.create_entry(
            title = form.title.data,
            date = form.date.data,
            duration = form.timeSpent.data,
            learned = form.whatILearned.data,
            resources = form.ResourcesToRemember.data,
        )
        return redirect(url_for('index'))
    return render_template('new.html', form=form)





if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG)
