#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Object Storage Quota info."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_storage_quota_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ObjectStorageQuota

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Object Storage Quota",
        field_name="object_storage_quota",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-quota",
        samples=docs.result_object_storage_quota_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            display_name="Quota Usage",
            field_name="quota_usage",
            field_type=FieldType.dict,
            docs_url="https://techdocs.akamai.com/linode-api/reference"
            "/get-object-storage-quota-usage",
            samples=docs.result_object_storage_quota_usage_samples,
            get=lambda client, object_storage_quota, params: ObjectStorageQuota(
                client, object_storage_quota["quota_id"]
            )
            .usage()
            .dict,
        ),
    ],
    attributes=[
        InfoModuleAttr(
            name="quota_id",
            display_name="Quota ID",
            type=FieldType.string,
            get=lambda client, params: client.load(
                ObjectStorageQuota, params.get("quota_id")
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
- Get info about a Linode Object Storage Quota.
module: object_storage_quota_info
notes: []
options:
  quota_id:
    description:
    - The Quota ID of the Object Storage Quota to resolve.
    required: true
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Object Storage Quota.
"""
EXAMPLES = r"""
- name: Get info about an Object Storage quota
  linode.cloud.object_storage_quota_info:
    quota_id: obj-buckets-us-sea-1.linodeobjects.com
"""
RETURN = r"""
object_storage_quota:
  description: The returned Object Storage Quota.
  returned: always
  sample:
  - description: Maximum number of buckets this customer is allowed to have on this
      endpoint
    endpoint_type: E1
    quota_id: obj-buckets-us-sea-1.linodeobjects.com
    quota_limit: 1000
    quota_name: Number of Buckets
    resource_metric: bucket
    s3_endpoint: us-sea-1.linodeobjects.com
  type: dict
quota_usage:
  description: The returned Quota Usage.
  returned: always
  sample:
  - quota_limit: 1000
    usage: 0
  type: dict
"""

if __name__ == "__main__":
    module.run()
