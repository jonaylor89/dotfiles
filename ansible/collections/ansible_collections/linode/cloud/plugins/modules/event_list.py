#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file contains the implementation of the event_list module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.event_list as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_list import (
    ListModule,
)

module = ListModule(
    result_display_name="Events",
    result_field_name="events",
    endpoint_template="/account/events",
    result_docs_url="https://techdocs.akamai.com/linode-api/reference/get-events",
    examples=docs.specdoc_examples,
    result_samples=docs.result_events_samples,
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
- List and filter on Events.
module: event_list
notes: []
options:
  count:
    description:
    - The number of Events to return.
    - If undefined, all results will be returned.
    required: false
    type: int
  filters:
    description:
    - A list of filters to apply to the resulting Events.
    elements: dict
    required: false
    suboptions:
      name:
        description:
        - The name of the field to filter on.
        - Valid filterable fields can be found [here](https://techdocs.akamai.com/linode-api/reference/get-events).
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
    - The order to list Events in.
    required: false
    type: str
  order_by:
    description:
    - The attribute to order Events by.
    required: false
    type: str
requirements:
- python >= 3
short_description: List and filter on Events.
"""
EXAMPLES = r"""
- name: List all of the events for the current Linode Account
  linode.cloud.event_list: {}
- name: List the latest 5 events for the current Linode Account
  linode.cloud.event_list:
    count: 5
    order_by: created
    order: desc
- name: List all Linode Instance creation events for the current Linode Account
  linode.cloud.event_list:
    filters:
    - name: action
      values: linode_create
"""
RETURN = r"""
events:
  description: The returned Events.
  elements: dict
  returned: always
  sample:
  - - action: ticket_create
      created: '2018-01-01T00:01:01'
      duration: 300.56
      entity:
        id: 11111
        label: Problem booting my Linode
        type: ticket
        url: /v4/support/tickets/11111
      id: 123
      message: None
      percent_complete: null
      rate: null
      read: true
      secondary_entity:
        id: linode/debian11
        label: linode1234
        type: linode
        url: /v4/linode/instances/1234
      seen: true
      status: null
      time_remaining: null
      username: exampleUser
  type: list
"""

if __name__ == "__main__":
    module.run()
