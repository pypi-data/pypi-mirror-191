"""kafka的生产者代理模块."""
from pyproxypattern import Proxy
from contextlib import asynccontextmanager, contextmanager
from typing import Dict, List, Tuple, Any, Optional, Union, Callable, Generator, AsyncGenerator
from .models import KafkaType
from types import MethodType


class ProducerProxy(Proxy):
    """kafka生产者的代理类.

    支持aiokafka,confluent-kafka和kafka-python
    """
    __slots__ = ('instance', "_callbacks", "_instance_check", "_type", "publish", "mount")

    def __init__(self, *, addresses: Optional[str] = None,
                 client_id: Optional[str] = None,
                 acks: Union[int, str] = 1,
                 kafka_type: KafkaType = KafkaType.Kafka, **conn_params: Any) -> None:
        """创建一个kafka生产者代理.

        本代理可以代理`aiokafka.AIOKafkaProducer`,`confluent_kafka.Producer`或`kafka.KafkaProducer`.
        参数`conn_params`需要参考不同的文档:

        + `aiokafka.AIOKafkaProducer`或`kafka.KafkaProducer`: <https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html>
        + `confluent_kafka.Producer`: <https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md>

        同时提供一个公共的发布接口`publish`和一个公共的关闭接口`stop`

        Args:
            addresses (Optional[str], optional): 代理实例连接的地址. Defaults to None.
            client_id (Optional[str], optional): 指定代理实例的客户端id. Defaults to None.
            acks (Union[int, str], optional): 指定kafka生产者客户端的消息到达确认策略,0为不确认,"all"为全部确认,其他正整数为需要确认的leader数量
            kafka_type (KafkaType, optional): 指定kafka客户端类型,可以是`KafkaType.Kafka`,`KafkaType.AioKafka`,`KafkaType.ConfluentKafka`之一. Defaults to KafkaType.Kafka.
        """
        self._type: KafkaType = kafka_type
        super().__init__()
        self.attach_callback(self.regist_methods)
        if addresses:
            instance = self.new_instance_from_addresses(
                addresses,
                client_id=client_id,
                acks=acks,
                kafka_type=kafka_type, **conn_params
            )
            self.initialize(instance)

    def regist_methods(self, instance: Any) -> None:
        if self._type is KafkaType.AioKafka:
            self.publish = MethodType(_publish_async, self)
            self.mount = MethodType(_mount_async, self)
        else:
            self.publish = MethodType(_publish_sync, self)
            self.mount = MethodType(_mount_sync, self)

    @property
    def type(self) -> KafkaType:
        """运行时获取本代理代理的对象类型"""
        if self.instance is None:
            raise NotImplemented
        return self._type

    def new_instance_from_addresses(self, addresses: str, *,
                                    client_id: Optional[str] = None, acks: Union[int, str] = 1,
                                    kafka_type: Optional[KafkaType] = None, **conn_params: Any) -> Any:
        configs: Dict[str, Any] = {}
        configs.update(**conn_params)
        if acks is not None:
            self
        if kafka_type is not None:
            self._type = kafka_type
        if self._type is KafkaType.ConfluentKafka:
            from confluent_kafka import Producer
            configs.update({
                'bootstrap.servers': addresses,
                'acks': acks
            })
            if client_id is not None:
                configs.update({"client.id": client_id})
            return Producer(configs)
        else:
            configs.update(bootstrap_servers=addresses.split(","), acks=acks)
            if client_id is not None:
                configs.update(client_id=client_id)
            if self._type is KafkaType.AioKafka:
                from aiokafka import AIOKafkaProducer
                return AIOKafkaProducer(**configs)
            else:
                from kafka import KafkaProducer
                return KafkaProducer(**configs)

    def initialize_from_addresses(self, addresses: str, *,
                                  client_id: Optional[str] = None, acks: Union[int, str] = 1,
                                  kafka_type: Optional[KafkaType] = None, **conn_params: Any) -> None:
        """本代理可以代理`aiokafka.AIOKafkaProducer`,`confluent_kafka.Producer`或`kafka.KafkaProducer`.
        参数`conn_params`需要参考不同的文档:

        + `aiokafka.AIOKafkaProducer`或`kafka.KafkaProducer`: <https://kafka-python.readthedocs.io/en/master/apidoc/KafkaProducer.html>
        + `confluent_kafka.Producer`: <https://github.com/confluentinc/librdkafka/blob/master/CONFIGURATION.md>

        Args:
            addresses (Optional[str], optional): 代理实例连接的地址. Defaults to None.
            client_id (Optional[str], optional): 指定代理实例的客户端id. Defaults to None.
            acks (Union[int, str], optional): 指定kafka生产者客户端的消息到达确认策略,0为不确认,"all"为全部确认,其他正整数为需要确认的leader数量
            kafka_type (KafkaType, optional): 指定kafka客户端类型,可以是`KafkaType.Kafka`,`KafkaType.AioKafka`,`KafkaType.ConfluentKafka`之一. Defaults to KafkaType.Kafka.
        """
        instance = self.new_instance_from_addresses(
            addresses,
            client_id=client_id,
            acks=acks,
            kafka_type=kafka_type, **conn_params
        )
        self.initialize(instance)


async def _publish_async(self: ProducerProxy, topic: str, value: Union[str, bytes], *,
                         key: Optional[Union[str, bytes]] = None,
                         partition: Optional[int] = None,
                         timestamp: Optional[int] = None,
                         headers: Optional[Union[Dict[str, bytes], List[Tuple[str, bytes]]]] = None,) -> None:
    if self._type is not KafkaType.AioKafka:
        raise NotImplemented
    else:
        await self.instance.send_and_wait(
            topic=topic,
            value=value.encode("utf-8") if isinstance(value, str) else value,
            key=key.encode("utf-8") if isinstance(key, str) else key,
            headers=headers,
            partition=partition,
            timestamp_ms=timestamp)


def acked(err: Any, msg: Any) -> None:
    """Called once for each message produced to indicate delivery result.

    confluent_kafka使用.
    Triggered by poll() or flush()
    """
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


def _publish_sync(self: ProducerProxy, topic: str, value: Union[str, bytes], *,
                  key: Optional[Union[str, bytes]] = None,
                  partition: Optional[int] = None,
                  timestamp: Optional[int] = None,
                  headers: Optional[Union[Dict[str, bytes], List[Tuple[str, bytes]]]] = None,
                  on_delivery: Optional[Callable] = None) -> None:
    if self._type is KafkaType.ConfluentKafka:
        cb = acked
        if on_delivery:
            cb = on_delivery
        self.instance.produce(topic=topic, value=value, key=key,
                              partition=partition if partition is not None else -1,
                              timestamp=timestamp if timestamp is not None else 0,
                              headers=headers, on_delivery=cb)
        self.instance.poll(0)

    else:
        f = self.instance.send(topic=topic,
                               value=value.encode("utf-8") if isinstance(value, str) else value,
                               key=key.encode("utf-8") if isinstance(key, str) else key,
                               headers=headers,
                               partition=partition,
                               timestamp_ms=timestamp)
        # print(f.get(timeout=60))


@contextmanager
def _mount_sync(self: ProducerProxy) -> Generator[ProducerProxy, None, None]:
    if self.instance is None:
        raise NotImplemented
    try:
        yield self
    finally:
        if self.type is KafkaType.Kafka:
            self.instance.flush()
            self.instance.close()
        else:
            self.instance.flush()


@asynccontextmanager
async def _mount_async(self: ProducerProxy) -> AsyncGenerator[ProducerProxy, None]:
    if self.instance is None:
        raise NotImplemented
    try:
        await self.instance.start()
        yield self
    finally:
        await self.instance.stop()
