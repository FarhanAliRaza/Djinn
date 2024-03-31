import pytest
from {{cookiecutter.project_slug}}.users.models import User


@pytest.fixture
def bucky(db):
    user = User.objects.create(email="test@test.com")
    user.set_password("pass1234")
    user.save()
    return user
