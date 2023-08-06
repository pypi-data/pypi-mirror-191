# One Use Case, One Workflow

!!! note "Use case modeled as a workflow"
    Use cases can be thought as a set of orchestrated steps that are executed until completion (think about step functions, airflow, temporal, etc). These steps can **(1)** interact with third-party services **(2)** interact with the system database, and **(3)** perform in-memory operations that do calculations.

!!! note "Aim for durable execution and idempotency"
    You want to write your workflows in a way that the retrial of the steps do not cause the system to end up in an inconsistent state. Now, this is not 100% achievable if you are not building you application in a durable execution platform. But you can still apply most of these principles.

    To do this you want to split you workflow into two parts, the **first part** would go from start up to the commit of an atomic transaction againt the application database. In this part you want to limit the code to only invoking `query`[^1] operations and modifying application models in memory, this part would end when the changes are committed as an ACID transaction against the application database.

    The **second part** starts after the commit of the state changes up to the end of the workflow execution. This part would invoke `command`[^2] operations against third-party services. Thinks like sending notification via email, SMS, WhatsApp, or sending analytics on application usage to other services, goes here. The reason why this implementation won't be 100% durable is that, with API requests, in case of failure the best think you can do is to retry the call n-number of times (Durable execution platforms would ensure these steps are retried indefinatelly up until completion).


[^1]: Operations that request information on the current state of a system but do not alter the state. Idempotent by definition.
[^2]: Operations that do modify the state of a system. Not idempotent by default (you could use an idempotency key).
