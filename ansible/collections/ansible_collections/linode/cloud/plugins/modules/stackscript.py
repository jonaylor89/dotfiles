#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode StackScripts."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.stackscript as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import StackScript

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This StackScript's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this StackScript."],
    ),
    "description": SpecField(
        type=FieldType.string,
        editable=True,
        description=["A description for the StackScript."],
    ),
    "images": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=["Images that can be deployed using this StackScript."],
    ),
    "is_public": SpecField(
        type=FieldType.bool,
        editable=True,
        description=[
            "This determines whether other users can use your StackScript."
        ],
    ),
    "rev_note": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "This field allows you to add notes for "
            "the set of revisions made to this StackScript."
        ],
    ),
    "script": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The script to execute when provisioning a new Linode with this StackScript."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode StackScript."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "stackscript": SpecReturnValue(
            description="The StackScript in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/post-add-stack-script",
            type=FieldType.dict,
            sample=docs.result_stackscript_samples,
        )
    },
)

MUTABLE_FIELDS = {"description", "images", "is_public", "rev_note", "script"}

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
- Manage a Linode StackScript.
module: stackscript
notes: []
options:
  description:
    description:
    - A description for the StackScript.
    required: false
    type: str
  images:
    description:
    - Images that can be deployed using this StackScript.
    elements: str
    required: false
    type: list
  is_public:
    description:
    - This determines whether other users can use your StackScript.
    required: false
    type: bool
  label:
    description:
    - This StackScript's unique label.
    required: true
    type: str
  rev_note:
    description:
    - This field allows you to add notes for the set of revisions made to this StackScript.
    required: false
    type: str
  script:
    description:
    - The script to execute when provisioning a new Linode with this StackScript.
    required: false
    type: str
  state:
    choices:
    - present
    - absent
    description:
    - The state of this StackScript.
    required: true
    type: str
requirements:
- python >= 3
short_description: Manage a Linode StackScript.
"""
EXAMPLES = r"""
- name: Create a basic StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    images:
    - linode/ubuntu22.04
    description: Install a system package
    script: '#!/bin/bash

      # <UDF name="package" label="System Package to Install" example="nginx" default="">

      apt-get -q update && apt-get -q -y install $PACKAGE

      '
    state: present
- name: Delete a StackScript
  linode.cloud.stackscript:
    label: my-stackscript
    state: absent
"""
RETURN = r"""
stackscript:
  description: The StackScript in JSON serialized form.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
    deployments_active: 1
    deployments_total: 12
    description: This StackScript installs and configures MySQL
    id: 10079
    images:
    - linode/debian11
    - linode/debian10
    is_public: true
    label: a-stackscript
    mine: true
    rev_note: Set up MySQL
    script: '#!/bin/bash'
    updated: '2018-01-01T00:01:01'
    user_defined_fields:
    - default: null
      example: hunter2
      label: Enter the password
      manyOf: avalue,anothervalue,thirdvalue
      name: DB_PASSWORD
      oneOf: avalue,anothervalue,thirdvalue
    user_gravatar_id: a445b305abda30ebc766bc7fda037c37
    username: myuser
  type: dict
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode StackScripts"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of = ["state", "label"]
        self.results = {
            "changed": False,
            "actions": [],
            "stackscript": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
            required_if=[("state", "present", ("images", "script"))],
        )

    def _get_stackscript_by_label(self, label: str) -> Optional[StackScript]:
        try:
            return self.client.linode.stackscripts(StackScript.label == label)[
                0
            ]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get stackscript {0}: {1}".format(
                    label, exception
                )
            )

    def _create_stackscript(self) -> Optional[StackScript]:
        params = copy.deepcopy(self.module.params)
        label = params.pop("label")
        script = params.pop("script")
        images = params.pop("images")

        try:
            return self.client.linode.stackscript_create(
                label, script, images, **params
            )
        except Exception as exception:
            return self.fail(
                msg="failed to create stackscript: {0}".format(exception)
            )

    def _update_stackscript(self, stackscript: StackScript) -> None:
        stackscript._api_get()

        params = filter_null_values(self.module.params)

        handle_updates(
            stackscript, params, MUTABLE_FIELDS, self.register_action
        )

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get("label")

        stackscript = self._get_stackscript_by_label(label)

        # Create the stackscript if it does not already exist
        if stackscript is None:
            stackscript = self._create_stackscript()
            self.register_action("Created stackscript {0}".format(label))

        self._update_stackscript(stackscript)

        # Force lazy-loading
        stackscript._api_get()

        self.results["stackscript"] = stackscript._raw_json

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        stackscript = self._get_stackscript_by_label(label)

        if stackscript is not None:
            self.results["stackscript"] = stackscript._raw_json
            stackscript.delete()
            self.register_action("Deleted stackscript {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for StackScript module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the StackScript module"""
    Module()


if __name__ == "__main__":
    main()
