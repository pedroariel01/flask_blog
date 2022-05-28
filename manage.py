#!/usr/bin/env python
import os
import sys
import click
from app import create_app, db
from app.models import User, Role, Post
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app) 
migrate = Migrate(app, db)

def make_shell_context():
   return dict(app=app, db=db, User=User, Role=Role,Post=Post)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
   import unittest
   tests = unittest.TestLoader().discover('tests')
   unittest.TextTestRunner(verbosity=2).run(tests) 

@app.cli.command()
@click.option('--length', default=25,
              help='Number of functions to include in the profiler report.')
@click.option('--profile-dir', default=None,
              help='Directory where profiler data files are saved.')
def profile(length, profile_dir):
    """Start the application under the code profiler."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()
    
if __name__ == '__main__': 
   manager.run() 