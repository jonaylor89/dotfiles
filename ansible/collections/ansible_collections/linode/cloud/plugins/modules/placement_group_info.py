#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Placement Group info."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    placement_group_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import PlacementGroup

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Placement Group",
        field_name="placement_group",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-placement-group",
        samples=docs.result_placement_group_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                PlacementGroup, params.get("id")
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
- Get info about a Linode Placement Group.
module: placement_group_info
notes: []
options:
  id:
    description:
    - The ID of the Placement Group to resolve.
    required: true
    type: int
requirements:
- python >= 3
short_description: Get info about a Linode Placement Group.
"""
EXAMPLES = r"""
- name: Get info about a Linode placement group
  linode.cloud.placement_group_info:
    api_version: v4beta
    id: 123
"""
RETURN = r"""
placement_group:
  description: The returned Placement Group.
  returned: always
  sample:
  - id: 123
    is_compliant: true
    label: test
    members:
    - is_compliant: true
      linode_id: 123
    placement_group_policy: strict
    placement_group_type: anti_affinity:local
    region: eu-west
  type: dict
"""

if __name__ == "__main__":
    module.run()
