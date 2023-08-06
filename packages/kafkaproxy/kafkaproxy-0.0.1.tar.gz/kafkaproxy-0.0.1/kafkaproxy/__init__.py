"""kafka生产者和消费者的代理工具.

代理对象用于推迟初始化.我们可以在需要的地方用代理对象的全局变量直接编写逻辑,避免被代理的对象来回在函数间传递.
本项目支持代理3种kafka模块中的对应模块,使用枚举`KafkaType`中的取值在调用方法`initialize_from_addresses`初始化时指定.
代理对象除了原样代理对象外还提供了生产者和消费者的统一通用接口包装.
由于对应的方法是动态绑定的,因此如果需要他们的typehints可以用`typing.cast`将代理对象转化为对应的协议对象

+ 同步接口生产者使用`ProducerProtocol`
+ 异步接口生产者使用`AioProducerProtocol`
+ 同步接消费产者使用`ConsumerProtocol`
+ 异步接消费产者使用`AioConsumerProtocol`
"""

from .consumer import ConsumerProxy
from .producer import ProducerProxy
from .models import (
    ConsumerRecord,
    KafkaType,
    KafkaAutoOffsetReset
)

from .protocols import (
    ProducerProtocol,
    AioProducerProtocol,
    ConsumerProtocol,
    AioConsumerProtocol
)
