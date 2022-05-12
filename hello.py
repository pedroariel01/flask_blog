from flask import Flask , render_template ,session, redirect, url_for,flash
from flask import request
from flask import make_response
from flask_script import Manager, Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from datetime import datetime
from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField 
from wtforms.validators import InputRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
import os
from flask_mail import Mail, Message
from decouple import config

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
manager  = Manager(app)
moment = Moment(app) 
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app) 
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand) 

app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
app.config['MAIL_PORT'] = 465 
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME') 
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')

app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'


mail = Mail(app) 

class Role(db.Model):
  __tablename__ = 'roles' 
  id = db.Column(db.Integer, primary_key=True) 
  name = db.Column(db.String(64), unique=True)
  
  users = db.relationship('User', backref='role',lazy='dynamic')

  def __repr__(self): 
          return '<Role %r>' % self.name


class User(db.Model): 
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True) 
  username = db.Column(db.String(64), unique=True, index=True)
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id')) 

  def __repr__(self): 
      return '<User %r>' % self.username 



class NameForm(FlaskForm): 
     name = StringField('What is your name?', validators=[InputRequired()]) 
     submit = SubmitField('Submit') 

def make_shell_context():
   return dict(app=app, db=db, User=User, Role=Role)
manager.add_command('shell', Shell(make_context=make_shell_context))

def send_email(to, subject, template, **kwargs): 
   
   msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                     sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to]) 
   msg.body = render_template(template + '.txt', **kwargs)
   msg.html = render_template(template + '.html', **kwargs)
   mail.send(msg) 

# def index_old():
#   name = None 
#   form = NameForm()
#   if form.validate_on_submit():
#     old_name = session.get('name')
#     if old_name is not None and old_name != form.name.data:
#       flash('IT looks like you changed your name')
#     session['name'] = form.name.data 
#     return redirect(url_for('index')) 
#   return render_template('index.html', form=form, name=session.get('name'),current_time=datetime.utcnow())


@app.route('/',methods=['GET', 'POST'])
def index(): 
    # response  = make_response('<h1>Hello, Man!</h1>')
    # response.set_cookie('answer', '42')
    # return response
#    user_agent = request.headers.get('User-Agent')
#    return '<h1>Hello, your browser is %s!</h1>' %user_agent
  name = None 
  form = NameForm()
  if form.validate_on_submit():

    
    user = User.query.filter_by(username= form.name.data).first()
    send_email(app.config['MAIL_USERNAME'], 'New User', 
                                  'mail/new_user', user=user)
    if user is None:
      user = User(username = form.name.data)
      db.session.add(user)
      session['known'] =False
      # if app.config['MAIL_USERNAME']:
         

    else:
      session['known'] =True
    session['name'] = form.name.data
    form.name.data = ''
    return redirect(url_for('index')) 
  return render_template('index.html', form=form, name=session.get('name'),
      known = session.get('known', False),
      current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
     return render_template('user.html', name=name)  

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404


if __name__ == '__main__':  
  manager.run()