"""
The Celery applications the obligation contract runs: one task that sends a message, with its link and its
error callback, and the tasks a chord needs. ``app`` keeps results in Redis; ``database_app`` keeps them in
SQLAlchemy, where a chord is joined by polling (``chord_unlock``) instead of Redis's counter.
"""

import os
import tempfile

import redis

from celery import Celery, signals

BROKER = os.environ.get('TEST_BROKER', 'redis://localhost:6379/10')
BACKEND = os.environ.get('TEST_BACKEND', 'redis://localhost:6379/11')
DATABASE_BACKEND = os.environ.get(
    'DUE_WORK_DATABASE_BACKEND', f'db+sqlite:///{os.path.join(tempfile.gettempdir(), "due_work_results.sqlite")}'
)
#: What the tasks did, readable from the test process and every worker process.
RECORDS = redis.Redis.from_url(os.environ.get('DUE_WORK_RECORDS', 'redis://localhost:6379/12'))


def application(name, backend):
    """A Celery app with this contract's tasks, its results in ``backend``."""
    app = Celery(name, broker=BROKER, backend=backend)
    app.conf.update(
        task_acks_late=True,
        worker_prefetch_multiplier=1,
        # Read by the worker only: a history that requeues a lost task sets it in the worker's environment.
        task_reject_on_worker_lost=os.environ.get('DUE_WORK_REJECT_ON_WORKER_LOST') == '1',
    )

    @app.task(shared=False, name='due_work.send_message')
    def send_message(message):
        # EXTERNAL SEAM: the message leaves for the customer.
        RECORDS.rpush('sent', message)
        return message

    @app.task(shared=False, bind=True, max_retries=1, name='due_work.send_after_a_retry')
    def send_after_a_retry(self, message):
        """
        A header that retries once before it sends, so chord_unlock (first run 1 s after the chord) always finds
        the chord unfinished and retries itself, however fast or slow the machine.
        """
        if self.request.retries == 0:
            raise self.retry(countdown=3)
        RECORDS.rpush('sent', message)
        return message

    @app.task(shared=False, name='due_work.fail_message')
    def fail_message(message):
        """A header task that fails as an application's task can: its message is never sent."""
        raise ValueError(f'could not send {message!r}')

    @app.task(shared=False, name='due_work.announce')
    def announce(result):
        """The link: tell the customer it was sent."""
        RECORDS.rpush('announced', f'sent {result!r}')

    @app.task(shared=False, name='due_work.report_failure')
    def report_failure(request, exc, traceback):
        """The error callback: tell the customer it failed."""
        RECORDS.rpush('announced', f'failed: {type(exc).__name__}')

    @app.task(shared=False, name='due_work.announce_all')
    def announce_all(results):
        """A chord's body: tell the customer which messages the header sent, as it received them."""
        RECORDS.rpush('announced', f'sent {len(results)} messages')
        RECORDS.rpush('body input', repr(sorted(results)))

    return app


app = application('due_work', BACKEND)
database_app = application('due_work_database', DATABASE_BACKEND)

send_message = app.tasks['due_work.send_message']
fail_message = app.tasks['due_work.fail_message']
announce = app.tasks['due_work.announce']
report_failure = app.tasks['due_work.report_failure']
announce_all = app.tasks['due_work.announce_all']


@signals.task_failure.connect(weak=False)
def record_a_failed_chord_join(sender=None, exception=None, **_kwargs):
    """
    OBSERVE: chord_unlock joins a chord on a database backend and keeps no result (ignore_result), so the
    only trace of it failing is Celery's task_failure signal, recorded here for the test to read.
    """
    if getattr(sender, 'name', None) == 'celery.chord_unlock':
        RECORDS.rpush('chord_unlock failed', type(exception).__name__)
