#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing IP addresses of all VPCs."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpcs_ip_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="all VPC IP Addresses",
    result_field_name="vpcs_ips",
    endpoint_template="/vpcs/ips",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpcs-ips",
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
- List and filter on all VPC IP Addresses.
module: vpcs_ip_list
notes: []
options:
  count:
    description:
    - The number of all VPC IP Addresses to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting all VPC IP Addresses.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-vpcs-ips).
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
    - The order to list all VPC IP Addresses in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order all VPC IP Addresses by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on all VPC IP Addresses.
"""
EXAMPLES = r"""
- name: List all IPs of all VPCs in the account.
  linode.cloud.vpcs_ip_list: {}
"""
RETURN = r"""
vpcs_ips:
  description: The returned all VPC IP Addresses.
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
