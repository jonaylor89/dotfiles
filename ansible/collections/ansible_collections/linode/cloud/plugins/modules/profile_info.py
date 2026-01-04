#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Profile info."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.profile_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Profile",
        field_name="profile",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-profile",
        samples=docs.result_profile_samples,
        get=lambda client, params: client.profile()._raw_json,
    ),
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
- Get info about a Linode Profile.
module: profile_info
notes: []
options: {}
requirements:
- python >= 3
short_description: Get info about a Linode Profile.
"""
EXAMPLES = r"""
- name: Get info about the current Linode profile
  linode.cloud.profile_info: {}
"""
RETURN = r"""
profile:
  description: The returned Profile.
  returned: always
  sample:
  - authentication_type: password
    authorized_keys:
    - null
    email: example-user@gmail.com
    email_notifications: true
    ip_whitelist_enabled: false
    lish_auth_method: keys_only
    referrals:
      code: 871be32f49c1411b14f29f618aaf0c14637fb8d3
      completed: 0
      credit: 0
      pending: 0
      total: 0
      url: https://www.linode.com/?r=871be32f49c1411b14f29f618aaf0c14637fb8d3
    restricted: false
    timezone: US/Eastern
    two_factor_auth: true
    uid: 1234
    username: exampleUser
    verified_phone_number: '+5555555555'
  type: dict
"""

if __name__ == "__main__":
    module.run()
