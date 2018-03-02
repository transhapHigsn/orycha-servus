from hashlib import sha256

from orycha_db import db
from bson.objectid import ObjectId
from bson.json_util import dumps
import pymongo
servus = db.orycha_servus


class Orycha:
    length = 0

    def __init__(self, **kwargs):
        self.token_id = self.get_last_entry_field(field='token_id')
        self.name = kwargs['name']
        self.difficulty = 0
        self.parent_id = self.get_last_entry_field()
        self.parent_hash = self.hash_parent()
        self.data = {}

    def __str__(self):
        return 'Orycha -> {}'.format(self.name)

    def __repr__(self):
        return 'Orycha #{}'.format(self.token_id)

    @classmethod
    def create(cls, **kwargs):
        s = cls(**kwargs)
        servus.insert_one(s.as_dict())
        s._id = str(s._id)
        return s

    @classmethod
    def get(cls, **kwargs):
        return servus.find_one(kwargs)

    @classmethod
    def get_all(cls, **kwargs):
        cur = servus.find(kwargs)
        nodes_dict = dict()
        for c in cur:
            c['_id'] = str(c['_id'])
            nodes_dict[c['token_id']] = c

        return nodes_dict

    @classmethod
    def set_data(cls, token_id, data):
        node = servus.find_one({'token_id': token_id})
        difficulty = 0 if not node.get('difficulty') else node['difficulty']
        _ = servus.update_one({'token_id': token_id},
                              {'$set': {
                                  'data': data
                              }})
        current_hash = hash_node(token_id, difficulty=difficulty)
        difficulty += 1
        if difficulty > 9:
            difficulty -= 9
        node = servus.update_one({'token_id': token_id},
                                 {'$set': {
                                     'hash': current_hash,
                                     'difficulty': difficulty,
                                 }})
        return node

    @classmethod
    def delete(cls, search_by):
        node = servus.delete_one(search_by)
        return node

    def as_dict(self):
        return self.__dict__

    def hash_parent(self):
        parent_id = ObjectId(self.parent_id)
        parent = servus.find_one({'_id': parent_id})
        if not parent:
            return
        return sha256(dumps(parent).encode()).hexdigest()

    def get_last_entry_field(self, field='_id'):
        cur = servus.find({}).sort('_id', pymongo.DESCENDING).limit(1)
        for c in cur:
            last = c
            break

        if not last:
            return 0

        if field == '_id':
            return str(last['_id'])
        else:
            return last[field] + 1


def hash_node(token_id, difficulty):
    node = servus.find_one({'token_id': token_id})
    digest = sha256(dumps(node).encode()).hexdigest()
    nonce = 0
    while digest[:2] != str(difficulty) * 2:
        node['nonce'] = nonce
        digest = sha256(dumps(node).encode()).hexdigest()
        nonce += 1
    return digest
