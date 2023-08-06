from types import ModuleType

from budosystems.xtra import pytest_suite
from budosystems.xtra.pytest_suite import repository

def test_subproject_import():
    assert isinstance(pytest_suite, ModuleType)
    assert isinstance(pytest_suite.repository, ModuleType)
