#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Account Availability info."""

from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    account_availability_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import AccountAvailability

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Account Availability",
        field_name="account_availability",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-account-availability",
        samples=docs.result_account_availability_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="region",
            display_name="Region",
            type=FieldType.string,
            get=lambda client, params: client.load(
                AccountAvailability, params.get("region")
            )._raw_json,
        ),
    ],
    requires_beta=True,
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
- Get info about a Linode Account Availability.
- WARNING! This module makes use of beta endpoints and requires the C(api_version)
  field be explicitly set to C(v4beta).
module: account_availability_info
notes: []
options:
  region:
    description:
    - The Region of the Account Availability to resolve.
    required: true
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Account Availability. WARNING! This module
  makes use of beta endpoints and requires the C(api_version) field be explicitly
  set to C(v4beta).
"""
EXAMPLES = r"""
- name: Get info about the current Linode account availability
  linode.cloud.account_availability_info:
    api_version: v4beta
    region: us-east
"""
RETURN = r"""
account_availability:
  description: The returned Account Availability.
  returned: always
  sample:
  - available:
    - NodeBalancers
    - Block Storage
    - Kubernetes
    region: us-east
    unavailable:
    - Linode
  type: dict
"""

if __name__ == "__main__":
    module.run()
