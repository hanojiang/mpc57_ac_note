# SR CS port

SR和CS port是SWC设计中主要使用的两种port,分别用于swc间数据的传递及服务的调用。

在使用两种port时,需要经过两个步骤：

1. port interface 定义:类似面向对象语言中的类的定义;
2. port实例化,即需要在swc中基于interface实例化port,创建对应的port prototype.所以对于一个port interface可以有实例化多个port prototype.

![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/swcab_port.png)

## SR

SR类型的port,在定义时需要绑定传递的数据类型(应用数据类型IDT),且在实例化port后,需要对port传递数据的初始值进行设置.

## CS

CS类型的port,则需要在定义时确认绑定的operation,简单的说就是确定服务端可以提供的调用函数.

## port与runable

实例化的port必须和runable结合才能保证port有效的传递数据和函数调用. 具体的, 对于SR port, 需要在trigger 和access point 中分别设置触发条件和端口操作(access point其实决定了生成哪一些和port相关的RTE代码, 所以如果没有设置正确的access point, 即使连接了port间的connector,也不会生成相关RTE代码). CS端口的服务端,即service 端口无需显示设置trigger和access point, 而client 端可设置为 on operation invocation或on operation call return 触发和 invoke operations.
