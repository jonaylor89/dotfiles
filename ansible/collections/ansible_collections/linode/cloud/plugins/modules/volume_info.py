#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Volumes."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.volume as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.volume_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    create_filter_and,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Volume

linode_volume_info_spec = {
    # We need to overwrite attributes to exclude them as requirements
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "id": SpecField(
        type=FieldType.integer,
        required=False,
        conflicts_with=["label"],
        description=[
            "The ID of the Volume.",
            "Optional if `label` is defined.",
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=False,
        conflicts_with=["id"],
        description=[
            "The label of the Volume.",
            "Optional if `id` is defined.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode Volume."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_volume_info_spec,
    examples=docs.specdoc_examples,
    return_values={
        "volume": SpecReturnValue(
            description="The volume in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-volume",
            type=FieldType.dict,
            sample=docs_parent.result_volume_samples,
        ),
    },
)

linode_volume_valid_filters = ["id", "label"]

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
- Get info about a Linode Volume.
module: volume_info
notes: []
options:
  id:
    description:
    - The ID of the Volume.
    - Optional if `label` is defined.
    required: false
    type: int
  label:
    description:
    - The label of the Volume.
    - Optional if `id` is defined.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Volume.
"""
EXAMPLES = r"""
- name: Get info about a volume by label
  linode.cloud.volume_info:
    label: example-volume
- name: Get info about a volume by id
  linode.cloud.volume_info:
    id: 12345
"""
RETURN = r"""
volume:
  description: The volume in JSON serialized form.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
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
  type: dict
"""


class LinodeVolumeInfo(LinodeModuleBase):
    """Module for getting info about a Linode Volume"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "volume": None,
        }

        self._volume = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_matching_volume(self, spec_args: dict) -> Optional[Volume]:
        filter_items = {
            k: v
            for k, v in spec_args.items()
            if k in linode_volume_valid_filters and v is not None
        }

        filter_statement = create_filter_and(Volume, filter_items)

        try:
            # Special case because ID is not filterable
            if "id" in filter_items.keys():
                result = Volume(self.client, spec_args.get("id"))
                result._api_get()  # Force lazy-loading

                return result

            return self.client.volumes(filter_statement)[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(msg="failed to get volume {0}".format(exception))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for volume info module"""

        volume = self._get_matching_volume(kwargs)

        if volume is None:
            self.fail("failed to get volume")

        self.results["volume"] = volume._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume info module"""
    LinodeVolumeInfo()


if __name__ == "__main__":
    main()
