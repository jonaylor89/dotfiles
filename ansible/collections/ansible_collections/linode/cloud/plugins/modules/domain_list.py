#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file contains the implementation of the domain_list module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Domains",
    result_field_name="domains",
    endpoint_template="/domains",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-domains",
    examples=docs.specdoc_examples,
    result_samples=docs.result_domains_samples,
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
- List and filter on Domains.
module: domain_list
notes: []
options:
  count:
    description:
    - The number of Domains to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Domains.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-domains).
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
    - The order to list Domains in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Domains by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Domains.
"""
EXAMPLES = r"""
- name: List all of the domains for the current Linode Account
  linode.cloud.domain_list: {}
- name: Resolve all domains for the current Linode Account
  linode.cloud.domain_list:
    filters:
    - name: domain
      values: example.org
"""
RETURN = r"""
domains:
  description: The returned Domains.
  elements: dict
  returned: always
  sample:
  - - axfr_ips: []
      description: null
      domain: example.org
      expire_sec: 300
      group: null
      id: 1234
      master_ips: []
      refresh_sec: 300
      retry_sec: 300
      soa_email: admin@example.org
      status: active
      tags:
      - example tag
      - another example
      ttl_sec: 300
      type: master
  type: list
"""

if __name__ == "__main__":
    module.run()
