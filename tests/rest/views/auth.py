import unittest
import os
import configparser

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from sqlalchemy import (
    create_engine
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)

from zope.sqlalchemy import ZopeTransactionExtension

import transaction
from sqlalchemy.orm.session import Session

from argux_server.rest.views.auth import RestAuthenticationViews

from argux_server.scripts import initializedb


class RestAuthViewsTests(unittest.TestCase):

    def setUp(self):
        config_file = os.environ['ARGUX_CONFIG']
        config = configparser.ConfigParser()
        config.read(config_file)

        settings = config['app:main']

        from argux_server import main
        app = main({}, **settings)
        from webtest import TestApp
        self.testapp = TestApp(app)

    def tearDown(self):
        del self.testapp

    def test_login(self):
        """

        """
        # r = request.Request.blank(
        #     path='/argux/rest/1.0/login')
        resp = self.testapp.post_json(
            '/rest/1.0/login',
            dict(username='admin',password='admin'))

        self.assertEquals(resp.status_int, 200)
