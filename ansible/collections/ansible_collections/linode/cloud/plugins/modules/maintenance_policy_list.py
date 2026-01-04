#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to list Linode Maintenance Policies.
"NOTE: This module is under v4beta.","""
from __future__ import absolute_import, division, print_function

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    maintenance_policy_list as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Maintenance Policies",
    result_field_name="maintenance_policies",
    endpoint_template="/maintenance/policies",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-maintenance-policies",
    examples=docs.specdoc_examples,
    result_samples=docs.result_maintenance_policy_samples,
    requires_beta=True,
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
- List and filter on Maintenance Policies.
- WARNING! This module makes use of beta endpoints and requires the C(api_version)
  field be explicitly set to C(v4beta).
module: maintenance_policy_list
notes: []
options:
  count:
    description:
    - The number of Maintenance Policies to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Maintenance Policies.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-maintenance-policies).
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
    - The order to list Maintenance Policies in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Maintenance Policies by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Maintenance Policies. WARNING! This module makes
  use of beta endpoints and requires the C(api_version) field be explicitly set to
  C(v4beta).
"""
EXAMPLES = r"""
- name: List all of the Linode Maintenance Policies
  linode.cloud.maintenance_policy_list: {}
"""
RETURN = r"""
maintenance_policies:
  description: The returned Maintenance Policies.
  elements: dict
  returned: always
  sample:
  - - description: Migrates the Linode to a new host while it remains fully operational.
        Recommended for maximizing availability.
      is_default: true
      label: Migrate
      notification_period_sec: 300
      slug: linode/migrate
      type: migrate
    - description: Powers off the Linode at the start of the maintenance event and
        reboots it once the maintenance finishes. Recommended for maximizing performance.
      is_default: false
      label: Power-off/on
      notification_period_sec: 1800
      slug: linode/power_off_on
      type: power_off_on
  type: list
"""

if __name__ == "__main__":
    module.run()
