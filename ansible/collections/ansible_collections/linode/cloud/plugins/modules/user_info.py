#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode user."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.user_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import User

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="user",
        field_type=FieldType.dict,
        display_name="User",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-user",
        samples=docs.result_user_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="grants",
            field_type=FieldType.dict,
            display_name="Grants",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-user-grants",
            samples=docs.result_grants_samples,
            get=lambda client, user, params: client.get(
                # We can't use the UserGrants type here because
                # it does not serialize directly to JSON or store
                # the API response JSON.
                f"/account/users/{user['username']}/grants"
            ),
        )
    ],
    attributes=[
        InfoModuleAttr(
            name="username",
            display_name="Username",
            type=FieldType.string,
            get=lambda client, params: client.load(
                User, params.get("username")
            )._raw_json,
        )
    ],
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
- Get info about a Linode User.
module: user_info
notes: []
options:
  username:
    description:
    - The Username of the User to resolve.
    required: true
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode User.
"""
EXAMPLES = r"""
- name: Get info about a user
  linode.cloud.user_info:
    username: my-cool-user
"""
RETURN = r"""
grants:
  description: The returned Grants.
  returned: always
  sample:
  - domain:
    - id: 123
      label: example-entity
      permissions: read_only
    global:
      account_access: read_only
      add_databases: true
      add_domains: true
      add_firewalls: true
      add_images: true
      add_linodes: true
      add_longview: true
      add_nodebalancers: true
      add_stackscripts: true
      add_volumes: true
      cancel_account: false
      longview_subscription: true
    image:
    - id: 123
      label: example-entity
      permissions: read_only
    linode:
    - id: 123
      label: example-entity
      permissions: read_only
    longview:
    - id: 123
      label: example-entity
      permissions: read_only
    nodebalancer:
    - id: 123
      label: example-entity
      permissions: read_only
    stackscript:
    - id: 123
      label: example-entity
      permissions: read_only
    volume:
    - id: 123
      label: example-entity
      permissions: read_only
  type: dict
user:
  description: The returned User.
  returned: always
  sample:
  - email: example_user@linode.com
    restricted: true
    ssh_keys:
    - home-pc
    - laptop
    tfa_enabled: null
    user_type: default
    username: example_user
  type: dict
"""

if __name__ == "__main__":
    module.run()
