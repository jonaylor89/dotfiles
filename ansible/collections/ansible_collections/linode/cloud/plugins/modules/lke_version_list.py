#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode LKE Versions."""

from __future__ import absolute_import, division, print_function

from typing import Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    lke_version_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)
from ansible_specdoc.objects import FieldType, SpecField


def custom_field_resolver(params: Dict[str, str]) -> Dict[str, str]:
    """
    Resolves the appropriate documentation and examples based on the 'tier' parameter.

    :param params: The parameters passed to the module.

    :returns: The appropriate documentation and examples.
    """
    if params.get("tier"):
        return {
            "endpoint_template": f"/lke/tiers/{params.get('tier')}/versions",
        }
    return {
        "endpoint_template": "/lke/versions",
    }


module = ListModule(
    result_display_name="LKE Versions",
    result_field_name="lke_versions",
    endpoint_template="/lke/versions",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-versions",
    result_samples=docs.result_lke_versions_samples,
    examples=docs.specdoc_examples,
    custom_options={
        "tier": SpecField(
            type=FieldType.string,
            choices=["standard", "enterprise"],
            description=[
                "Specifies the service tier for retrieving LKE version details.",
                "NOTE: LKE Enterprise may not currently be available to all users ",
                "and can only be used with v4beta.",
            ],
            required=False,
        ),
    },
    custom_field_resolver=custom_field_resolver,
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
- List and filter on LKE Versions.
module: lke_version_list
notes: []
options:
  count:
    description:
    - The number of LKE Versions to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting LKE Versions.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-lke-versions).
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
    - The order to list LKE Versions in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order LKE Versions by.
    required: false
    type: str
  tier:
    choices:
    - standard
    - enterprise
    description:
    - Specifies the service tier for retrieving LKE version details.
    - 'NOTE: LKE Enterprise may not currently be available to all users '
    - and can only be used with v4beta.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on LKE Versions.
"""
EXAMPLES = r"""
- name: List all Kubernetes versions available for deployment to a Kubernetes cluster
  linode.cloud.lke_version_list: null
- name: List all enterprise-tier Kubernetes versions available for deployment to a
    Kubernetes cluster
  linode.cloud.lke_version_list:
    tier: enterprise
"""
RETURN = r"""
lke_versions:
  description: The returned LKE Versions.
  elements: dict
  returned: always
  sample:
  - - id: '1.32'
    - id: '1.31'
    - id: '1.30'
  - - id: v1.31.1+lke1
      tier: enterprise
  type: list
"""

if __name__ == "__main__":
    module.run()
