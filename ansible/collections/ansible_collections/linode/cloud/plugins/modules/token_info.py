#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Token."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import PersonalAccessToken

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="token",
        field_type=FieldType.dict,
        display_name="Personal Access Token",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-personal-access-tokens",
        samples=docs_parent.result_token_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                PersonalAccessToken,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.profile.tokens,
                PersonalAccessToken.label == params.get("label"),
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
- Get info about a Linode Personal Access Token.
module: token_info
notes: []
options:
  id:
    description:
    - The ID of the Personal Access Token to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the Personal Access Token to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Personal Access Token.
"""
EXAMPLES = r"""
- name: Get info about a token by label
  linode.cloud.token_info:
    label: my-token
- name: Get info about a token by ID
  linode.cloud.token_info:
    id: 12345
"""
RETURN = r"""
token:
  description: The returned Personal Access Token.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
    expiry: '2018-01-01T13:46:32'
    id: 123
    label: linode-cli
    scopes: '*'
    token: abcdefghijklmnop
  type: dict
"""

if __name__ == "__main__":
    module.run()
