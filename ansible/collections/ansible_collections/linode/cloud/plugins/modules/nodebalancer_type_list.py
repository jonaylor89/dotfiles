#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Node Balancer Types."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_type_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Node Balancer Types",
    result_field_name="nodebalancer_types",
    endpoint_template="/nodebalancers/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_nodebalancer_type_samples,
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
- List and filter on Node Balancer Types.
module: nodebalancer_type_list
notes: []
options:
  count:
    description:
    - The number of Node Balancer Types to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Node Balancer Types.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-node-balancer-types).
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
    - The order to list Node Balancer Types in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Node Balancer Types by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Node Balancer Types.
"""
EXAMPLES = r"""
- name: List all of the Linode Node Balancer Types
  linode.cloud.nodebalancer_type_list: {}
- name: List a Linode Node Balancer Type named NodeBalancer
  linode.cloud.nodebalancer_type_list:
    filters:
    - name: label
      values: NodeBalancer
"""
RETURN = r"""
nodebalancer_types:
  description: The returned Node Balancer Types.
  elements: dict
  returned: always
  sample:
  - - id: nodebalancer
      label: NodeBalancer
      price:
        hourly: 0.015
        monthly: 10.0
      region_prices:
      - hourly: 0.018
        id: id-cgk
        monthly: 12.0
      - hourly: 0.021
        id: br-gru
        monthly: 14.0
      transfer: 0
  type: list
"""

if __name__ == "__main__":
    module.run()
