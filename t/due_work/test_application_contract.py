"""
An application's own tasks, checked with ``celery.contrib.testing.obligation``.

``test_worker_contract.py`` checks Celery's worker. This file is the other half: what an application built on
Celery writes to check its own tasks. It supplies how its code sends the task, how to see what the task did, and
what that should be; ``task_contract`` supplies the worker, its failure stages and what Celery does at each.

Run it as ``t/due_work`` is run (Python 3.11 or later, Linux or macOS, Redis on localhost)::

    pytest t/due_work/test_application_contract.py -p no:cacheprovider
"""

import uuid

import pytest
import redis
from pytest_obligation import HistoriesDiverged, due_work_contract_suite
from pytest_obligation.integrations.task_queues import TaskOutcome
from pytest_obligation.process_histories import assert_process_deaths_converge

from celery.contrib.testing.obligation import task_contract

from . import welcome_app as welcome

APP = 't.due_work.welcome_app:app'
#: Which address each history signed up, so each history counts only its own user's emails.
ADDRESSES = {}


def sign_up_someone(task, link=False):
    """ARRANGE: an empty broker and result backend, then a new user signed up through the application's command."""
    for url in (welcome.app.conf.broker_url, welcome.app.conf.result_backend):
        redis.Redis.from_url(url).flushdb()
    email = f'user-{uuid.uuid4().hex[:12]}@example.com'
    result = welcome.sign_up(email, task=task, link=welcome.record_welcomed.si(email) if link else None)
    ADDRESSES[result.id] = email
    return result


def emails_received(result):
    """OBSERVE: how many welcome emails this history's user received."""
    return welcome.STORE.llen(f'outbox:{ADDRESSES[result.id]}')


def contract(task, **declared):
    return task_contract(
        APP,
        task,
        # REAL PRODUCTION: the application's sign-up command, which sends the task.
        send=lambda: sign_up_someone(task, link=declared.get('publishes', False)),
        effect=emails_received,
        expected_effect=1,
        **declared,
    )


# Celery's default configuration. What the worker does when it loses the task's pool child is declared by
# task_contract, stage by stage: lost as it starts, the email is never sent and the task is not run again.
@due_work_contract_suite(contract(welcome.send_welcome_email, sigkill=True))
class test_DefaultConfiguration:
    """Generated from the contract above: the declared stages are a strict xfail, every other stage converges."""


# Requeued when its pool child is lost, so nothing is lost; but a child lost after the email left sends it twice.
# That is the task's own finding, not Celery's, so the application declares it.
@due_work_contract_suite(
    contract(
        welcome.send_welcome_email_requeued,
        known={'died at mark_as_done': TaskOutcome(status='SUCCESS', effect=2)},
        because='a pool child lost after the email left, before the result was stored, runs the task again and '
        'sends the email twice: send_welcome_email_requeued sends no key the provider could drop a repeat by',
    )
)
class test_RequeuedWithoutAKey:
    """Generated from the contract above."""


# Requeued, and sent with a key: every stage reaches a normal run. Nothing is declared.
@due_work_contract_suite(contract(welcome.send_welcome_email_once))
class test_RequeuedWithAKey:
    """Generated from the contract above."""


# The same task with a link: a link the broker refuses is Celery's to declare.
@due_work_contract_suite(
    contract(welcome.send_welcome_email_once, publishes=True, name='a worker runs it with a link')
)
class test_WithALink:
    """Generated from the contract above."""


def test_the_task_own_finding_is_never_declared_by_celery():
    """Without the application's ``known``, the duplicate email fails the history: task_contract does not hide it."""
    history = contract(welcome.send_welcome_email_requeued).process_handoffs[0]
    duplicate = r"'died at mark_as_done': TaskOutcome\(status='SUCCESS', effect=2\)"
    with pytest.raises(HistoriesDiverged, match=duplicate):
        assert_process_deaths_converge(history)
