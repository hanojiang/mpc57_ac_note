# 链接文件介绍

链接文件是嵌入式软件开发中不可或缺的一部分，其作用是在代码编译后，依赖链接文件中对存储划分和代码段的组织链接出最终的可执行文件。简单的说，就是将每个c文件对应的.o文件中的各段安装链接文件要求存放于指定的位置(flash, ram)。区别于不同的工具链，常见的链接文件如.ld、.lds等。

本篇文章以MPC 57X系列芯片为例，对ld文件的构成进行介绍。完整的链接文件主要包含两个部分， memory{}和section{}。

* memory{}：对存储区进行分区
* section{}： 确定.o文件中段(section, 如代码段.code, 数据段.data)的放置位置

## 1. memory介绍

```ld
MEMORY
{
   ResetWord : ORIGIN = 0x00F8C000 , LENGTH = 0x00000030 /* 48 Byte */
   FLASH : ORIGIN = 0x01000000 , LENGTH = 0x00570000 /* 5 MiB */
   STARTUP_STACK : ORIGIN = 0x40000000 , LENGTH = 0x00000C00 /* 3 KiB */
   SYSTEM_RAM : ORIGIN = 0x40000C00 , LENGTH = 0x000BF400 /* 765 KiB */
}
```

存储分区划分的格式为：**分区名 ： ORIGIN = 开始地址, LENGTH = 长度**，以上述ld代码为例，ResetWord为分区名，其起始地址为0x00F8C000， 占用存储长度为0x00000030， 也就是48个字节。该分区主要用于启动相关存储使用。FLASH分区主要用于代码和数据存放。STARTUP_STACK和SYSTEM_RAM主要用于ram空间的划分。关于分区存放内容必须要和section{}部分一起使用才有意义。

## 2. section介绍

![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/ld_section.png)

section各部分组成如上图。

* secname：指定段的名字。
* start_expression:指定该段的起始地址。
* attributes: 指定段的属性，如对齐 ALIGN、AT、CLEAR、NOLOAD等。
* contents: 指定段的内容。
* memory_block: 段分配的存储分区，也就是memory中定义的分区。

### 2.1 contents
以下面图片为例：
![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/section.png)
自定义的段.mydata包含了foo.o文件的.data段。接下来是两个.o文件的.data段(空格隔开)。还可以是库文件中.o文件中的.data段。

### 2.2 attributes
关于属性，可参考文档[^1]。
这里主要说明两个：

#### 2.2.1 ALIGN

ALIGN(value)属性将当前地址按value值对齐，其结果地址可通过下面公式计算：
**(. + value - 1) & ~(value - 1)**

#### 2.2.2 AT

AT属性指定一个表达式expr，该表达式指明该节将在内存中加载的地址。仅当该节链接到的地址与应加载该节的地址不同时，这才有意义。
![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/AT.png)

[^1]:ghs\comp_201516\manuals\build_ppc.pdf( MULTI: Building Applications for Embedded Power Architecture)
