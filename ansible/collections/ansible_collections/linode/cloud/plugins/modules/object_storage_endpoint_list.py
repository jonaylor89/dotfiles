#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file implements the linode.cloud.object_storage_endpoints_list module."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_endpoint_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Object Storage Endpoints",
    result_field_name="endpoints",
    endpoint_template="/object-storage/endpoints",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-endpoints",
    examples=docs.specdoc_examples,
    result_samples=docs.result_endpoints_sample,
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
- List and filter on Object Storage Endpoints.
module: object_storage_endpoint_list
notes: []
options:
  count:
    description:
    - The number of Object Storage Endpoints to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Object Storage Endpoints.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-object-storage-endpoints).
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
    - The order to list Object Storage Endpoints in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Object Storage Endpoints by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Object Storage Endpoints.
"""
EXAMPLES = r"""
- name: List all available Object Storage Endpoints
  linode.cloud.object_storage_endpoint_list: {}
"""
RETURN = r"""
endpoints:
  description: The returned Object Storage Endpoints.
  elements: dict
  returned: always
  sample:
  - - endpoint_type: E0
      region: us-southeast
      s3_endpoint: us-southeast-1.linodeobjects.com
    - endpoint_type: E0
      region: us-east
      s3_endpoint: us-east-1.linodeobjects.com
    - endpoint_type: E1
      region: us-iad
      s3_endpoint: us-iad-1.linodeobjects.com
    - endpoint_type: E1
      region: us-mia
      s3_endpoint: us-mia-1.linodeobjects.com
    - endpoint_type: E1
      region: fr-par
      s3_endpoint: fr-par-1.linodeobjects.com
    - endpoint_type: E3
      region: gb-lon
      s3_endpoint: gb-lon-1.linodeobjects.com
    - endpoint_type: E2
      region: sg-sin-2
      s3_endpoint: sg-sin-1.linodeobjects.com
    - endpoint_type: E1
      region: us-ord
      s3_endpoint: us-ord-1.linodeobjects.com
    - endpoint_type: E1
      region: us-sea
      s3_endpoint: us-sea-1.linodeobjects.com
    - endpoint_type: E2
      region: au-mel
      s3_endpoint: au-mel-1.linodeobjects.com
    - endpoint_type: E1
      region: id-cgk
      s3_endpoint: id-cgk-1.linodeobjects.com
    - endpoint_type: E1
      region: in-maa
      s3_endpoint: in-maa-1.linodeobjects.com
    - endpoint_type: E1
      region: se-sto
      s3_endpoint: se-sto-1.linodeobjects.com
    - endpoint_type: E1
      region: it-mil
      s3_endpoint: it-mil-1.linodeobjects.com
    - endpoint_type: E1
      region: jp-osa
      s3_endpoint: jp-osa-1.linodeobjects.com
    - endpoint_type: E1
      region: es-mad
      s3_endpoint: es-mad-1.linodeobjects.com
    - endpoint_type: E1
      region: us-lax
      s3_endpoint: us-lax-1.linodeobjects.com
    - endpoint_type: E1
      region: nl-ams
      s3_endpoint: nl-ams-1.linodeobjects.com
    - endpoint_type: E0
      region: ap-south
      s3_endpoint: ap-south-1.linodeobjects.com
    - endpoint_type: E1
      region: br-gru
      s3_endpoint: br-gru-1.linodeobjects.com
    - endpoint_type: E0
      region: eu-central
      s3_endpoint: eu-central-1.linodeobjects.com
  type: list
"""

if __name__ == "__main__":
    module.run()
