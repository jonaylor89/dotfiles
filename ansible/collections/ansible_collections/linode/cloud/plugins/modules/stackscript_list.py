#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode StackScripts."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.stackscript_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="StackScripts",
    result_field_name="stackscripts",
    endpoint_template="/linode/stackscripts",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-stack-scripts",
    examples=docs.specdoc_examples,
    result_samples=docs.result_stackscripts_samples,
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
- List and filter on StackScripts.
module: stackscript_list
notes: []
options:
  count:
    description:
    - The number of StackScripts to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting StackScripts.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-stack-scripts).
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
    - The order to list StackScripts in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order StackScripts by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on StackScripts.
"""
EXAMPLES = r"""
- name: List all of the stackscripts for the current Linode Account
  linode.cloud.stackscript_list: {}
- name: List the latest 5 stackscripts for the current Linode Account
  linode.cloud.stackscript_list:
    count: 5
    order_by: created
    order: desc
- name: List all personal stackscripts for the current Linode Account
  linode.cloud.stackscript_list:
    filters:
    - name: mine
      values: true
"""
RETURN = r"""
stackscripts:
  description: The returned StackScripts.
  elements: dict
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      deployments_active: 1
      deployments_total: 12
      description: 'This StackScript installs and configures MySQL

        '
      id: 10079
      images:
      - linode/debian11
      - linode/debian10
      is_public: true
      label: a-stackscript
      mine: true
      rev_note: Set up MySQL
      script: '"#!/bin/bash"

        '
      updated: '2018-01-01T00:01:01'
      user_defined_fields:
      - default: null
        example: hunter2
        label: Enter the password
        manyOf: avalue,anothervalue,thirdvalue
        name: DB_PASSWORD
        oneOf: avalue,anothervalue,thirdvalue
      user_gravatar_id: a445b305abda30ebc766bc7fda037c37
      username: myuser
  type: list
"""

if __name__ == "__main__":
    module.run()
