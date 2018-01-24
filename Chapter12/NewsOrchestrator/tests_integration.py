# -*- coding: utf-8 -*-
import json
import unittest

from app import app

from flask_testing import TestCase


class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('config.TestingConfig')
        return app


class TestIntegration(BaseTestCase):

    def setUp(self):
        dict_obj = dict(
            title='My Test',
            content='Just a service test',
            author='unittest',
            tags=['Test', 'unit_test'],
        )

        with self.client:
            self.response_post = self.client.post(
                '/famous',
                data=json.dumps(dict_obj),
                content_type='application/json',
            )
            self.data_post = json.loads(self.response_post.data.decode())

    def test_get_single_news(self):
        response = self.client.get('famous/{id}'.format(id=self.data_post['news']['id']))
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', data['status'])
        self.assertTrue(len(data['news']) > 0)
        self.assertEqual(
            data['news']['title'],
            'My Test',
        )
        self.assertEqual(
            data['news']['content'],
            'Just a service test'
        )
        self.assertEqual(
            data['news']['author'],
            'unittest'
        )

    def test_add_news(self):
        """Test to insert a News."""
        self.assertEqual(self.response_post.status_code, 201)
        self.assertEqual('success', self.data_post['status'])
        self.assertEqual('My Test', self.data_post['news']['title'])


if __name__ == '__main__':
    unittest.main()
