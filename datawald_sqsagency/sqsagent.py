#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

from .sqsagency import SQSAgency


def deploy() -> list:
    return [
        {
            "service": "DataWald",
            "class": "SQSAgent",
            "functions": {
                "retrieve_entities_from_source": {
                    "is_static": False,
                    "label": "sqsagency",
                    "mutation": [],
                    "query": [],
                    "type": "Event",
                    "support_methods": [],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "datawald_agency",
                    "disabled_in_resources": True,  # Ignore adding to resource list.
                },
                "insert_update_entities_to_target": {
                    "is_static": False,
                    "label": "sqsagency",
                    "mutation": [],
                    "query": [],
                    "type": "Event",
                    "support_methods": [],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "datawald_agency",
                    "disabled_in_resources": True,  # Ignore adding to resource list.
                },
                "update_sync_task": {
                    "is_static": False,
                    "label": "sqsagency",
                    "mutation": [],
                    "query": [],
                    "type": "Event",
                    "support_methods": [],
                    "is_auth_required": False,
                    "is_graphql": False,
                    "settings": "datawald_agency",
                    "disabled_in_resources": True,  # Ignore adding to resource list.
                },
            },
        }
    ]


class SQSAgent(SQSAgency):
    def __init__(self, logger, **setting):
        SQSAgency.__init__(self, logger, **setting)
