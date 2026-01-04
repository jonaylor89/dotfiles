#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Region."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.region as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.region_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Region

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Region",
        field_name="region",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-region",
        samples=docs_parent.result_region_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                Region, params.get("id")
            )._raw_json,
        ),
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
- Get info about a Linode Region.
module: region_info
notes: []
options:
  id:
    description:
    - The ID of the Region to resolve.
    required: true
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Region.
"""
EXAMPLES = r"""
- name: Get Info of a Linode Region
  linode.cloud.region_info:
    id: us-mia
"""
RETURN = r"""
region:
  description: The returned Region.
  returned: always
  sample:
  - capabilities:
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
    - Placement Group
    country: us
    id: us-mia
    label: Miami, FL
    placement_group_limits:
      maximum_linodes_per_pg: 5
      maximum_pgs_per_customer: null
    resolvers:
      ipv4: 172.233.160.34, 172.233.160.27, 172.233.160.30, 172.233.160.29, 172.233.160.32,
        172.233.160.28, 172.233.160.33, 172.233.160.26, 172.233.160.25, 172.233.160.31
      ipv6: 2a01:7e04::f03c:93ff:fead:d31f, 2a01:7e04::f03c:93ff:fead:d37f, 2a01:7e04::f03c:93ff:fead:d30c,
        2a01:7e04::f03c:93ff:fead:d318, 2a01:7e04::f03c:93ff:fead:d316, 2a01:7e04::f03c:93ff:fead:d339,
        2a01:7e04::f03c:93ff:fead:d367, 2a01:7e04::f03c:93ff:fead:d395, 2a01:7e04::f03c:93ff:fead:d3d0,
        2a01:7e04::f03c:93ff:fead:d38e
    site_type: core
    status: ok
  type: dict
"""

if __name__ == "__main__":
    module.run()
