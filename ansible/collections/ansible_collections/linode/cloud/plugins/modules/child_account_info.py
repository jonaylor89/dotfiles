#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Child Account."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    child_account_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import ChildAccount

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="child_account",
        field_type=FieldType.dict,
        display_name="Child Account",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-child-account",
        samples=docs.result_child_account_samples,
    ),
    attributes=[
        InfoModuleAttr(
            display_name="EUUID",
            name="euuid",
            type=FieldType.string,
            get=lambda client, params: client.load(
                ChildAccount,
                params.get("euuid"),
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
    description=[
        "Get info about a Linode Child Account.",
        "NOTE: Parent/Child related features may not be generally available.",
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
- Get info about a Linode Child Account.
- 'NOTE: Parent/Child related features may not be generally available.'
module: child_account_info
notes: []
options:
  euuid:
    description:
    - The EUUID of the Child Account to resolve.
    required: true
    type: str
requirements:
- python >= 3
short_description: 'Get info about a Linode Child Account. NOTE: Parent/Child related
  features may not be generally available.'
"""
EXAMPLES = r"""
- name: Get info about a Child Account by EUUID
  linode.cloud.child_account_info:
    euuid: FFFFFFFF-FFFF-FFFF-FFFFFFFFFFFFFFFF
"""
RETURN = r"""
child_account:
  description: The returned Child Account.
  returned: always
  sample:
  - active_since: '2018-01-01T00:01:01'
    address_1: 123 Main Street
    address_2: Suite A
    balance: 200
    balance_uninvoiced: 145
    billing_source: external
    capabilities:
    - Linodes
    - NodeBalancers
    - Block Storage
    - Object Storage
    city: Philadelphia
    company: Linode LLC
    country: US
    credit_card:
      expiry: 11/2022
      last_four: 1111
    email: john.smith@linode.com
    euuid: E1AF5EEC-526F-487D-B317EBEB34C87D71
    first_name: John
    last_name: Smith
    phone: 215-555-1212
    state: PA
    tax_id: ATU99999999
    zip: 19102-1234
  type: dict
"""

if __name__ == "__main__":
    module.run()
