#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list SSH keys in their Linode profile."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="SSH Keys",
    result_field_name="ssh_keys",
    endpoint_template="/profile/sshkeys",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-ssh-keys",
    examples=docs.ssh_key_list_specdoc_examples,
    result_samples=docs.result_ssh_key_list_samples,
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
- List and filter on SSH Keys.
module: ssh_key_list
notes: []
options:
  count:
    description:
    - The number of SSH Keys to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting SSH Keys.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-ssh-keys).
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
    - The order to list SSH Keys in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order SSH Keys by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on SSH Keys.
"""
EXAMPLES = r"""
- name: List all of the SSH keys for the current Linode Account
  linode.cloud.ssh_key_list: {}
- name: List the latest 5 SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:
    count: 5
    order_by: created
    order: desc
- name: List filtered personal SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:
    filters:
    - name: label-or-some-other-field
      values: MySSHKey1
- name: List filtered personal SSH keys for the current Linode Account
  linode.cloud.ssh_key_list:
    filters:
    - name: label-or-some-other-field
      values:
      - MySSHKey1
      - MySSHKey2
"""
RETURN = r"""
ssh_keys:
  description: The returned SSH Keys.
  elements: dict
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      id: 42
      label: MySSHKey1
      ssh_key: ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer
  type: list
"""

if __name__ == "__main__":
    module.run()
