#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode SSH key."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import SSHKey

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="ssh_key",
        field_type=FieldType.dict,
        display_name="SSH Key",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-ssh-key",
        samples=docs.ssh_key_info_response_sample,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                SSHKey,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.profile.ssh_keys,
                SSHKey.label == params.get("label"),
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
- Get info about a Linode SSH Key.
module: ssh_key_info
notes: []
options:
  id:
    description:
    - The ID of the SSH Key to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the SSH Key to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode SSH Key.
"""
EXAMPLES = r"""
- name: Get info about a SSH key by label
  linode.cloud.ssh_key_info:
    label: my-ssh-key
- name: Get info about a SSH key by ID
  linode.cloud.ssh_key_info:
    id: 12345
"""
RETURN = r"""
ssh_key:
  description: The returned SSH Key.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
    id: 42
    label: My SSH Key
    ssh_key: ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer
  type: dict
"""

if __name__ == "__main__":
    module.run()
