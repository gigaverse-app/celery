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

Needs Python 3.11 or later, ``pytest-obligation``, a broker and result backend
the test can reach, and Linux or macOS: the stages are reached through the
prefork pool.
"""
import importlib
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

__all__ = ('task_contract', 'celery_outcomes')

#: The pool child exits as the task starts, and after its body ran but before its result was stored.
_PRERUN, _BEFORE_STORE = 'died at task_prerun', 'died at mark_as_done'
_SIGKILL = ' (SIGKILL)'
_ON_SUCCESS = "the task's on_success hook raised"
_LINK_REFUSED = "the broker refused the task's link"

_NOT_RUN_AGAIN = (
    'with acks_late and reject_on_worker_lost not both set (Celery\'s default), a task whose pool child is lost '
    'is recorded FAILURE (WorkerLostError) and is not run again: lost as it starts, its effect never happens; '
    'lost after its body ran and before its result was stored, it is recorded FAILURE though its effect happened. '
    'Set both on the task to have it run again instead, and make the task safe to run twice'
)
_LINK_LOST = (
    'when the broker refuses the task\'s link, the task is recorded FAILURE though its effect happened, and the '
    'message is acknowledged, so the link is not sent again (https://github.com/celery/celery/issues/10725)'
)


def celery_outcomes(task, *, initial_effect, expected_effect, publishes=False, sigkill=False):
    """What Celery leaves a task at each stage where it differs from a normal run, for the task's configuration.

    Keyed by the stage's history label; each value is ``(state, effect)``, with
    the task's effect not having happened (``initial_effect``) or having
    happened once (``expected_effect``). Stages not listed reach a normal run:
    the result stored before the pool child was lost, and an ``on_success`` hook
    that raises, both keep the task SUCCESS. A stage where the task runs twice
    is never listed: that outcome belongs to the task.
    """
    outcomes = {}
    if not (task.acks_late and task.reject_on_worker_lost):
        outcomes[_PRERUN] = ('FAILURE', initial_effect)
        outcomes[_BEFORE_STORE] = ('FAILURE', expected_effect)
    if sigkill:
        outcomes.update({f'{stage}{_SIGKILL}': outcome for stage, outcome in list(outcomes.items())})
    if publishes:
        outcomes[_LINK_REFUSED] = ('FAILURE', expected_effect)
    return outcomes


def _reasons(task, publishes):
    reasons = []
    if not (task.acks_late and task.reject_on_worker_lost):
        reasons.append(_NOT_RUN_AGAIN)
    if publishes:
        reasons.append(_LINK_LOST)
    return reasons


def _resolve(app, task):
    """The application and task objects, as the worker child will import them."""
    module, _, attribute = app.partition(':')
    application = getattr(importlib.import_module(module), attribute or 'app')
    name = task if isinstance(task, str) else task.name
    assert name in application.tasks, (
        f'{app} has no task {name!r}: pass the task registered on the application the worker runs'
    )
    return application, application.tasks[name]


def task_contract(
    app: str,
    task: Any,
    *,
    send: Callable[[], Any],
    effect: Callable[[Any], Any],
    expected_effect: Any,
    initial_effect: Any = 0,
    publishes: bool = False,
    known: Mapping[str, Any] | None = None,
    because: str | None = None,
    sigkill: bool = False,
    name: str | None = None,
    fixtures: tuple[str, ...] = (),
    env: Mapping[str, str] | None = None,
    log: Path | None = None,
    quiet: float = 1.0,
    timeout: float = 60.0,
):
    """Celery's contract with its worker, for one of the application's tasks.

    Arguments:
        app: The Celery application the worker runs, as ``'module:attribute'``.
            The worker child imports it, so its configuration must not depend
            on anything only the test process sets.
        task: The task to fail at each stage, or its registered name.
        send: The application's own code that sends the task, such as the
            view or service that calls ``.delay()``. Returns the task's
            :class:`~celery.result.AsyncResult` (or its id).
        effect: What the task did, read from the :class:`~celery.result.AsyncResult`:
            for example how many emails reached this user. Observe the task's
            own effect; each history starts from a fresh one, so ``send``
            should use a new identity each time.
        expected_effect: ``effect`` after one successful run.
        initial_effect: ``effect`` before the task ran.
        publishes: The task's execution publishes another task (a link, a
            chain's next step, a chord body), so the broker can refuse it.
        known: The application's own known differences, by history label, as
            :class:`~pytest_obligation.integrations.task_queues.TaskOutcome`
            values: what the task does that you cannot fix yet. Requires
            ``because``.
        because: Why the ``known`` differences exist, with a link to their issue.
        sigkill: Also lose the pool child at each stage by ``SIGKILL``, as the
            kernel's OOM killer would.
        fixtures: pytest fixtures every generated case requests, such as one
            that empties the broker and result backend.

    The remaining arguments go to pytest-obligation's ``worker_history``.
    """
    from pytest_obligation import Findings
    from pytest_obligation.integrations.celery_worker import (DEATH_POINTS, FAILURE_POINTS, SIGKILL_DEATH_POINTS,
                                                              worker_contract, worker_history)
    from pytest_obligation.integrations.task_queues import TaskOutcome

    from celery.result import AsyncResult

    assert (known is None) == (because is None), 'known= and because= go together: say why each difference exists'
    application, target = _resolve(app, task)

    def sent():
        result = send()
        return result if isinstance(result, AsyncResult) else AsyncResult(result, app=application)

    def observe(result):
        # OBSERVE: the state Celery recorded, and what the task did.
        return TaskOutcome(status=AsyncResult(result.id, app=application).state, effect=effect(result))

    def settled(result):
        return AsyncResult(result.id, app=application).ready()

    declared = {
        stage: TaskOutcome(status=status, effect=value)
        for stage, (status, value) in celery_outcomes(
            target, initial_effect=initial_effect, expected_effect=expected_effect, publishes=publishes,
            sigkill=sigkill,
        ).items()
    }
    declared.update(known or {})
    expected = TaskOutcome(status='SUCCESS', effect=expected_effect)
    history = worker_history(
        name=name or f'a worker runs {target.name}',
        app=app,
        task=target.name,
        send=sent,
        observe=observe,
        initial=TaskOutcome(status='PENDING', effect=initial_effect),
        expected=expected,
        settled=settled,
        death_points=DEATH_POINTS + (SIGKILL_DEATH_POINTS if sigkill else ()),
        failure_points=FAILURE_POINTS if publishes else (_ON_SUCCESS,),
        quiet=quiet,
        timeout=timeout,
        env=env,
        log=log,
        findings=Findings(expected, declared) if declared else None,
    )
    reasons = [*_reasons(target, publishes), *([because] if because else [])]
    return worker_contract(
        name=name or f'celery: {target.name} through the worker',
        process_handoffs=(history,),
        handoff_gaps={history.name: '; '.join(reasons)} if declared else None,
        fixtures=fixtures,
    )
