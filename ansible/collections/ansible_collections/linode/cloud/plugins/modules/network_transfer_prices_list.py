#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Network Transfer Prices."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    network_transfer_prices_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Network Transfer Prices",
    result_field_name="network_transfer_prices",
    endpoint_template="/network-transfer/prices",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-network-transfer-prices",
    examples=docs.specdoc_examples,
    result_samples=docs.result_network_transfer_prices_samples,
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
- List and filter on Network Transfer Prices.
module: network_transfer_prices_list
notes: []
options:
  count:
    description:
    - The number of Network Transfer Prices to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Network Transfer Prices.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-network-transfer-prices).
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
    - The order to list Network Transfer Prices in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Network Transfer Prices by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Network Transfer Prices.
"""
EXAMPLES = r"""
- name: List all of the Linode Network Transfer Prices
  linode.cloud.network_transfer_prices_list: {}
- name: List a Linode Network Transfer Price named Distributed Network Transfer
  linode.cloud.network_transfer_prices_list:
    filters:
    - name: label
      values: Distributed Network Transfer
"""
RETURN = r"""
network_transfer_prices:
  description: The returned Network Transfer Prices.
  elements: dict
  returned: always
  sample:
  - - id: distributed_network_transfer
      label: Distributed Network Transfer
      price:
        hourly: 0.01
        monthly: null
      region_prices: []
      transfer: 0
  type: list
"""

if __name__ == "__main__":
    module.run()
