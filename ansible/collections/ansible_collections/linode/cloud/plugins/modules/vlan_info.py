#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode VLAN info."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vlan_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import VLAN

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="vlan",
        field_type=FieldType.dict,
        display_name="VLAN",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-vlans",
        samples=docs.result_vlan_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                VLAN,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.networking.vlans,
                VLAN.label == params.get("label"),
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
- Get info about a Linode VLAN.
module: vlan_info
notes: []
options:
  id:
    description:
    - The ID of the VLAN to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the VLAN to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode VLAN.
"""
EXAMPLES = r"""
- name: Get info about a VLAN by label
  linode.cloud.vlan_info:
    api_version: v4beta
    label: example-vlan
"""
RETURN = r"""
vlan:
  description: The returned VLAN.
  returned: always
  sample:
  - created: '2020-01-01T00:01:01'
    label: vlan-example
    linodes:
    - 111
    - 222
    region: ap-west
  type: dict
"""

if __name__ == "__main__":
    module.run()
