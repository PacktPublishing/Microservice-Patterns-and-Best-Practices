import os
import pytest

from .service import Command

from nameko.testing.services import worker_factory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def session():
    db_engine = create_engine(os.environ.get('COMMANDDB_TEST_HOST'))
    Session = sessionmaker(db_engine)
    return Session()


def test_command(session):
    data = {
        "title": "title test",
        "author": "author test",
        "content": "content test",
        "tags": [
            "test tag1",
            "test tag2",
        ],
    }
    command = worker_factory(Command, db=session)
    result = command.add_news(data)
    assert result['title'] == "title test"
    assert result['version'] == 1

    data['id'] = result['id']
    data['version'] = result['version']
    command = worker_factory(Command, db=session)
    result = command.add_news(data)
    assert result['version'] == 2
