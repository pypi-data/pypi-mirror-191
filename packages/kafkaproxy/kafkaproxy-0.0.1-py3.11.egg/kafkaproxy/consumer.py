"""kafka的消费者代理模块."""
from contextlib import asynccontextmanager, contextmanager
from pyproxypattern import Proxy
from typing import Any, Optional, Dict, Generator, AsyncGenerator, AsyncIterable, Iterable, cast
from types import MethodType
from .models import KafkaType, KafkaAutoOffsetReset, ConsumerRecord


class ConsumerProxy(Proxy):
    """kafka消费者的代理类.

    支持aiokafka,confluent-kafka和kafka-python
    """
    __slots__ = ('instance', "_callbacks", "_instance_check", "_type", "watch")

    def __init__(self, *, addresses: Optional[str] = None, topics: Optional[str] = None,
                 client_id: Optional[str] = None, group_id: Optional[str] = None,
                 auto_offset_reset: KafkaAutoOffsetReset = KafkaAutoOffsetReset.latest,
                 kafka_type: KafkaType = KafkaType.Kafka, **conn_params: Any) -> None:
        """创建一个kafka消费者代理.

        本代理可以代理`aiokafka.AIOKafkaConsumer`,`confluent_kafka.Consumer`或`kafka.KafkaConsumer`.
        参数`conn_params`需要参考不同的文档:

        + `aiokafka.AIOKafkaConsumer`或`kafka.KafkaConsumer`: <https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html>
        + `confluent_kafka.Consumer`: <https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md>

        本代理提供了统一的接口`watch`用于监听消息队列;`stop`用于停止监听,

        Args:
            addresses (Optional[str], optional): 代理实例连接的地址. Defaults to None.
            topics (Optional[str], optional): 代理实例监听的主题. Defaults to None.
            client_id (Optional[str], optional): 指定代理实例的客户端id. Defaults to None.
            group_id (Optional[str], optional): 指定代理实例客户端所在的群组id. Defaults to None.
            auto_offset_reset (KafkaAutoOffsetReset, optional): 指定代理实例从什么偏移位置开始监听消息. Defaults to KafkaAutoOffsetReset.latest.
            kafka_type (KafkaType, optional): 指定kafka客户端类型,可以是`KafkaType.Kafka`,`KafkaType.AioKafka`,`KafkaType.ConfluentKafka`之一. Defaults to KafkaType.Kafka.
        """
        self._type: KafkaType = kafka_type
        super().__init__()
        self.attach_callback(self.regist_methods)
        if addresses and topics:
            instance = self.new_instance_from_addresses(
                addresses, topics,
                client_id=client_id, group_id=group_id,
                auto_offset_reset=auto_offset_reset,
                kafka_type=kafka_type, **conn_params
            )
            self.initialize(instance)

    def regist_methods(self, instance: Any) -> None:
        if self._type is KafkaType.AioKafka:
            self.watch = MethodType(_watch_async, self)
        else:
            self.watch = MethodType(_watch_sync, self)

    @property
    def type(self) -> KafkaType:
        """运行时获取本代理代理的对象类型"""
        if self.instance is None:
            raise NotImplemented
        return self._type

    def new_instance_from_addresses(self, addresses: str, topics: str, *,
                                    client_id: Optional[str] = None, group_id: Optional[str] = None,
                                    auto_offset_reset: KafkaAutoOffsetReset = KafkaAutoOffsetReset.latest,
                                    kafka_type: Optional[KafkaType] = None, **conn_params: Any) -> Any:
        configs: Dict[str, Any] = {}
        configs.update(**conn_params)
        if kafka_type is not None:
            self._type = kafka_type
        if self._type is KafkaType.ConfluentKafka:
            from confluent_kafka import Consumer
            configs.update({
                'bootstrap.servers': addresses,
                'auto.offset.reset': auto_offset_reset.name
            })
            if client_id is not None:
                configs.update({"client.id": client_id})
            if group_id is not None:
                configs.update({"group.id": group_id})
            return Consumer(configs)
        else:
            topiclist = topics.split(",")
            configs.update(bootstrap_servers=addresses.split(","), auto_offset_reset=auto_offset_reset.name)
            if client_id is not None:
                configs.update(client_id=client_id)
            if group_id is not None:
                configs.update(group_id=group_id)
            if self._type is KafkaType.AioKafka:
                from aiokafka import AIOKafkaConsumer
                return AIOKafkaConsumer(*topiclist, **configs)
            else:
                from kafka import KafkaConsumer
                return KafkaConsumer(*topiclist, **configs)

    def initialize_from_addresses(self, addresses: str, topics: str, *,
                                  client_id: Optional[str] = None, group_id: Optional[str] = None,
                                  auto_offset_reset: KafkaAutoOffsetReset = KafkaAutoOffsetReset.latest,
                                  kafka_type: Optional[KafkaType] = None, **conn_params: Any) -> None:
        """初始化一个kafka消费者代理对象.

        本代理可以代理`aiokafka.AIOKafkaConsumer`,`confluent_kafka.Consumer`或`kafka.KafkaConsumer`.
        参数`conn_params`需要参考不同的文档:

        + `aiokafka.AIOKafkaConsumer`或`kafka.KafkaConsumer`: <https://kafka-python.readthedocs.io/en/master/apidoc/KafkaConsumer.html>
        + `confluent_kafka.Consumer`: <https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md>

        Args:
            addresses (str): 代理实例连接的地址
            topics (str): 代理实例监听的主题
            client_id (Optional[str], optional): 指定代理实例的客户端id. Defaults to None.
            group_id (Optional[str], optional): 指定代理实例客户端所在的群组id. Defaults to None.
            auto_offset_reset (KafkaAutoOffsetReset, optional): 指定代理实例从什么偏移位置开始监听消息. Defaults to KafkaAutoOffsetReset.latest.
            kafka_type (Optional[KafkaType], optional): 指定kafka客户端类型,可以是`KafkaType.Kafka`,`KafkaType.AioKafka`,`KafkaType.ConfluentKafka`之一. Defaults to None.
        """
        instance = self.new_instance_from_addresses(
            addresses, topics,
            client_id=client_id, group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            kafka_type=kafka_type, **conn_params
        )
        self.initialize(instance)

    async def watch_aiokafka(self) -> AsyncGenerator[ConsumerRecord, None]:
        async for msg in self.instance:
            record = cast(ConsumerRecord, msg)
            yield record

    def watch_kafkapython(self) -> Generator[ConsumerRecord, None, None]:
        for msg in self.instance:
            record = ConsumerRecord(msg.topic, msg.partition, msg.offset, msg.timestamp, msg.timestamp_type,
                                    msg.key, msg.value, msg.checksum,
                                    msg.serialized_key_size, msg.serialized_value_size, msg.headers)
            yield record

    def watch_confluentkafka(self) -> Generator[ConsumerRecord, None, None]:
        while True:
            msg = self.instance.poll(timeout=1.0)
            if not msg:
                continue
            if msg.error():
                raise msg.error()
            else:
                self.instance.store_offsets(msg)
                tst, ts = msg.timestamp()
                key = msg.key()
                key_size = len(key) if key else -1
                value = msg.value()
                value_size = len(value) if value else -1
                record = ConsumerRecord(msg.topic(), msg.partition(), msg.offset(), ts, tst,
                                        key, value,
                                        -1, key_size, value_size, msg.headers())
                yield record


@asynccontextmanager
async def _watch_async(self: ConsumerProxy) -> AsyncGenerator[AsyncIterable[ConsumerRecord], None]:
    if self.instance is None:
        raise NotImplemented
    try:
        await self.instance.start()
        yield self.watch_aiokafka()
    finally:
        await self.instance.stop()


@contextmanager
def _watch_sync(self: ConsumerProxy) -> Generator[Iterable[ConsumerRecord], None, None]:
    if self.instance is None:
        raise NotImplemented
    try:
        if self.type is KafkaType.Kafka:
            yield self.watch_kafkapython()
        else:
            yield self.watch_confluentkafka()
    finally:
        self.instance.close()
