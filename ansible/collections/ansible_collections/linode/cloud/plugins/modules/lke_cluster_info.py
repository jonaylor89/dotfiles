#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Volumes."""

from __future__ import absolute_import, division, print_function

from typing import Any, Dict, List, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    lke_cluster as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    lke_cluster_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    jsonify_node_pool,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_lke_shared import (
    safe_get_cluster_acl,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError, LKECluster

linode_lke_cluster_info_spec = {
    "id": SpecField(
        type=FieldType.integer,
        required=False,
        conflicts_with=["label"],
        description=[
            "The ID of the LKE cluster.",
            "Optional if `label` is defined.",
        ],
    ),
    "label": SpecField(
        type=FieldType.string,
        required=False,
        conflicts_with=["id"],
        description=[
            "The label of the LKE cluster.",
            "Optional if `id` is defined.",
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode LKE cluster."],
    requirements=global_requirements,
    author=global_authors,
    options=linode_lke_cluster_info_spec,
    examples=docs.examples,
    return_values={
        "cluster": SpecReturnValue(
            description="The LKE cluster in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-cluster",
            type=FieldType.dict,
            sample=docs_parent.result_cluster,
        ),
        "node_pools": SpecReturnValue(
            description="A list of node pools in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-cluster-pools",
            type=FieldType.list,
            sample=docs_parent.result_node_pools,
        ),
        "kubeconfig": SpecReturnValue(
            description="The Base64-encoded kubeconfig used to access this cluster. \n"
            "NOTE: This value may be unavailable if the cluster is not "
            "fully provisioned.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-cluster-kubeconfig",
            type=FieldType.string,
            sample=['"a3ViZWNvbmZpZyBjb250ZW50Cg=="'],
        ),
        "dashboard_url": SpecReturnValue(
            description="The Cluster Dashboard access URL.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/get-lke-cluster-dashboard",
            type=FieldType.string,
            sample=['"https://example.dashboard.linodelke.net"'],
        ),
    },
)

VALID_FILTERS = ["id", "label"]

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
- Get info about a Linode LKE cluster.
module: lke_cluster_info
notes: []
options:
  id:
    description:
    - The ID of the LKE cluster.
    - Optional if `label` is defined.
    required: false
    type: int
  label:
    description:
    - The label of the LKE cluster.
    - Optional if `id` is defined.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode LKE cluster.
"""
EXAMPLES = r"""
- name: Get info about an LKE cluster by label
  linode.cloud.lke_cluster_info:
    label: my-cluster
- name: Get info about an LKE cluster by ID
  linode.cloud.lke_cluster_info:
    id: 12345
"""
RETURN = r"""
cluster:
  description: The LKE cluster in JSON serialized form.
  returned: always
  sample:
  - control_plane:
      acl:
        addresses:
          ipv4:
          - 0.0.0.0/0
          ipv6:
          - 2001:db8:1234:abcd::/64
        enabled: true
      high_availability: true
    created: '2019-09-12T21:25:30Z'
    id: 1234
    k8s_version: '1.28'
    label: lkecluster12345
    region: us-central
    tags:
    - ecomm
    - blogs
    updated: '2019-09-13T21:24:16Z'
  type: dict
dashboard_url:
  description: The Cluster Dashboard access URL.
  returned: always
  sample:
  - https://example.dashboard.linodelke.net
  type: str
kubeconfig:
  description: "The Base64-encoded kubeconfig used to access this cluster. \nNOTE:\
    \ This value may be unavailable if the cluster is not fully provisioned."
  returned: always
  sample:
  - a3ViZWNvbmZpZyBjb250ZW50Cg==
  type: str
node_pools:
  description: A list of node pools in JSON serialized form.
  returned: always
  sample:
  - - autoscaler:
        enabled: true
        max: 12
        min: 3
      count: 6
      disk_encryption: enabled
      disks:
      - size: 1024
        type: ext-4
      id: 456
      nodes:
      - id: '123456'
        instance_id: 123458
        status: ready
      tags:
      - example tag
      - another example
      type: g6-standard-4
  type: list
"""


class LinodeLKEClusterInfo(LinodeModuleBase):
    """Module for getting info about a Linode Volume"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.required_one_of: List[str] = []
        self.results: Dict[str, Any] = {
            "cluster": None,
            "node_pools": [],
            "dashboard_url": None,
            "kubeconfig": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=self.required_one_of,
        )

    def _get_cluster_by_name(self, name: str) -> Optional[LKECluster]:
        try:
            clusters = self.client.lke.clusters()

            for cluster in clusters:
                if cluster.label == name:
                    return cluster

            return None
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get lke cluster {0}: {1}".format(name, exception)
            )

    def _get_cluster_from_kwargs(self, **kwargs: Any) -> LKECluster:
        args = filter_null_values(kwargs)

        if "id" in args:
            cluster = LKECluster(self.client, args.get("id"))
            cluster._api_get()
            return cluster

        if "label" in args:
            return self._get_cluster_by_name(args.get("label"))

        return self.fail(msg="one of `label` or `id` must be specified")

    def _populate_results(self, cluster: LKECluster) -> None:
        cluster._api_get()

        cluster_json = cluster._raw_json

        # We need to inject the control plane ACL configuration into the cluster's JSON
        # because it is not returned from the cluster GET endopint
        cluster_json["control_plane"]["acl"] = safe_get_cluster_acl(cluster)

        # Inject the APL URLs if APL is enabled
        if cluster.apl_enabled:
            cluster_json["apl_console_url"] = cluster.apl_console_url
            cluster_json["apl_health_check_url"] = cluster.apl_health_check_url

        self.results["cluster"] = cluster_json

        self.results["node_pools"] = [
            jsonify_node_pool(pool) for pool in cluster.pools
        ]

        # Retrieve kubeconfig
        try:
            self.results["kubeconfig"] = cluster.kubeconfig
        except ApiError as err:
            ignored_error_messages = {
                503: "Kubeconfig not yet available...",
                401: "Current token is not authorized to view this endpoint.",
            }

            if err.status not in ignored_error_messages:
                raise err

            self.results["kubeconfig"] = ignored_error_messages[err.status]

        # Retrieve dashboard URL
        try:
            self.results["dashboard_url"] = self.client.get(
                "/lke/clusters/{}/dashboard".format(cluster.id)
            )["url"]
        except ApiError as err:
            if err.status != 503:
                raise err

            self.results["dashboard_url"] = "Dashboard URL not yet available..."

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for LKE cluster info module"""

        cluster = self._get_cluster_from_kwargs(**kwargs)

        if cluster is None:
            self.fail("failed to get cluster")

        self._populate_results(cluster)

        return self.results


def main() -> None:
    """Constructs and calls the Linode Volume info module"""
    LinodeLKEClusterInfo()


if __name__ == "__main__":
    main()
