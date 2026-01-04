#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Instance info."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance_info as docs
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
from linode_api4 import Instance

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        display_name="Instance",
        field_name="instance",
        field_type=FieldType.dict,
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-instance",
        samples=docs_parent.result_instance_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="configs",
            field_type=FieldType.list,
            display_name="Configs",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-config",
            samples=docs_parent.result_configs_samples,
            get=lambda client, instance, params: paginated_list_to_json(
                Instance(client, instance.get("id")).configs
            ),
        ),
        InfoModuleResult(
            field_name="disks",
            field_type=FieldType.list,
            display_name="Disks",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-disk",
            samples=docs_parent.result_disks_samples,
            get=lambda client, instance, params: paginated_list_to_json(
                Instance(client, instance.get("id")).disks
            ),
        ),
        InfoModuleResult(
            field_name="networking",
            field_type=FieldType.dict,
            display_name="Networking Configuration",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-ips",
            samples=docs_parent.result_networking_samples,
            get=lambda client, instance, params: client.get(
                "/linode/instances/{0}/ips".format(instance.get("id"))
            ),
        ),
    ],
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Instance, params.get("id")
            )._raw_json,
        ),
        InfoModuleAttr(
            name="label",
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.linode.instances,
                Instance.label == params.get("label"),
                raise_not_found=True,
            )._raw_json,
        ),
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
- Get info about a Linode Instance.
module: instance_info
notes: []
options:
  id:
    description:
    - The ID of the Instance to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the Instance to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Instance.
"""
EXAMPLES = r"""
- name: Get info about an instance by label
  linode.cloud.instance_info:
    label: my-instance
- name: Get info about an instance by id
  linode.cloud.instance_info:
    id: 12345
"""
RETURN = r"""
configs:
  description: The returned Configs.
  returned: always
  sample:
  - - comments: This is my main Config
      devices:
        sda:
          disk_id: 124458
          volume_id: null
        sdb:
          disk_id: 124458
          volume_id: null
        sdc:
          disk_id: 124458
          volume_id: null
        sdd:
          disk_id: 124458
          volume_id: null
        sde:
          disk_id: 124458
          volume_id: null
        sdf:
          disk_id: 124458
          volume_id: null
        sdg:
          disk_id: 124458
          volume_id: null
        sdh:
          disk_id: 124458
          volume_id: null
      helpers:
        devtmpfs_automount: false
        distro: true
        modules_dep: true
        network: true
        updatedb_disabled: true
      id: 23456
      interfaces:
      - ipam_address: 10.0.0.1/24
        label: example-interface
        purpose: vlan
      kernel: linode/latest-64bit
      label: My Config
      memory_limit: 2048
      root_device: /dev/sda
      run_level: default
      virt_mode: paravirt
  type: list
disks:
  description: The returned Disks.
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      disk_encryption: enabled
      filesystem: ext4
      id: 25674
      label: Debian 9 Disk
      size: 48640
      status: ready
      updated: '2018-01-01T00:01:01'
  type: list
instance:
  description: The returned Instance.
  returned: always
  sample:
  - alerts:
      cpu: 180
      io: 10000
      network_in: 10
      network_out: 10
      transfer_quota: 80
    backups:
      enabled: true
      last_successful: '2018-01-01T00:01:01'
      schedule:
        day: Saturday
        window: W22
    created: '2018-01-01T00:01:01'
    disk_encryption: enabled
    group: Linode-Group
    has_user_data: true
    hypervisor: kvm
    id: 123
    image: linode/debian11
    ipv4:
    - 203.0.113.1
    - 192.0.2.1
    ipv6: c001:d00d::1337/128
    label: linode123
    lke_cluster_id: null
    maintenance_policy: linode/migrate
    placement_group:
      id: 123
      label: test
      placement_group_policy: strict
      placement_group_type: anti_affinity:local
    region: us-east
    specs:
      disk: 81920
      memory: 4096
      transfer: 4000
      vcpus: 2
    status: running
    tags:
    - example tag
    - another example
    type: g6-standard-1
    updated: '2018-01-01T00:01:01'
    watchdog_enabled: true
  type: dict
networking:
  description: The returned Networking Configuration.
  returned: always
  sample:
  - ipv4:
      private:
      - address: 192.168.133.234
        gateway: null
        linode_id: 123
        prefix: 17
        public: false
        rdns: null
        region: us-east
        subnet_mask: 255.255.128.0
        type: ipv4
      public:
      - address: 97.107.143.141
        gateway: 97.107.143.1
        linode_id: 123
        prefix: 24
        public: true
        rdns: test.example.org
        region: us-east
        subnet_mask: 255.255.255.0
        type: ipv4
      reserved:
      - address: 97.107.143.141
        gateway: 97.107.143.1
        linode_id: 123
        prefix: 24
        public: true
        rdns: test.example.org
        region: us-east
        subnet_mask: 255.255.255.0
        type: ipv4
      shared:
      - address: 97.107.143.141
        gateway: 97.107.143.1
        linode_id: 123
        prefix: 24
        public: true
        rdns: test.example.org
        region: us-east
        subnet_mask: 255.255.255.0
        type: ipv4
    ipv6:
      global:
        prefix: 124
        range: 2600:3c01::2:5000:0
        region: us-east
        route_target: 2600:3c01::2:5000:f
      link_local:
        address: fe80::f03c:91ff:fe24:3a2f
        gateway: fe80::1
        linode_id: 123
        prefix: 64
        public: false
        rdns: null
        region: us-east
        subnet_mask: ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
        type: ipv6
      slaac:
        address: 2600:3c03::f03c:91ff:fe24:3a2f
        gateway: fe80::1
        linode_id: 123
        prefix: 64
        public: true
        rdns: null
        region: us-east
        subnet_mask: ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff
        type: ipv6
  type: dict
"""

if __name__ == "__main__":
    module.run()
