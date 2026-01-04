#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode StackScript."""

from __future__ import absolute_import, division, print_function

# pylint: disable=line-too-long
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.stackscript as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.stackscript_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import StackScript

module = InfoModule(
    examples=docs.specdoc_examples,
    primary_result=InfoModuleResult(
        field_name="stackscript",
        field_type=FieldType.dict,
        display_name="StackScript",
        samples=docs_parent.result_stackscript_samples,
    ),
    attributes=[
        InfoModuleAttr(
            name="id",
            display_name="ID",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                StackScript, params.get("id")
            )._raw_json,
        ),
        InfoModuleAttr(
            name="label",
            display_name="label",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.linode.stackscripts,
                StackScript.label == params.get("label"),
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
- Get info about a Linode StackScript.
module: stackscript_info
notes: []
options:
  id:
    description:
    - The ID of the StackScript to resolve.
    required: false
    type: int
  label:
    description:
    - The label of the StackScript to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode StackScript.
"""
EXAMPLES = r"""
- name: Get info about a StackScript by label
  linode.cloud.stackscript_info:
    label: my-stackscript
- name: Get info about a StackScript by ID
  linode.cloud.stackscript_info:
    id: 12345
"""
RETURN = r"""
stackscript:
  description: The returned StackScript.
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

if __name__ == "__main__":
    module.run()
