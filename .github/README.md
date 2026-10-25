# Celery, checked by pytest-obligation

[![pytest-obligation](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/gigaverse-app/celery/obligation-readme/.github/obligation-badge.json)](#what-the-contract-finds-in-celerys-main)

This is [Celery](https://github.com/celery/celery) with one addition: a
[pytest-obligation](https://github.com/gigaverse-app/pytest-obligation) contract for Celery's
worker, in [`t/due_work`](../t/due_work). Celery's own README is [`README.rst`](../README.rst).

The contract sends one task, with a link and an error callback, through a real `celery worker`,
and a chord of two such tasks. It fails each run at one of Celery's stages: the worker's pool
child is lost as the task starts, before or after its result is stored, the task's `on_success`
hook raises, or the broker refuses the next publish. Then it restarts the worker and compares
what each run leaves with a normal run: the task's state, the messages sent, and which of the
link and the error callback ran.

Every night it runs against Celery's current `main`, and the report below is updated whenever
what it finds changes.

- [celery/celery#10726](https://github.com/celery/celery/pull/10726) proposes this contract to Celery.
- [celery/celery#10724](https://github.com/celery/celery/issues/10724) came from it, and is fixed on
  `main` by #10752 and #10759. The contract saw both fixes without being told about them.
- [celery/celery#10725](https://github.com/celery/celery/issues/10725) and
  [celery/celery#10949](https://github.com/celery/celery/issues/10949) are still open.

## What the contract finds in Celery's main

<!-- pytest-obligation:start -->
<!-- pytest-obligation:end -->
