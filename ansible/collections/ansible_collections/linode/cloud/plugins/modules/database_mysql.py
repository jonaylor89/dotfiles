#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
This module contains all of the functionality for Linode MySQL Database Clusters.
Deprecated in favor of database_mysql_v2.
"""

from __future__ import absolute_import, division, print_function

from typing import Any, Optional, Set

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_mysql as docs
import polling
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    SPEC_UPDATE_WINDOW,
    call_protected_provisioning,
    validate_shared_db_input,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values,
    handle_updates,
    mapping_to_dict,
    paginated_list_to_json,
    poll_condition,
)
from ansible_specdoc.objects import (
    DeprecationInfo,
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import ApiError
from linode_api4.objects import MySQLDatabase

SPEC = {
    "label": SpecField(
        type=FieldType.string,
        required=True,
        description=["This database's unique label."],
    ),
    "state": SpecField(
        type=FieldType.string,
        choices=["present", "absent"],
        required=True,
        description=["The state of this database."],
    ),
    "allow_list": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of IP addresses that can access the Managed Database.",
            "Each item must be a range in CIDR format.",
        ],
        default=[],
        editable=True,
    ),
    "cluster_size": SpecField(
        type=FieldType.integer,
        description=[
            "The number of Linode Instance nodes deployed to the Managed Database."
        ],
        choices=[1, 3],
        default=1,
    ),
    "encrypted": SpecField(
        type=FieldType.bool,
        description=["Whether the Managed Databases is encrypted."],
    ),
    "engine": SpecField(
        type=FieldType.string,
        description=["The Managed Database engine in engine/version format."],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The Region ID for the Managed Database."],
    ),
    "replication_type": SpecField(
        type=FieldType.string,
        description=[
            "The replication method used for the Managed Database.",
            "Defaults to none for a single cluster and "
            "semi_synch for a high availability cluster.",
            "Must be none for a single node cluster.",
            "Must be asynch or semi_synch for a high availability cluster.",
        ],
        choices=["none", "asynch", "semi_synch"],
        default="none",
    ),
    "ssl_connection": SpecField(
        type=FieldType.bool,
        description=[
            "Whether to require SSL credentials to "
            "establish a connection to the Managed Database."
        ],
        default=True,
    ),
    "type": SpecField(
        type=FieldType.string,
        description=[
            "The Linode Instance type used by the "
            "Managed Database for its nodes."
        ],
    ),
    "updates": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_UPDATE_WINDOW,
        description=[
            "Configuration settings for automated patch "
            "update maintenance for the Managed Database."
        ],
        editable=True,
    ),
    "wait": SpecField(
        type=FieldType.bool,
        default=True,
        description=[
            "Wait for the database to have status `available` before returning."
        ],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        default=3600,
        description=[
            "The amount of time, in seconds, to wait for an image to "
            "have status `available`."
        ],
    ),
}

SPECDOC_META = SpecDocMeta(
    description=["Manage a Linode MySQL database."],
    requirements=global_requirements,
    author=global_authors,
    options=SPEC,
    examples=docs.specdoc_examples,
    return_values={
        "database": SpecReturnValue(
            description="The database in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance",
            type=FieldType.dict,
            sample=docs.result_database_samples,
        ),
        "backups": SpecReturnValue(
            description="The database backups in JSON serialized form.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance-backup",
            type=FieldType.dict,
            sample=docs.result_backups_samples,
        ),
        "ssl_cert": SpecReturnValue(
            description="The SSL CA certificate for an accessible Managed MySQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance-ssl",
            type=FieldType.dict,
            sample=docs.result_ssl_cert_samples,
        ),
        "credentials": SpecReturnValue(
            description="The root username and password for an accessible Managed MySQL Database.",
            docs_url="https://techdocs.akamai.com/linode-api/reference/"
            "get-databases-mysql-instance-credentials",
            type=FieldType.dict,
            sample=docs.result_credentials_samples,
        ),
    },
    deprecated=DeprecationInfo(
        alternative="This module has been deprecated in favor of `database_mysql_v2`.",
        why="This module has been deprecated because it relies on deprecated API endpoints.",
        removed_in="0.35.0",
    ),
)

MUTABLE_FIELDS = {"allow_list", "updates"}

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
deprecated:
  alternative: This module has been deprecated in favor of `database_mysql_v2`.
  removed_in: 0.35.0
  why: This module has been deprecated because it relies on deprecated API endpoints.
description:
- Manage a Linode MySQL database.
module: database_mysql
notes: []
options:
  allow_list:
    default: []
    description:
    - A list of IP addresses that can access the Managed Database.
    - Each item must be a range in CIDR format.
    elements: str
    required: false
    type: list
  cluster_size:
    choices:
    - 1
    - 3
    default: 1
    description:
    - The number of Linode Instance nodes deployed to the Managed Database.
    required: false
    type: int
  encrypted:
    description:
    - Whether the Managed Databases is encrypted.
    required: false
    type: bool
  engine:
    description:
    - The Managed Database engine in engine/version format.
    required: false
    type: str
  label:
    description:
    - This database's unique label.
    required: true
    type: str
  region:
    description:
    - The Region ID for the Managed Database.
    required: false
    type: str
  replication_type:
    choices:
    - none
    - asynch
    - semi_synch
    default: none
    description:
    - The replication method used for the Managed Database.
    - Defaults to none for a single cluster and semi_synch for a high availability
      cluster.
    - Must be none for a single node cluster.
    - Must be asynch or semi_synch for a high availability cluster.
    required: false
    type: str
  ssl_connection:
    default: true
    description:
    - Whether to require SSL credentials to establish a connection to the Managed
      Database.
    required: false
    type: bool
  state:
    choices:
    - present
    - absent
    description:
    - The state of this database.
    required: true
    type: str
  type:
    description:
    - The Linode Instance type used by the Managed Database for its nodes.
    required: false
    type: str
  updates:
    description:
    - Configuration settings for automated patch update maintenance for the Managed
      Database.
    required: false
    suboptions:
      day_of_week:
        choices:
        - 1
        - 2
        - 3
        - 4
        - 5
        - 6
        - 7
        description:
        - The day to perform maintenance. 1=Monday, 2=Tuesday, etc.
        required: true
        type: int
      duration:
        choices:
        - 1
        - 3
        description:
        - The maximum maintenance window time in hours.
        required: true
        type: int
      frequency:
        choices:
        - weekly
        - monthly
        default: weekly
        description:
        - Whether maintenance occurs on a weekly or monthly basis.
        required: false
        type: str
      hour_of_day:
        description:
        - The hour to begin maintenance based in UTC time.
        required: true
        type: int
      week_of_month:
        description:
        - The week of the month to perform monthly frequency updates.
        - Defaults to None.
        - Required for monthly frequency updates.
        - Must be null for weekly frequency updates.
        required: false
        type: int
    type: dict
  wait:
    default: true
    description:
    - Wait for the database to have status `available` before returning.
    required: false
    type: bool
  wait_timeout:
    default: 3600
    description:
    - The amount of time, in seconds, to wait for an image to have status `available`.
    required: false
    type: int
requirements:
- python >= 3
short_description: Manage a Linode MySQL database.
"""
EXAMPLES = r"""
- name: Create a basic MySQL database
  linode.cloud.database_mysql:
    label: my-db
    region: us-east
    engine: mysql/8.0.30
    type: g6-standard-1
    allow_list:
    - 0.0.0.0/0
    state: present
- name: Create a complex 3 node MySQL database
  linode.cloud.database_mysql:
    label: my-db
    region: us-east
    engine: mysql/8.0.30
    type: g6-standard-1
    allow_list:
    - 0.0.0.0/0
    encrypted: true
    cluster_size: 3
    replication_type: semi_synch
    ssl_connection: true
    state: present
- name: Delete a MySQL database
  linode.cloud.database_mysql:
    label: my-db
    state: absent
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
  description: The root username and password for an accessible Managed MySQL Database.
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
    engine: mysql
    hosts:
      primary: lin-123-456-mysql-mysql-primary.servers.linodedb.net
      secondary: lin-123-456-mysql-primary-private.servers.linodedb.net
    id: 123
    label: example-db
    port: 3306
    region: us-east
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
    version: 8.0.30
  type: dict
ssl_cert:
  description: The SSL CA certificate for an accessible Managed MySQL Database.
  returned: always
  sample:
  - ca_certificate: LS0tLS1CRUdJ...==
  type: dict
"""


class Module(LinodeModuleBase):
    """Module for creating and destroying Linode Databases"""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "database": None,
            "backups": None,
            "credentials": None,
            "ssl_cert": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
            required_one_of=[("state", "label")],
            required_if=[
                ("state", "present", ["region", "engine", "type"], True)
            ],
        )

    def _get_database_by_label(self, label: str) -> Optional[MySQLDatabase]:
        try:
            resp = [
                db
                for db in self.client.database.mysql_instances()
                if db.label == label
            ]

            return resp[0]
        except IndexError:
            return None
        except Exception as exception:
            return self.fail(
                msg="failed to get database {0}: {1}".format(label, exception)
            )

    @staticmethod
    def _wait_for_database_status(
        database: MySQLDatabase, status: Set[str], step: int, timeout: int
    ) -> None:
        def condition_func() -> bool:
            database._api_get()
            return database.status in status

        poll_condition(condition_func, step, timeout)

    def _create_database(self) -> Optional[MySQLDatabase]:
        params = self.module.params

        create_params = {
            "allow_list",
            "cluster_size",
            "encrypted",
            "replication_type",
            "ssl_connection",
        }

        additional_args = {
            k: v
            for k, v in params.items()
            if k in create_params and k is not None
        }

        try:
            return self.client.database.mysql_create(
                params.get("label"),
                params.get("region"),
                params.get("engine"),
                params.get("type"),
                **additional_args,
            )
        except ApiError as err:
            return self.fail(
                msg="Failed to create database: {}".format(
                    "; ".join(err.errors)
                )
            )

    def _update_database(self, database: MySQLDatabase) -> None:
        try:
            database._api_get()

            params = filter_null_values(self.module.params)

            # Engine is input as a slug
            if "engine" in params:
                params["engine"] = params["engine"].split("/")[0]

            try:
                changed_fields = handle_updates(
                    database, params, MUTABLE_FIELDS, self.register_action
                )
            except Exception as err:
                self.fail(msg="Failed to update database: {}".format(err))

            # We only want to wait on fields that trigger an update
            if len(changed_fields) > 0 and self.module.params["wait"]:
                try:
                    self._wait_for_database_status(database, {"updating"}, 1, 4)
                except polling.TimeoutException:
                    # Only certain field updates will trigger an update event.
                    # Assume the database will not enter an updating status
                    # if the status has not updated at this point.
                    pass
                except Exception as err:
                    self.fail(
                        msg="failed to wait for database updating: {}".format(
                            err
                        )
                    )

                try:
                    self._wait_for_database_status(database, {"active"}, 4, 240)
                except Exception as err:
                    self.fail(
                        msg="failed to wait for database active: {}".format(err)
                    )
        except ApiError as err:
            self.fail(
                msg="Failed to update database: {}".format(
                    "; ".join(err.errors)
                )
            )

    def _write_result(self, database: MySQLDatabase) -> None:
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

    def _handle_present(self) -> None:
        params = self.module.params

        label = params.get("label")

        database = self._get_database_by_label(label)

        # Create the database if it does not already exist
        if database is None:
            database = self._create_database()
            self.register_action("Created database {0}".format(label))

        if params.get("wait"):
            try:
                self._wait_for_database_status(
                    database, {"active"}, 4, self._timeout_ctx.seconds_remaining
                )
            except Exception as err:
                self.fail(
                    msg="failed to wait for database active: {}".format(err)
                )

        self._update_database(database)

        self._write_result(database)

    def _handle_absent(self) -> None:
        label: str = self.module.params.get("label")

        database = self._get_database_by_label(label)

        if database is not None:
            self._write_result(database)

            database.delete()
            self.register_action("Deleted database {0}".format(label))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for MySQL module"""

        try:
            validate_shared_db_input(self.module.params)
        except ValueError as err:
            self.fail(msg="Invalid param: {}".format(err))

        state = kwargs.get("state")

        if state == "absent":
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the database_mysql module"""
    Module()


if __name__ == "__main__":
    main()
