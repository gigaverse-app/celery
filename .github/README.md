# Celery, checked by pytest-obligation

[![pytest-obligation](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/gigaverse-app/celery-obligation/main/.github/obligation-badge.json)](#what-the-contract-finds-in-celerys-main)

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
  `main` by [celery/celery#10752](https://github.com/celery/celery/pull/10752) and
  [celery/celery#10759](https://github.com/celery/celery/pull/10759). The contract saw both fixes without being told about them.
- [celery/celery#10725](https://github.com/celery/celery/issues/10725) and
  [celery/celery#10954](https://github.com/celery/celery/issues/10954) are still open.

## What the contract finds in Celery's main

<!-- pytest-obligation:start -->
> [!CAUTION]
> **The test step failed.**
>
> 9 failed contract checks recorded.
>
> Contract counts cover only obligation checks; inspect the run log for other failures.

<a href="https://github.com/gigaverse-app/pytest-obligation"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/sticky-banner-dark.svg"><img alt="pytest-obligation: what passed, what is missing, what to fix" src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/sticky-banner-light.svg" width="640"></picture></a>

### Obligation contract checks

Other pytest tests and workflow steps are not included in these counts.

<p><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-5-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-5-light.svg" width="18" height="36" alt="5 applications" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="69" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-1-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-1-light.svg" width="18" height="36" alt="1 contract checks passed" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="75" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/divider-light.svg" width="1" height="36" alt="" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="12" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-9-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/bad-9-light.svg" width="18" height="36" alt="9 contract failures" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="68" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="18" height="36" alt="0 blocked checks" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="75" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="18" height="36" alt="0 coverage gaps" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="72" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/good-0-light.svg" width="18" height="36" alt="0 rejected bindings" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="73" height="36" alt="" align="middle"></picture><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-0-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/neutral-0-light.svg" width="18" height="36" alt="0 skipped tests" align="middle"></picture><picture><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/space.svg" width="69" height="36" alt="" align="middle"></picture><br><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/captions-with-skips-dark.svg"><img src="https://raw.githubusercontent.com/gigaverse-app/pytest-obligation/main/docs/assets/report-glyphs/captions-with-skips-light.svg" width="640" height="34" alt="applications · contract checks passed · contract failures · blocked checks · coverage gaps · rejected bindings · skipped tests" align="middle"></picture></p>

**Failures: 1 unexpected + 8 known expected.** Expected failures are declared by the application and do not fail CI. Review their reasons and evidence below; counts are checks, not distinct product bugs.

<details>
<summary>Application inventory and skipped tests</summary>

**5** applications with results · **0** applications not run
Checks skipped: **0**.


Static declarations only; dynamically generated suites may be absent. No application code was imported.
Application name unresolved: t.due&#95;work.test&#95;application&#95;contract.test&#95;DefaultConfiguration; showing its suite name.
Application name unresolved: t.due&#95;work.test&#95;application&#95;contract.test&#95;RequeuedWithoutAKey; showing its suite name.
Application name unresolved: t.due&#95;work.test&#95;application&#95;contract.test&#95;RequeuedWithAKey; showing its suite name.

</details>

### Applications

All collected applications, most actionable first. Expand the evidence below for reasons and tickets.

| Application | Passed | Failed | Blocked | Gaps | Rejected |
| :--- | ---: | ---: | ---: | ---: | ---: |
| celery: the worker runni&#8203;ng a task | 0 | 🔴 **6** | 0 | 0 | 0 |
| celery: a worker runs we&#8203;lcome.send&#95;welcome&#95;email | 0 | 🔴 **1** | 0 | 0 | 0 |
| celery: a worker runs we&#8203;lcome.send&#95;welcome&#95;email&#8203;&#95;requeued | 0 | 🔴 **1** | 0 | 0 | 0 |
| celery: a worker runs it&#8203; with a link | 0 | 🔴 **1** | 0 | 0 | 0 |

<details>
<summary>1 applications · zero failures, blocked checks or gaps</summary>

| Application | Passed | Failed | Blocked | Gaps | Rejected |
| :--- | ---: | ---: | ---: | ---: | ---: |
| celery: a worker runs we&#8203;lcome.send&#95;welcome&#95;email&#8203;&#95;once | **1** | 0 | 0 | 0 | 0 |

</details>

### Evidence and decisions


<details>
<summary><strong>celery: the worker runni&#8203;ng a task</strong> · evidence and decisions</summary>

Contract contract setup: <code>t/due&#95;work/test&#95;worker&#95;contract.py:306</code>

**1 unexpected failures**

AssertionError: a worker runs a chord with results in a database, whose chord&#95;unlock retries while a header runs: these histories no longer leave what the table pins: died at task&#95;postrun (SIGKILL): pinned (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), now (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,))<br>asser…

<details>
<summary><strong>1 unexpected failures · diagnostics</strong></summary>

- <code>process-a worker runs a chord with results in a database, whose chord&#95;unlock retries while a header runs-assert&#95;process&#95;deaths&#95;converge</code>: **Check failed**
- **call:** AssertionError: a worker runs a chord with results in a database, whose chord&#95;unlock retries while a header runs: these histories no longer leave what the table pins: died at task&#95;postrun (SIGKILL): pinned (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), now (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,))<br>assert not {&#x27;died at task&#95;postrun (SIGKILL)&#x27;: (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,))}
  - Guarantee: Unfinished work gets recovered

</details>

<details>
<summary><strong>🔴 Known defects · application-declared expected failures</strong></summary>

Application reason: once the link is published, a failure still runs the failure path: a child lost after the link, before the store, records FAILURE for a task whose effect and link happened, and fires the error callback beside the link (https://github.com/celery/celery/issues/10954); and a link the broker refuses records FAILURE and acknowledges the message, so the link is never sent (https://github.com/celery/celery/issues/10725). FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs send&#95;message-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs send&#95;message: normal operation reaches (&#x27;SUCCESS&#x27;, 1, (&quot;sent &#x27;your order has shipped&#x27;&quot;,)), but these histories reach something else: {&#x27;died at task&#95;prerun&#x27;: (&#x27;FAILURE&#x27;, 0, (&#x27;failed: WorkerLostError&#x27;,)), &#x27;died at mark&#95;as&#95;done&#x27;: (&#x27;FAILURE&#x27;, 1, (&#x27;failed: WorkerLostError&#x27;, &quot;sent &#x27;your order has shipped&#x27;&quot;)), &quot;the broker refused the task&#x27;s link&quot;: (&#x27;FAILURE&#x27;, 1, (&#x27;failed: OperationalError&#x27;,))}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a commit that a dead worker never runs: commit the handoff with the state that owes it, or make that state selectable by recovery. A repeat is recovery redoing an external call…

</details>

Application reason: a header lost after its effect and before its store, or a refused body publish, fails the chord for good though every message was sent (https://github.com/celery/celery/issues/10954, https://github.com/celery/celery/issues/10725#issuecomment-6318108091); a header lost as it starts is never run again (task&#95;reject&#95;on&#95;worker&#95;lost off). CHORD&#95;FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs a chord of two send&#95;message tasks-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs a chord of two send&#95;message tasks: normal operation reaches (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,)), but these histories reach something else: {&#x27;died at task&#95;prerun&#x27;: (&#x27;FAILURE&#x27;, 1, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at mark&#95;as&#95;done&#x27;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at task&#95;prerun (SIGKILL)&#x27;: (&#x27;FAILURE&#x27;, 1, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at mark&#95;as&#95;done (SIGKILL)&#x27;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), &quot;the broker refused the task&#x27;s link&quot;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ())}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code a…

</details>

Application reason: a header lost before its store runs again and sends its message twice, as task&#95;reject&#95;on&#95;worker&#95;lost documents; a refused body publish fails the chord for good. REQUEUED&#95;CHORD&#95;FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker that requeues a task whose pool child was lost runs a chord of two send&#95;message tasks-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker that requeues a task whose pool child was lost runs a chord of two send&#95;message tasks: normal operation reaches (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,)), but these histories reach something else: {&#x27;died at mark&#95;as&#95;done&#x27;: (&#x27;SUCCESS&#x27;, 3, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,)), &#x27;died at mark&#95;as&#95;done (SIGKILL)&#x27;: (&#x27;SUCCESS&#x27;, 3, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,)), &quot;the broker refused the task&#x27;s link&quot;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ())}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a …

</details>

Application reason: the good header lost as it starts is never run again (task&#95;reject&#95;on&#95;worker&#95;lost off); the error callback fires once, as in normal operation. FAILING&#95;HEADER&#95;FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs a chord whose other header task fails-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs a chord whose other header task fails: normal operation reaches (&#x27;FAILURE&#x27;, 1, (&#x27;failed: ChordError&#x27;,), ()), but these histories reach something else: {&#x27;died at task&#95;prerun&#x27;: (&#x27;FAILURE&#x27;, 0, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at task&#95;prerun (SIGKILL)&#x27;: (&#x27;FAILURE&#x27;, 0, (&#x27;failed: ChordError&#x27;,), ())}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a commit that a dead worker never runs: commit the handoff with the state that owes it, or make that state selectable by recovery. A repeat is recovery redoing an external call whose effect already exists: make the call idempotent, or record the attempt before it

</details>

Application reason: as on Redis: a header lost after its effect, or a refused body publish, fails the chord for good; a header lost as it starts is never run again. DATABASE&#95;CHORD&#95;FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs a chord of two send&#95;message tasks with results in a database-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs a chord of two send&#95;message tasks with results in a database: normal operation reaches (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,)), but these histories reach something else: {&#x27;died at task&#95;prerun&#x27;: (&#x27;FAILURE&#x27;, 1, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at mark&#95;as&#95;done&#x27;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at task&#95;prerun (SIGKILL)&#x27;: (&#x27;FAILURE&#x27;, 1, (&#x27;failed: ChordError&#x27;,), ()), &#x27;died at mark&#95;as&#95;done (SIGKILL)&#x27;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), &quot;the broker refused the task&#x27;s link&quot;: (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ())}. Work was lost or repeated. A loss is work handed off only by a messa…

</details>

Application reason: a refused chord&#95;unlock retry loses the chord: the body stays PENDING forever and no callback fires (https://github.com/celery/celery/issues/10955); a header lost after publishing its own retry is recorded FAILURE and fails the chord though the retry still sends (the shape of https://github.com/celery/celery/issues/10954). WAITING&#95;DATABASE&#95;CHORD&#95;FINDINGS pins each history

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs a chord with results in a database, whose chord&#95;unlock retries while a header runs-assert&#95;process&#95;deaths&#95;converge</code>: Check failed
- **call:** AssertionError: a worker runs a chord with results in a database, whose chord&#95;unlock retries while a header runs: these histories no longer leave what the table pins: died at task&#95;postrun (SIGKILL): pinned (&#x27;FAILURE&#x27;, 2, (&#x27;failed: ChordError&#x27;,), ()), now (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,))<br>assert not {&#x27;died at task&#95;postrun (SIGKILL)&#x27;: (&#x27;SUCCESS&#x27;, 2, (&#x27;sent 2 messages&#x27;,), (&quot;&#91;&#x27;order 1 has shipped&#x27;, &#x27;order 2 has shipped&#x27;&#93;&quot;,))}

</details>

These are application declarations. An expected failure can come from a declared gap or an unmet proof precondition; inspect its execution and diagnostics before treating it as a reproduced product defect.

</details>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Unfinished work gets recovered (A)** · Not claimed by application. Application reason: Celery keeps no owed state of its own to sweep: a message the worker did not acknowledge is the broker&#x27;s to redeliver (task&#95;acks&#95;late), and one it did acknowledge is settled
- **Worker ownership is bounded (B)** · Not claimed by application. Application reason: a task&#x27;s lease is the broker&#x27;s visibility timeout or connection, not a fenced claim Celery can check
- **Uncertain outcomes are handled (C)** · Not claimed by application. Application reason: with task&#95;acks&#95;late a task whose worker died may run again; whether it reached its service is its own
- **Needed records are retained (D)** · Not applicable (application decision). Application reason: stored results are the record of settled work, not work still owed
- **Results eventually settle correctly (E)** · Not applicable (application decision). Application reason: one worker settles each delivery; no two results race to write it
- **Owed work is discovered from stored facts (F)** · Not applicable (application decision). Application reason: the obligation is the message itself, not a fact derived from product state
- **Execution respects its gate (G)** · Not claimed by application. Application reason: Celery&#x27;s worker contract has no application readiness predicate; dependencies and product gates need their own ExecutionGate binding, including release with its notification lost.
- **Repeating work is harmless (H)** · Not claimed by application. Application reason: a task can run more than once (with task&#95;acks&#95;late, a redelivery after its worker was lost), so rerunning it must be safe, but that is a property of each task&#x27;s function, not of Celery
- **Intent and work are saved together (I)** · Not claimed by application. Application reason: Celery&#x27;s worker receives already admitted work; it cannot make an application&#x27;s product transaction atomic with enqueue. Bind Profile I on the application&#x27;s command contract.
- **Retries have a limit (J)** · Not claimed by application. Application reason: a task&#x27;s retries are its own (self.retry, autoretry&#95;for); a redelivery after a lost worker is not counted as one

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · No generated scenario bindings collected</strong></summary>

No optional schedule-exploration cases were collected for this suite. Other Hypothesis use inside application callbacks is not assessed here.

</details>

---

<details>
<summary><strong>⚪ 0 supported guarantees</strong></summary>


Suite (application code): <code>t.due&#95;work.test&#95;worker&#95;contract.test&#95;WorkerContract</code>

</details>

</details>

<details>
<summary><strong>celery: a worker runs we&#8203;lcome.send&#95;welcome&#95;email</strong> · evidence and decisions</summary>

Contract suite: <code>t/due&#95;work/test&#95;application&#95;contract.py:59</code>

<details>
<summary><strong>🔴 Known defects · application-declared expected failures</strong></summary>

Application reason: with acks&#95;late and reject&#95;on&#95;worker&#95;lost not both set (Celery&#x27;s default), a task whose pool child is lost is recorded FAILURE (WorkerLostError) and is not run again: lost as it starts, its effect never happens; lost after its body ran and before its result was stored, it is recorded FAILURE though its effect happened. Set both on the task to have it run again instead, and make the task safe to run twice

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs welcome.send&#95;welcome&#95;email-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs welcome.send&#95;welcome&#95;email: normal operation reaches TaskOutcome(status=&#x27;SUCCESS&#x27;, effect=1), but these histories reach something else: {&#x27;died at task&#95;prerun&#x27;: TaskOutcome(status=&#x27;FAILURE&#x27;, effect=0), &#x27;died at mark&#95;as&#95;done&#x27;: TaskOutcome(status=&#x27;FAILURE&#x27;, effect=1), &#x27;died at task&#95;prerun (SIGKILL)&#x27;: TaskOutcome(status=&#x27;FAILURE&#x27;, effect=0), &#x27;died at mark&#95;as&#95;done (SIGKILL)&#x27;: TaskOutcome(status=&#x27;FAILURE&#x27;, effect=1)}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a commit that a dead worker never runs: commit the handoff with the state that owes it, or make that state selectable by recovery. A repeat is recovery…

</details>

These are application declarations. An expected failure can come from a declared gap or an unmet proof precondition; inspect its execution and diagnostics before treating it as a reproduced product defect.

</details>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Unfinished work gets recovered (A)** · Not claimed by application. Application reason: Celery keeps no owed state of its own to sweep: a message the worker did not acknowledge is the broker&#x27;s to redeliver (task&#95;acks&#95;late), and one it did acknowledge is settled
- **Worker ownership is bounded (B)** · Not claimed by application. Application reason: a task&#x27;s lease is the broker&#x27;s visibility timeout or connection, not a fenced claim Celery can check
- **Uncertain outcomes are handled (C)** · Not claimed by application. Application reason: with task&#95;acks&#95;late a task whose worker died may run again; whether it reached its service is its own
- **Needed records are retained (D)** · Not applicable (application decision). Application reason: stored results are the record of settled work, not work still owed
- **Results eventually settle correctly (E)** · Not applicable (application decision). Application reason: one worker settles each delivery; no two results race to write it
- **Owed work is discovered from stored facts (F)** · Not applicable (application decision). Application reason: the obligation is the message itself, not a fact derived from product state
- **Execution respects its gate (G)** · Not claimed by application. Application reason: Celery&#x27;s worker contract has no application readiness predicate; dependencies and product gates need their own ExecutionGate binding, including release with its notification lost.
- **Repeating work is harmless (H)** · Not claimed by application. Application reason: a task can run more than once (with task&#95;acks&#95;late, a redelivery after its worker was lost), so rerunning it must be safe, but that is a property of each task&#x27;s function, not of Celery
- **Intent and work are saved together (I)** · Not claimed by application. Application reason: Celery&#x27;s worker receives already admitted work; it cannot make an application&#x27;s product transaction atomic with enqueue. Bind Profile I on the application&#x27;s command contract.
- **Retries have a limit (J)** · Not claimed by application. Application reason: a task&#x27;s retries are its own (self.retry, autoretry&#95;for); a redelivery after a lost worker is not counted as one

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · No generated scenario bindings collected</strong></summary>

No optional schedule-exploration cases were collected for this suite. Other Hypothesis use inside application callbacks is not assessed here.

</details>

---

<details>
<summary><strong>⚪ 0 supported guarantees</strong></summary>


Suite (application code): <code>t.due&#95;work.test&#95;application&#95;contract.test&#95;DefaultConfiguration</code>

</details>

</details>

<details>
<summary><strong>celery: a worker runs we&#8203;lcome.send&#95;welcome&#95;email&#8203;&#95;requeued</strong> · evidence and decisions</summary>

Contract suite: <code>t/due&#95;work/test&#95;application&#95;contract.py:66</code>

<details>
<summary><strong>🔴 Known defects · application-declared expected failures</strong></summary>

Application reason: a pool child lost after the email left, before the result was stored, runs the task again and sends the email twice: send&#95;welcome&#95;email&#95;requeued sends no key the provider could drop a repeat by

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs welcome.send&#95;welcome&#95;email&#95;requeued-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs welcome.send&#95;welcome&#95;email&#95;requeued: normal operation reaches TaskOutcome(status=&#x27;SUCCESS&#x27;, effect=1), but these histories reach something else: {&#x27;died at mark&#95;as&#95;done&#x27;: TaskOutcome(status=&#x27;SUCCESS&#x27;, effect=2)}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a commit that a dead worker never runs: commit the handoff with the state that owes it, or make that state selectable by recovery. A repeat is recovery redoing an external call whose effect already exists: make the call idempotent, or record the attempt before it

</details>

These are application declarations. An expected failure can come from a declared gap or an unmet proof precondition; inspect its execution and diagnostics before treating it as a reproduced product defect.

</details>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Unfinished work gets recovered (A)** · Not claimed by application. Application reason: Celery keeps no owed state of its own to sweep: a message the worker did not acknowledge is the broker&#x27;s to redeliver (task&#95;acks&#95;late), and one it did acknowledge is settled
- **Worker ownership is bounded (B)** · Not claimed by application. Application reason: a task&#x27;s lease is the broker&#x27;s visibility timeout or connection, not a fenced claim Celery can check
- **Uncertain outcomes are handled (C)** · Not claimed by application. Application reason: with task&#95;acks&#95;late a task whose worker died may run again; whether it reached its service is its own
- **Needed records are retained (D)** · Not applicable (application decision). Application reason: stored results are the record of settled work, not work still owed
- **Results eventually settle correctly (E)** · Not applicable (application decision). Application reason: one worker settles each delivery; no two results race to write it
- **Owed work is discovered from stored facts (F)** · Not applicable (application decision). Application reason: the obligation is the message itself, not a fact derived from product state
- **Execution respects its gate (G)** · Not claimed by application. Application reason: Celery&#x27;s worker contract has no application readiness predicate; dependencies and product gates need their own ExecutionGate binding, including release with its notification lost.
- **Repeating work is harmless (H)** · Not claimed by application. Application reason: a task can run more than once (with task&#95;acks&#95;late, a redelivery after its worker was lost), so rerunning it must be safe, but that is a property of each task&#x27;s function, not of Celery
- **Intent and work are saved together (I)** · Not claimed by application. Application reason: Celery&#x27;s worker receives already admitted work; it cannot make an application&#x27;s product transaction atomic with enqueue. Bind Profile I on the application&#x27;s command contract.
- **Retries have a limit (J)** · Not claimed by application. Application reason: a task&#x27;s retries are its own (self.retry, autoretry&#95;for); a redelivery after a lost worker is not counted as one

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · No generated scenario bindings collected</strong></summary>

No optional schedule-exploration cases were collected for this suite. Other Hypothesis use inside application callbacks is not assessed here.

</details>

---

<details>
<summary><strong>⚪ 0 supported guarantees</strong></summary>


Suite (application code): <code>t.due&#95;work.test&#95;application&#95;contract.test&#95;RequeuedWithoutAKey</code>

</details>

</details>

<details>
<summary><strong>celery: a worker runs it&#8203; with a link</strong> · evidence and decisions</summary>

Contract suite: <code>t/due&#95;work/test&#95;application&#95;contract.py:85</code>

<details>
<summary><strong>🔴 Known defects · application-declared expected failures</strong></summary>

Application reason: when the broker refuses the task&#x27;s link, the task is recorded FAILURE though its effect happened, and the message is acknowledged, so the link is not sent again (https://github.com/celery/celery/issues/10725)

Ticket not reported.

<details>
<summary>1 affected checks · execution evidence</summary>

- <code>process-a worker runs it with a link-assert&#95;process&#95;deaths&#95;converge</code>: Known expected failure
- **call:** HistoriesDiverged: a worker runs it with a link: normal operation reaches TaskOutcome(status=&#x27;SUCCESS&#x27;, effect=1), but these histories reach something else: {&quot;the broker refused the task&#x27;s link&quot;: TaskOutcome(status=&#x27;FAILURE&#x27;, effect=1)}. Work was lost or repeated. A loss is work handed off only by a message, a commit hook or code after a commit that a dead worker never runs: commit the handoff with the state that owes it, or make that state selectable by recovery. A repeat is recovery redoing an external call whose effect already exists: make the call idempotent, or record the attempt before it

</details>

These are application declarations. An expected failure can come from a declared gap or an unmet proof precondition; inspect its execution and diagnostics before treating it as a reproduced product defect.

</details>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Unfinished work gets recovered (A)** · Not claimed by application. Application reason: Celery keeps no owed state of its own to sweep: a message the worker did not acknowledge is the broker&#x27;s to redeliver (task&#95;acks&#95;late), and one it did acknowledge is settled
- **Worker ownership is bounded (B)** · Not claimed by application. Application reason: a task&#x27;s lease is the broker&#x27;s visibility timeout or connection, not a fenced claim Celery can check
- **Uncertain outcomes are handled (C)** · Not claimed by application. Application reason: with task&#95;acks&#95;late a task whose worker died may run again; whether it reached its service is its own
- **Needed records are retained (D)** · Not applicable (application decision). Application reason: stored results are the record of settled work, not work still owed
- **Results eventually settle correctly (E)** · Not applicable (application decision). Application reason: one worker settles each delivery; no two results race to write it
- **Owed work is discovered from stored facts (F)** · Not applicable (application decision). Application reason: the obligation is the message itself, not a fact derived from product state
- **Execution respects its gate (G)** · Not claimed by application. Application reason: Celery&#x27;s worker contract has no application readiness predicate; dependencies and product gates need their own ExecutionGate binding, including release with its notification lost.
- **Repeating work is harmless (H)** · Not claimed by application. Application reason: a task can run more than once (with task&#95;acks&#95;late, a redelivery after its worker was lost), so rerunning it must be safe, but that is a property of each task&#x27;s function, not of Celery
- **Intent and work are saved together (I)** · Not claimed by application. Application reason: Celery&#x27;s worker receives already admitted work; it cannot make an application&#x27;s product transaction atomic with enqueue. Bind Profile I on the application&#x27;s command contract.
- **Retries have a limit (J)** · Not claimed by application. Application reason: a task&#x27;s retries are its own (self.retry, autoretry&#95;for); a redelivery after a lost worker is not counted as one

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · No generated scenario bindings collected</strong></summary>

No optional schedule-exploration cases were collected for this suite. Other Hypothesis use inside application callbacks is not assessed here.

</details>

---

<details>
<summary><strong>⚪ 0 supported guarantees</strong></summary>


Suite (application code): <code>t.due&#95;work.test&#95;application&#95;contract.test&#95;WithALink</code>

</details>

</details>

<details>
<summary><strong>celery: a worker runs we&#8203;lcome.send&#95;welcome&#95;email&#8203;&#95;once</strong> · evidence and decisions</summary>

Contract suite: <code>t/due&#95;work/test&#95;application&#95;contract.py:79</code>

<details>
<summary><strong>⚪ Deliberate exclusions</strong></summary>

- **Unfinished work gets recovered (A)** · Not claimed by application. Application reason: Celery keeps no owed state of its own to sweep: a message the worker did not acknowledge is the broker&#x27;s to redeliver (task&#95;acks&#95;late), and one it did acknowledge is settled
- **Worker ownership is bounded (B)** · Not claimed by application. Application reason: a task&#x27;s lease is the broker&#x27;s visibility timeout or connection, not a fenced claim Celery can check
- **Uncertain outcomes are handled (C)** · Not claimed by application. Application reason: with task&#95;acks&#95;late a task whose worker died may run again; whether it reached its service is its own
- **Needed records are retained (D)** · Not applicable (application decision). Application reason: stored results are the record of settled work, not work still owed
- **Results eventually settle correctly (E)** · Not applicable (application decision). Application reason: one worker settles each delivery; no two results race to write it
- **Owed work is discovered from stored facts (F)** · Not applicable (application decision). Application reason: the obligation is the message itself, not a fact derived from product state
- **Execution respects its gate (G)** · Not claimed by application. Application reason: Celery&#x27;s worker contract has no application readiness predicate; dependencies and product gates need their own ExecutionGate binding, including release with its notification lost.
- **Repeating work is harmless (H)** · Not claimed by application. Application reason: a task can run more than once (with task&#95;acks&#95;late, a redelivery after its worker was lost), so rerunning it must be safe, but that is a property of each task&#x27;s function, not of Celery
- **Intent and work are saved together (I)** · Not claimed by application. Application reason: Celery&#x27;s worker receives already admitted work; it cannot make an application&#x27;s product transaction atomic with enqueue. Bind Profile I on the application&#x27;s command contract.
- **Retries have a limit (J)** · Not claimed by application. Application reason: a task&#x27;s retries are its own (self.retry, autoretry&#95;for); a redelivery after a lost worker is not counted as one

These are scope decisions, not demonstrated defects. Review their reasons when the application changes.

</details>

---

<details>
<summary><strong>Hypothesis · No generated scenario bindings collected</strong></summary>

No optional schedule-exploration cases were collected for this suite. Other Hypothesis use inside application callbacks is not assessed here.

</details>

---

<details>
<summary><strong>⚪ 0 supported guarantees</strong></summary>


Suite (application code): <code>t.due&#95;work.test&#95;application&#95;contract.test&#95;RequeuedWithAKey</code>

</details>

</details>

---

<details>
<summary><strong>What do these numbers mean?</strong></summary>

- **Failures:** an executed assertion failed unexpectedly or was an application-declared expected failure. Expected failures still permit successful CI; the visible breakdown distinguishes them.
- **Rejected bindings:** repair the connection to production code; these checks provide no supporting evidence.
- **Blocked checks:** checks could not establish a result, including missing execution, setup/cleanup errors, binding-debt or unclassified expected failures, and unexpected passes requiring declaration review.
- **Coverage gaps:** guarantees not assessed, missing scenarios, or with declared gaps. Each affected guarantee counts once. Deliberate exclusions are shown separately.

Pass/fail/blocked/rejected counts partition unique checks. Gaps count guarantees, not extra tests. Declined and not-applicable declarations remain separate and do not establish passing coverage. Graphics color contract results: passing checks and zero issues are green, failures and rejected bindings are red, blocked checks and gaps are amber. Missing reports never show green zeroes. The workflow status above is separate from these contract counts.

Elapsed time covers the pytest session. Summed check time includes setup, execution and cleanup; parallel work overlaps.
Application totals include discovered declarations and reported suites. Skipped checks count known deselections and explicit pytest skips; incomplete selected checks are not skips. Uncollected applications have unknown check counts. Zero recorded outcomes do not certify passing coverage.

Application names, quoted reasons and diagnostic values come from application code. Guarantee labels come from pytest-obligation. Results cover collected suites only; passing checks do not rate every test's quality.

Test step (reported): **failure**
Source: <code>nightly run of t/due&#95;work against Celery&#x27;s current main</code>

</details>

[Report guide](https://github.com/gigaverse-app/pytest-obligation/blob/main/package/docs/github-action-report.md)
<!-- pytest-obligation:end -->
