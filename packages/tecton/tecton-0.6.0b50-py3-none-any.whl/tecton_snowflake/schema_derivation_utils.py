import json
from typing import List

import pendulum

from tecton_core import materialization_context
from tecton_core import schema_derivation_utils as core_schema_derivation_utils
from tecton_core import specs
from tecton_proto.args import data_source_pb2
from tecton_proto.args import feature_view_pb2
from tecton_proto.args import virtual_data_source_pb2
from tecton_proto.common import schema_pb2
from tecton_proto.common import spark_schema_pb2
from tecton_snowflake import pipeline_helper
from tecton_snowflake import snowflake_type_utils
from tecton_snowflake.utils import format_sql


def get_data_source_schema_sql(ds_args: data_source_pb2.SnowflakeDataSourceArgs) -> str:
    """Return the SQL used to query the data source provided."""
    if ds_args.HasField("table"):
        full_table_name = f"{ds_args.database}.{ds_args.schema}.{ds_args.table}"
        sql_str = f"SELECT * FROM {full_table_name};"
    elif ds_args.HasField("query"):
        sql_str = f"{ds_args.query}"
    else:
        raise ValueError("A Snowflake source must have one of 'query' or 'table' set")
    return format_sql(sql_str)


def get_snowflake_schema(
    ds_args: virtual_data_source_pb2.VirtualDataSourceArgs, connection: "snowflake.connector.Connection"
) -> spark_schema_pb2.SparkSchema:
    """Derive schema for snowflake data source on snowflake compute.

    This method is used for notebook driven development.
    The logic should mirror logic in resolveBatch() in SnowflakeDDL.kt.
    """
    cur = connection.cursor()

    sql_str = get_data_source_schema_sql(ds_args.snowflake_ds_config)
    cur.execute(sql_str)
    # Get the schema from the previously ran query
    query_id = cur.sfqid
    cur.execute(f"DESCRIBE RESULT '{query_id}';")
    schema_list = cur.fetchall()  # TODO: use fetch_pandas_all() once it supports describe statements

    proto = spark_schema_pb2.SparkSchema()
    for row in schema_list:
        # schema returned is in the form (name, type,...)
        name = row[0]
        proto_field = proto.fields.add()
        proto_field.name = name
        proto_field.structfield_json = json.dumps({"name": name, "type": row[1], "nullable": True, "metadata": {}})
    return proto


def get_feature_view_view_schema(
    feature_view_args: feature_view_pb2.FeatureViewArgs,
    transformation_specs: List[specs.TransformationSpec],
    data_source_specs: List[specs.DataSourceSpec],
    connection: "snowflake.connector.Connection",
) -> schema_pb2.Schema:
    """Compute the Feature View view schema.

    This method is used for notebook driven development.
    The logic should mirror logic in resolve() in SnowflakeDDL.kt.
    """
    cur = connection.cursor()

    # Create a default materialization context for the feature view.
    _tecton_materialization_context = materialization_context.BoundMaterializationContext._create_internal(
        pendulum.from_timestamp(0, pendulum.tz.UTC),
        pendulum.datetime(2100, 1, 1),
        pendulum.Duration(),
    )

    sql_str = pipeline_helper.pipeline_to_sql_string(
        feature_view_args.pipeline,
        data_source_specs,
        transformation_specs,
        materialization_context=_tecton_materialization_context,
    )
    cur.execute(sql_str)
    # Get the schema from the previously ran query
    query_id = cur.sfqid
    cur.execute(f"DESCRIBE RESULT '{query_id}';")
    schema_list = cur.fetchall()  # TODO: use fetch_pandas_all() once it supports describe statements

    columns = []
    for row in schema_list:
        # schema returned is in the form (name, type,...)
        name = row[0]
        raw_snowflake_type = row[1].split("(")[
            0
        ]  # ex. a string type is returned as VARCHAR(16777216) from snowflake. The raw_snowflake_type field expects VARCHAR.
        tecton_type = snowflake_type_utils.snowflake_type_to_tecton_type(raw_snowflake_type, name)
        column_proto = schema_pb2.Column()
        column_proto.CopyFrom(core_schema_derivation_utils.TECTON_TYPE_TO_COLUMN_TYPE[tecton_type])
        column_proto.name = name
        column_proto.raw_snowflake_type = raw_snowflake_type
        columns.append(column_proto)

    return schema_pb2.Schema(columns=columns)
