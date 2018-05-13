from datetime import datetime
from app import app,db
from flask import render_template,flash,redirect,url_for,Markup,request
from flask_login import current_user,login_user,logout_user,login_required
from app.forms import LoginForm, UserRegistrationForm,EditProfileForm
from app.model import User,Post
from sqlalchemy import not_
from werkzeug.urls import url_parse
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.filter(not_(Post.user_id.contains(current_user.id))).all()
    return render_template('index.html',title=current_user.name,posts=posts)


@app.route('/login',methods=['GET','POST'])
def login():
    app.logger.info('Microblog login')
    # check if current user is anonymous(False) or registered(True)
    if current_user.is_authenticated :
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.name.data).first()
        # check for username and password
        if user is None or not user.check_password(form.pwd.data):
            flash(Markup("<div style='background:red;color:white'>Invalid Username or Passord </div>"))
            return redirect(url_for('login'))
        # log-in a user after this current_user = this user
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            return redirect(url_for('index'))
        return redirect(next_page)
    # if validate on submit is False
    return render_template('login.html',title="Sign In",form=form)


@app.route('/logout')
def logout():
    app.logger.info('Microblog logout')
    logout_user()
    return redirect(url_for('login'))


@app.route('/register',methods=['GET','POST'])
def register():
    app.logger.info('Microblog register')
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = UserRegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,email=form.email.data)
        user.set_password(form.pwd.data)
        db.session.add(user)
        db.session.commit()
        flash(Markup("<div style='color:blue'>Congratulations!!! You have been registered </div>"))
        return redirect(url_for('index'))
    return render_template('register.html',title='Sign Up',form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user_name = User.query.filter_by(name=username).first_or_404()
    posts = Post.query.filter((Post.user_id.contains(current_user.id))).all()
    return render_template('user.html',user=user_name,posts=posts)


@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit():
    app.logger.info('Microblog editProfile')
    form = EditProfileForm(current_user.name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(Markup('<div style="background:green;color:white">changes have been saved!!!</div>'))
        return redirect(url_for('edit'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.about_me.data = current_user.about_me
    return render_template('edit.html', title='Edit Profile', form=form)


@app.before_request
def last_seen():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()



