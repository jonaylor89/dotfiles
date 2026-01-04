#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Instance Types."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.type_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Types",
    result_field_name="types",
    endpoint_template="/linode/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_type_samples,
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
- List and filter on Types.
module: type_list
notes: []
options:
  count:
    description:
    - The number of Types to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Types.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-linode-types).
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
    - The order to list Types in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Types by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Types.
"""
EXAMPLES = r"""
- name: List all of the Linode Instance Types
  linode.cloud.type_list: {}
- name: List a Linode Instance Type named Nanode 1GB
  linode.cloud.type_list:
    filters:
    - name: label
      values: Nanode 1GB
"""
RETURN = r"""
types:
  description: The returned Types.
  elements: dict
  returned: always
  sample:
  - - addons:
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
  type: list
"""

if __name__ == "__main__":
    module.run()
