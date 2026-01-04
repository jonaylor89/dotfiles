#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode SSH keys."""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ssh_key as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    handle_updates,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import SSHKey

ssh_key_spec = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This SSH key's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this SSH key."],
    ),
    "ssh_key": SpecField(
        type=FieldType.string,
        description=["The SSH public key value."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode SSH key."],
    requirements=global_requirements,
    author=global_authors,
    options=ssh_key_spec,
    examples=docs.specdoc_examples,
    return_values={
        "ssh_key": SpecReturnValue(
            description="The created SSH key in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/post-add-ssh-key",
            type=FieldType.dict,
            sample=docs.result_ssh_key_samples,
        )
    },
)

MUTABLE_FIELDS = {"label"}

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
- Manage a Linode SSH key.
module: ssh_key
notes: []
options:
  label:
    description:
    - This SSH key's unique label.
    required: true
    type: str
  ssh_key:
    description:
    - The SSH public key value.
    required: false
    type: str
  state:
    choices:
    - present
    - absent
    description:
    - The state of this SSH key.
    required: true
    type: str
requirements:
- python >= 3
short_description: Manage a Linode SSH key.
"""
EXAMPLES = r"""
- name: Create a basic SSH key
  linode.cloud.ssh_key:
    label: my-ssh-key
    state: present
- name: Delete a SSH key
  linode.cloud.ssh_key:
    label: my-ssh-key
    state: absent
"""
RETURN = r"""
ssh_key:
  description: The created SSH key in JSON serialized form.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
    id: 42
    label: My SSH Key
    ssh_key: ssh-rsa AAAA_valid_public_ssh_key_123456785== user@their-computer
  type: dict
"""


class SSHKeyModule(LinodeModuleBase):
    """Module for creating and destroying Linode SSH keys"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "ssh_key": None,
        }
        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_if=[["state", "present", ["ssh_key"]]],
        )

    def _create_ssh_key(self) -> Optional[SSHKey]:
        params = self.module.params
        try:
            return self.client.profile.ssh_key_upload(
                params.get("ssh_key"), params.get("label")
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create SSH key: {0}".format(exception)
            )

    def _get_ssh_key_by_label(self, label: str) -> Optional[SSHKey]:
        try:
            return self.client.profile.ssh_keys(SSHKey.label == label)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg=f"failed to get SSH key {label}: {exception}")

    def _update_ssh_key(self, ssh_key: SSHKey) -> None:
        ssh_key._api_get()

        handle_updates(
            ssh_key, self.module.params, MUTABLE_FIELDS, self.register_action
        )

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get("label")

        ssh_key = self._get_ssh_key_by_label(label)

        # Create the ssh_key if it does not already exist
        if ssh_key is None:
            ssh_key = self._create_ssh_key()
            self.register_action(f"Created SSH key {label}")

        self._update_ssh_key(ssh_key)

        # Force lazy-loading
        ssh_key._api_get()

        self.results["ssh_key"] = ssh_key._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        ssh_key = self._get_ssh_key_by_label(label)

        if ssh_key is not None:
            self.results["ssh_key"] = ssh_key._raw_json
            ssh_key.delete()
            self.register_action("Deleted SSH key {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for SSH key module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the SSH key module"""
    SSHKeyModule()


if __name__ == "__main__":
    main()
