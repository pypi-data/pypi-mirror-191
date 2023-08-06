#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Connect to the MongoDB instance """


from pymongo import MongoClient


from baseblock import EnvIO
from baseblock import BaseObject
from baseblock import CryptoBase


class MongoSrvConnector(BaseObject):
    """ Connect to the MongoDB instance  """

    def __init__(self,
                 srv_key: str = 'MONGODB_SRV'):
        """ Change Log

        Created:
            16-Aug-2022
            craigtrim@gmail.com
        Updated:
            11-Feb-2023
            craigtrim@gmail.com
            *   renamed from 'mongo-connector'

        Args:
            srv_key (str, optional): the SRV string for connecting to the Cloud Instance of MongoDB. Defaults to 'MONGODB_SRV'.
                it is assumed that this string is encrypted using `baseblock.CryptoBase.encrypt_str`
        """
        BaseObject.__init__(self, __name__)
        self._client = MongoClient(
            self._connection_string(
                EnvIO.str_or_exception(srv_key)))

    def _connection_string(self,
                           constr) -> str:
        constr = CryptoBase().decrypt_str(constr)
        constr = constr.replace('AMPERSAND', '&')
        return constr

    def client(self) -> MongoClient:
        return self._client
