#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing IP addresses of a VPC."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_ip_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
    ListModuleParam,
)
from ansible_specdoc.objects import FieldType

module = ListModule(
    result_display_name="VPC IP Addresses",
    result_field_name="vpcs_ips",
    endpoint_template="/vpcs/{vpc_id}/ips",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc-ips",
    examples=docs.specdoc_examples,
    result_samples=docs.result_vpc_ip_view_samples,
    params=[
        ListModuleParam(
            display_name="VPC",
            name="vpc_id",
            type=FieldType.integer,
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
- List and filter on VPC IP Addresses.
module: vpc_ip_list
notes: []
options:
  count:
    description:
    - The number of VPC IP Addresses to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting VPC IP Addresses.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpc-ips).
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
    - The order to list VPC IP Addresses in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order VPC IP Addresses by.
    required: false
    type: str
  vpc_id:
    description:
    - The parent VPC for the VPC IP Addresses.
    required: true
    type: int
requirements:
- python >= 3
short_description: List and filter on VPC IP Addresses.
"""
EXAMPLES = r"""
- name: List all IPs of a specific VPC.
  linode.cloud.vpc_ip_list:
    vpc_id: 12345
"""
RETURN = r"""
vpcs_ips:
  description: The returned VPC IP Addresses.
  elements: dict
  returned: always
  sample:
  - - active: false
      address: 10.0.0.2
      address_range: null
      config_id: 60480976
      gateway: 10.0.0.1
      interface_id: 1373818
      linode_id: 57328104
      nat_1_1: null
      prefix: 24
      region: us-mia
      subnet_id: 55829
      subnet_mask: 255.255.255.0
      vpc_id: 56242
  type: list
"""

if __name__ == "__main__":
    module.run()
