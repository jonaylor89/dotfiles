#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Type."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.type_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import LinodeClient, Type


def _get_by_id(client: LinodeClient, params: Dict[str, Any]) -> None:
    """
    This function is intended to be passed into the ID get attribute.

    NOTE: This is not implemented as a lambda because Type currently does not work with
    client.load().
    """
    inst_type = Type(client, params.get("id"))
    inst_type._api_get()
    return inst_type._raw_json


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="type",
        field_type=FieldType.dict,
        display_name="Type",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-type",
        samples=docs.result_type_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.string,
            get=_get_by_id,
        )
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
- Get info about a Linode Type.
module: type_info
notes: []
options:
  id:
    description:
    - The ID of the Type to resolve.
    required: true
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Type.
"""
EXAMPLES = r"""
- name: Get info about a Linode type by ID
  linode.cloud.type_info:
    id: g6-standard-2
"""
RETURN = r"""
type:
  description: The returned Type.
  returned: always
  sample:
  - addons:
      backups:
        price:
          hourly: 0.008
          monthly: 5
    class: standard
    disk: 81920
    gpus: 0
    id: g6-standard-2
    label: Linode 4GB
    memory: 4096
    network_out: 1000
    price:
      hourly: 0.03
      monthly: 20
    successor: null
    transfer: 4000
    vcpus: 2
  type: dict
"""

if __name__ == "__main__":
    module.run()
