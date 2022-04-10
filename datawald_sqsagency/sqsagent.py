#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from .sqsagency import SQSAgency


class SQSAgent(SQSAgency):
    def __init__(self, logger, **setting):
        SQSAgency.__init__(self, logger, **setting)
