#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to view Nodebalancer Stats."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_stats as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import NodeBalancer

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="node_balancer_stats",
        field_type=FieldType.dict,
        display_name="Node Balancer Stats",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-stats",
        samples=docs.result_nodebalancer_stats_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                NodeBalancer,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.nodebalancers,
                NodeBalancer.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
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
- Get info about a Linode Node Balancer Stats.
module: nodebalancer_stats
notes: []
options:
  id:
    description:
    - The ID of the Node Balancer Stats to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the Node Balancer Stats to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Node Balancer Stats.
"""
EXAMPLES = r"""
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given id
  linode.cloud.nodebalancer_stats:
    id: 12345
- name: List all of the Nodebalancer Stats for the Nodebalancer with the given label
  linode.cloud.nodebalancer_stats:
    label: example_label
"""
RETURN = r"""
node_balancer_stats:
  description: The returned Node Balancer Stats.
  returned: always
  sample:
  - - connections:
      - 1679586600000
      - 0
      title: sample-title
      traffic:
        in:
        - 1679586600000
        - 0
        out:
        - 1679586600000
        - 0
  type: dict
"""

if __name__ == "__main__":
    module.run()
