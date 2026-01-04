#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the functionality for listing subnets under a VPC."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="VPC Subnets",
    result_field_name="subnets",
    endpoint_template="/vpcs/{vpc_id}/subnets",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc-subnets",
    result_samples=docs.result_vpc_samples,
    examples=docs.specdoc_examples,
    params=[
        ListModuleParam(
            display_name="VPC", name="vpc_id", type=FieldType.integer
        )
    ],
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
- List and filter on VPC Subnets.
module: vpc_subnet_list
notes: []
options:
  count:
    description:
    - The number of VPC Subnets to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting VPC Subnets.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpc-subnets).
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
    - The order to list VPC Subnets in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order VPC Subnets by.
    required: false
    type: str
  vpc_id:
    description:
    - The parent VPC for the VPC Subnets.
    required: true
    type: int
requirements:
- python >= 3
short_description: List and filter on VPC Subnets.
"""
EXAMPLES = r"""
- name: List all of the subnets under a VPC
  linode.cloud.vpc_subnet_list:
    vpc_id: 12345
- name: List all of the subnets with a given label under a VPC
  linode.cloud.vpc_subnet_list:
    vpc_id: 12345
    filters:
    - name: label
      values: my-subnet
"""
RETURN = r"""
subnets:
  description: The returned VPC Subnets.
  elements: dict
  returned: always
  sample:
  - - created: '2023-08-31T18:53:04'
      id: 271
      ipv4: 10.0.0.0/24
      label: test-subnet
      linodes:
      - id: 1234567
        interfaces:
        - active: false
          id: 654321
      updated: '2023-08-31T18:53:04'
  type: list
"""

if __name__ == "__main__":
    module.run()
