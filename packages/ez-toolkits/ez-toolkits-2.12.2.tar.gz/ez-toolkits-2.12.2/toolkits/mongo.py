from loguru import logger
from pymongo import MongoClient

from . import utils


class Mongo():

    mongo = MongoClient()

    def __init__(self, mongo_url=None):
        ''' Initiation '''
        if mongo_url != None:
            self.mongo = MongoClient(mongo_url)

    def close(self):
        try:
            self.mongo.close()
        except Exception as e:
            logger.exception(e)

    def connect_test(self):
        info = 'MongoDB连接测试'
        try:
            logger.info(f'{info}......')
            self.mongo.server_info()
            logger.success(f'{info}[成功]')
            return True
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False

    def collection(self, database, name):
        return self.mongo[database][name]

    def collection_insert(self, database, collection, data, drop=None):
        db_collection = self.mongo[database][collection]
        info = '插入数据'
        try:
            logger.info(f'{info}......')
            # 是否删除 collection
            if drop == True:
                # 删除 collection
                db_collection.drop()
            # 插入数据
            if utils.vTrue(data, dict):
                # 插入一条数据
                result = db_collection.insert_one(data)
            elif utils.vTrue(data, list):
                # 插入多条数据
                result = db_collection.insert_many(data)
            else:
                logger.error(f'{info}[失败]')
                logger.error('数据类型错误')
                return False
            logger.success(f'{info}[成功]')
            return result
        except Exception as e:
            logger.error(f'{info}[失败]')
            logger.exception(e)
            return False
