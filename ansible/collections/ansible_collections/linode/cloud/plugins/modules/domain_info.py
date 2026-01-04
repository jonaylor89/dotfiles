#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This file contains the implementation of the domain_info module."""

from __future__ import absolute_import, division, print_function

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain as docs_parent
import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleResult,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    paginated_list_to_json,
    safe_find,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Domain

module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="domain",
        field_type=FieldType.dict,
        display_name="Domain",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain",
        samples=docs_parent.result_domain_samples,
    ),
    secondary_results=[
        InfoModuleResult(
            field_name="records",
            field_type=FieldType.list,
            display_name="records",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-records",
            samples=docs_parent.result_records_samples,
            get=lambda client, domain, params: paginated_list_to_json(
                Domain(client, domain["id"]).records
            ),
        ),
        InfoModuleResult(
            field_name="zone_file",
            field_type=FieldType.dict,
            display_name="zone file",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-zone",
            samples=docs_parent.result_zone_file_samples,
            get=lambda client, domain, params: {
                "zone_file": Domain(client, domain["id"]).zone_file_view()
            },
        ),
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: client.load(
                Domain,
                params.get("id"),
            )._raw_json,
        ),
        InfoModuleAttr(
            display_name="domain",
            name="domain",
            type=FieldType.string,
            get=lambda client, params: safe_find(
                client.domains,
                Domain.domain == params.get("domain"),
                raise_not_found=True,
            )._raw_json,
        ),
    ],
    examples=docs.specdoc_examples,
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
- Get info about a Linode Domain.
module: domain_info
notes: []
options:
  domain:
    description:
    - The domain of the Domain to resolve.
    required: false
    type: str
  id:
    description:
    - The ID of the Domain to resolve.
    required: false
    type: int
requirements:
- python >= 3
short_description: Get info about a Linode Domain.
"""
EXAMPLES = r"""
- name: Get info about a domain by domain
  linode.cloud.domain_info:
    domain: my-domain.com
- name: Get info about a domain by id
  linode.cloud.domain_info:
    id: 12345
"""
RETURN = r"""
domain:
  description: The returned Domain.
  returned: always
  sample:
  - axfr_ips: []
    description: null
    domain: example.org
    expire_sec: 300
    group: null
    id: 1234
    master_ips: []
    refresh_sec: 300
    retry_sec: 300
    soa_email: admin@example.org
    status: active
    tags:
    - example tag
    - another example
    ttl_sec: 300
    type: master
  type: dict
records:
  description: The returned records.
  returned: always
  sample:
  - - created: '2018-01-01T00:01:01'
      id: 123456
      name: test
      port: 80
      priority: 50
      protocol: null
      service: null
      tag: null
      target: 192.0.2.0
      ttl_sec: 604800
      type: A
      updated: '2018-01-01T00:01:01'
      weight: 50
  type: list
zone_file:
  description: The returned zone file.
  returned: always
  sample:
  - zone_file:
    - ; example.com [123]
    - $TTL 864000
    - '@  IN  SOA  ns1.linode.com. user.example.com. 2021000066 14400 14400 1209600
      86400'
    - '@    NS  ns1.linode.com.'
    - '@    NS  ns2.linode.com.'
    - '@    NS  ns3.linode.com.'
    - '@    NS  ns4.linode.com.'
    - '@    NS  ns5.linode.com.'
  type: dict
"""

if __name__ == "__main__":
    module.run()
