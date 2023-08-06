"""Test for use case."""
from typing import Union

import pytest
from result import Ok, Result

from use_case_registry import UseCaseRegistry
from use_case_registry.errors import IdentifiedError, NotIdentifiedError
from use_case_registry.use_case import IUsecase


class TestIUsecase:
    """Test definition for IUsecase."""

    def test_cannot_be_instantiated(self) -> None:
        """IUsecase is an interface an cannot be instantiated."""
        write_ops_registry = UseCaseRegistry[str](max_length=1)

        with pytest.raises(TypeError):
            IUsecase(
                write_ops_registry=write_ops_registry,
            )  # type:ignore[abstract]

    def test_interface_can_be_extendend(self) -> None:
        """Test interface can be extended."""

        class ConcreteUsecase(IUsecase):
            def __init__(
                self,
                name: str,
                last_name: str,
                write_ops_registry: UseCaseRegistry[str],
            ) -> None:
                """Construct concrete implementation."""
                self.name = name
                self.last_name = last_name
                super().__init__(write_ops_registry)

            def execute(
                self,
            ) -> Result[None, Union[IdentifiedError, NotIdentifiedError]]:
                return Ok()

        write_ops_registry = UseCaseRegistry[str](max_length=1)

        ConcreteUsecase(
            name="Peter",
            last_name="Parket",
            write_ops_registry=write_ops_registry,
        )
