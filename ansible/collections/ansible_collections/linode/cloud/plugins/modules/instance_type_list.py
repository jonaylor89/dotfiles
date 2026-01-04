#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode instance types. Deprecated in favor of type_list."""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    instance_type_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Instance Types",
    result_field_name="instance_types",
    endpoint_template="/linode/types",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-types",
    examples=docs.specdoc_examples,
    result_samples=docs.result_instance_type_samples,
    deprecated=True,
    deprecation_message="This module has been deprecated in favor of `type_list`.",
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
- '**NOTE: This module has been deprecated in favor of `type_list`.**'
- List and filter on Instance Types.
module: instance_type_list
notes: []
options:
  count:
    description:
    - The number of Instance Types to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Instance Types.
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
    - The order to list Instance Types in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Instance Types by.
    required: false
    type: str
requirements:
- python >= 3
short_description: '**NOTE: This module has been deprecated in favor of `type_list`.**
  List and filter on Instance Types.'
"""
EXAMPLES = r"""
- name: List all of the Linode instance types
  linode.cloud.instance_type_list: {}
- name: Resolve all Linode instance types
  linode.cloud.instance_type_list:
    filters:
    - name: class
      values: nanode
"""
RETURN = r"""
instance_types:
  description: The returned Instance Types.
  elements: dict
  returned: always
  sample:
  - - addons:
        backups:
          price:
            hourly: 0.008
            monthly: 5
          region_prices:
          - hourly: 0.02
            id: ap-west
            monthly: 20
          - hourly: 0.02
            id: ap-northeast
            monthly: 20
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
      region_prices:
      - hourly: 0.02
        id: ap-west
        monthly: 20
      - hourly: 0.02
        id: ap-northeast
        monthly: 20
      successor: null
      transfer: 4000
      vcpus: 2
  type: list
"""

if __name__ == "__main__":
    module.run()
