from unittest.mock import MagicMock

import pytest

from be_task_ca.user.repository.repository import Repository


@pytest.fixture
def mock_repo():
    return MagicMock(spec=Repository)
