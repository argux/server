import unittest

from pyramid import testing
from pyramid import request
from pyramid.registry import Registry

from tests.mock import dao

from argux_server.rest.views.admin.user import RestUserViews

class RestAdminUserViewsTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    @unittest.skip('not implemented')
    def test_create_user(self):
        """

        """
        r = request.Request.blank(path='/rest/1.0/admin/user/jdoe')
        r.registry = Registry()
        r.registry.settings = {}
        r.registry.settings['dao'] = dao.DAO()
        v = RestUserViews(r)
        response = v.admin_user_1_view_create()

        self.assertEquals(host['name'], "localhost")
