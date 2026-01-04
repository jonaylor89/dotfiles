#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module allows users to retrieve information about a Linode IP address."""


from __future__ import absolute_import, division, print_function

from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.ip_info as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import IPAddress

spec = {
    # Disable the default values
    "state": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "label": SpecField(type=FieldType.string, required=False, doc_hide=True),
    "address": SpecField(
        type=FieldType.string,
        required=True,
        description=["The IP address to operate on."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode IP."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "ip": SpecReturnValue(
            description="The IP in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-ip",
            type=FieldType.dict,
            sample=docs.result_ip_samples,
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
- Get info about a Linode IP.
module: ip_info
notes: []
options:
  address:
    description:
    - The IP address to operate on.
    required: true
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode IP.
"""
EXAMPLES = r"""
- name: Get info about an IP address
  linode.cloud.ip_info:
    address: 97.107.143.141
"""
RETURN = r"""
ip:
  description: The IP in JSON serialized form.
  returned: always
  sample:
  - address: 97.107.143.141
    gateway: 97.107.143.1
    linode_id: 123
    prefix: 24
    public: true
    rdns: test.example.org
    region: us-east
    subnet_mask: 255.255.255.0
    type: ipv4
    vpc_nat_1_1:
      address: 139.144.244.36
      subnet_id: 194
      vpc_id: 242
  type: dict
"""


class Module(LinodeModuleBase):
    """Module for getting info about a Linode user"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {"ip": None}

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[],
            mutually_exclusive=[],
        )

    def _get_ip(self, address: str) -> IPAddress:
        try:
            ip_addr = IPAddress(self.client, address)
            ip_addr._api_get()
            return ip_addr
        except Exception as exception:
            self.fail(
                msg="failed to get IP address {0}: {1}".format(
                    address, exception
                ),
                exception=exception,
            )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for ip_info module"""

        params = filter_null_values(self.module.params)

        address = params.get("address")
        ip_addr = self._get_ip(address)

        self.results["ip"] = ip_addr._raw_json

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
