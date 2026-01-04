#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode images."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Images",
    result_field_name="images",
    endpoint_template="/images",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-images",
    result_samples=docs.result_images_samples,
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
- List and filter on Images.
module: image_list
notes: []
options:
  count:
    description:
    - The number of Images to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Images.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-images).
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
    - The order to list Images in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Images by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Images.
"""
EXAMPLES = r"""
- name: List all of the images for the current Linode Account
  linode.cloud.image_list: {}
- name: List the latest 5 images for the current Linode Account
  linode.cloud.image_list:
    count: 5
    order_by: created
    order: desc
- name: Resolve all Alpine Linux images
  linode.cloud.image_list:
    filters:
    - name: vendor
      values: Alpine
"""
RETURN = r"""
images:
  description: The returned Images.
  elements: dict
  returned: always
  sample:
  - - created: '2021-08-14T22:44:02'
      created_by: my-account
      deprecated: false
      description: Example Image description.
      eol: '2026-07-01T04:00:00'
      expiry: null
      id: private/123
      is_public: false
      label: test
      regions:
      - region: us-east
        status: available
      - region: us-central
        status: pending
      size: 2500
      status: null
      tags:
      - test
      total_size: 5000
      type: manual
      updated: '2021-08-14T22:44:02'
      vendor: Debian
  type: list
"""

if __name__ == "__main__":
    module.run()
