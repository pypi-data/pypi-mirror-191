# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 12:52:00 2023

@author: yqlim
"""
import logging
logger = logging.getLogger(__name__)

import uuid

class RequestForQuote(object):
    def __init__(self, requestor: str = '', request_id: str = '') -> None:
        self.requestor = requestor
        if request_id:
            self.request_id = request_id
        else:
            self.request_id = uuid.uuid4()

class Option(object):
    def __init__(self, option_id: str = '') -> None:
        if option_id:
            self.option_id = option_id
        else:
            self.option_id = uuid.uuid4()

class Order(object):
    def __init__(self):
        pass