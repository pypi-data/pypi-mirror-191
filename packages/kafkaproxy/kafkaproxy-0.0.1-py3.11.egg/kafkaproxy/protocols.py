"""kafka代理的协议模块."""
from typing import Callable, Optional, Tuple, Dict, Union, Protocol, List, ContextManager, Iterable, AsyncContextManager, AsyncIterable
from .models import ConsumerRecord


class ProducerProtocol(Protocol):
    """同步生产者协议"""

    def publish(self, topic: str, value: Union[str, bytes], *,
                key: Union[str, bytes, None] = None,
                partition: int = -1,
                timestamp: int = 0,
                headers: Union[Dict[str, bytes], List[Tuple[str, bytes]], None] = None,
                on_delivery: Optional[Callable] = None) -> None:
        """同步发布接口.

        Args:
            topic (str): 发布去的主题
            value (Union[str, bytes]): 发布的值
            key (Optional[Union[str, bytes]], optional): 发布的键. Defaults to None.
            partition (Optional[int], optional):  发布去的分区. Defaults to None.
            timestamp (Optional[int], optional): 发布ms级时间戳. Defaults to None.
            headers (Optional[Union[Dict[str, bytes], List[Tuple[str, bytes]]]], optional): 发布的数据头. Defaults to None.
            on_delivery (Optional[Callable], optional): 发布成功后的回调,仅对ConfluentKafka有效. Defaults to None.
        """

    def mount(self) -> ContextManager["ProducerProtocol"]:
        """同步挂载接口.

        提供一个管理回收连接资源的上下文管理器.

        Example:
            p = cast(ProducerProtocol, kafkap)
            with p.mount() as cli:
                cli.publish("topic1", f"send {i}")
                print("send ok")

        Yields:
            ProducerProtocol: 返回一个同步发布协议对象
        """


class AioProducerProtocol(Protocol):
    """异步生产者协议"""
    async def publish(self, topic: str, value: Union[str, bytes], *,
                      key: Optional[Union[str, bytes]] = None,
                      partition: Optional[int] = None,
                      timestamp: Optional[int] = None,
                      headers: Optional[Union[Dict[str, bytes], List[Tuple[str, bytes]]]] = None,) -> None:
        """异步发布接口.

        Args:
            topic (str): 发布去的主题
            value (Union[str, bytes]): 发布的值
            key (Optional[Union[str, bytes]], optional): 发布的键. Defaults to None.
            partition (Optional[int], optional):  发布去的分区. Defaults to None.
            timestamp (Optional[int], optional): 发布ms级时间戳. Defaults to None.
            headers (Optional[Union[Dict[str, bytes], List[Tuple[str, bytes]]]], optional): 发布的数据头. Defaults to None.
        """

    def mount(self) -> AsyncContextManager["AioProducerProtocol"]:
        """同步挂载接口.

        提供一个管理回收连接资源的上下文管理器.

        Example:
            p = cast(AioProducerProtocol, kafkap)
            async with p.mount() as cli:
                await cli.publish("topic1", f"send {i}")
                print("send ok")

        Yields:
            AioProducerProtocol: 返回一个异步发布协议对象
        """


class ConsumerProtocol(Protocol):
    """同步消费者的协议."""

    def watch(self) -> ContextManager[Iterable[ConsumerRecord]]:
        """同步监听接口.

        调用后获得一个管理启动关闭连接并且返回一个可迭代对象的上下文管理器.监听获取消息可以直接使用`for`实现.

        Example:
            c = cast(ConsumerProtocol, kafkac)
            with c.watch() as g:
                for record in g:
                    print(record.value)

        Yields:
            Iterable[ConsumerRecord]: 返回一个消息的可迭代对象
        """


class AioConsumerProtocol(Protocol):
    """异步消费者的协议."""

    def watch(self) -> AsyncContextManager[AsyncIterable[ConsumerRecord]]:
        """异步监听接口.

        调用后获得一个管理启动关闭连接并且返回一个异步可迭代对象的上下文管理器.监听获取消息可以直接使用`async for`实现.

        Example:
            c = cast(AioConsumerProtocol, kafkac)
            async with c.watch() as g:
                async for record in g:
                    print(record.value)

        Yields:
            AsyncIterable[ConsumerRecord]: 返回一个消息的异步可迭代对象
        """
