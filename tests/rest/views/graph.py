import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from tests.mock import dao

from argux_server.rest.views.item import RestItemViews

class RestGraphViewsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()
