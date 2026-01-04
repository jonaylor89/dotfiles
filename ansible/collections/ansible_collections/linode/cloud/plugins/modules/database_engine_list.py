#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list all available Managed Database engine types and versions."""
from __future__ import absolute_import, division, print_function

from typing import Any, Dict, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_engine_list as docs,
)
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
            "https://techdocs.akamai.com/linode-api/reference/get-databases-engines",
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
        description=["The order to list database engine types in."],
        default="asc",
        choices=["desc", "asc"],
    ),
    "order_by": SpecField(
        type=FieldType.string,
        description=["The attribute to order database engine types by."],
    ),
    "filters": SpecField(
        type=FieldType.list,
        element_type=FieldType.dict,
        suboptions=spec_filter,
        description=[
            "A list of filters to apply to the resulting database engine types."
        ],
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
    description=["List and filter on Managed Database engine types."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "engines": SpecReturnValue(
            description="The returned database engine types.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-databases-engines",
            type=FieldType.list,
            elements=FieldType.dict,
            sample=docs.result_engines_samples,
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
- List and filter on Managed Database engine types.
module: database_engine_list
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
    - A list of filters to apply to the resulting database engine types.
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
    - The order to list database engine types in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order database engine types by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Managed Database engine types.
"""
EXAMPLES = r"""
- name: List all of the available Managed Database engine types
  linode.cloud.database_engine_list: {}
- name: Resolve all Database engine types
  linode.cloud.database_engine_list:
    filters:
    - name: engine
      values: mysql
"""
RETURN = r"""
engines:
  description: The returned database engine types.
  elements: dict
  returned: always
  sample:
  - - engine: mysql
      id: mysql/8.0.30
      version: 8.0.30
  type: list
"""


class Module(LinodeModuleBase):
    """Module for getting a list of Managed Database engine types"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results: Dict[str, Any] = {"database_engines": []}

        super().__init__(module_arg_spec=self.module_arg_spec)

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for database engine type list module"""

        filter_dict = construct_api_filter(self.module.params)

        self.results["database_engines"] = get_all_paginated(
            self.client,
            "/databases/engines/",
            filter_dict,
            num_results=self.module.params["count"],
        )
        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
