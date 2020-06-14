# iohwab cs接口调用分析
## swc框图

iohwab swc定义了读取前门状态的两个S接口和一个写灯状态S接口，SWC框图如下图所示：
![]()

## 生成代码分析
生成的代码涉及到一下几个文件：
> rte.c
> CtSaDoor.c
> rte_CtSaDoor.h
> CtCddIoHwAb.c

调用关系如下图所示：

![](./pic/iohwab_trace.PNG)

调用步骤如下：

1. event事件触发`RCtSaDoorReadDoor(&Rte_Instance_CpSaDoorFrontRight);`, `Rte_Instance_CpSaDoorFrontRight`为实例化的`struct Rte_CDS_CtSaDoor`。
2. RCtSaDoorReadDoor函数中调用 **`Rte_Call_<p>_<o> (C/S invocation)`**
3. 实质是调用结构体中的函数指针 `Rte_CallInst1_CtSaDoor_PpDoorIoHwAb_ReadChannel`。
4. `Rte_CallInst1_CtSaDoor_PpDoorIoHwAb_ReadChannel`中调用iohwab中的runable中的dio接口，写io值，实现灯状态改变。