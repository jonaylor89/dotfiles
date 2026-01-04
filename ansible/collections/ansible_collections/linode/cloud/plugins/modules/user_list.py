#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Users."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Users",
    result_field_name="users",
    endpoint_template="/account/users",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-users",
    examples=docs.specdoc_examples,
    result_samples=docs.result_users_samples,
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
- List and filter on Users.
module: user_list
notes: []
options:
  count:
    description:
    - The number of Users to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Users.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-users).
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
    - The order to list Users in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Users by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Users.
"""
EXAMPLES = r"""
- name: List all of the users for the current Linode Account
  linode.cloud.user_list: {}
"""
RETURN = r"""
users:
  description: The returned Users.
  elements: dict
  returned: always
  sample:
  - - email: example_user@linode.com
      restricted: true
      ssh_keys:
      - home-pc
      - laptop
      tfa_enabled: null
      user_type: default
      username: example_user
  type: list
"""

if __name__ == "__main__":
    module.run()
