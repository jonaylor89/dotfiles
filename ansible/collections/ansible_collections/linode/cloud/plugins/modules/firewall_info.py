#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode Firewall."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Firewall

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="firewall",
        field_type=FieldType.dict,
        display_name="Firewall",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall",
        samples=docs_parent.result_firewall_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="devices",
            field_type=FieldType.list,
            display_name="devices",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall-devices",
            samples=docs_parent.result_devices_samples,
            get=lambda client, firewall, params: paginated_list_to_json(
                Firewall(client, firewall["id"]).devices
            ),
        ),
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Firewall,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.networking.firewalls,
                Firewall.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
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
- Get info about a Linode Firewall.
module: firewall_info
notes: []
options:
  id:
    description:
    - The ID of the Firewall to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the Firewall to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Firewall.
"""
EXAMPLES = r"""
- name: Get info about a Firewall by label
  linode.cloud.firewall_info:
    label: my-firewall
- name: Get info about a Firewall by id
  linode.cloud.firewall_info:
    id: 12345
"""
RETURN = r"""
devices:
  description: The returned devices.
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      entity:
        id: 123
        label: my-linode
        type: linode
        url: /v4/linode/instances/123
      id: 123
      updated: '2018-01-02T00:01:01'
  type: list
firewall:
  description: The returned Firewall.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
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
  type: dict
"""

if __name__ == "__main__":
    module.run()
