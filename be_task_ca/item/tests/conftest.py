from unittest.mock import MagicMock

import pytest

from be_task_ca.app import app
from be_task_ca.item.repository.repository import Repository


@pytest.fixture
def mock_repo():
    return MagicMock(spec=Repository)


@pytest.fixture
def mock_api_repo():
    mock_repo = MagicMock(Repository)
    app.dependency_overrides[Repository] = lambda: mock_repo
    return mock_repo
