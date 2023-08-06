#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Connect to a local MongoDB instance  """


from pymongo import MongoClient

from baseblock import BaseObject


class MongoLocalConnector(BaseObject):
    """ Connect to a local MongoDB instance 

    Reference:
        https://github.com/craigtrim/mongodb-cloud-helper/issues/1
    """

    def __init__(self):
        """ Change Log

        Created:
            11-Feb-2023
            craigtrim@gmail.com
            *   https://github.com/craigtrim/mongodb-cloud-helper/issues/1
        """
        BaseObject.__init__(self, __name__)
        self._client = MongoClient()

    def client(self) -> MongoClient:
        return self._client
