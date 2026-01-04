#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode VPCs."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="VPCs",
    result_field_name="vpcs",
    endpoint_template="/vpcs",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpcs",
    examples=docs.specdoc_examples,
    result_samples=docs.result_vpc_samples,
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
- List and filter on VPCs.
module: vpc_list
notes: []
options:
  count:
    description:
    - The number of VPCs to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting VPCs.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpcs).
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
    - The order to list VPCs in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order VPCs by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on VPCs.
"""
EXAMPLES = r"""
- name: List all of the VPCs for the current user
  linode.cloud.vpc_list: {}
- name: List all of the VPCS for the current user with the given label
  linode.cloud.vpc_list:
    filters:
    - name: label
      values: my-vpc
"""
RETURN = r"""
vpcs:
  description: The returned VPCs.
  elements: dict
  returned: always
  sample:
  - - created: '2023-08-31T18:35:01'
      description: A description of this VPC
      id: 344
      label: my-vpc
      region: us-east
      subnets: []
      updated: '2023-08-31T18:35:03'
  type: list
"""

if __name__ == "__main__":
    module.run()
