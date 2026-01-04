#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

import copy
from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.firewall_device as docs
import linode_api4
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

MODULE_SPEC = {
    "firewall_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=["The ID of the Firewall that contains this device."],
    ),
    "entity_id": SpecField(
        type=FieldType.integer,
        required=True,
        description=[
            "The ID for this Firewall Device. This will be the ID of the Linode Entity."
        ],
    ),
    "entity_type": SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The type of Linode Entity. Currently only supports linode and nodebalancer."
        ],
        choices=["linode", "nodebalancer"],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=False,
        doc_hide=True,
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode Firewall Devices."],
    requirements=global_requirements,
    author=global_authors,
    options=MODULE_SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "device": SpecReturnValue(
            description="The Firewall Device in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-firewall-device",
            type=FieldType.dict,
            sample=docs.result_device_samples,
        )
    },
)

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
- Manage Linode Firewall Devices.
module: firewall_device
notes: []
options:
  entity_id:
    description:
    - The ID for this Firewall Device. This will be the ID of the Linode Entity.
    required: true
    type: int
  entity_type:
    choices:
    - linode
    - nodebalancer
    description:
    - The type of Linode Entity. Currently only supports linode and nodebalancer.
    required: true
    type: str
  firewall_id:
    description:
    - The ID of the Firewall that contains this device.
    required: true
    type: int
  state:
    choices:
    - present
    - absent
    description:
    - The desired state of the target.
    required: true
    type: str
requirements:
- python >= 3
short_description: Manage Linode Firewall Devices.
"""
EXAMPLES = r"""
- name: Create a Firewall
  linode.cloud.firewall:
    label: my-firewall
    rules:
      inbound_policy: DROP
    state: present
  register: firewall_result
- name: Create an Instance
  linode.cloud.instance:
    label: my-instance
    region: us-east
    private_ip: true
    type: g6-standard-1
    state: present
  register: instance_result
- name: Attach the instance to the Firewall
  linode.cloud.firewall_device:
    firewall_id: '{{ firewall_result.firewall.id }}'
    entity_id: '{{ instance_result.instance.id }}'
    entity_type: linode
    state: present
"""
RETURN = r"""
device:
  description: The Firewall Device in JSON serialized form.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
    entity:
      id: 123
      label: my-linode
      type: linode
      url: /v4/linode/instances/123
    id: 123
    updated: '2018-01-02T00:01:01'
  type: dict
"""


class LinodeFirewallDevice(LinodeModuleBase):
    """Module for managing Linode Firewall devices"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "device": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_device(self) -> Optional[linode_api4.FirewallDevice]:
        try:
            params = self.module.params
            firewall_id = params["firewall_id"]
            entity_id = params["entity_id"]
            entity_type = params["entity_type"]

            firewall = linode_api4.Firewall(self.client, firewall_id)
            for device in firewall.devices:
                if (
                    device.entity.id == entity_id
                    and device.entity.type == entity_type
                ):
                    return device

            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get device {0}: {1}".format(entity_id, exception)
            )

    def _create_device(self) -> linode_api4.FirewallDevice:
        try:
            params = copy.deepcopy(self.module.params)

            firewall_id = params["firewall_id"]
            entity_id = params["entity_id"]
            entity_type = params["entity_type"]

            firewall = linode_api4.Firewall(self.client, firewall_id)

            device = firewall.device_create(entity_id, entity_type, **params)
            self.register_action(
                "Created Device {}: {}".format(entity_id, device.created)
            )

            return device
        except Exception as exception:
            return self.fail(
                msg="failed to create firewall device {0}: {1}".format(
                    self.module.params.get("entity_id"), exception
                )
            )

    def _handle_present(self) -> None:
        device = self._get_device()

        # Create the device if it does not already exist
        if device is None:
            device = self._create_device()

        # Force lazy-loading
        device._api_get()

        self.results["device"] = device._raw_json

    def _handle_absent(self) -> None:
        device = self._get_device()

        if device is not None:
            self.results["device"] = device._raw_json

            device.delete()
            self.register_action(
                "Deleted firewall device {0}".format(
                    self.module.params.get("entity_id")
                )
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for firewall_device module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeFirewallDevice()


if __name__ == "__main__":
    main()
