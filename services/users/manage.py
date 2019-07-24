#!/usr/bin/env python

import sys
import unittest

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

cli = FlaskGroup(create_app=create_app)

@cli.command()
def test():
    """ Runs the tests without code coverage """

    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    user1 = User(username='tom', email='tom@example.com')
    user2 = User(username='jerry', email='jerry@example.com')
    db.session.add_all([user1, user2])
    db.session.commit()

if __name__ == "__main__":
    cli()

