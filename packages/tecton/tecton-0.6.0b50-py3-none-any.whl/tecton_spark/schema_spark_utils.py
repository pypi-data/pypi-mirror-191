import pyspark.sql.types as spark_types

from tecton_core import schema_derivation_utils as core_schema_derivation_utils
from tecton_core.data_types import ArrayType
from tecton_core.data_types import BoolType
from tecton_core.data_types import DataType
from tecton_core.data_types import Float32Type
from tecton_core.data_types import Float64Type
from tecton_core.data_types import Int32Type
from tecton_core.data_types import Int64Type
from tecton_core.data_types import StringType
from tecton_core.data_types import StructType
from tecton_core.data_types import TimestampType
from tecton_core.schema import Schema
from tecton_proto.common.schema_pb2 import Schema as SchemaProto


# Keep in sync with DataTypeUtils.kt and tecton_core/schema_derivation_utils. . Use "simple strings" as the keys so that fields like "nullable" are ignored.
SPARK_TYPE_SIMPLE_STRING_TO_TECTON_TYPE = {
    spark_types.StringType().simpleString(): StringType(),
    spark_types.LongType().simpleString(): Int64Type(),
    spark_types.DoubleType().simpleString(): Float64Type(),
    spark_types.BooleanType().simpleString(): BoolType(),
    spark_types.IntegerType().simpleString(): Int32Type(),
    spark_types.TimestampType().simpleString(): TimestampType(),
    # Array types.
    spark_types.ArrayType(spark_types.LongType()).simpleString(): ArrayType(Int64Type()),
    spark_types.ArrayType(spark_types.FloatType()).simpleString(): ArrayType(Float32Type()),
    spark_types.ArrayType(spark_types.DoubleType()).simpleString(): ArrayType(Float64Type()),
    spark_types.ArrayType(spark_types.StringType()).simpleString(): ArrayType(StringType()),
}

# Map from simple (i.e non-complex) Tecton data types to Spark Types.
SIMPLE_TECTON_DATA_TYPE_TO_SPARK_DATA_TYPE = {
    Int32Type(): spark_types.IntegerType(),
    Int64Type(): spark_types.LongType(),
    Float32Type(): spark_types.FloatType(),
    Float64Type(): spark_types.DoubleType(),
    StringType(): spark_types.StringType(),
    BoolType(): spark_types.BooleanType(),
    TimestampType(): spark_types.TimestampType(),
}


def schema_from_spark(spark_schema: spark_types.StructType) -> Schema:
    proto = SchemaProto()
    for field in spark_schema:
        column = proto.columns.add()

        if field.dataType.simpleString() not in SPARK_TYPE_SIMPLE_STRING_TO_TECTON_TYPE:
            raise ValueError(
                f"Field {field.name} is of type {field.dataType.simpleString()}, which is not a supported type for features. "
                + f"Please change {field.name} to be one of our supported types: https://docs.tecton.ai/latest/faq/creating_and_managing_features.html"
            )
        tecton_type = SPARK_TYPE_SIMPLE_STRING_TO_TECTON_TYPE[field.dataType.simpleString()]
        column.CopyFrom(core_schema_derivation_utils.TECTON_TYPE_TO_COLUMN_TYPE[tecton_type])
        column.name = field.name

    return Schema(proto)


def spark_data_type_from_tecton_data_type(tecton_data_type: DataType) -> spark_types.DataType:
    if tecton_data_type in SIMPLE_TECTON_DATA_TYPE_TO_SPARK_DATA_TYPE:
        return SIMPLE_TECTON_DATA_TYPE_TO_SPARK_DATA_TYPE[tecton_data_type]
    elif isinstance(tecton_data_type, ArrayType):
        element_type = spark_data_type_from_tecton_data_type(tecton_data_type.element_type)
        return spark_types.ArrayType(element_type)
    elif isinstance(tecton_data_type, StructType):
        spark_struct = spark_types.StructType()
        for field in tecton_data_type.fields:
            spark_struct.add(field.name, spark_data_type_from_tecton_data_type(field.data_type))
        return spark_struct
    else:
        assert False, f"Unsupported type: {tecton_data_type}"


def schema_to_spark(schema: Schema) -> spark_types.StructType:
    ret = spark_types.StructType()
    for col_name, col_spark_data_type in column_name_spark_data_types(schema):
        ret.add(col_name, col_spark_data_type)
    return ret


def column_name_spark_data_types(schema: Schema):
    return [(c[0], spark_data_type_from_tecton_data_type(c[1])) for c in schema.column_name_and_data_types()]
