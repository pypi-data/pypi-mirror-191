from __future__ import annotations

import enum
from typing import Any, List, Literal, Optional, Union, cast

import pyarrow as pa
from pydantic import BaseConfig, BaseModel, Field
from typing_extensions import Annotated

from chalk.utils.json import TJSON

__all__ = [
    "SerializedDType",
    "BaseSerializedDType",
    "deserialize_dtype_json",
    "serialize_pyarrow_dtype",
]


class DTypeCode(enum.IntEnum):
    # NULL = 1
    BOOL = 2
    INT8 = 3
    INT16 = 4
    INT32 = 5
    INT64 = 6
    UINT8 = 7
    UINT16 = 8
    UINT32 = 9
    UINT64 = 10
    FLOAT16 = 11
    FLOAT32 = 12
    FLOAT64 = 13
    TIME32 = 14  # time unit
    TIME64 = 15  # time unit
    TIMESTAMP = 16  # time unit, time zone
    DATE32 = 17
    DATE64 = 18
    DURATION = 19  # time unit
    BINARY = 20  # length
    STRING = 21
    LARGE_BINARY = 22
    LARGE_STRING = 23
    # Decimal is not yet supported by chalk
    # DECIMAL128 = 24  # precision, scale
    LIST = 25  # value type, size
    LARGE_LIST = 26  # value type
    STRUCT = 27  # fields


class TimeUnitCode(str, enum.Enum):
    SECOND = "s"
    MILLISECONDS = "ms"
    MICROSECONDS = "us"
    NANOSECONDS = "ns"


class BaseSerializedDType(BaseModel):
    type_code: DTypeCode

    def to_pyarrow_dtype(self) -> pa.DataType:
        raise NotImplementedError

    class Config(BaseConfig):
        use_enum_values = True


class SingletonDType(BaseSerializedDType):
    type_code: Literal[
        DTypeCode.BOOL,
        DTypeCode.INT8,
        DTypeCode.INT16,
        DTypeCode.INT32,
        DTypeCode.INT64,
        DTypeCode.UINT8,
        DTypeCode.UINT16,
        DTypeCode.UINT32,
        DTypeCode.UINT64,
        DTypeCode.FLOAT16,
        DTypeCode.FLOAT32,
        DTypeCode.FLOAT64,
        DTypeCode.DATE32,
        DTypeCode.DATE64,
        DTypeCode.STRING,
        DTypeCode.LARGE_STRING,
        DTypeCode.LARGE_BINARY,
    ]

    def to_pyarrow_dtype(self) -> pa.DataType:
        if self.type_code == DTypeCode.BOOL:
            return pa.bool_()
        try:
            return getattr(pa, self.type_code.name.lower())()
        except AttributeError:
            raise ValueError(f"Unsupported dtype: {self.type_code}") from None


class TimeUnitDType(BaseSerializedDType):
    type_code: Literal[DTypeCode.TIME32, DTypeCode.TIME64, DTypeCode.DURATION]
    time_unit: TimeUnitCode

    def to_pyarrow_dtype(self) -> pa.DataType:
        return getattr(pa, self.type_code.name.lower())(self.time_unit)

    class Config(BaseSerializedDType.Config):
        use_enum_values = True


class TimestampDType(BaseSerializedDType):
    type_code: Literal[DTypeCode.TIMESTAMP]
    time_unit: TimeUnitCode
    timezone: Optional[str]

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.timestamp(self.time_unit, self.timezone)


class BinaryDType(BaseSerializedDType):
    type_code: Literal[DTypeCode.BINARY]
    length: int

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.binary(self.length)


class ListDType(BaseSerializedDType):
    type_code: Literal[DTypeCode.LIST]
    inner_dtype: BaseSerializedDType
    length: int

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.list_(self.inner_dtype.to_pyarrow_dtype(), self.length)


class LargeListDType(BaseSerializedDType):
    type_code: Literal[DTypeCode.LARGE_LIST]
    inner_dtype: BaseSerializedDType

    def to_pyarrow_dtype(self) -> pa.DataType:
        return pa.large_list(self.inner_dtype.to_pyarrow_dtype())


class StructField(BaseModel):
    name: str
    dtype: BaseSerializedDType
    nullable: bool = True

    def to_pyarrow_dtype(self) -> pa.Field:
        return pa.field(self.name, self.dtype.to_pyarrow_dtype(), self.nullable)


class StructDType(BaseSerializedDType):
    type_code: Literal[DTypeCode.STRUCT]
    fields: List[StructField]

    def to_pyarrow_dtype(self) -> pa.Field:
        return pa.struct([x.to_pyarrow_dtype() for x in self.fields])


SerializedDType = Annotated[
    Union[SingletonDType, TimeUnitDType, TimestampDType, BinaryDType, ListDType, LargeListDType, StructDType],
    Field(discriminator="type_code"),
]


class _Deserializer(BaseModel):
    __root__: SerializedDType


def deserialize_dtype_json(dtype_json: TJSON) -> SerializedDType:
    deserializer = _Deserializer(__root__=cast(Any, dtype_json))
    return deserializer.__root__


def serialize_pyarrow_dtype(pa_dtype: pa.DataType) -> SerializedDType:
    if pa.types.is_boolean(pa_dtype):
        return SingletonDType(type_code=DTypeCode.BOOL)
    if pa.types.is_uint8(pa_dtype):
        return SingletonDType(type_code=DTypeCode.UINT8)
    if pa.types.is_uint16(pa_dtype):
        return SingletonDType(type_code=DTypeCode.UINT16)
    if pa.types.is_uint32(pa_dtype):
        return SingletonDType(type_code=DTypeCode.UINT32)
    if pa.types.is_uint64(pa_dtype):
        return SingletonDType(type_code=DTypeCode.UINT64)
    if pa.types.is_int8(pa_dtype):
        return SingletonDType(type_code=DTypeCode.INT8)
    if pa.types.is_int16(pa_dtype):
        return SingletonDType(type_code=DTypeCode.INT16)
    if pa.types.is_int32(pa_dtype):
        return SingletonDType(type_code=DTypeCode.INT32)
    if pa.types.is_int64(pa_dtype):
        return SingletonDType(type_code=DTypeCode.INT64)
    if pa.types.is_float16(pa_dtype):
        return SingletonDType(type_code=DTypeCode.FLOAT16)
    if pa.types.is_float32(pa_dtype):
        return SingletonDType(type_code=DTypeCode.FLOAT32)
    if pa.types.is_float64(pa_dtype):
        return SingletonDType(type_code=DTypeCode.FLOAT64)
    if pa.types.is_time32(pa_dtype):
        return TimeUnitDType(type_code=DTypeCode.TIME32, time_unit=TimeUnitCode(pa_dtype.unit))

    if pa.types.is_time64(pa_dtype):
        return TimeUnitDType(type_code=DTypeCode.TIME64, time_unit=TimeUnitCode(pa_dtype.unit))

    if pa.types.is_timestamp(pa_dtype):
        return TimestampDType(
            type_code=DTypeCode.TIMESTAMP,
            time_unit=TimeUnitCode(pa_dtype.unit),
            timezone=pa_dtype.tz,
        )

    if pa.types.is_date32(pa_dtype):
        return SingletonDType(type_code=DTypeCode.DATE32)
    if pa.types.is_date64(pa_dtype):
        return SingletonDType(type_code=DTypeCode.DATE64)
    if pa.types.is_duration(pa_dtype):
        return TimeUnitDType(type_code=DTypeCode.DURATION, time_unit=TimeUnitCode(pa_dtype.unit))

    if pa.types.is_large_string(pa_dtype):
        return SingletonDType(type_code=DTypeCode.LARGE_STRING)
    if pa.types.is_large_binary(pa_dtype):
        return SingletonDType(type_code=DTypeCode.LARGE_BINARY)
    if pa.types.is_fixed_size_binary(pa_dtype):
        return BinaryDType(type_code=DTypeCode.BINARY, length=pa_dtype.byte_width)
    if pa.types.is_binary(pa_dtype):
        return BinaryDType(type_code=DTypeCode.BINARY, length=-1)
    if pa.types.is_string(pa_dtype):
        return SingletonDType(type_code=DTypeCode.STRING)

    if pa.types.is_large_list(pa_dtype):
        return LargeListDType(type_code=DTypeCode.LARGE_LIST, inner_dtype=serialize_pyarrow_dtype(pa_dtype.value_type))
    if pa.types.is_fixed_size_list(pa_dtype):
        return ListDType(
            type_code=DTypeCode.LIST,
            inner_dtype=serialize_pyarrow_dtype(pa_dtype.value_type),
            length=pa_dtype.list_size,
        )

    if pa.types.is_list(pa_dtype):
        return ListDType(
            type_code=DTypeCode.LIST,
            inner_dtype=serialize_pyarrow_dtype(pa_dtype.value_type),
            length=-1,
        )

    if pa.types.is_struct(pa_dtype):
        schema = pa.schema(pa_dtype)
        return StructDType(
            type_code=DTypeCode.STRUCT,
            fields=[
                StructField(name=name, dtype=serialize_pyarrow_dtype(dtype))
                for (name, dtype) in zip(schema.names, schema.types)
            ],
        )

    raise ValueError(f"Unsupported dtype: {pa_dtype}")
