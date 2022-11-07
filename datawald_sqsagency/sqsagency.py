#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

__author__ = "bibow"

import traceback
from datetime import datetime
from datawald_agency import Agency
from datawald_connector import DatawaldConnector
from sqs_connector import SQSConnector


class SQSAgency(Agency):
    def __init__(self, logger, **setting):
        self.logger = logger
        self.setting = setting
        self.sqsconnector = SQSConnector(logger, **setting)
        self.datawald = DatawaldConnector(logger, **setting)
        Agency.__init__(self, logger, datawald=self.datawald)
        if setting.get("tx_type"):
            Agency.tx_type = setting.get("tx_type")

        self.map = setting.get("TXMAP", {})

    def tx_entities_src(self, **kwargs):
        try:
            raw_entities = kwargs.pop("messages")
            entities = list(
                map(
                    lambda raw_entity: self.tx_entity_src(raw_entity, **kwargs),
                    raw_entities,
                )
            )

            return entities
        except Exception:
            log = traceback.format_exc()
            self.logger.exception(log)
            raise

    def tx_entity_src(self, raw_entity, **kwargs):
        tx_type = kwargs.get("tx_type")
        target = kwargs.get("target")
        entity = {
            "src_id": raw_entity[self.setting["src_metadata"][target][tx_type]["src_id"]],
            "created_at": raw_entity[
                self.setting["src_metadata"][target][tx_type]["created_at"]
            ],
            "updated_at": raw_entity[
                self.setting["src_metadata"][target][tx_type]["updated_at"]
            ],
        }

        if type(entity["created_at"]) == str:
            entity["created_at"] = datetime.strptime(
                entity["created_at"], "%Y-%m-%dT%H:%M:%S%z"
            )
        if type(entity["updated_at"]) == str:
            entity["updated_at"] = datetime.strptime(
                entity["updated_at"], "%Y-%m-%dT%H:%M:%S%z"
            )

        try:
            if tx_type == "product":
                metadatas = self.get_product_metadatas(**kwargs)
                entity.update({"data": self.transform_data(raw_entity, metadatas)})
            else:
                entity.update(
                    {"data": self.transform_data(raw_entity, self.map[target].get(tx_type))}
                )
        except Exception:
            log = traceback.format_exc()
            entity.update({"tx_status": "F", "tx_note": log})
            self.logger.exception(log)

        return entity

    def tx_transactions_src(self, **kwargs):
        return self.tx_entities_src(**kwargs)

    def tx_persons_src(self, **kwargs):
        return self.tx_entities_src(**kwargs)

    def tx_assets_src(self, **kwargs):
        return self.tx_entities_src(**kwargs)
