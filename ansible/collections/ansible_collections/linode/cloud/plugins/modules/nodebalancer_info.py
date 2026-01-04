#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode NodeBalancer."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    nodebalancer_info as docs,
)
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
from linode_api4 import LinodeClient, NodeBalancer


def _get_firewalls_data(
    client: LinodeClient, nodebalancer: NodeBalancer, params: Dict[str, Any]
) -> List[Any]:
    firewalls = NodeBalancer(client, nodebalancer["id"]).firewalls()
    firewalls_json = []
    for firewall in firewalls:
        firewall._api_get()
        firewalls_json.append(firewall._raw_json)
    return firewalls_json


def _get_nodes(
    client: LinodeClient, nodebalancer: NodeBalancer, params: Dict[str, Any]
) -> List[Any]:
    configs = NodeBalancer(client, nodebalancer["id"]).configs
    nodes_json = []
    for config in configs:
        for node in config.nodes:
            node._api_get()
            nodes_json.append(node._raw_json)
    return nodes_json


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="node_balancer",
        field_type=FieldType.dict,
        display_name="Node Balancer",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer",
        samples=docs_parent.result_node_balancer_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="configs",
            field_type=FieldType.list,
            display_name="configs",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-configs",
            samples=docs_parent.result_configs_samples,
            get=lambda client, nodebalancer, params: paginated_list_to_json(
                NodeBalancer(client, nodebalancer["id"]).configs
            ),
        ),
        InfoModuleResult(
            field_name="nodes",
            field_type=FieldType.list,
            display_name="nodes",
            docs_url="https://techdocs.akamai.com/linode-api/"
            + "reference/get-node-balancer-config-nodes",
            samples=docs_parent.result_nodes_samples,
            get=_get_nodes,
        ),
        InfoModuleResult(
            field_name="firewalls",
            field_type=FieldType.list,
            display_name="firewalls",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls",
            samples=docs_parent.result_firewalls_samples,
            get=lambda client, nodebalancer, params: [
                firewall.id
                for firewall in NodeBalancer(
                    client, nodebalancer["id"]
                ).firewalls()
            ],
        ),
        InfoModuleResult(
            field_name="firewalls_data",
            field_type=FieldType.list,
            display_name="firewalls_data",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-node-balancer-firewalls",
            samples=docs_parent.result_firewalls_data_samples,
            get=_get_firewalls_data,
        ),
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                NodeBalancer,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="label",
            name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.nodebalancers,
                NodeBalancer.label == params.get("label"),
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
- Get info about a Linode Node Balancer.
module: nodebalancer_info
notes: []
options:
  id:
    description:
    - The ID of the Node Balancer to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the Node Balancer to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Node Balancer.
"""
EXAMPLES = r"""
- name: Get a NodeBalancer by its id
  linode.cloud.nodebalancer_info:
    id: 12345
- name: Get a NodeBalancer by its label
  linode.cloud.nodebalancer_info:
    label: cool_nodebalancer
"""
RETURN = r"""
configs:
  description: The returned configs.
  returned: always
  sample:
  - - algorithm: roundrobin
      check: http_body
      check_attempts: 3
      check_body: it works
      check_interval: 90
      check_passive: true
      check_path: /test
      check_timeout: 10
      cipher_suite: recommended
      id: 4567
      nodebalancer_id: 12345
      nodes_status:
        down: 0
        up: 4
      port: 80
      protocol: http
      proxy_protocol: none
      ssl_cert: null
      ssl_commonname: null
      ssl_fingerprint: null
      ssl_key: null
      stickiness: http_cookie
  type: list
firewalls:
  description: The returned firewalls.
  returned: always
  sample:
  - - 1234
    - 5678
  type: list
firewalls_data:
  description: The returned firewalls_data.
  returned: always
  sample:
  - - created: '2020-04-10T13:34:00'
      entities:
      - id: 1234
        label: example-label
        type: nodebalancer
        url: /v4/nodebalancers/1234
      id: 45678
      label: very-cool-label
      rules:
        fingerprint: abcdefg
        inbound: []
        inbound_policy: DROP
        outbound: []
        outbound_policy: DROP
        version: 1
      status: enabled
      tags: []
      updated: '2020-04-10T13:34:01'
  type: list
node_balancer:
  description: The returned Node Balancer.
  returned: always
  sample:
  - client_conn_throttle: 0
    created: '2018-01-01T00:01:01'
    hostname: 192.0.2.1.ip.linodeusercontent.com
    id: 12345
    ipv4: 12.34.56.78
    ipv6: null
    label: balancer12345
    region: us-east
    tags:
    - example tag
    - another example
    transfer:
      in: 28.91200828552246
      out: 3.5487728118896484
      total: 32.46078109741211
    updated: '2018-03-01T00:01:01'
  type: dict
nodes:
  description: The returned nodes.
  returned: always
  sample:
  - - address: 192.168.210.120:80
      config_id: 4567
      id: 54321
      label: node54321
      mode: accept
      nodebalancer_id: 12345
      status: UP
      weight: 50
  type: list
"""

if __name__ == "__main__":
    module.run()
