#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode tokens."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.token_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Tokens",
    result_field_name="tokens",
    endpoint_template="/profile/tokens",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-personal-access-tokens",
    examples=docs.specdoc_examples,
    result_samples=docs.result_tokens_samples,
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
- List and filter on Tokens.
module: token_list
notes: []
options:
  count:
    description:
    - The number of Tokens to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Tokens.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-personal-access-tokens).
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
    - The order to list Tokens in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Tokens by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Tokens.
"""
EXAMPLES = r"""
- name: List all of the Personal Access Tokens active for the current user
  linode.cloud.token_list: {}
- name: Resolve all of the Personal Access Tokens active for the current user
  linode.cloud.token_list:
    filters:
    - name: label
      values: myTokenLabel
"""
RETURN = r"""
tokens:
  description: The returned Tokens.
  elements: dict
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      expiry: '2018-01-01T13:46:32'
      id: 123
      label: linode-cli
      scopes: '*'
      token: abcdefghijklmnop
  type: list
"""

if __name__ == "__main__":
    module.run()
