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

        self.map = setting.get("TXMAP", {})

    def tx_transactions_src(self, **kwargs):
        try:
            raw_transactions = kwargs.pop("messages")
            transactions = list(
                map(
                    lambda raw_transaction: self.tx_transaction_src(
                        raw_transaction, **kwargs
                    ),
                    raw_transactions,
                )
            )

            return transactions
        except Exception:
            log = traceback.format_exc()
            self.logger.exception(log)
            raise

    def tx_transaction_src(self, raw_transaction, **kwargs):
        tx_type = kwargs.get("tx_type")
        transaction = {
            "src_id": raw_transaction[self.setting["src_metadata"][tx_type]["src_id"]],
            "created_at": datetime.strptime(
                raw_transaction[self.setting["src_metadata"][tx_type]["created_at"]],
                "%Y-%m-%d %H:%M:%S",
            ),
            "updated_at": datetime.strptime(
                raw_transaction[self.setting["src_metadata"][tx_type]["updated_at"]],
                "%Y-%m-%d %H:%M:%S",
            ),
        }
        try:
            transaction.update(
                {"data": self.transform_data(raw_transaction, self.map.get(tx_type))}
            )
        except Exception:
            log = traceback.format_exc()
            transaction.update({"tx_status": "F", "tx_note": log})
            self.logger.exception(log)

        return transaction

    def tx_assets_src(self, **kwargs):
        raw_assets = kwargs.pop("messages")
        assets = list(
            map(lambda raw_asset: self.tx_asset_src(raw_asset, **kwargs), raw_assets)
        )

        return assets

    def tx_asset_src(self, raw_asset, **kwargs):
        tx_type = kwargs.get("tx_type")
        asset = {
            "src_id": raw_asset[self.setting["src_metadata"][tx_type]["src_id"]],
            "created_at": raw_asset[
                self.setting["src_metadata"][tx_type]["created_at"]
            ],
            "updated_at": raw_asset[
                self.setting["src_metadata"][tx_type]["updated_at"]
            ],
        }
        try:
            if tx_type == "product":
                metadatas = self.get_product_metadatas(**kwargs)
                asset.update({"data": self.transform_data(raw_asset, metadatas)})
        except Exception:
            log = traceback.format_exc()
            asset.update({"tx_status": "F", "tx_note": log})
            self.logger.exception(log)

        return asset
