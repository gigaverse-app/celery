"""
Celery's contract with its worker, checked with pytest-obligation.

pytest-obligation (https://github.com/gigaverse-app/pytest-obligation) is a
pytest plugin that checks background work is neither lost nor run twice. A
contract names the guarantees a system offers and binds each to real code; the
harness then generates the test cases.

This contract binds Celery's worker itself, through ``worker_contract`` from
the harness's Celery worker integration. Each history goes through a real
``celery worker`` with one prefork child, run as a child process of the test:

* one task, ``send_message``, with a link and an error callback;
* chords, whose body (``announce_all``) has an error callback: on the Redis
  result backend; with ``task_reject_on_worker_lost``; with a header that
  fails; and on a database result backend, which joins a chord by polling
  (``chord_unlock``), once with headers that finish at once and once with a
  slow header, so ``chord_unlock`` waits and retries.

The harness fails each at Celery's own stages, on the first execution of one
header task: the pool child exits or is killed with SIGKILL as the task
starts, before its result is stored, and after; its ``on_success`` hook
raises; and the broker refuses the first other publish the worker makes.
Recovery is the worker starting again. What diverges from normal operation is
declared as a gap per history, a strict xfail, and each history's ``Findings``
pin what every failure leaves, in the same run as the verdict.

This directory is not part of the integration suite, which shares one session
worker: its tests start their own workers. Run it (Python 3.11 or later, Linux
or macOS, Redis on localhost, SQLAlchemy)::

    pip install -e . -r requirements/test.txt -r requirements/test-due-work.txt sqlalchemy
    pytest t/due_work -p no:cacheprovider
"""

import redis
from pytest_obligation import Findings, due_work_contract_suite
from pytest_obligation.helpers import wait_until
from pytest_obligation.integrations.celery_worker import (DEATH_POINTS, FAILURE_POINTS, SIGKILL_DEATH_POINTS,
                                                          worker_contract, worker_history)

from celery import chord
from celery.backends.database.models import Task, TaskSet
from celery.result import AsyncResult

from . import app as due_work

MESSAGE = 'your order has shipped'
SENT = f'sent {MESSAGE!r}'


def empty():
    # ARRANGE: an empty broker, result backends and record.
    for url in (due_work.BROKER, due_work.BACKEND):
        redis.Redis.from_url(url).flushdb()
    due_work.RECORDS.flushdb()
    session = due_work.database_app.backend.ResultSession()
    try:
        session.query(Task).delete()
        session.query(TaskSet).delete()
        session.commit()
    finally:
        session.close()


def send():
    # ARRANGE: the task, with its link and error callback.
    empty()
    return due_work.send_message.apply_async(
        (MESSAGE,), link=due_work.announce.s(), link_error=due_work.report_failure.s()
    ).id


def chord_of(app, *headers):
    """ARRANGE: a chord of these header tasks, and a body that announces what they sent, with an error callback."""

    def send():
        empty()
        # The worker answers before the chord is sent, so a slow start never lets chord_unlock (first run 1 s
        # after the chord, a countdown Celery fixes) overtake a header and decide the history by timing.
        wait_until(lambda: app.control.ping(timeout=0.5), timeout=30, what='the worker did not start')
        header = [
            app.tasks[f'due_work.{task}'].s(f'order {n} has shipped') for n, task in enumerate(headers, start=1)
        ]
        body = app.tasks['due_work.announce_all'].s().on_error(app.tasks['due_work.report_failure'].s())
        return chord(header, app=app)(body).id

    return send


def what_happened(task_id):
    # OBSERVE: the task's recorded state, how many messages left, and what the callbacks announced.
    return (
        AsyncResult(task_id, app=due_work.app).state,
        due_work.RECORDS.llen('sent'),
        # Sorted: the link and the error callback run in different processes, in either order.
        tuple(sorted(entry.decode() for entry in due_work.RECORDS.lrange('announced', 0, -1))),
    )


def settled(task_id):
    return AsyncResult(task_id, app=due_work.app).ready()


def what_the_chord_did(app):
    """OBSERVE: the body's state, how many messages left, what the callbacks announced, and the body's input."""

    def observe(body_id):
        return (
            AsyncResult(body_id, app=app).state,
            due_work.RECORDS.llen('sent'),
            tuple(sorted(entry.decode() for entry in due_work.RECORDS.lrange('announced', 0, -1))),
            tuple(entry.decode() for entry in due_work.RECORDS.lrange('body input', 0, -1)),
        )

    return observe


# What each failure leaves after the worker starts again, pinned in the same run as the
# verdict; every history not listed reaches normal operation. A change in the worker moves
# an entry, and the case names it. Celery's main fixed two earlier entries: a pool child
# lost after SUCCESS was stored (#10752) and an on_success hook that raises (#10759) now
# reach normal operation.
FINDINGS = Findings(
    ('SUCCESS', 1, (SENT,)),
    {
        # The child died as the task started: the message is never sent, the error callback fires, and
        # nothing runs the task again (task_reject_on_worker_lost is off by default).
        'died at task_prerun': ('FAILURE', 0, ('failed: WorkerLostError',)),
        # FINDING (#10954): the message was sent and the link announced it; the task is recorded FAILURE and
        # the error callback announces a failure too.
        'died at mark_as_done': ('FAILURE', 1, ('failed: WorkerLostError', SENT)),
        # FINDING (#10725): the message was sent; the refused link records FAILURE, and the message is
        # acknowledged, so the link is never published again.
        "the broker refused the task's link": ('FAILURE', 1, ('failed: OperationalError',)),
    },
)

SEND_MESSAGE = worker_history(
    name='a worker runs send_message',
    app='t.due_work.app:app',
    task=due_work.send_message.name,
    send=send,
    observe=what_happened,
    initial=('PENDING', 0, ()),
    expected=FINDINGS.delivered,
    settled=settled,
    findings=FINDINGS,
)

BOTH_SENT = repr(['order 1 has shipped', 'order 2 has shipped'])


def body_ready(app):
    return lambda body_id: AsyncResult(body_id, app=app).ready()


def broker_owes_nothing():
    """No message is queued, or reserved and unacknowledged (a retry waiting out its countdown is reserved)."""
    broker = redis.Redis.from_url(due_work.BROKER)
    return broker.llen('celery') == 0 and broker.hlen('unacked') == 0


def body_ready_or_chord_unlock_failed(body_id):
    """
    The chord is settled when its body is, or the chord_unlock joining it has failed for good, and the broker owes
    nothing more: a header's own retry has run, so what the history observes no longer depends on machine speed.
    """
    body = AsyncResult(body_id, app=due_work.database_app)
    return (body.ready() or due_work.RECORDS.llen('chord_unlock failed') > 0) and broker_owes_nothing()


def chord_history(
    name,
    send,
    app,
    findings,
    *,
    app_path='t.due_work.app:app',
    env=None,
    task='due_work.send_message',
    settled=None,
    death_points=DEATH_POINTS + SIGKILL_DEATH_POINTS,
    failure_points=FAILURE_POINTS,
):
    """A chord through the worker, failing at Celery's stages (SIGKILL deaths included) on the header ``task``."""
    return worker_history(
        name=name,
        app=app_path,
        task=task,
        send=send,
        observe=what_the_chord_did(app),
        initial=('PENDING', 0, (), ()),
        expected=findings.delivered,
        settled=settled or body_ready(app),
        death_points=death_points,
        failure_points=failure_points,
        findings=findings,
        env=env,
    )


# What each failure leaves a chord, pinned per history. The faults hit the first execution of the header
# task named in the history; "the broker refused the task's link" refuses the first other publish the
# worker makes: the chord's body, or chord_unlock's retry while it waits for a header.
LOST_AS_IT_STARTED = {
    # The header's child died as it started: its message is never sent and, with task_reject_on_worker_lost
    # off (the default), nothing runs it again; the chord fails. Documented, not a defect.
    'died at task_prerun': ('FAILURE', 1, ('failed: ChordError',), ()),
    'died at task_prerun (SIGKILL)': ('FAILURE', 1, ('failed: ChordError',), ()),
}
LOST_AFTER_ITS_EFFECT = {
    # FINDING (#10954): both messages were sent; the header lost before its store is recorded FAILURE, so the
    # chord fails and its body never runs.
    'died at mark_as_done': ('FAILURE', 2, ('failed: ChordError',), ()),
    'died at mark_as_done (SIGKILL)': ('FAILURE', 2, ('failed: ChordError',), ()),
}
BODY_REFUSED = {
    # FINDING (#10725, comment): both messages were sent; the body's publish is refused, the chord is recorded
    # FAILURE, and nothing publishes the body again.
    "the broker refused the task's link": ('FAILURE', 2, ('failed: ChordError',), ()),
}

CHORD_FINDINGS = Findings(
    ('SUCCESS', 2, ('sent 2 messages',), (BOTH_SENT,)), LOST_AS_IT_STARTED | LOST_AFTER_ITS_EFFECT | BODY_REFUSED
)
REQUEUED_CHORD_FINDINGS = Findings(
    ('SUCCESS', 2, ('sent 2 messages',), (BOTH_SENT,)),
    {
        # task_reject_on_worker_lost requeues the header lost before its store, and it runs again: its message
        # is sent twice (Celery's documented at-least-once). The body still runs once, with the right input.
        'died at mark_as_done': ('SUCCESS', 3, ('sent 2 messages',), (BOTH_SENT,)),
        'died at mark_as_done (SIGKILL)': ('SUCCESS', 3, ('sent 2 messages',), (BOTH_SENT,)),
    }
    | BODY_REFUSED,
)
FAILING_HEADER_FINDINGS = Findings(
    ('FAILURE', 1, ('failed: ChordError',), ()),
    {
        # The good header was lost as it started, so neither header sent anything; the error callback still
        # fires once, as in normal operation.
        'died at task_prerun': ('FAILURE', 0, ('failed: ChordError',), ()),
        'died at task_prerun (SIGKILL)': ('FAILURE', 0, ('failed: ChordError',), ()),
    },
)
DATABASE_CHORD_FINDINGS = Findings(
    ('SUCCESS', 2, ('sent 2 messages',), (BOTH_SENT,)), LOST_AS_IT_STARTED | LOST_AFTER_ITS_EFFECT | BODY_REFUSED
)
WAITING_DATABASE_CHORD_FINDINGS = Findings(
    ('SUCCESS', 2, ('sent 2 messages',), (BOTH_SENT,)),
    LOST_AS_IT_STARTED
    | {
        # FINDING (the shape of #10954): the header's first execution had already published its own retry when
        # its child died. The header is recorded FAILURE and the chord fails with ChordError, yet the retry still
        # runs and sends its message.
        'died at task_postrun': ('FAILURE', 2, ('failed: ChordError',), ()),
        'died at task_postrun (SIGKILL)': ('FAILURE', 2, ('failed: ChordError',), ()),
        # FINDING (#10955): chord_unlock's retry is refused while the header waits on its own. Task.retry turns
        # that into Reject(requeue=False), chord_unlock keeps no result, and the chord is never joined: both
        # messages were sent, the body stays PENDING forever, and no callback ever fires.
        "the broker refused the task's link": ('PENDING', 2, (), ()),
    },
)

CHORD = chord_history(
    'a worker runs a chord of two send_message tasks',
    chord_of(due_work.app, 'send_message', 'send_message'),
    due_work.app,
    CHORD_FINDINGS,
)
REQUEUED_CHORD = chord_history(
    'a worker that requeues a task whose pool child was lost runs a chord of two send_message tasks',
    chord_of(due_work.app, 'send_message', 'send_message'),
    due_work.app,
    REQUEUED_CHORD_FINDINGS,
    env={'DUE_WORK_REJECT_ON_WORKER_LOST': '1'},
)
FAILING_HEADER = chord_history(
    'a worker runs a chord whose other header task fails',
    chord_of(due_work.app, 'send_message', 'fail_message'),
    due_work.app,
    FAILING_HEADER_FINDINGS,
    # A chord whose header failed publishes nothing from the worker, so there is no publish to refuse.
    failure_points=("the task's on_success hook raised",),
)
DATABASE_CHORD = chord_history(
    'a worker runs a chord of two send_message tasks with results in a database',
    chord_of(due_work.database_app, 'send_message', 'send_message'),
    due_work.database_app,
    DATABASE_CHORD_FINDINGS,
    app_path='t.due_work.app:database_app',
    settled=body_ready_or_chord_unlock_failed,
)
WAITING_DATABASE_CHORD = chord_history(
    'a worker runs a chord with results in a database, whose chord_unlock retries while a header runs',
    chord_of(due_work.database_app, 'send_after_a_retry', 'send_message'),
    due_work.database_app,
    WAITING_DATABASE_CHORD_FINDINGS,
    app_path='t.due_work.app:database_app',
    task='due_work.send_after_a_retry',
    settled=body_ready_or_chord_unlock_failed,
    # The header's first execution ends in its retry: it never stores a result or runs on_success, so only
    # the deaths around it, and the refused publish of chord_unlock's own retry, can be reached.
    death_points=('task_prerun', 'task_postrun', 'task_prerun (SIGKILL)', 'task_postrun (SIGKILL)'),
    failure_points=("the broker refused the task's link",),
)
CHORDS = (CHORD, REQUEUED_CHORD, FAILING_HEADER, DATABASE_CHORD, WAITING_DATABASE_CHORD)

CONTRACT = worker_contract(
    name='celery: the worker running a task',
    process_handoffs=(SEND_MESSAGE, *CHORDS),
    handoff_gaps={
        SEND_MESSAGE.name: (
            'once the link is published, a failure still runs the failure path: a child lost after the link, before '
            'the store, records FAILURE for a task whose effect and link happened, and fires the error callback '
            'beside the link (https://github.com/celery/celery/issues/10954); and a link the broker refuses records '
            'FAILURE and acknowledges the message, so the link is never sent '
            '(https://github.com/celery/celery/issues/10725). '
            'FINDINGS pins each history'
        ),
        CHORD.name: (
            'a header lost after its effect and before its store, or a refused body publish, fails the chord for '
            'good though every message was sent (https://github.com/celery/celery/issues/10954, '
            'https://github.com/celery/celery/issues/10725#issuecomment-6318108091); a header lost as it starts '
            'is never run again (task_reject_on_worker_lost off). CHORD_FINDINGS pins each history'
        ),
        REQUEUED_CHORD.name: (
            'a header lost before its store runs again and sends its message twice, as task_reject_on_worker_lost '
            'documents; a refused body publish fails the chord for good. REQUEUED_CHORD_FINDINGS pins each history'
        ),
        FAILING_HEADER.name: (
            'the good header lost as it starts is never run again (task_reject_on_worker_lost off); the error '
            'callback fires once, as in normal operation. FAILING_HEADER_FINDINGS pins each history'
        ),
        DATABASE_CHORD.name: (
            'as on Redis: a header lost after its effect, or a refused body publish, fails the chord for good; '
            'a header lost as it starts is never run again. DATABASE_CHORD_FINDINGS pins each history'
        ),
        WAITING_DATABASE_CHORD.name: (
            'a refused chord_unlock retry loses the chord: the body stays PENDING forever and no callback fires '
            '(https://github.com/celery/celery/issues/10955); a header lost after publishing its own retry is '
            'recorded FAILURE and fails the chord though the retry still sends (the shape of '
            'https://github.com/celery/celery/issues/10954). WAITING_DATABASE_CHORD_FINDINGS pins each history'
        ),
    },
)


# This is where the magic happens. The class is empty on purpose: the decorator reads CONTRACT
# and generates its tests, bound to Celery's real worker. No test case is written by hand; this
# file supplies only the tasks and how to see what they did, and the stages where the worker can
# fail come from the harness's Celery integration.
#
# Each history's generated case is how the findings were made: it runs the work through the
# worker once per stage, failing there, then starts the worker again and compares each run with a
# normal one. A task whose link was published, then refused or followed by a lost pool child, ends
# FAILURE with its error callback fired. The contract declares that as a gap, so it is reported as a
# strict XFAIL; the day every stage converges, it passes, and the strict marker fails the run until
# the gap is removed.
@due_work_contract_suite(CONTRACT)
class test_WorkerContract:
    """Every case in this class is generated from CONTRACT; see the comment above."""
