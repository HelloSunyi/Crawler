# -*- coding: utf-8 -*-
import base64
import time
import zlib
from pymongo import MongoClient
from ..settings import DB_INFO


class BaseStore(object):

    def save(self, page_id, raw):
        pass

    @staticmethod
    def compress(raw):
        pass


class MongoStore(BaseStore):

    def __init__(self, config):
        """Initialize mongodb from settings"""
        self.mongo_client = MongoClient(config['host'], config['port'])
        self.mongo_collection = self.mongo_client[config['db']][
            config['collection']]

    @staticmethod
    def compress(raw):
        raw_zlib = zlib.compress(raw, zlib.Z_BEST_COMPRESSION)
        raw_base64 = base64.b64encode(raw_zlib)
        return raw_base64

    def save(self, page_id, raw):
        self.mongo_collection.replace_one({'_id': page_id},
                                          {'_id': page_id,
                                           'html': self.compress(raw),
                                           'time': int(time.time())},
                                          True)


def get_storage(source_name):
    if DB_INFO['type'] == 'mongodb':
        # db: source_name, collection: raw
        DB_INFO['db'] = source_name
        DB_INFO['collection'] = 'raw'
        return MongoStore(DB_INFO)
    return None
