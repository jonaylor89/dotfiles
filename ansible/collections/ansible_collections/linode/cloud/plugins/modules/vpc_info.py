#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode VPC Subnet."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import VPC

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="vpc",
        field_type=FieldType.dict,
        display_name="VPC",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc",
        samples=docs_parent.result_vpc_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                VPC,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.vpcs,
                VPC.label == params.get("label"),
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
- Get info about a Linode VPC.
module: vpc_info
notes: []
options:
  id:
    description:
    - The ID of the VPC to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the VPC to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode VPC.
"""
EXAMPLES = r"""
- name: Get info about a VPC by label
  linode.cloud.vpc_info:
    label: my-vpc
- name: Get info about a VPC by ID
  linode.cloud.vpc_info:
    id: 12345
"""
RETURN = r"""
vpc:
  description: The returned VPC.
  returned: always
  sample:
  - created: '2023-08-31T18:35:01'
    description: A description of this VPC
    id: 344
    label: my-vpc
    region: us-east
    subnets: []
    updated: '2023-08-31T18:35:03'
  type: dict
"""

if __name__ == "__main__":
    module.run()
