# Clean Architecture

!!! note "Framework Agnostic"
    Core business logic is more stable that framework decisions. Either you are exposing your application via a CLI, RestAPI, gRPC, or even as a Slack/WhatsApp application the business use cases supported should be the same across the Presentation Layer you are using.
    
    Of course, this also applied to whether you are using an specif framework for you API (`FastAPI`, `Django`, `Flask`, etc) or your CLI (`parseargs`, `click`, `Typer`, etc) whatever you decide you use where, should be couple to the core logic of your application.

!!! note "Database Agnostic"
    The way you decide to store your application entities, models, aggregates, objects... in the persistance layer (a.k.a database) shouldn't constraint the capabilities of your application. In fact, you should decouple your core business logic from your database implementation using the **repository pattern**, basically you're application knows about the interface the database must implement, whether the implementation uses a `DynamoDB` or a `PostgresSQL` database is something the core business logic doesn't care about.

    