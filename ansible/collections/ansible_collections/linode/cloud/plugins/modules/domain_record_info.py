#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domain records."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    domain_record as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    domain_record_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common_info import (
    InfoModule,
    InfoModuleAttr,
    InfoModuleParam,
    InfoModuleParamGroup,
    InfoModuleParamGroupPolicy,
    InfoModuleResult,
)
from ansible_specdoc.objects import FieldType
from linode_api4 import Domain, DomainRecord, LinodeClient


def _domain_from_params(client: LinodeClient, params: Dict[str, Any]) -> Domain:
    domain_id = params.get("domain_id", None)
    domain = params.get("domain", None)

    if domain_id is not None:
        return Domain(client, domain_id)

    if domain is not None:
        target_domains = client.domains(Domain.domain == domain)
        if len(target_domains) < 1:
            raise ValueError(f"No domain with name {domain} found")

        return target_domains[0]

    raise ValueError("One of domain_id or domain must be specified")


module = InfoModule(
    primary_result=InfoModuleResult(
        field_name="record",
        field_type=FieldType.dict,
        display_name="Domain Records",
        docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-record",
        samples=docs_parent.result_record_samples,
    ),
    params=[
        InfoModuleParamGroup(
            InfoModuleParam(
                display_name="Domain ID",
                name="domain_id",
                type=FieldType.integer,
            ),
            InfoModuleParam(
                display_name="Domain",
                name="domain",
                type=FieldType.string,
            ),
            policies=[InfoModuleParamGroupPolicy.EXACTLY_ONE_OF],
        )
    ],
    attributes=[
        InfoModuleAttr(
            display_name="ID",
            name="id",
            type=FieldType.integer,
            get=lambda client, params: [
                client.load(
                    DomainRecord,
                    params.get("id"),
                    target_parent_id=_domain_from_params(client, params).id,
                )._raw_json
            ],
        ),
        InfoModuleAttr(
            display_name="name",
            name="name",
            type=FieldType.string,
            get=lambda client, params: [
                record._raw_json
                for record in _domain_from_params(client, params).records
                if record.name == params.get("name")
            ],
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
- Get info about a Linode Domain Records.
module: domain_record_info
notes: []
options:
  domain:
    description:
    - The ID of the Domain for this resource.
    required: false
    type: str
  domain_id:
    description:
    - The ID of the Domain ID for this resource.
    required: false
    type: int
  id:
    description:
    - The ID of the Domain Records to resolve.
    required: false
    type: int
  name:
    description:
    - The name of the Domain Records to resolve.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode Domain Records.
"""
EXAMPLES = r"""
- name: Get info about domain records by name
  linode.cloud.domain_record_info:
    domain: my-domain.com
    name: my-subdomain
    type: A
    target: 0.0.0.0
- name: Get info about a domain record by id
  linode.cloud.domain_info:
    domain: my-domain.com
    id: 12345
"""
RETURN = r"""
record:
  description: The returned Domain Records.
  returned: always
  sample:
  - created: '2018-01-01T00:01:01'
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
  type: dict
"""

if __name__ == "__main__":
    module.run()
