# -*- coding: utf-8 -*-
import json
import unittest

from mock import patch

from app import app
from views import error_response

from flask_testing import TestCase


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['TESTING'])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['DEBUG'])
        self.assertFalse(app.config['TESTING'])


class TestGetSingleNews(BaseTestCase):

    @patch('views.rpc_get_news')
    @patch('nameko.standalone.events.event_dispatcher')
    def test_success(self, event_dispatcher_mock, rpc_get_news_mock):
        event_dispatcher_mock.return_value = lambda v1, v2, v3: None
        rpc_get_news_mock.return_value = {
            "news": [
                {
                    "_id": 1,
                    "author": "unittest",
                    "content": "Just a service test",
                    "created_at": {
                        "$date": 1514741833010
                    },
                    "news_type": "famous",
                    "tags": [
                        "Test",
                        "unit_test"
                    ],
                    "title": "My Test",
                    "version": 1
                }
            ],
            "status": "success"
        }

        response = self.client.get('/famous/1')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertTrue(len(data['news']) > 0)
        for d in data['news']:
            self.assertEqual(
                d['title'],
                'My Test',
            )
            self.assertEqual(
                d['content'],
                'Just a service test'
            )
            self.assertEqual(
                d['author'],
                'unittest'
            )

    @patch('views.rpc_get_news')
    @patch('nameko.standalone.events.event_dispatcher')
    def test_fail(self, event_dispatcher_mock, rpc_get_news_mock):
        event_dispatcher_mock.return_value = lambda v1, v2, v3: None
        rpc_get_news_mock.return_value = None

        response = self.client.get('/famous/1')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 500)
        self.assertEqual('fail', data['status'])
        self.assertEqual("'NoneType' object is not subscriptable", data['message'])


class TestAddNews(BaseTestCase):

    @patch('views.rpc_command')
    def test_sucess(self, rpc_command_mock):
        """Test to insert a News."""
        dict_obj = dict(
            title='My Test',
            content='Just a service test',
            author='unittest',
            tags=['Test', 'unit_test'],
        )

        rpc_command_mock.return_value = {
            'status': 'success',
            'news': dict_obj,
        }

        with self.client:
            response = self.client.post(
                '/famous',
                data=json.dumps(dict_obj),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual('success', data['status'])
            self.assertEqual('My Test', data['news']['title'])

    def test_fail_by_invalid_input(self):
        dict_obj = None
        with self.client:
            response = self.client.post(
                '/famous',
                data=json.dumps(dict_obj),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertEqual('fail', data['status'])
            self.assertEqual('Invalid payload', data['message'])

    @patch('views.rpc_command')
    def test_fail_to_register(self, rpc_command_mock):
        """Test to insert a News."""
        dict_obj = dict(
            title='My Test',
            content='Just a service test',
            author='unittest',
            tags=['Test', 'unit_test'],
        )

        rpc_command_mock.side_effect = Exception('Forced test fail')

        with self.client:
            response = self.client.post(
                '/famous',
                data=json.dumps(dict_obj),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 500)
            self.assertEqual('fail', data['status'])
            self.assertEqual('Forced test fail', data['message'])


class TestGetAllNewsPerType(BaseTestCase):

    @patch('views.rpc_get_all_news')
    def test_sucess(self, rpc_get_all_news_mock):
        """Test to get all News paginated."""
        rpc_get_all_news_mock.return_value = {
            "news": [
                {
                    "_id": 1,
                    "author": "unittest",
                    "content": "Just a service test 1",
                    "created_at": {
                        "$date": 1514741833010
                    },
                    "news_type": "famous",
                    "tags": [
                        "Test",
                        "unit_test"
                    ],
                    "title": "My Test 1",
                    "version": 1
                },
                {
                    "_id": 2,
                    "author": "unittest",
                    "content": "Just a service test 2",
                    "created_at": {
                        "$date": 1514741833010
                    },
                    "news_type": "famous",
                    "tags": [
                        "Test",
                        "unit_test"
                    ],
                    "title": "My Test 2",
                    "version": 1
                },
            ],
            "status": "success"
        }
        with self.client:
            response = self.client.get('/famous/1/10')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', data['status'])
            self.assertEqual(2, len(data['news']))
            counter = 1
            for d in data['news']:
                self.assertEqual(
                    d['title'],
                    'My Test {}'.format(counter)
                )
                self.assertEqual(
                    d['content'],
                    'Just a service test {}'.format(counter)
                )
                self.assertEqual(
                    d['author'],
                    'unittest'
                )
                counter += 1

    @patch('views.rpc_get_all_news')
    def test_fail(self, rpc_get_all_news_mock):
        """Test to get all News paginated."""
        rpc_get_all_news_mock.side_effect = Exception('Forced test fail')
        with self.client:
            response = self.client.get('/famous/1/10')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 500)
            self.assertEqual('fail', data['status'])
            self.assertEqual('Forced test fail', data['message'])


class TestUtilsFunctions(BaseTestCase):

    def test_error_message(self):
        response = error_response('test message error', 500)
        data = json.loads(response[0].data.decode())
        self.assertEqual(response[1], 500)
        self.assertEqual('fail', data['status'])
        self.assertEqual('test message error', data['message'])


if __name__ == '__main__':
    unittest.main()
