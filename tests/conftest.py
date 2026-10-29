import pytest
from gardavu.demo import configured_rules, demo_doctors


@pytest.fixture
def rules():
    return configured_rules(8)


@pytest.fixture
def doctors():
    return demo_doctors()
