# 信号与端口映射

对于通过外部信号作为输入的端口，需要对signal和port 进行映射。主要工作有两步：

1. 外部端口的delegation，即标明该端口对应的数据为外部输入，如can 信号。
2. 数据映射，需要将port和can signal绑定，称为data mapping。

分别如下图所示：

![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/port_delegation.png)
**<center> delegation </center>**

![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/data%20mapping.png)
**<center> data mapping </center>**