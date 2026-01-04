#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Volume Types."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.volume_type_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Volume Types",
    result_field_name="volume_types",
    endpoint_template="/volumes/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-volume-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_volume_type_samples,
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
- List and filter on Volume Types.
module: volume_type_list
notes: []
options:
  count:
    description:
    - The number of Volume Types to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Volume Types.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-volume-types).
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
    - The order to list Volume Types in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Volume Types by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Volume Types.
"""
EXAMPLES = r"""
- name: List all of the Linode Volume Types
  linode.cloud.volume_type_list: {}
- name: List a Linode Volume Type named Storage Volume
  linode.cloud.volume_type_list:
    filters:
    - name: label
      values: Storage Volume
"""
RETURN = r"""
volume_types:
  description: The returned Volume Types.
  elements: dict
  returned: always
  sample:
  - - id: volume
      label: Storage Volume
      price:
        hourly: 0.00015
        monthly: 0.1
      region_prices:
      - hourly: 0.00018
        id: id-cgk
        monthly: 0.12
      - hourly: 0.00021
        id: br-gru
        monthly: 0.14
      transfer: 0
  type: list
"""

if __name__ == "__main__":
    module.run()
