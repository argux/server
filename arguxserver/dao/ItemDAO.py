
from arguxserver.models import (
    DBSession,
    Host,
    ItemCategory,
    ItemName,
    Item
    )

def getItemsFromHost(host):
    i = DBSession.query(Item).filter(Item.host_id == host.id)
    return i

def getItemByHostKey(host, key):
    i = DBSession.query(Item).filter(Item.host_id == host.id).filter(Item.key == key).first()
    return i

def createItem(host, key, name, category, itemtype):
    i = Item(host_id=host.id, key=key, name=name, category=category, itemtype=itemtype)
    DBSession.add(i)
    return i
