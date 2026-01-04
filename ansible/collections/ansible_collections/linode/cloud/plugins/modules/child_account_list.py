#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all the functionality for listing Linode Account Children."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    child_account_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

RESULT_DISPLAY_NAME = "Child Account"

module = ListModule(
    result_display_name=RESULT_DISPLAY_NAME,
    result_field_name="child_accounts",
    endpoint_template="/account/child-accounts",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-child-accounts",
    examples=docs.specdoc_examples,
    result_samples=docs.result_child_accounts_samples,
    description=[
        f"List and filter on {RESULT_DISPLAY_NAME}.",
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
- List and filter on Child Account.
- 'NOTE: Parent/Child related features may not be generally available.'
module: child_account_list
notes: []
options:
  count:
    description:
    - The number of Child Account to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Child Account.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-child-accounts).
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
    - The order to list Child Account in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Child Account by.
    required: false
    type: str
requirements:
- python >= 3
short_description: 'List and filter on Child Account. NOTE: Parent/Child related features
  may not be generally available.'
"""
EXAMPLES = r"""
- name: List all of the Child Accounts under the current Account
  linode.cloud.child_account_list: {}
"""
RETURN = r"""
child_accounts:
  description: The returned Child Account.
  elements: dict
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
  type: list
"""

if __name__ == "__main__":
    module.run()
