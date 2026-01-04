#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode databases."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_list as docs
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
            (
                "Valid filterable attributes can be found here: "
                "https://techdocs.akamai.com/linode-api/reference/get-databases-engines"
            ),
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
    "order": SpecField(
        type=FieldType.string,
        description=["The order to list databases in."],
        default="asc",
        choices=["desc", "asc"],
    ),
    "order_by": SpecField(
        type=FieldType.string,
        description=["The attribute to order databases by."],
    ),
    "filters": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=spec_filter,
        description=["A list of filters to apply to the resulting databases."],
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
    description=["List and filter on Linode Managed Databases."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "databases": SpecReturnValue(
            description="The returned database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-databases-instances",
            type=FieldType.list,
            elements=FieldType.dict,
            sample=docs.result_images_samples,
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
- List and filter on Linode Managed Databases.
module: database_list
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
    - A list of filters to apply to the resulting databases.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - 'Valid filterable attributes can be found here: https://techdocs.akamai.com/linode-api/reference/get-databases-engines'
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
    - The order to list databases in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order databases by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Linode Managed Databases.
"""
EXAMPLES = r"""
- name: List all of the databases for the current Linode Account
  linode.cloud.database_list: {}
- name: Resolve all MySQL databases for the current Linode Account
  linode.cloud.database_list:
    filters:
    - name: engine
      values: mysql
"""
RETURN = r"""
databases:
  description: The returned database.
  elements: dict
  returned: always
  sample:
  - - allow_list:
      - 203.0.113.1/32
      - 192.0.1.0/24
      cluster_size: 3
      created: '2022-01-01T00:01:01'
      encrypted: false
      engine: mysql
      hosts:
        primary: lin-123-456-mysql-mysql-primary.servers.linodedb.net
        secondary: lin-123-456-mysql-primary-private.servers.linodedb.net
      id: 123
      instance_uri: /v4/databases/mysql/instances/123
      label: example-db
      region: us-east
      status: active
      type: g6-dedicated-2
      updated: '2022-01-01T00:01:01'
      updates:
        day_of_week: 1
        duration: 3
        frequency: weekly
        hour_of_day: 0
        week_of_month: null
      version: 8.0.30
  type: list
"""


class Module(LinodeModuleBase):
    """Module for getting info about a Linode databases"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results: Dict[str, Any] = {"databases": []}

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for database list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results["databases"] = get_all_paginated(
            self.client,
            "/databases/instances",
            filter_dict,
            num_results=self.module.params["count"],
        )
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
