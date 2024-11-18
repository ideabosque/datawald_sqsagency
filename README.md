# Datawald SQSAgency

The `datawald_sqsagency` module serves as a critical element of the DataWald integration framework, designed to leverage AWS SQS for seamless triggering and efficient data operations. This module ensures reliable data transformation, retrieval, and insertion, enabling a smooth and integrated data flow within the AWS ecosystem.

## Configuration Guide

The `datawald_sqsagency` module integrates Amazon SQS for message-driven communication. This guide outlines the step-by-step process to configure `datawald_sqsagency` using the `se-configdata` table in DynamoDB, ensuring a streamlined setup and optimized performance.

---

### Source Metadata

Define the metadata structure required for retrieving and synchronizing data from various sources. Below is an example configuration:

```json
{
  "setting_id": "datawald_sqsagency",
  "variable": "src_metadata",
  "value": {
    "hubspot": {
      "contact": {
        "created_at": "created_at",
        "src_id": "id",
        "updated_at": "updated_at"
      },
      "order": {
        "created_at": "created_at",
        "src_id": "entity_id",
        "updated_at": "updated_at"
      },
      "product": {
        "created_at": "created_at",
        "src_id": "entity_id",
        "updated_at": "updated_at"
      }
    },
    "ns": {
      "customer": {
        "created_at": "created_at",
        "src_id": "ext_customer_id",
        "updated_at": "updated_at"
      },
      "opportunity": {
        "created_at": "created_at",
        "src_id": "oppo_id",
        "updated_at": "updated_at"
      },
      "order": {
        "created_at": "created_at",
        "src_id": "order_id",
        "updated_at": "updated_at"
      },
      "quote": {
        "created_at": "created_at",
        "src_id": "quote_id",
        "updated_at": "updated_at"
      },
      "rma": {
        "created_at": "created_at",
        "src_id": "rma_id",
        "updated_at": "updated_at"
      }
    }
  }
}
```

This structure defines the source metadata for multiple platforms, ensuring seamless integration and synchronization.

---

### Transformation Data Mapping

Set up transformation rules for data mapping in DynamoDB. These rules enable dynamic and flexible data transformations for SQS integration:

```json
{
  "setting_id": "datawald_sqsagency",
  "variable": "TXMAP",
  "value": {
    "hubspot": {
      "contact": {
        "email": {
          "funct": "src['email']",
          "src": [
            {
              "key": "email",
              "label": "email"
            }
          ],
          "type": "attribute"
        },
        "city": {
          "funct": "src['billing_address']['city'] if src.get('billing_address', None) else ''",
          "src": [
            {
              "key": "billing_address",
              "label": "billing_address"
            }
          ],
          "type": "attribute"
        },
        "company": {
          "funct": "src['company_name']",
          "src": [
            {
              "key": "company_name",
              "label": "company_name"
            }
          ],
          "type": "attribute"
        }
      },
      "order": {
        "amount": {
          "funct": "str(src['grand_total']) if src['grand_total'] else None",
          "src": [
            {
              "key": "grand_total",
              "label": "grand_total"
            }
          ],
          "type": "attribute"
        },
        "billing_address": {
          "funct": "';'.join(src.get('billing_address', [])) if src['billing_address'] else ''",
          "src": [
            {
              "key": "billing_address",
              "label": "billing_address"
            }
          ],
          "type": "attribute"
        }
      }
    }
  }
}
```

### Key Features:
1. **Dynamic Data Transformation**: Customize data processing using flexible function mappings.
2. **Comprehensive Source-Target Alignment**: Map attributes across systems for seamless synchronization.
3. **Message-Oriented Integration**: Integrate with SQS for reliable and scalable message-based communication.

