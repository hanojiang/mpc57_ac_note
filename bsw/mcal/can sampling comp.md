# can 控制器采样点设置及波特率计算
## can控制器时钟选择

时钟定义在MCU模块中，如下图所示，EB中配置了几个参考时钟。
![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/mcu_clock.PNG)

然后在CAN的时钟ref中选择需要使用的时钟，如下图，选择了ClkRefPnt_SYS_CLK = 160Mhz。

![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/can_clock.PNG)

最后设置can控制器的波特率为500kbps。主要涉及以下几个参数：

1. Prescaller 预分频 32
2. 波特率 500 
3. propagation segment 5
4. phase segment1 2
5. phase segment2 2
6. synchronization segment:默认值为1.

![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/can_baudrate.PNG)

## 采样点与波特率计算

经典can segment如下图所示(来源自芯片手册)：

![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/can_segments.PNG)
由于芯片寄存器中的段参数设置位为实质段值减去1，所以图中，PROPSEG和PSEG1的和要加2，PSEG2要加1，而配置参数中就是实际值（详见EB CAN UM手册**AUTOSAR_MCAL_CAN_UM.pdf**，如下图 SEG1取值为1-8），即寄存器值加1的结果（寄存器值0-7）。因此，后续计算公式中的段值默认为加上1的结果。

![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/eb_seg1.PNG)
can采样点计算公式：
$$rate = \frac{1+propseg+pseg1}{1+propseg+pseg1+pseg2}$$

波特率计算公式为：
![](https://raw.githubusercontent.com/hanojiang/picgo_pic_bed/master/pic/bd_comp.PNG)
注意波特率公式中的段值为寄存器的值。

因此，当配置为图片中值时，波特率为：

$$bd = \frac{160}{32 \times (1 + 5 + 2 + 2)}=500 kbps $$