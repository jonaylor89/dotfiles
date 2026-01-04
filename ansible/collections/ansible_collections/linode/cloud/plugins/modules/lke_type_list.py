#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode LKE Types."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.lke_type_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="LKE Types",
    result_field_name="lke_types",
    endpoint_template="/lke/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_lke_type_samples,
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
- List and filter on LKE Types.
module: lke_type_list
notes: []
options:
  count:
    description:
    - The number of LKE Types to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting LKE Types.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-lke-types).
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
    - The order to list LKE Types in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order LKE Types by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on LKE Types.
"""
EXAMPLES = r"""
- name: List all of the Linode LKE Types
  linode.cloud.lke_type_list: {}
- name: List a Linode LKE Type named LKE High Availability
  linode.cloud.lke_type_list:
    filters:
    - name: label
      values: LKE High Availability
"""
RETURN = r"""
lke_types:
  description: The returned LKE Types.
  elements: dict
  returned: always
  sample:
  - - id: lke-ha
      label: LKE High Availability
      price:
        hourly: 0.09
        monthly: 60.0
      region_prices:
      - hourly: 0.108
        id: id-cgk
        monthly: 72.0
      - hourly: 0.126
        id: br-gru
        monthly: 84.0
      transfer: 0
  type: list
"""

if __name__ == "__main__":
    module.run()
