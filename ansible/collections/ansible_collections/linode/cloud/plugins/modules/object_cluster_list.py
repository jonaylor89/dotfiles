#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Object Storage clusters. ."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    object_cluster_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Object Storage Clusters",
    result_field_name="clusters",
    endpoint_template="/object-storage/clusters",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-object-storage-clusters",
    result_samples=docs.result_object_clusters_samples,
    examples=docs.specdoc_examples,
    deprecated=True,
    deprecation_message="This module has been deprecated because it "
    + "relies on deprecated API endpoints. Going forward, `region` will "
    + "be the preferred way to designate where Object Storage resources "
    + "should be created.",
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
- '**NOTE: This module has been deprecated because it relies on deprecated API endpoints.
  Going forward, `region` will be the preferred way to designate where Object Storage
  resources should be created.**'
- List and filter on Object Storage Clusters.
module: object_cluster_list
notes: []
options:
  count:
    description:
    - The number of Object Storage Clusters to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Object Storage Clusters.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-object-storage-clusters).
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
    - The order to list Object Storage Clusters in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Object Storage Clusters by.
    required: false
    type: str
requirements:
- python >= 3
short_description: '**NOTE: This module has been deprecated because it relies on deprecated
  API endpoints. Going forward, `region` will be the preferred way to designate where
  Object Storage resources should be created.** List and filter on Object Storage
  Clusters.'
"""
EXAMPLES = r"""
- name: List all of the object storage clusters for the current Linode Account
  linode.cloud.object_cluster_list: {}
- name: Resolve all object storage clusters for the current Linode Account
  linode.cloud.object_cluster_list:
    filters:
    - name: region
      values: us-east
"""
RETURN = r"""
clusters:
  description: The returned Object Storage Clusters.
  elements: dict
  returned: always
  sample:
  - - domain: us-east-1.linodeobjects.com
      id: us-east-1
      region: us-east
      static_site_domain: website-us-east-1.linodeobjects.com
      status: available
  type: list
"""

if __name__ == "__main__":
    module.run()
