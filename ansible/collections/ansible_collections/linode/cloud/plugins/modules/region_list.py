#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode regions."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.region_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Regions",
    result_field_name="regions",
    endpoint_template="/regions",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-regions",
    examples=docs.specdoc_examples,
    result_samples=docs.result_regions_samples,
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
- List and filter on Regions.
module: region_list
notes: []
options:
  count:
    description:
    - The number of Regions to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Regions.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-regions).
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
    - The order to list Regions in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Regions by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Regions.
"""
EXAMPLES = r"""
- name: List all of the Linode regions
  linode.cloud.region_list: {}
- name: Filtered Linode regions
  linode.cloud.region_list:
    filters:
    - name: site_type
      values: core
"""
RETURN = r"""
regions:
  description: The returned Regions.
  elements: dict
  returned: always
  sample:
  - - capabilities:
      - Linodes
      - Backups
      - NodeBalancers
      - Block Storage
      - Object Storage
      - Kubernetes
      - Cloud Firewall
      - Vlans
      - VPCs
      - Metadata
      - Premium Plans
      country: us
      id: us-mia
      label: Miami, FL
      resolvers:
        ipv4: 172.233.160.34, 172.233.160.27
        ipv6: 2a01:7e04::f03c:93ff:fead:d31f, 2a01:7e04::f03c:93ff:fead:d37f
      site_type: core
      status: ok
  type: list
"""

if __name__ == "__main__":
    module.run()
