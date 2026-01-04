#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for listing Linode Firewalls."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Firewalls",
    result_field_name="firewalls",
    endpoint_template="/networking/firewalls",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewalls",
    examples=docs.specdoc_examples,
    result_samples=docs.result_firewalls_samples,
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
- List and filter on Firewalls.
module: firewall_list
notes: []
options:
  count:
    description:
    - The number of Firewalls to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Firewalls.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-firewalls).
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
    - The order to list Firewalls in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Firewalls by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Firewalls.
"""
EXAMPLES = r"""
- name: List all of the accessible firewalls for the current Linode Account
  linode.cloud.firewall_list: {}
- name: Resolve all accessible firewall for the current Linode Account
  linode.cloud.firewall_list:
    filters:
    - name: label
      values: myFirewallLabel
"""
RETURN = r"""
firewalls:
  description: The returned Firewalls.
  elements: dict
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      id: 123
      label: firewall123
      rules:
        inbound:
        - action: ACCEPT
          addresses:
            ipv4:
            - 192.0.2.0/24
            ipv6:
            - 2001:DB8::/32
          description: An example firewall rule description.
          label: firewallrule123
          ports: 22-24, 80, 443
          protocol: TCP
        inbound_policy: DROP
        outbound:
        - action: ACCEPT
          addresses:
            ipv4:
            - 192.0.2.0/24
            ipv6:
            - 2001:DB8::/32
          description: An example firewall rule description.
          label: firewallrule123
          ports: 22-24, 80, 443
          protocol: TCP
        outbound_policy: DROP
      status: enabled
      tags:
      - example tag
      - another example
      updated: '2018-01-02T00:01:01'
  type: list
"""

if __name__ == "__main__":
    module.run()
