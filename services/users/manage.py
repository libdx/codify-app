#!/usr/bin/env python

import sys
import unittest
import coverage
import click

from flask.cli import FlaskGroup

from project import create_app, db
from project.api.models import User

def start_coverage():
    cov = coverage.coverage(
        branch=True,
        include='project/*',
        omit=[
            'project/tests/*',
            'project/config.py',
        ]
    )
    cov.start()
    return cov

cli = FlaskGroup(create_app=create_app)

@cli.command()
@click.option('--coverage', '-c', is_flag=True)
def test(coverage):
    """Runs the tests optionally with code coverage"""
    cov = start_coverage()

    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        if coverage:
            cov.stop()
            cov.save()
            print('\nCoverage Summary:')
            cov.report()
            cov.html_report()
            cov.erase()
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

