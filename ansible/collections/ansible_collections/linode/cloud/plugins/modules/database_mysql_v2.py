#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains the implementation for the linode.cloud.database_mysql_v2 module."""

from __future__ import absolute_import, division, print_function

import copy
from typing import Any, Optional

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.database_mysql_v2 as docs
from ansible_collections.linode.cloud.plugins.module_utils.linode_common import (
    LinodeModuleBase,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_database_shared import (
    SPEC_FORK,
    SPEC_UPDATE_WINDOW_V2,
    call_protected_provisioning,
    wait_for_database_status,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import (
    global_authors,
    global_requirements,
)
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import (
    filter_null_values_recursive,
    handle_updates,
    mapping_to_dict,
    poll_condition,
    safe_find,
)
from ansible_specdoc.objects import (
    FieldType,
    SpecDocMeta,
    SpecField,
    SpecReturnValue,
)
from linode_api4 import MySQLDatabase

SPEC_ENGINE_CONFIG_MYSQL = {
    "connect_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The number of seconds that the mysqld server waits for a connect packet "
            + "before responding with Bad handshake."
        ],
    ),
    "default_time_zone": SpecField(
        type=FieldType.string,
        description=[
            "Default server time zone as an offset from UTC (from -12:00 to +12:00), "
            + "a time zone name, or 'SYSTEM' to use the MySQL server default."
        ],
    ),
    "group_concat_max_len": SpecField(
        type=FieldType.integer,
        description=[
            "The maximum permitted result length in bytes for the GROUP_CONCAT() function."
        ],
    ),
    "information_schema_stats_expiry": SpecField(
        type=FieldType.integer,
        description=["The time, in seconds, before cached statistics expire."],
    ),
    "innodb_change_buffer_max_size": SpecField(
        type=FieldType.integer,
        description=[
            "Maximum size for the InnoDB change buffer, "
            + "as a percentage of the total size of the buffer pool."
        ],
    ),
    "innodb_flush_neighbors": SpecField(
        type=FieldType.integer,
        description=[
            "Specifies whether flushing a page from the InnoDB buffer pool also "
            + "flushes other dirty pages in the same extent."
        ],
    ),
    "innodb_ft_min_token_size": SpecField(
        type=FieldType.integer,
        description=[
            "Minimum length of words that are stored in an InnoDB FULLTEXT index."
        ],
    ),
    "innodb_ft_server_stopword_table": SpecField(
        type=FieldType.string,
        description=[
            "This option is used to specify your own InnoDB FULLTEXT "
            + "index stopword list for all InnoDB tables."
        ],
    ),
    "innodb_lock_wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The length of time in seconds an InnoDB transaction waits "
            + "for a row lock before giving up."
        ],
    ),
    "innodb_log_buffer_size": SpecField(
        type=FieldType.integer,
        description=[
            "The size in bytes of the buffer that InnoDB uses to write to the log files on disk."
        ],
    ),
    "innodb_online_alter_log_max_size": SpecField(
        type=FieldType.integer,
        description=[
            "The upper limit in bytes on the size of the temporary log files "
            + "used during online DDL operations for InnoDB tables."
        ],
    ),
    "innodb_read_io_threads": SpecField(
        type=FieldType.integer,
        description=[
            "The number of I/O threads for read operations in InnoDB."
        ],
    ),
    "innodb_rollback_on_timeout": SpecField(
        type=FieldType.bool,
        description=[
            "When enabled a transaction timeout causes InnoDB to "
            + "abort and roll back the entire transaction."
        ],
    ),
    "innodb_thread_concurrency": SpecField(
        type=FieldType.integer,
        description=[
            "Defines the maximum number of threads permitted inside of InnoDB."
        ],
    ),
    "innodb_write_io_threads": SpecField(
        type=FieldType.integer,
        description=[
            "The number of I/O threads for write operations in InnoDB."
        ],
    ),
    "interactive_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The number of seconds the server waits for activity on an "
            + "interactive connection before closing it."
        ],
    ),
    "internal_tmp_mem_storage_engine": SpecField(
        type=FieldType.string,
        description=[
            "The storage engine for in-memory internal temporary tables."
        ],
        choices=["TempTable", "MEMORY"],
    ),
    "max_allowed_packet": SpecField(
        type=FieldType.integer,
        description=[
            "Size of the largest message in bytes that can be received by the server.",
            "Default is 67108864 (64M).",
        ],
    ),
    "max_heap_table_size": SpecField(
        type=FieldType.integer,
        description=[
            "Limits the size of internal in-memory tables.",
            "Also set tmp_table_size.",
            "Default is 16777216 (16M).",
        ],
    ),
    "net_buffer_length": SpecField(
        type=FieldType.integer,
        description=[
            "Start sizes of connection buffer and result buffer.",
            "Default is 16384 (16K).",
        ],
    ),
    "net_read_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The number of seconds to wait for more data from a connection "
            + "before aborting the read."
        ],
    ),
    "net_write_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The number of seconds to wait for a block to be written "
            + "to a connection before aborting the write."
        ],
    ),
    "sort_buffer_size": SpecField(
        type=FieldType.integer,
        description=[
            "Sort buffer size in bytes for ORDER BY optimization.",
            "Default is 262144 (256K).",
        ],
    ),
    "sql_mode": SpecField(
        type=FieldType.string,
        description=[
            "Global SQL mode.",
            "Set to empty to use MySQL server defaults.",
        ],
    ),
    "sql_require_primary_key": SpecField(
        type=FieldType.bool,
        description=[
            "Require primary key to be defined for new tables or old tables modified "
            + "with ALTER TABLE and fail if missing."
        ],
    ),
    "tmp_table_size": SpecField(
        type=FieldType.integer,
        description=[
            "Limits the size of internal in-memory tables.",
            "Also sets max_heap_table_size.",
            "Default is 16777216 (16M).",
        ],
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The number of seconds the server waits for activity on a "
            + "noninteractive connection before closing it."
        ],
    ),
}

SPEC_ENGINE_CONFIG = {
    "mysql": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_ENGINE_CONFIG_MYSQL,
        description=["MySQL specific configuration fields."],
    ),
    "binlog_retention_period": SpecField(
        type=FieldType.integer,
        description=[
            "The minimum amount of time in seconds to keep binlog entries before deletion.",
            "This may be extended for use cases like MySQL Debezium Kafka connector.",
        ],
    ),
}

SPEC = {
    "state": SpecField(
        type=FieldType.string,
        choices=["resume", "suspend", "present", "absent"],
        required=True,
        description=["The desired state of the Managed Database."],
    ),
    "allow_list": SpecField(
        type=FieldType.list,
        element_type=FieldType.string,
        description=[
            "A list of IP addresses and CIDR ranges that can access the Managed Database."
        ],
        editable=True,
    ),
    "cluster_size": SpecField(
        type=FieldType.integer,
        description=[
            "The number of Linode instance nodes deployed to the Managed Database."
        ],
        editable=True,
    ),
    "engine": SpecField(
        type=FieldType.string,
        description=["The Managed Database engine in engine/version format."],
        editable=True,
    ),
    "engine_config": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_ENGINE_CONFIG,
        description=[
            "Various parameters used to configure this database's underlying engine.",
            "NOTE: If a configuration parameter is not current accepted by this field, "
            + "configure using the linode.cloud.api_request module.",
        ],
        editable=True,
    ),
    "label": SpecField(
        type=FieldType.string,
        description=["The label of the Managed Database."],
    ),
    "region": SpecField(
        type=FieldType.string,
        description=["The region of the Managed Database."],
    ),
    "type": SpecField(
        type=FieldType.string,
        description=[
            "The Linode Instance type used by the Managed Database for its nodes."
        ],
        editable=True,
    ),
    "fork": SpecField(
        type=FieldType.dict,
        description=["Information about a database to fork from."],
        suboptions=SPEC_FORK,
    ),
    "updates": SpecField(
        type=FieldType.dict,
        suboptions=SPEC_UPDATE_WINDOW_V2,
        description=[
            "Configuration settings for automated patch "
            "update maintenance for the Managed Database."
        ],
        editable=True,
    ),
    "wait_timeout": SpecField(
        type=FieldType.integer,
        description=[
            "The maximum number of seconds a poll operation can take before "
            "raising an error."
        ],
        default=45 * 60,
    ),
}

SPECDOC_META = SpecDocMeta(
    description=[
        "Create, read, and update a Linode MySQL database.",
    ],
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
- Create, read, and update a Linode MySQL database.
module: database_mysql_v2
notes: []
options:
  allow_list:
    description:
    - A list of IP addresses and CIDR ranges that can access the Managed Database.
    elements: str
    required: false
    type: list
  cluster_size:
    description:
    - The number of Linode instance nodes deployed to the Managed Database.
    required: false
    type: int
  engine:
    description:
    - The Managed Database engine in engine/version format.
    required: false
    type: str
  engine_config:
    description:
    - Various parameters used to configure this database's underlying engine.
    - 'NOTE: If a configuration parameter is not current accepted by this field, configure
      using the linode.cloud.api_request module.'
    required: false
    suboptions:
      binlog_retention_period:
        description:
        - The minimum amount of time in seconds to keep binlog entries before deletion.
        - This may be extended for use cases like MySQL Debezium Kafka connector.
        required: false
        type: int
      mysql:
        description:
        - MySQL specific configuration fields.
        required: false
        suboptions:
          connect_timeout:
            description:
            - The number of seconds that the mysqld server waits for a connect packet
              before responding with Bad handshake.
            required: false
            type: int
          default_time_zone:
            description:
            - Default server time zone as an offset from UTC (from -12:00 to +12:00),
              a time zone name, or 'SYSTEM' to use the MySQL server default.
            required: false
            type: str
          group_concat_max_len:
            description:
            - The maximum permitted result length in bytes for the GROUP_CONCAT()
              function.
            required: false
            type: int
          information_schema_stats_expiry:
            description:
            - The time, in seconds, before cached statistics expire.
            required: false
            type: int
          innodb_change_buffer_max_size:
            description:
            - Maximum size for the InnoDB change buffer, as a percentage of the total
              size of the buffer pool.
            required: false
            type: int
          innodb_flush_neighbors:
            description:
            - Specifies whether flushing a page from the InnoDB buffer pool also flushes
              other dirty pages in the same extent.
            required: false
            type: int
          innodb_ft_min_token_size:
            description:
            - Minimum length of words that are stored in an InnoDB FULLTEXT index.
            required: false
            type: int
          innodb_ft_server_stopword_table:
            description:
            - This option is used to specify your own InnoDB FULLTEXT index stopword
              list for all InnoDB tables.
            required: false
            type: str
          innodb_lock_wait_timeout:
            description:
            - The length of time in seconds an InnoDB transaction waits for a row
              lock before giving up.
            required: false
            type: int
          innodb_log_buffer_size:
            description:
            - The size in bytes of the buffer that InnoDB uses to write to the log
              files on disk.
            required: false
            type: int
          innodb_online_alter_log_max_size:
            description:
            - The upper limit in bytes on the size of the temporary log files used
              during online DDL operations for InnoDB tables.
            required: false
            type: int
          innodb_read_io_threads:
            description:
            - The number of I/O threads for read operations in InnoDB.
            required: false
            type: int
          innodb_rollback_on_timeout:
            description:
            - When enabled a transaction timeout causes InnoDB to abort and roll back
              the entire transaction.
            required: false
            type: bool
          innodb_thread_concurrency:
            description:
            - Defines the maximum number of threads permitted inside of InnoDB.
            required: false
            type: int
          innodb_write_io_threads:
            description:
            - The number of I/O threads for write operations in InnoDB.
            required: false
            type: int
          interactive_timeout:
            description:
            - The number of seconds the server waits for activity on an interactive
              connection before closing it.
            required: false
            type: int
          internal_tmp_mem_storage_engine:
            choices:
            - TempTable
            - MEMORY
            description:
            - The storage engine for in-memory internal temporary tables.
            required: false
            type: str
          max_allowed_packet:
            description:
            - Size of the largest message in bytes that can be received by the server.
            - Default is 67108864 (64M).
            required: false
            type: int
          max_heap_table_size:
            description:
            - Limits the size of internal in-memory tables.
            - Also set tmp_table_size.
            - Default is 16777216 (16M).
            required: false
            type: int
          net_buffer_length:
            description:
            - Start sizes of connection buffer and result buffer.
            - Default is 16384 (16K).
            required: false
            type: int
          net_read_timeout:
            description:
            - The number of seconds to wait for more data from a connection before
              aborting the read.
            required: false
            type: int
          net_write_timeout:
            description:
            - The number of seconds to wait for a block to be written to a connection
              before aborting the write.
            required: false
            type: int
          sort_buffer_size:
            description:
            - Sort buffer size in bytes for ORDER BY optimization.
            - Default is 262144 (256K).
            required: false
            type: int
          sql_mode:
            description:
            - Global SQL mode.
            - Set to empty to use MySQL server defaults.
            required: false
            type: str
          sql_require_primary_key:
            description:
            - Require primary key to be defined for new tables or old tables modified
              with ALTER TABLE and fail if missing.
            required: false
            type: bool
          tmp_table_size:
            description:
            - Limits the size of internal in-memory tables.
            - Also sets max_heap_table_size.
            - Default is 16777216 (16M).
            required: false
            type: int
          wait_timeout:
            description:
            - The number of seconds the server waits for activity on a noninteractive
              connection before closing it.
            required: false
            type: int
        type: dict
    type: dict
  fork:
    description:
    - Information about a database to fork from.
    required: false
    suboptions:
      restore_time:
        description:
        - The database timestamp from which it was restored.
        required: false
        type: str
      source:
        description:
        - The instance id of the database that was forked from.
        required: false
        type: int
    type: dict
  label:
    description:
    - The label of the Managed Database.
    required: false
    type: str
  region:
    description:
    - The region of the Managed Database.
    required: false
    type: str
  state:
    choices:
    - resume
    - suspend
    - present
    - absent
    description:
    - The desired state of the Managed Database.
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
        description:
        - The maximum maintenance window time in hours.
        required: true
        type: int
      frequency:
        choices:
        - weekly
        default: weekly
        description:
        - The frequency at which maintenance occurs.
        required: false
        type: str
      hour_of_day:
        description:
        - The hour to begin maintenance based in UTC time.
        required: true
        type: int
    type: dict
  wait_timeout:
    default: 2700
    description:
    - The maximum number of seconds a poll operation can take before raising an error.
    required: false
    type: int
requirements:
- python >= 3
short_description: Create, read, and update a Linode MySQL database.
"""
EXAMPLES = r"""
- name: Create a basic MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    allow_list:
    - 0.0.0.0/0
    state: present
- name: Create a MySQL database with three nodes
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-standard-1
    cluster_size: 3
    allow_list:
    - 0.0.0.0/0
    state: present
- name: Create a MySQL database with an explicit maintenance schedule and engine configuration
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    engine_config:
      binlog_retention_period: 600
      mysql:
        connect_timeout: 20
    updates:
      duration: 4
      frequency: weekly
      hour_of_day: 16
      day_of_week: 4
    state: present
- name: Create a MySQL database forked from another database
  linode.cloud.database_mysql_v2:
    label: my-db
    region: us-mia
    engine: mysql/8
    type: g6-nanode-1
    fork:
      source: 12345
    state: present
- name: Delete a MySQL database
  linode.cloud.database_mysql_v2:
    label: my-db
    state: absent
"""
RETURN = r"""
credentials:
  description: The root username and password for an accessible Managed MySQL Database.
  returned: always
  sample:
  - password: s3cur3P@ssw0rd
    username: akmadmin
  type: dict
database:
  description: The database in JSON serialized form.
  returned: always
  sample:
  - allow_list:
    - 10.0.0.3/32
    cluster_size: 3
    created: '2025-02-10T20:10:20'
    encrypted: true
    engine: mysql
    engine_config:
      binlog_retention_period: 600
      mysql:
        connect_timeout: 20
    hosts:
      primary: a225891-akamai-prod-1798333-default.g2a.akamaidb.net
      standby: replica-a225891-akamai-prod-1798333-default.g2a.akamaidb.net
    id: 12345
    label: my-db
    members:
      172.104.207.136: primary
      194.195.112.177: failover
      45.79.126.72: failover
    oldest_restore_time: '2025-02-10T20:15:07'
    platform: rdbms-default
    port: 11876
    region: ap-west
    ssl_connection: true
    status: active
    total_disk_size_gb: 30
    type: g6-standard-1
    updated: '2025-02-10T20:25:55'
    updates:
      day_of_week: 4
      duration: 4
      frequency: weekly
      hour_of_day: 16
      pending: []
    used_disk_size_gb: 0
    version: 8.0.35
  type: dict
ssl_cert:
  description: The SSL CA certificate for an accessible Managed MySQL Database.
  returned: always
  sample:
  - ca_certificate: LS0tLS1CRUdJ...==
  type: dict
"""


class Module(LinodeModuleBase):
    """Module implementation for database_mysql_v2."""

    def __init__(self) -> None:
        self.module_arg_spec = SPECDOC_META.ansible_spec
        self.results = {
            "changed": False,
            "actions": [],
            "database": None,
            "ssl_cert": None,
            "credentials": None,
        }

        super().__init__(
            module_arg_spec=self.module_arg_spec,
        )

    def _create(self) -> MySQLDatabase:
        params = filter_null_values_recursive(
            {
                k: v
                for k, v in self.module.params.items()
                if k
                in [
                    "allow_list",
                    "cluster_size",
                    "engine",
                    "engine_config",
                    "fork",
                    "label",
                    "region",
                    "type",
                ]
            }
        )

        # This is necessary because `type` is a Python-reserved keyword
        if "type" in params:
            params["ltype"] = params.pop("type")

        create_poller = self.client.polling.event_poller_create(
            "database", "database_create"
        )

        database = self.client.database.mysql_create(**params)

        create_poller.set_entity_id(database.id)
        create_poller.wait_for_next_event_finished(
            timeout=self._timeout_ctx.seconds_remaining
        )

        wait_for_database_status(
            self.client,
            database,
            "active",
            timeout=self._timeout_ctx.seconds_remaining,
        )

        # The `updates` field is not currently supported in the POST
        # request body.
        updates = params.get("updates")
        if updates is not None:
            database.updates = params.get("updates")
            database.save()

            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        return database

    def _update(self, database: MySQLDatabase) -> None:
        database._api_get()

        params = copy.deepcopy(self.module.params)

        # The database PUT endpoint accepts `version` rather than `engine`
        engine = params.pop("engine", None)
        if engine is not None:
            engine_components = engine.split("/")

            if len(engine_components) < 2:
                raise ValueError(f"Invalid engine: {engine}")

            major_version = int(engine_components[1])

            # Evil hack to correct for the API returning a three-part value for the
            # `version` field while the user specifies the major version, while still
            # using handle_updates.
            #
            # If anyone can think of a better way to do this, please correct it :)
            if int(database.version.split(".")[0]) != major_version:
                params["version"] = major_version

        # The `updates` field is returned with an additional `pending` key that isn't
        # defined by the user, so we need to inject the actual value here.
        if "updates" in params and params["updates"] is not None:
            params["updates"]["pending"] = database.updates.pending

        # Apply updates
        updated_fields = handle_updates(
            database,
            params,
            {
                "label",
                "allow_list",
                "cluster_size",
                "engine_config",
                "updates",
                "type",
                "version",
            },
            self.register_action,
        )

        # NOTE: We don't poll for the database_update event here because it is not
        # triggered under all conditions.
        if len(updated_fields) > 0:
            wait_for_database_status(
                self.client,
                database,
                "active",
                timeout=self._timeout_ctx.seconds_remaining,
            )

        # Sometimes the cluster_size attribute doesn't update until shortly after
        # a resize operation
        if "cluster_size" in updated_fields:

            def __poll_condition() -> bool:
                database._api_get()
                return database.cluster_size == params["cluster_size"]

            poll_condition(
                __poll_condition,
                timeout=self._timeout_ctx.seconds_remaining,
                step=1,
            )

    def _populate_results(self, database: MySQLDatabase) -> None:
        database._api_get()

        self.results["database"] = database._raw_json
        self.results["credentials"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.credentials)
        )
        self.results["ssl_cert"] = call_protected_provisioning(
            lambda: mapping_to_dict(database.ssl)
        )

    def _handle_present(self) -> None:
        params = self.module.params

        result = safe_find(
            self.client.database.mysql_instances,
            MySQLDatabase.label == params.get("label"),
        )
        if result is None:
            result = self._create()
            self.register_action("Created MySQL database {0}".format(result.id))

        self._update(result)

        self._populate_results(result)

    def _handle_else(self, state: str) -> None:
        params = self.module.params

        database = safe_find(
            self.client.database.mysql_instances,
            MySQLDatabase.label == params.get("label"),
        )

        if database is not None:
            self._populate_results(database)

            if state == "suspend":
                self._handle_suspend(database)
            elif state == "resume":
                self._handle_resume(database)
            else:
                self._handle_absent(database)

    def _handle_absent(self, database: MySQLDatabase) -> None:
        database.delete()
        self.register_action(f"Deleted MySQL database {database.id}")

    def _handle_suspend(self, database: MySQLDatabase) -> None:
        database.suspend()
        self.register_action(f"Suspended MySQL database {database.id}")

    def _handle_resume(self, database: MySQLDatabase) -> None:
        database.resume()
        self.register_action(f"Resumed MySQL database {database.id}")

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for token module"""
        state = kwargs.get("state")

        if state == "present":
            self._handle_present()
        else:
            self._handle_else(state)

        return self.results


def main() -> None:
    """Constructs and calls the Linode MySQL database module"""
    Module()


if __name__ == "__main__":
    main()
