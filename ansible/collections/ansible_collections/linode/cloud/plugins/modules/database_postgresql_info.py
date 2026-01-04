#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module allows users to retrieve information about a Linode PostgreSQL Managed Database.
NOTE: This module is compatible with Aiven-backed clusters.
"""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional

from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_postgresql as docs_parent,
)
from ansible_collections.linode.cloud.plugins.module_utils.doc_fragments import (
    database_postgresql_info as docs,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    call_protected_provisioning,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    mapping_to_dict,
    paginated_list_to_json,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import PostgreSQLDatabase

spec = {
    "id": SpecField(
        type=FieldType.string,
        conflicts_with=["label"],
        description=["The ID of the PostgreSQL Database."],
    ),
    "label": SpecField(
        type=FieldType.string,
        conflicts_with=["id"],
        description=["The label of the PostgreSQL Database."],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Get info about a Linode PostgreSQL Managed Database."],
    requirements=global_requirements,
    author=global_authors,
    options=spec,
    examples=docs.specdoc_examples,
    return_values={
        "database": SpecReturnValue(
            description="The database in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgre-sql-instance",
            type=FieldType.dict,
            sample=docs_parent.result_database_samples,
        ),
        "backups": SpecReturnValue(
            description="The database backups in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgre-sql-instance-backups",
            type=FieldType.dict,
            sample=docs_parent.result_backups_samples,
        ),
        "ssl_cert": SpecReturnValue(
            description="The SSL CA certificate for an accessible Managed PostgreSQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgresql-instance-ssl",
            type=FieldType.dict,
            sample=docs_parent.result_ssl_cert_samples,
        ),
        "credentials": SpecReturnValue(
            description="The root username and password for an accessible Managed "
            "PostgreSQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-postgre-sql-instance-credentials",
            type=FieldType.dict,
            sample=docs_parent.result_credentials_samples,
        ),
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
- Get info about a Linode PostgreSQL Managed Database.
module: database_postgresql_info
notes: []
options:
  id:
    description:
    - The ID of the PostgreSQL Database.
    required: false
    type: str
  label:
    description:
    - The label of the PostgreSQL Database.
    required: false
    type: str
requirements:
- python >= 3
short_description: Get info about a Linode PostgreSQL Managed Database.
"""
EXAMPLES = r"""
- name: Get info about a Managed PostgreSQL Database by label
  linode.cloud.database_postgresql_info:
    label: my-db
- name: Get info about a Managed PostgreSQL Database by ID
  linode.cloud.database_postgresql_info:
    id: 12345
"""
RETURN = r"""
backups:
  description: The database backups in JSON serialized form.
  returned: always
  sample:
  - - created: '2022-01-01T00:01:01'
      id: 123
      label: Scheduled - 02/04/22 11:11 UTC-XcCRmI
      type: auto
  type: dict
credentials:
  description: The root username and password for an accessible Managed PostgreSQL
    Database.
  returned: always
  sample:
  - password: s3cur3P@ssw0rd
    username: linroot
  type: dict
database:
  description: The database in JSON serialized form.
  returned: always
  sample:
  - allow_list:
    - 203.0.113.1/32
    - 192.0.1.0/24
    cluster_size: 3
    created: '2022-01-01T00:01:01'
    encrypted: false
    engine: postgresql
    hosts:
      primary: lin-0000-000-pgsql-primary.servers.linodedb.net
      secondary: lin-0000-000-pgsql-primary-private.servers.linodedb.net
    id: 123
    label: example-db
    port: 3306
    region: us-east
    replication_commit_type: local
    replication_type: semi_synch
    ssl_connection: true
    status: active
    type: g6-dedicated-2
    updated: '2022-01-01T00:01:01'
    updates:
      day_of_week: 1
      duration: 3
      frequency: weekly
      hour_of_day: 0
      week_of_month: null
    version: '14.6'
  type: dict
ssl_cert:
  description: The SSL CA certificate for an accessible Managed PostgreSQL Database.
  returned: always
  sample:
  - ca_certificate: LS0tLS1CRUdJ...==
  type: dict
"""


class Module(LinodeModuleBase):
    """Module for getting info about a Linode PostgreSQL database"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "database": None,
            "backups": None,
            "credentials": None,
            "ssl_cert": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("id", "label")],
            mutually_exclusive=[("id", "label")],
        )

    def _get_database_by_label(
        self, label: str
    ) -> Optional[PostgreSQLDatabase]:
        try:
            resp = [
                db
                for db in self.client.database.postgresql_instances()
                if db.label == label
            ]

            return resp[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get database {0}: {1}".format(label, exception)
            )

    def _get_database_by_id(self, database_id: int) -> PostgreSQLDatabase:
        return self._get_resource_by_id(PostgreSQLDatabase, database_id)

    def _write_result(self, database: PostgreSQLDatabase) -> None:
        # Force lazy-loading
        database._api_get()

        self.results["database"] = database._raw_json
        self.results["backups"] = call_protected_provisioning(
            lambda: paginated_list_to_json(database.backups)
        )
        self.results["credentials"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials)
        )
        self.results["ssl_cert"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl)
        )

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for database info module"""

        params = filter_null_values(self.module.params)

        if "id" in params:
            self._write_result(self._get_database_by_id(params.get("id")))

        if "label" in params:
            self._write_result(self._get_database_by_label(params.get("label")))

        return self.results


def main() -> None:
    """Constructs and calls the module"""
    Module()


if __name__ == "__main__":
    main()
