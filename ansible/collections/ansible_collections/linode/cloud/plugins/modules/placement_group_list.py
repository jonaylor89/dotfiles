#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Placement Groups."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    placement_group_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Placement Groups",
    result_field_name="placement_groups",
    endpoint_template="/placement/groups",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-placement-groups",
    result_samples=docs.result_placement_groups_samples,
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
- List and filter on Placement Groups.
module: placement_group_list
notes: []
options:
  count:
    description:
    - The number of Placement Groups to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Placement Groups.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-placement-groups).
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
    - The order to list Placement Groups in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Placement Groups by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Placement Groups.
"""
EXAMPLES = r"""
- name: List all of Linode placement group for the current account
  linode.cloud.placement_group_list:
    api_version: v4beta
"""
RETURN = r"""
placement_groups:
  description: The returned Placement Groups.
  elements: dict
  returned: always
  sample:
  - - id: 123
      is_compliant: true
      label: test
      members:
      - is_compliant: true
        linode_id: 123
      placement_group_policy: strict
      placement_group_type: anti_affinity:local
      region: eu-west
  type: list
"""

if __name__ == "__main__":
    module.run()
