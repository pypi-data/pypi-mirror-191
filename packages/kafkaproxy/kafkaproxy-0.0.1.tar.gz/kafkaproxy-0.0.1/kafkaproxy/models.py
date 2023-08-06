"""数据模型模块.

定义模块使用到的数据模型.
"""
from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional, Sequence, Tuple


class KafkaType(Enum):
    Kafka = auto()
    AioKafka = auto()
    ConfluentKafka = auto()


class KafkaAutoOffsetReset(Enum):
    earliest = auto()
    latest = auto()
    error = auto()


@dataclass
class ConsumerRecord:
    topic: str
    "The topic this record is received from"

    partition: int
    "The partition from which this record is received"

    offset: int
    "The position of this record in the corresponding Kafka partition."

    timestamp: int
    "The timestamp of this record"

    timestamp_type: int
    "The timestamp type of this record"

    key: Optional[bytes]
    "The key (or `None` if no key is specified)"

    value: Optional[bytes]
    "The value"

    checksum: int
    "Deprecated"

    serialized_key_size: int
    "The size of the serialized, uncompressed key in bytes."

    serialized_value_size: int
    "The size of the serialized, uncompressed value in bytes."

    headers: Sequence[Tuple[str, bytes]]
    "The headers"
