# SR CS port

SR和CS port是SWC设计中主要使用的两种port,分别用于swc间数据的传递及服务的调用。

在使用两种port时,需要经过两个步骤：
1. port interface 定义:类似面向对象语言中的类的定义;
2. port实例化,即需要在swc中基于interface实例化port,创建对应的port prototype.所以对于一个port interface可以有实例化多个port prototype.

![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/swcab_port.png)
## SR