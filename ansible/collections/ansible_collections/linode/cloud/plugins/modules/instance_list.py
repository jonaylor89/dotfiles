#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode instances."""
from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.instance_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Instances",
    result_field_name="instances",
    endpoint_template="/linode/instances",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-linode-instances",
    examples=docs.specdoc_examples,
    result_samples=docs.result_instances_samples,
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
- List and filter on Instances.
module: instance_list
notes: []
options:
  count:
    description:
    - The number of Instances to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Instances.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-linode-instances).
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
    - The order to list Instances in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Instances by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Instances.
"""
EXAMPLES = r"""
- name: List all of the instances for the current Linode Account
  linode.cloud.instance_list: {}
- name: Resolve all instances for the current Linode Account
  linode.cloud.instance_list:
    filters:
    - name: label
      values: myInstanceLabel
"""
RETURN = r"""
instances:
  description: The returned Instances.
  elements: dict
  returned: always
  sample:
  - - alerts:
        cpu: 180
        io: 10000
        network_in: 10
        network_out: 10
        transfer_quota: 80
      backups:
        available: true
        enabled: true
        last_successful: '2018-01-01T00:01:01'
        schedule:
          day: Saturday
          window: W22
      created: '2018-01-01T00:01:01'
      disk_encryption: enabled
      group: Linode-Group
      host_uuid: example-uuid
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
  type: list
"""

if __name__ == "__main__":
    module.run()
