from pyramid.view import (
    view_config,
    view_defaults,
    notfound_view_config
    )

from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound

from arguxserver import models

from arguxserver.util import time_offset_expr

import dateutil.parser

from datetime import datetime, timedelta

from . import RestView

@view_defaults(renderer='json')
class RestTriggerViews(RestView):
    """
    
    self.request:  set via parent constructor
    self.dao:      set via parent constructor
    """

    @view_config(
            route_name='rest_triggers_1',
            request_method='POST')
    def trigger_1_view_create(self):
        dao     = self.dao
        host    = self.request.matchdict['host']
        item    = self.request.matchdict['item']
        name    = self.request.json_body.get('name', None)
        rule    = self.request.json_body.get('rule', None)
        description = self.request.json_body.get('description', None)

        h = dao.HostDAO.getHostByName(host)
        i = dao.ItemDAO.getItemByHostKey(h, item)

        try:
            t = dao.ItemDAO.createTrigger(i, name, rule, description)
        except Exception:
            return Response(
                status='400 Bad Request',
                content_type='application/json; charset=UTF-8')

        return Response(
            status='201 Created',
            content_type='application/json; charset=UTF-8')

    #
    # Read Values
    #
    @view_config(
            route_name='rest_triggers_1',
            request_method='GET')
    def trigger_1_view_read(self):
        dao     = self.dao
        host    = self.request.matchdict['host']
        item    = self.request.matchdict['item']

        triggers = []

        h = dao.HostDAO.getHostByName(host)
        i = dao.ItemDAO.getItemByHostKey(h, item)

        t = dao.ItemDAO.getTriggers(i)
        for trigger in t:
            triggers.append( {
                'id':   trigger.id,
                'name': trigger.name,
                'rule': trigger.rule
            })

        return {
                'host':host,
                'item':item,
                'triggers': triggers }