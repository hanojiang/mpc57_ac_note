# SR CS port

SR和CS port是SWC设计中主要使用的两种port,分别用于swc间数据的传递及服务的调用。

## SR

SR类型的port,在定义时需要绑定传递的数据类型(应用数据类型IDT),且在实例化port后,需要对port传递数据的初始值进行设置.

## CS

CS类型的port,则需要在定义时确认绑定的operation,简单的说就是确定服务端可以提供的调用函数.

## port与runable

实例化的port必须和runable结合才能保证port有效的传递数据和函数调用. 具体的, 对于SR port, 需要在trigger 和access point 中分别设置触发条件和端口操作(access point其实决定了生成哪一些和port相关的RTE代码, 所以如果没有设置正确的access point, 即使连接了port间的connector,也不会生成相关RTE代码). CS端口的服务端,即service 端口无需显示设置trigger和access point, 而client 端可设置为 on operation invocation或on operation call return 触发和 invoke operations.
在使用两种port时,需要经过两个步骤：

1. port interface 定义:类似面向对象语言中的类的定义;
2. port实例化,即需要在swc中基于interface实例化port,创建对应的port prototype.所以对于一个port interface可以有实例化多个port prototype.

本篇文章以如下图所示 swc模型为例，梳理两种端口的使用及生成代码的差异。
![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/swcAandB.png)
**<center>SWC模型</center>**

## 模型说明

模型中共有两个SWC,分别为CpApSwcA和CpApSwcB(后续简称SWC A和 SWC B),其中各自的runnable及其配置类型如下：

- SWC A:
    * RunableA_0
        * trigger: 50 ms
        * access points: write data和 invoke operations如下图所示
        * PORT
            * send: PpEngSpeedA, 发送一个U16速度值
            * client: PpAddSumA(CheckSum port)

![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/swca_access_point.png)
**<center>RunableA_0 access points</center>**

- SWC B:
    * RunableB_0
        * trigger: on data reception
        * access points: read data
    * RunableB_1
        * trigger: On Operation Invocation
        * access points: NA
    * PORT
        * receive: PpEngSpeedB, 接收一个U16速度值
        * service: PpAddSumB(CheckSum port)

对于 CS端口CheckSum的设置如下，两个输入和一个输出：
![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/CS_PORT_interface.png)
**<center>CheckSum CS port 设置</center>**

## OS配置
OS配置的层级关系如下：
OS Cores -> OS Applications -> Tasks，实例中在 OsCore1 -> OsCore1.OsApplication_Trusted_Core1 ->Tasks中创建新的Task: My_Task,用于映射模型中的runnable。如下图所示，注意，对于RunnableA_0，由于是周期性触发，需要关联一个alarm事件，实质上就是设置一个定时器。对于RunnableB_1无需映射Task，因为其作为回调函数，只要RunnableA_0映射了Task即可，RunnableA_0中通过RTE间接调用RunnableB_1。

![](https://gitee.com/hzfy_haojiangwang/myPicBed/raw/master/swca_and_b_task.png)
**<center>Runable Task Mapping</center>**

## 生成代码分析

### 函数调用

在`Rte_OsApplication_Trusted_Core1.c`文件中对My_Task进行了实现，重点关注`RunnableA_0();`和`RunnableB_0();`分别由两个事件触发。
```c
TASK(My_Task) /* PRQA S 3408, 1503 */ /* MD_Rte_3408, MD_MSR_Unreachable */
{
  EventMaskType ev;
  EventMaskType evRun;

  for(;;)
  {
    (void)WaitEvent(Rte_Ev_Run_CpApMySwc_RCtApMySwcCode | Rte_Ev_Run_CpApSwcA_RunnableA_0); /* PRQA S 3417 */ /* MD_Rte_Os */
    (void)GetEvent(My_Task, &ev); /* PRQA S 3417 */ /* MD_Rte_Os */
    (void)ClearEvent(ev & (Rte_Ev_Run_CpApMySwc_RCtApMySwcCode | Rte_Ev_Run_CpApSwcA_RunnableA_0)); /* PRQA S 3417 */ /* MD_Rte_Os */

    if ((ev & Rte_Ev_Run_CpApMySwc_RCtApMySwcCode) != (EventMaskType)0)
    {
      /* START PRE RUNNABLE RCtApMySwcCode */
      /* read implicit data */
      *(&Rte_My_Task.Rte_RB.Rte_CtApMySwc_RCtApMySwcCode.Rte_PpDoorStateRearLeft_DeDoorState.value) = Rte_Signal_RearLeftDoor_omsg_RxCycle100_0_oCAN0_694e7b2f_Rx; /* PRQA S 1339, 2982 */ /* MD_Rte_1339, MD_Rte_2982 */
      /* STOP PRE RUNNABLE RCtApMySwcCode */
      /* call runnable */
      RCtApMySwcCode(); /* PRQA S 2987 */ /* MD_Rte_2987 */
    }

    if ((ev & Rte_Ev_Run_CpApSwcA_RunnableA_0) != (EventMaskType)0)
    {
      /* call runnable */
      RunnableA_0(); /* PRQA S 2987 */ /* MD_Rte_2987 */
    }

    (void)GetEvent(My_Task, &evRun); /* PRQA S 3417 */ /* MD_Rte_Os */
    if ((evRun & Rte_Ev_Run_CpApSwcB_RunnableB_0) != (EventMaskType)0)
    {
      (void)ClearEvent(Rte_Ev_Run_CpApSwcB_RunnableB_0); /* PRQA S 3417 */ /* MD_Rte_Os */

      /* call runnable */
      RunnableB_0(); /* PRQA S 2987 */ /* MD_Rte_2987 */
    }
  }
} /* PRQA S 6010, 6030, 6050, 6080 */ /* MD_MSR_STPTH, MD_MSR_STCYC, MD_MSR_STCAL, MD_MSR_STMIF */
```
### SR CS port RTE 分析

对于SWC A:
有两个RTE需要关注：
`Rte_Write_PpEngSpeedA_DeEngSpeed(uint16 data)`和`Rte_Call_PpAddSumA_CheckSum(uint16 argX, uint16 arg_Y, uint16 *arg_Z)`.其实可以看出模型access points直接关系到 RTE接口的生成。

```c
/**********************************************************************************************************************
 *
 * Runnable Entity Name: RunnableA_0
 *
 *---------------------------------------------------------------------------------------------------------------------
 *
 * Executed if at least one of the following trigger conditions occurred:
 *   - triggered on TimingEvent every 50ms
 *
 **********************************************************************************************************************
 *
 * Output Interfaces:
 * ==================
 *   Explicit S/R API:
 *   -----------------
 *   Std_ReturnType Rte_Write_PpEngSpeedA_DeEngSpeed(uint16 data)
 *
 * Client/Server Interfaces:
 * =========================
 *   Server Invocation:
 *   ------------------
 *   Std_ReturnType Rte_Call_PpAddSumA_CheckSum(uint16 argX, uint16 arg_Y, uint16 *arg_Z)
 *     Synchronous Server Invocation. Timeout: None
 *     Returned Application Errors: RTE_E_PiAddSum_E_NOT_OK
 *
 *********************************************************************************************************************/
/**********************************************************************************************************************
 * DO NOT CHANGE THIS COMMENT!           << Start of documentation area >>                  DO NOT CHANGE THIS COMMENT!
 * Symbol: RunnableA_0_doc
 *********************************************************************************************************************/


/**********************************************************************************************************************
 * DO NOT CHANGE THIS COMMENT!           << End of documentation area >>                    DO NOT CHANGE THIS COMMENT!
 *********************************************************************************************************************/

FUNC(void, CtApSwcA_CODE) RunnableA_0(void) /* PRQA S 0624, 3206 */ /* MD_Rte_0624, MD_Rte_3206 */
{
/**********************************************************************************************************************
 * DO NOT CHANGE THIS COMMENT!           << Start of runnable implementation >>             DO NOT CHANGE THIS COMMENT!
 * Symbol: RunnableA_0
 *********************************************************************************************************************/


/**********************************************************************************************************************
 * DO NOT CHANGE THIS COMMENT!           << End of runnable implementation >>               DO NOT CHANGE THIS COMMENT!
 *********************************************************************************************************************/
}
```

对于`Rte_Write_PpEngSpeedA_DeEngSpeed(uint16 data)`,通过函数的宏定义转换(`Rte_CtApSwcA.h`)：
```c
FUNC(Std_ReturnType, RTE_CODE) Rte_Write_CtApSwcA_PpEngSpeedA_DeEngSpeed(uint16 data);//Rte_CtApSwcA.h
/**********************************************************************************************************************
 * Rte_Write_<p>_<d> (explicit S/R communication with isQueued = false)
 *********************************************************************************************************************/
#  define Rte_Write_PpEngSpeedA_DeEngSpeed Rte_Write_CtApSwcA_PpEngSpeedA_DeEngSpeed
```
而函数`Rte_Write_CtApSwcA_PpEngSpeedA_DeEngSpeed(uint16 data)`的定义如下，直接对全局变量赋值(`Rte_OsApplication_Trusted_Core1.c`)：
```c
FUNC(Std_ReturnType, RTE_CODE) Rte_Write_CtApSwcA_PpEngSpeedA_DeEngSpeed(uint16 data) /* PRQA S 1505, 2982 */ /* MD_MSR_Rule8.7, MD_Rte_2982 */
{
  Std_ReturnType ret = RTE_E_OK; /* PRQA S 2981 */ /* MD_MSR_RetVal */

  Rte_CpApSwcA_PpEngSpeedA_DeEngSpeed = *(&data); /* PRQA S 1339, 2982 */ /* MD_Rte_1339, MD_Rte_2982 */
  /* scheduled trigger for runnables: RunnableB_0 */
  (void)SetEvent(My_Task, Rte_Ev_Run_CpApSwcB_RunnableB_0); /* PRQA S 3417 */ /* MD_Rte_Os */

  return ret;
} /* PRQA S 6010, 6030, 6050 */ /* MD_MSR_STPTH, MD_MSR_STCYC, MD_MSR_STCAL */
```
对于另一个RTE接口：`Rte_Call_PpAddSumA_CheckSum(uint16 argX, uint16 arg_Y, uint16 *arg_Z)`，宏定义如下：
```c
#  define Rte_Call_PpAddSumA_CheckSum RunnableB_1
```

所以就是 SWC B的RunnableB_1。

对于SWC B，RunnableB_0的RTE接口为：`Rte_Read_PpEngSpeedB_DeEngSpeed(uint16 *data)`,宏定义如下：
```c
/**********************************************************************************************************************
 * Rte_Read_<p>_<d> (explicit S/R communication with isQueued = false)
 *********************************************************************************************************************/
#  define Rte_Read_PpEngSpeedB_DeEngSpeed Rte_Read_CtApSwcB_PpEngSpeedB_DeEngSpeed
#  define Rte_Read_CtApSwcB_PpEngSpeedB_DeEngSpeed(data) (*(data) = Rte_CpApSwcA_PpEngSpeedA_DeEngSpeed, ((Std_ReturnType)RTE_E_OK))
```

由此，基本上对两种PORT及其生成代码有了简单的了解。
