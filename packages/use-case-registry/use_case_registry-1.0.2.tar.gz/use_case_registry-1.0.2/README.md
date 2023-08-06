# use-case-registry

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Build Status](https://github.com/Tomperez98/use-case-registry/workflows/test/badge.svg?branch=main&event=push)](https://github.com/Tomperez98/use-case-registry/actions?query=workflow%3Atest)

-----

Basically a typed annotated list (enforced), with fixed lenght, that can only be checked once. It's thought as a component to implement use cases for more complex applications.

These applications would implement one workflow per use case. The `UseCaseRegistry` convers a wide range of requirements for these workflows. (1) Capture a set of write operations to be executed as an ACID transaction against the application database (2) Capture the use case result (3) Capture a set of triggered errors that may ocurr during the use case workflow execution. 
