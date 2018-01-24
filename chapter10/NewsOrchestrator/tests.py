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


class TestNewsService(BaseTestCase):

    def test_add_news(self):
        """Test to insert a News to the database."""
        with self.client:
            response = self.client.post(
                '/famous',
                data=json.dumps(dict(
                    title='My Test',
                    content='Just a service test',
                    author='unittest',
                    tags=['Test', 'Functional_test'],
                )),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', data['status'])
            self.assertIn('My Test', data['news']['title'])

    def test_get_all_news(self):
        """Test to get all News paginated from the database."""
        with self.client:
            test_cases = [
                {'page': 1, 'num_per_page': 10, 'loop_couter': 0},
                {'page': 2, 'num_per_page': 10, 'loop_couter': 10},
                {'page': 1, 'num_per_page': 20, 'loop_couter': 0},
            ]
            for tc in test_cases:
                response = self.client.get(
                    '/famous/{}/{}'.format(
                        tc['page'], tc['num_per_page'])
                )
                data = json.loads(response.data.decode())
                self.assertEqual(response.status_code, 200)
                self.assertIn('success', data['status'])
                self.assertEqual(len(data['news']) > 0)
                for d in data['news']:
                    self.assertEqual(
                        d['title'],
                        'Title test-{}'.format(tc['loop_couter'])
                    )
                    self.assertEqual(
                        d['content'],
                        'Content test-{}'.format(tc['loop_couter'])
                    )
                    self.assertEqual(
                        d['author'],
                        'Author test-{}'.format(tc['loop_couter'])
                    )
                    tc['loop_couter'] += 1
