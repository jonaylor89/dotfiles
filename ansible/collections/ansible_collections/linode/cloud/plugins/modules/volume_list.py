#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list all Volumes they have permission to view."""
from __future__ import absolute_import, division, print_function

from typing import Any, Dict, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.volume_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    construct_api_filter,
    get_all_paginated,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)

spec_filter = {
    "name": SpecField(
        type=FieldType.string,
        required=True,
        description=[
            "The name of the field to filter on.",
            "Valid filterable attributes can be found here: "
            "https://techdocs.akamai.com/linode-api/reference/get-volumes",
        ],
    ),
    "values": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        required=True,
        description=[
            "A list of values to allow for this field.",
            "Fields will pass this filter if at least one of these values matches.",
        ],
    ),
}

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "order": SpecField(
        type=FieldType.string,
        description=["The order to list volumes in."],
        default="asc",
        choices=["desc", "asc"],
    ),
    "order_by": SpecField(
        type=FieldType.string,
        description=["The attribute to order volumes by."],
    ),
    "filters": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=spec_filter,
        description=["A list of filters to apply to the resulting volumes."],
    ),
    "count": SpecField(
        type=FieldType.integer,
        description=[
            "The number of results to return.",
            "If undefined, all results will be returned.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["List and filter on Linode Volumes."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "volumes": SpecReturnValue(
            description="The returned volumes.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-volumes",
            type=FieldType.list,
            elements=FieldType.dict,
            sample=docs.result_volumes_samples,
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
- List and filter on Linode Volumes.
module: volume_list
notes: []
options:
  count:
    description:
    - The number of results to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting volumes.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - 'Valid filterable attributes can be found here: https://techdocs.akamai.com/linode-api/reference/get-volumes'
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
    - The order to list volumes in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order volumes by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Linode Volumes.
"""
EXAMPLES = r"""
- name: List all of the volumes that the user is allowed to view
  linode.cloud.volume_list: {}
- name: Resolve all volumes that the user is allowed to view
  linode.cloud.volume_list:
    filters:
    - name: label
      values: myVolumeLabel
"""
RETURN = r"""
volumes:
  description: The returned volumes.
  elements: dict
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      filesystem_path: /dev/disk/by-id/scsi-0Linode_Volume_my-volume
      hardware_type: nvme
      id: 12345
      label: my-volume
      linode_id: 12346
      linode_label: linode123
      region: us-east
      size: 30
      status: active
      tags:
      - example tag
      - another example
      updated: '2018-01-01T00:01:01'
  type: list
"""


class Module(LinodeModuleBase):
    """Module for getting a list of Linode volumes"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results: Dict[str, Any] = {"volumes": []}

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for volume list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results["volumes"] = get_all_paginated(
            self.client,
            "/volumes",
            filter_dict,
            num_results=self.module.params["count"],
        )
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
