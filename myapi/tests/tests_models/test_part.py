import pytest
from ..factories import *
from myapi.utils import check_unique

@pytest.mark.django_db
def test_hello_branch():
    assert 1 == 1
