#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Object Storage Quotas."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_quota_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)


def custom_api_filter_constructor(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Customize a filter string for listing Object Storage Quota,
    because only a single basic filterable parameter can be supported currently by API.
    """
    if params.get("order_by") is not None or params.get("order") is not None:
        module.warn(
            "order or order_by is currently not supported in listing object_storage_quotas, "
            "and will be ignored if provided. "
            "Please refer to the API documentation for more information."
        )

    filters = params.get("filters")

    if filters is not None:
        if len(filters) == 1 and len(filters[0]["values"]) == 1:
            return {filters[0]["name"]: filters[0]["values"][0]}
        module.fail(
            "[error] The filter is not acceptable. "
            "Only a single filterable parameter can be supported currently by API. "
            "The filterable fields are limited. "
            "Please refer to the API documentation for more information."
        )

    return {}


module = ListModule(
    result_display_name="Object Storage Quotas",
    result_field_name="object_storage_quotas",
    endpoint_template="/object-storage/quotas",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-quotas",
    result_samples=docs.result_object_storage_quotas_samples,
    examples=docs.specdoc_examples,
    custom_api_filter_constructor=custom_api_filter_constructor,
)

SPECDOC_META = module.spec

DOCUMENTATION = r"""
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
- Zhiwei Liang (@zliang)
- Ye Chen (@yechen)
- Youjung Kim (@ykim)
- Vinay Shanthegowda (@vshanthe)
- Erik Zilber (@ezilber)
description:
- List and filter on Object Storage Quotas.
module: object_storage_quota_list
notes: []
options:
  count:
    description:
    - The number of Object Storage Quotas to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Object Storage Quotas.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-object-storage-quotas).
        required: true
        type: str
      values:
        description:
        - A list of values to allow for this field.
        - Fields will pass this filter if at least one of these values matches.
        elements: str
        required: true
        type: list
    type: list
  order:
    choices:
    - desc
    - asc
    default: asc
    description:
    - The order to list Object Storage Quotas in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Object Storage Quotas by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Object Storage Quotas.
"""
EXAMPLES = r"""
- name: List all of Object Storage Quotas for the current account
  linode.cloud.object_storage_quotas:
    filters:
    - name: s3_endpoint
      values:
      - es-mad-1.linodeobjects.com
"""
RETURN = r"""
object_storage_quotas:
  description: The returned Object Storage Quotas.
  elements: dict
  returned: always
  sample:
  - - description: Maximum number of buckets this customer is allowed to have on this
        endpoint
      endpoint_type: E1
      quota_id: obj-buckets-es-mad-1.linodeobjects.com
      quota_limit: 1000
      quota_name: Number of Buckets
      resource_metric: bucket
      s3_endpoint: es-mad-1.linodeobjects.com
    - description: Maximum number of bytes this customer is allowed to have on this
        endpoint
      endpoint_type: E1
      quota_id: obj-bytes-es-mad-1.linodeobjects.com
      quota_limit: 109951162777600
      quota_name: Total Capacity
      resource_metric: byte
      s3_endpoint: es-mad-1.linodeobjects.com
  type: list
"""

if __name__ == "__main__":
    module.run()
