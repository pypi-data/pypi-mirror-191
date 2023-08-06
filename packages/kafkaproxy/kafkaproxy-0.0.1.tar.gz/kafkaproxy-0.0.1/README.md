# kafkaproxy

kafka生产者和消费者的代理工具.

代理对象用于推迟初始化.我们可以在需要的地方用代理对象的全局变量直接编写逻辑,避免被代理的对象来回在函数间传递.

## 特性

+ 支持代理`kafka-python`,`aiokafka`和`confluent-kafka`的生产者消费者对象.
+ 提供统一通用的生产者消费者接口包装

## 安装

+ 只安装本项目不安装被代理对象的依赖: `pip install kafkaproxy`
+ 安装本项目同时确定要代理的对象包为`kafka-python`: `pip install kafkaproxy[kafka]`
+ 安装本项目同时确定要代理的对象包为`aiokafka`: `pip install kafkaproxy[aio]`
+ 安装本项目同时确定要代理的对象包为`confluent-kafka`: `pip install kafkaproxy[confluent]`

## 使用

本项目支持代理3种kafka模块中的对应模块,使用枚举`KafkaType`中的取值在调用方法`initialize_from_addresses`初始化时指定.
代理对象除了原样代理对象外还提供了生产者和消费者的统一通用接口包装.
由于对应的方法是动态绑定的,因此如果需要他们的typehints可以用`typing.cast`将代理对象转化为对应的协议对象

+ 同步接口生产者使用`ProducerProtocol`
+ 异步接口生产者使用`AioProducerProtocol`
+ 同步接消费产者使用`ConsumerProtocol`
+ 异步接消费产者使用`AioConsumerProtocol`

> 代理`kafka-python`或`confluent-kafka`生产者

```python
from kafkaproxy import ProducerProxy, KafkaType, ProducerProtocol
from typing import cast
import time
kafkap = ProducerProxy()


def run() -> None:
    p = cast(ProducerProtocol, kafkap)
    with p.mount() as cli:
        for i in range(10):
            cli.publish("topic1", f"send {i}")
            time.sleep(0.1)


# kafkap.initialize_from_addresses("localhost:9094", kafka_type=KafkaType.ConfluentKafka, acks="all")
kafkap.initialize_from_addresses("localhost:9094", kafka_type=KafkaType.Kafka)
try:
    print("start publishing")
    run()
finally:
    print("stoped")
```

> 代理`kafka-python`或`confluent-kafka`消费者

```python
from kafkaproxy import ConsumerProxy, KafkaType, ConsumerProtocol
from typing import cast

kafkac = ConsumerProxy()


def run() -> None:
    c = cast(ConsumerProtocol, kafkac)
    with c.watch() as g:
        for record in g:
            print(record.value)


# kafkac.initialize_from_addresses("localhost:9094", "topic1", group_id="test2", kafka_type=KafkaType.Kafka)
kafkac.initialize_from_addresses("localhost:9094", "topic1", group_id="test2", kafka_type=KafkaType.ConfluentKafka)
try:
    print("start watching")
    run()
finally:
    print("stoped")

```

> 代理`aiokafka`生产者

```python
import asyncio
from kafkaproxy import ProducerProxy, KafkaType, AioProducerProtocol
from typing import cast

kafkap = ProducerProxy()


async def run() -> None:
    p = cast(AioProducerProtocol, kafkap)
    async with p.mount() as cli:
        for i in range(10):
            await cli.publish("topic1", f"send {i}")
            await asyncio.sleep(0.1)


async def main() -> None:
    kafkap.initialize_from_addresses("localhost:9094", kafka_type=KafkaType.AioKafka, acks="all")
    await run()


try:
    print("start watching")
    asyncio.run(main())
finally:
    print("stoped")

```

> 代理`aiokafka`消费者

```python
import asyncio
from kafkaproxy import ConsumerProxy, KafkaAutoOffsetReset, KafkaType, AioConsumerProtocol
from typing import cast

kafkac = ConsumerProxy()


async def run() -> None:
    c = cast(AioConsumerProtocol, kafkac)
    async with c.watch() as g:
        async for record in g:
            print(record.value)


async def main() -> None:
    kafkac.initialize_from_addresses("localhost:9094", "topic1", group_id="test2", kafka_type=KafkaType.AioKafka, auto_offset_reset=KafkaAutoOffsetReset.earliest)
    await run()


try:
    print("start watching")
    asyncio.run(main())
finally:
    print("stoped")

```