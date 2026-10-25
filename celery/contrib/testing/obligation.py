"""Generated failure tests for an application's own tasks, with pytest-obligation.

`pytest-obligation <https://github.com/gigaverse-app/pytest-obligation>`_ runs
one of your tasks through a real ``celery worker`` many times. Each time it
fails the worker at a different stage: the pool child lost as the task starts,
after its body ran, or after its result was stored; the task's ``on_success``
hook raising; the broker refusing what the task publishes. Then it starts the
worker again, as a deployment would, and compares what is left with a normal
run.

This module supplies what only Celery knows: how to run its worker, where it
can fail, and what Celery itself does at each stage for the task's
configuration (``acks_late``, ``reject_on_worker_lost``). Your application
supplies what only it knows: how its own code sends the task, how to see what
the task did, and what that should be after one successful run::

    from celery.contrib.testing.obligation import task_contract
    from pytest_obligation import due_work_contract_suite

    WELCOME = task_contract(
        'myapp.celery:app',
        send_welcome_email,
        send=lambda: sign_up('ada@example.com'),
        effect=lambda result: outbox.count('ada@example.com'),
        expected_effect=1,
    )


    @due_work_contract_suite(WELCOME)
    class test_WelcomeEmail:
        pass

pytest then generates the cases. What Celery does at a stage by design is
declared here, stage by stage, as a strict expected failure: the test passes
while Celery behaves that way, and fails if a change in Celery moves it. Any
other difference fails the test. In particular, when ``reject_on_worker_lost``
requeues a task whose pool child was lost after its body ran, the task runs
again; whether that repeats its effect (a second email) is a property of the
task, not of Celery, so it is never declared here. If your task has such a
finding that you cannot fix yet, pass it as ``known`` with ``because``.

When your application recovers what Celery loses with a sweep of its own,
pass it as ``recovery`` and name it with ``recovered_by``: Celery's rows are
then not declared, and every failure must converge. A task that keeps no
result is observed by what it did alone.

This module is ``pytest_obligation.integrations.celery_tasks``, the one place
these rows are kept, so applications on any Celery release can use it from
pytest-obligation directly. Needs Python 3.11 or later, ``pytest-obligation``,
a broker the test can reach, and Linux or macOS: the stages are reached
through the prefork pool.
"""

__all__ = ('task_contract', 'celery_outcomes')  # noqa: F822 - resolved lazily by __getattr__


def __getattr__(name):
    # Imported on first use, so this module imports on Python 3.10 without pytest-obligation.
    if name in __all__:
        from pytest_obligation.integrations import celery_tasks

        return getattr(celery_tasks, name)
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')
