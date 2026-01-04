#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode VPC Subnet."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.vpc_subnet_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import VPC, LinodeClient, VPCSubnet


def _subnet_by_label(
    client: LinodeClient, params: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Gets a subnet with the given params using the `label` attribute.
    """

    label = params.get("label")
    vpc = client.load(VPC, params.get("vpc_id"))
    return safe_find(
        lambda: [v for v in vpc.subnets if v.label == label],
        raise_not_found=True,
    )._raw_json


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="subnet",
        field_type=FieldType.dict,
        display_name="VPC Subnet",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-vpc-subnet",
        samples=docs_parent.result_subnet_samples,
    ),
    params=[
        InfoModuleParam(
            display_name="VPC", name="vpc_id", type=FieldType.integer
        )
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                VPCSubnet,
                params.get("id"),
                target_parent_id=params.get("vpc_id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=_subnet_by_label,
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
- Get info about a Linode VPC Subnet.
module: vpc_subnet_info
notes: []
options:
  id:
    description:
    - The ID of the VPC Subnet to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the VPC Subnet to resolve.
    required: false
    type: str
  vpc_id:
    description:
    - The ID of the VPC for this resource.
    required: true
    type: int
requirements:
- python >= 3
short_description: Get info about a Linode VPC Subnet.
"""
EXAMPLES = r"""
- name: Get info about a VPC Subnet by label
  linode.cloud.vpc_subnet_info:
    vpc_id: 12345
    label: my-subnet
- name: Get info about a VPC Subnet by ID
  linode.cloud.vpc_subnet_info:
    vpc_id: 12345
    id: 123
"""
RETURN = r"""
subnet:
  description: The returned VPC Subnet.
  returned: always
  sample:
  - created: '2023-08-31T18:53:04'
    id: 271
    ipv4: 10.0.0.0/24
    label: test-subnet
    linodes:
    - id: 1234567
      interfaces:
      - active: false
        id: 654321
    updated: '2023-08-31T18:53:04'
  type: dict
"""

if __name__ == "__main__":
    module.run()
