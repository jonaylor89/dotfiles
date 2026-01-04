#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

from typing import Any, List, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.domain as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import Domain

linode_domain_spec = {
    "axfr_ips": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "The list of IPs that may perform a zone transfer for this Domain."
        ],
    ),
    "description": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "The list of IPs that may perform a "
            "zone transfer for this Domain."
        ],
    ),
    "domain": SpecField(
        type=FieldType.string,
        required=True,
        description=["The domain this Domain represents."],
    ),
    "expire_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds that may pass"
            " before this Domain is no longer authoritative."
        ],
    ),
    "master_ips": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=[
            "The IP addresses representing the master DNS for this Domain."
        ],
    ),
    "refresh_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds before "
            "this Domain should be refreshed."
        ],
    ),
    "retry_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The interval, in seconds, at which a "
            "failed refresh should be retried."
        ],
    ),
    "soa_email": SpecField(
        type=FieldType.string,
        description=["The Start of Authority email address."],
        editable=True,
    ),
    "status": SpecField(
        type=FieldType.string,
        description=[
            "Used to control whether this Domain is "
            "currently being rendered."
        ],
        editable=True,
    ),
    "state": SpecField(
        type=FieldType.string,
        description=["The desired state of the target."],
        choices=["present", "absent"],
        required=True,
    ),
    "tags": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        editable=True,
        description=["An array of tags applied to this object."],
    ),
    "ttl_sec": SpecField(
        type=FieldType.integer,
        editable=True,
        description=[
            "The amount of time in seconds that this "
            "Domain’s records may be cached by resolvers "
            "or other domain servers."
        ],
    ),
    "type": SpecField(
        type=FieldType.string,
        editable=True,
        description=[
            "Whether this Domain represents the authoritative "
            "source of information for the domain"
            " it describes (master), or whether it is a "
            "read-only copy of a master (slave)."
        ],
    ),
    # Deprecated
    "group": SpecField(type=FieldType.string, doc_hide=True),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage Linode Domains."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_domain_spec,
    examples=docs.specdoc_examples,
    return_values={
        "domain": SpecReturnValue(
            description="The domain in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain",
            type=FieldType.dict,
            sample=docs.result_domain_samples,
        ),
        "records": SpecReturnValue(
            description="The domain record in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-record",
            type=FieldType.list,
            sample=docs.result_records_samples,
        ),
        "zone_file": SpecReturnValue(
            description="The zone file for the last rendered zone for the specified domain.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-domain-zone",
            type=FieldType.dict,
            sample=docs.result_zone_file_samples,
        ),
    },
)

MUTABLE_FIELDS: Set[str] = {
    "axfr_ips",
    "description",
    "expire_sec",
    "master_ips",
    "refresh_sec",
    "retry_sec",
    "soa_email",
    "status",
    "tags",
    "ttl_sec",
    "type",
    "group",
}

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
- Manage Linode Domains.
module: domain
notes: []
options:
  axfr_ips:
    description:
    - The list of IPs that may perform a zone transfer for this Domain.
    elements: str
    required: false
    type: list
  description:
    description:
    - The list of IPs that may perform a zone transfer for this Domain.
    required: false
    type: str
  domain:
    description:
    - The domain this Domain represents.
    required: true
    type: str
  expire_sec:
    description:
    - The amount of time in seconds that may pass before this Domain is no longer
      authoritative.
    required: false
    type: int
  master_ips:
    description:
    - The IP addresses representing the master DNS for this Domain.
    elements: str
    required: false
    type: list
  refresh_sec:
    description:
    - The amount of time in seconds before this Domain should be refreshed.
    required: false
    type: int
  retry_sec:
    description:
    - The interval, in seconds, at which a failed refresh should be retried.
    required: false
    type: int
  soa_email:
    description:
    - The Start of Authority email address.
    required: false
    type: str
  state:
    choices:
    - present
    - absent
    description:
    - The desired state of the target.
    required: true
    type: str
  status:
    description:
    - Used to control whether this Domain is currently being rendered.
    required: false
    type: str
  tags:
    description:
    - An array of tags applied to this object.
    elements: str
    required: false
    type: list
  ttl_sec:
    description:
    - "The amount of time in seconds that this Domain\u2019s records may be cached\
      \ by resolvers or other domain servers."
    required: false
    type: int
  type:
    description:
    - Whether this Domain represents the authoritative source of information for the
      domain it describes (master), or whether it is a read-only copy of a master
      (slave).
    required: false
    type: str
requirements:
- python >= 3
short_description: Manage Linode Domains.
"""
EXAMPLES = r"""
- name: Create a domain
  linode.cloud.domain:
    domain: my-domain.com
    type: master
    state: present
- name: Delete a domain
  linode.cloud.domain:
    domain: my-domain.com
    state: absent
"""
RETURN = r"""
domain:
  description: The domain in JSON serialized form.
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
  description: The domain record in JSON serialized form.
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
  description: The zone file for the last rendered zone for the specified domain.
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


class LinodeDomain(LinodeModuleBase):
    """Module for creating and destroying Linode Domains"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results = {
            "changed": False,
            "actions": [],
            "domain": None,
            "zone_file": None,
        }

        self._domain: Optional[Domain] = None

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_domain_by_name(self, name: str) -> Optional[Domain]:
        try:
            domain = self.client.domains(Domain.domain == name)[0]

            # Fix for group returning '' rather than None
            if domain.group == "":
                domain.group = None

            return domain
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get domain {0}: {1}".format(name, exception)
            )

    def _create_domain(self) -> Optional[Domain]:
        params = self.module.params
        domain = params.pop("domain")
        master = params.pop("type") == "master"

        try:
            self.register_action("Created domain {0}".format(domain))
            return self.client.domain_create(domain, master, **params)
        except Exception as exception:
            return self.fail(
                msg="failed to create domain: {0}".format(exception)
            )

    def _update_domain(self) -> None:
        """Handles all update functionality for the current Domain"""

        handle_updates(
            self._domain,
            filter_null_values(self.module.params),
            MUTABLE_FIELDS,
            self.register_action,
        )

    def _handle_domain(self) -> None:
        params = self.module.params

        domain_name: str = params.get("domain")

        self._domain = self._get_domain_by_name(domain_name)

        # Create the domain if it does not already exist
        if self._domain is None:
            self._domain = self._create_domain()

        self._update_domain()

        # Force lazy-loading
        self._domain._api_get()

        self.results["domain"] = self._domain._raw_json
        self.results["records"] = paginated_list_to_json(self._domain.records)
        self.results["zone_file"] = self.client.get(
            "/domains/{}/zone-file".format(self._domain.id)
        )

    def _handle_domain_absent(self) -> None:
        domain_name: str = self.module.params.get("domain")

        self._domain = self._get_domain_by_name(domain_name)

        if self._domain is not None:
            self.results["domain"] = self._domain._raw_json
            self.results["records"] = paginated_list_to_json(
                self._domain.records
            )

            self._domain.delete()
            self.register_action("Deleted domain {0}".format(domain_name))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for Domain module"""
        state = kwargs.get("state")

        if state == "absent":
            self._handle_domain_absent()
            return self.results

        self._handle_domain()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeDomain()


if __name__ == "__main__":
    main()
