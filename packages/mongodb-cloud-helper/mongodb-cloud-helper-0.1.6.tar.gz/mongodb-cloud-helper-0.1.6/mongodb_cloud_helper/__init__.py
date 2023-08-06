from .bp import *
from .svc import *
from .bp.mongo_srv_connector import MongoSrvConnector
from .bp.mongo_local_connector import MongoLocalConnector
from .mongo_base_api import MongoBaseAPI


def remote_mongo_api() -> MongoBaseAPI:
    """ Connect to Remote Mongo

    Assumes env-var 'MONGODB_SRV' has encrypted SRV string

    Returns:
        MongoBaseAPI: an instantiated MongoBaseAPI
    """
    return MongoBaseAPI(MongoSrvConnector().client())


def local_mongo_api() -> MongoBaseAPI:
    """ Connect to Local Mongo

    Returns:
        MongoBaseAPI: an instantiated MongoBaseAPI
    """
    conn = MongoLocalConnector(user="user", password="pass")
    return MongoBaseAPI(conn.client())
