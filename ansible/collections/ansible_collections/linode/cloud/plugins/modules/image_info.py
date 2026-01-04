#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode image."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.image_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Image

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Image",
        field_name="image",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-image",
        samples=docs_parent.result_image_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                Image, params.get("id")
            )._raw_json,
        ),
        InfoModuleAttr(
            name="label",
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.images,
                Image.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
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
- Get info about a Linode Image.
module: image_info
notes: []
options:
  id:
    description:
    - The ID of the Image to resolve.
    required: false
    type: str
  label:
    description:
    - The label of the Image to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Image.
"""
EXAMPLES = r"""
- name: Get info about an image by label
  linode.cloud.image_info:
    label: my-image
- name: Get info about an image by ID
  linode.cloud.image_info:
    id: private/12345
"""
RETURN = r"""
image:
  description: The returned Image.
  returned: always
  sample:
  - capabilities: []
    created: '2021-08-14T22:44:02'
    created_by: my-account
    deprecated: false
    description: Example Image description.
    eol: '2026-07-01T04:00:00'
    expiry: null
    id: private/123
    is_public: true
    label: my-image
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
  type: dict
"""

if __name__ == "__main__":
    module.run()
