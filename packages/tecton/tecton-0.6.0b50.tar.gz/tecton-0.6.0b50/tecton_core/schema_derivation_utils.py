from tecton_core import aggregation_utils
from tecton_core import data_types as tecton_types
from tecton_core import errors
from tecton_proto.args import feature_view_pb2
from tecton_proto.common import column_type_pb2
from tecton_proto.common import schema_pb2


# Keep in sync with DataTypeUtils.kt. Use "simple strings" as the keys so that fields like "nullable" are ignored.
TECTON_TYPE_TO_COLUMN_TYPE = {
    tecton_types.StringType(): schema_pb2.Column(
        raw_spark_type="string",
        feature_server_type=column_type_pb2.COLUMN_TYPE_STRING,
        offline_data_type=tecton_types.StringType().proto,
        feature_server_data_type=tecton_types.StringType().proto,
    ),
    tecton_types.Int64Type(): schema_pb2.Column(
        raw_spark_type="long",
        feature_server_type=column_type_pb2.COLUMN_TYPE_INT64,
        offline_data_type=tecton_types.Int64Type().proto,
        feature_server_data_type=tecton_types.Int64Type().proto,
    ),
    tecton_types.Float64Type(): schema_pb2.Column(
        raw_spark_type="double",
        feature_server_type=column_type_pb2.COLUMN_TYPE_DOUBLE,
        offline_data_type=tecton_types.Float64Type().proto,
        feature_server_data_type=tecton_types.Float64Type().proto,
    ),
    tecton_types.BoolType(): schema_pb2.Column(
        raw_spark_type="boolean",
        feature_server_type=column_type_pb2.COLUMN_TYPE_BOOL,
        offline_data_type=tecton_types.BoolType().proto,
        feature_server_data_type=tecton_types.BoolType().proto,
    ),
    # Int32 has a different offline and feature server data type.
    tecton_types.Int32Type(): schema_pb2.Column(
        raw_spark_type="integer",
        feature_server_type=column_type_pb2.COLUMN_TYPE_INT64,
        offline_data_type=tecton_types.Int32Type().proto,
        feature_server_data_type=tecton_types.Int64Type().proto,
    ),
    # Timestamp type is special since it does not have a ColumnType.
    tecton_types.TimestampType(): schema_pb2.Column(
        raw_spark_type="timestamp",
        feature_server_type=column_type_pb2.COLUMN_TYPE_DERIVE_FROM_DATA_TYPE,
        offline_data_type=tecton_types.TimestampType().proto,
        feature_server_data_type=tecton_types.TimestampType().proto,
    ),
    # Array types.
    tecton_types.ArrayType(tecton_types.Int64Type()): schema_pb2.Column(
        raw_spark_type="long_array",
        feature_server_type=column_type_pb2.COLUMN_TYPE_INT64_ARRAY,
        offline_data_type=tecton_types.ArrayType(tecton_types.Int64Type()).proto,
        feature_server_data_type=tecton_types.ArrayType(tecton_types.Int64Type()).proto,
    ),
    tecton_types.ArrayType(tecton_types.Float32Type()): schema_pb2.Column(
        raw_spark_type="float_array",
        feature_server_type=column_type_pb2.COLUMN_TYPE_FLOAT_ARRAY,
        offline_data_type=tecton_types.ArrayType(tecton_types.Float32Type()).proto,
        feature_server_data_type=tecton_types.ArrayType(tecton_types.Float32Type()).proto,
    ),
    tecton_types.ArrayType(tecton_types.Float64Type()): schema_pb2.Column(
        raw_spark_type="double_array",
        feature_server_type=column_type_pb2.COLUMN_TYPE_DOUBLE_ARRAY,
        offline_data_type=tecton_types.ArrayType(tecton_types.Float64Type()).proto,
        feature_server_data_type=tecton_types.ArrayType(tecton_types.Float64Type()).proto,
    ),
    tecton_types.ArrayType(tecton_types.StringType()): schema_pb2.Column(
        raw_spark_type="string_array",
        feature_server_type=column_type_pb2.COLUMN_TYPE_STRING_ARRAY,
        offline_data_type=tecton_types.ArrayType(tecton_types.StringType()).proto,
        feature_server_data_type=tecton_types.ArrayType(tecton_types.StringType()).proto,
    ),
}


def _get_timestamp_field(feature_view_args: feature_view_pb2.FeatureViewArgs, view_schema: schema_pb2.Schema) -> str:
    timestamp_key = ""

    if feature_view_args.materialized_feature_view_args.HasField("timestamp_field"):
        timestamp_key = feature_view_args.materialized_feature_view_args.timestamp_field
    else:
        timestamp_fields = [
            column for column in view_schema.columns if column.offline_data_type == tecton_types.TimestampType().proto
        ]

        if len(timestamp_fields) != 1:
            raise errors.TectonValidationError(
                "The timestamp_field must be set on the Feature View or the feature view transformation output should contain only one and only one column of type Timestamp"
            )
        timestamp_key = timestamp_fields[0].name

    view_schema_column_names = [column.name for column in view_schema.columns]
    if timestamp_key not in view_schema_column_names:
        raise errors.TectonValidationError(
            f"Timestamp key {timestamp_key} not found in view schema. View schema has columns {','.join(view_schema_column_names)}"
        )
    return timestamp_key


def compute_materialization_schema_from_view_schema(
    view_schema: schema_pb2.Schema,
    feature_view_args: feature_view_pb2.FeatureViewArgs,
) -> schema_pb2.Schema:
    materialization_schema_columns = []
    view_schema_column_map = {column.name: column for column in view_schema.columns}

    # Add join key columns from view schema to materializaton schema.
    join_keys = []
    for entity in feature_view_args.entities:
        join_keys.extend(entity.join_keys)
    for join_key in join_keys:
        if join_key not in view_schema_column_map:
            raise errors.TectonValidationError(
                f"Join key {join_key} not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
            )
        materialization_schema_columns.append(view_schema_column_map[join_key])

    # Added column for timestamp.
    timestamp_key = _get_timestamp_field(feature_view_args, view_schema)
    materialization_schema_columns.append(view_schema_column_map[timestamp_key])

    # Add columns for aggregate features.
    added = []
    for aggregation in feature_view_args.materialized_feature_view_args.aggregations:
        if aggregation.column not in view_schema_column_map:
            raise errors.TectonValidationError(
                f"Column {aggregation.column} used for aggregations not found in view schema. View schema has columns {','.join(view_schema_column_map.keys())}"
            )
        input_column = view_schema_column_map[aggregation.column]

        is_continous = (
            feature_view_args.materialized_feature_view_args.stream_processing_mode
            == feature_view_pb2.StreamProcessingMode.STREAM_PROCESSING_MODE_CONTINUOUS
        )
        prefixes = aggregation_utils.get_materialization_aggregation_column_prefixes(
            aggregation.function.lower(), aggregation.function_params, is_continous
        )
        for prefix in prefixes:
            materialization_column_name = aggregation_utils.get_materialization_column_name(prefix, input_column.name)

            tecton_type = aggregation_utils.aggregation_prefix_to_tecton_type(prefix)
            if tecton_type is None:
                tecton_type = tecton_types.data_type_from_proto(input_column.offline_data_type)

            column_proto = schema_pb2.Column()
            column_proto.CopyFrom(TECTON_TYPE_TO_COLUMN_TYPE[tecton_type])
            column_proto.name = materialization_column_name

            if materialization_column_name not in added:
                materialization_schema_columns.append(column_proto)
                added.append(materialization_column_name)

    return schema_pb2.Schema(columns=materialization_schema_columns)
