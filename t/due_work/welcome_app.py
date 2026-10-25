"""
An application built on Celery, for the application-contract tests: sign a user up, then email them a welcome
message in the background. Each task is one way to write that job; the tests show what each one does when the
worker running it is lost.
"""

import os

import redis

from celery import Celery

app = Celery(
    'welcome',
    broker=os.environ.get('TEST_BROKER', 'redis://localhost:6379/10'),
    backend=os.environ.get('TEST_BACKEND', 'redis://localhost:6379/11'),
)
app.conf.update(worker_prefetch_multiplier=1)
#: The email provider's outbox and the users table, readable from the test process and every worker process.
STORE = redis.Redis.from_url(os.environ.get('DUE_WORK_RECORDS', 'redis://localhost:6379/12'))


def deliver(email, *, key=None):
    """The email provider: every call delivers a message, unless it repeats a key it has seen."""
    if key is None or STORE.set(f'provider key:{key}', 1, nx=True):
        STORE.rpush(f'outbox:{email}', 'Welcome!')


@app.task(name='welcome.send_welcome_email')
def send_welcome_email(email):
    """Celery's default configuration: the message is acknowledged before the task runs."""
    deliver(email)


@app.task(name='welcome.send_welcome_email_requeued', acks_late=True, reject_on_worker_lost=True)
def send_welcome_email_requeued(email):
    """Acknowledged after the task runs, and requeued if its pool child is lost, but sent without a key."""
    deliver(email)


@app.task(name='welcome.send_welcome_email_once', acks_late=True, reject_on_worker_lost=True)
def send_welcome_email_once(email):
    """Requeued if its pool child is lost, and sent with a key, so the provider drops a repeat."""
    deliver(email, key=f'welcome:{email}')


@app.task(name='welcome.record_welcomed')
def record_welcomed(email):
    """The link: record that the user was welcomed."""
    STORE.sadd('welcomed', email)


def sign_up(email, *, task=send_welcome_email, link=None):
    """The application's command: create the user and send the welcome email in the background."""
    STORE.sadd('users', email)
    return task.apply_async((email,), link=link)
