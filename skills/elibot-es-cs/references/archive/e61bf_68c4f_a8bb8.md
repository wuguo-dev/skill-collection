# CS机器人与西门子PLC的Profinet通讯配置

URL: https://docs.elibot.cn/cs/e61bf/68c4f/a8bb8
发布时间: 2026-01-12

# **1.  简介**



Profinet在自动化领域中是比较常见的总线协议，广泛应用于各种设备的控制，艾利特CS机器人支持做从站；本文介绍了西门子PLC通过博途软件与机器人进行组态建立通讯的配置步骤、各插槽模块的定义以及注意事项



**2. Profinet规范**



## **2.1 GSD文件**



请登官网直接下载GDS文件[下载中心_机器人技术-艾利特官网](https://www.elibot.com/service/technical?kw=GSD&type1=&type2=&type3=&type4=&type5=&wd=1&tp=1)



解压后如下：



![](https://wdcdn.qpic.cn/MTY4ODg1MTI2MzE5MDc3MQ_439427_RqEyrEVU0NUSzVdc_1784894928?w=730&h=110&type=image/png)



**2.45 版本 GSD**



● 仅支持在 TIA Portal V20 中使用，无法在任何低于 V20 的版本中导入。



**2.42 版本 GSD**



● 可在 V18、V19、V20 中使用，且能向下兼容到 V18。



● 在 V17 及更低版本中无法使用。



**2.31 版本 GSD**



● 兼容性最广，可在 V12 SP1、V13、V13 SP1、V14、V14 SP1、V15、V15.1、V16、V17、V18、V19、V20 中使用。



● 在 V12 及更低版本中无法使用。



![](https://wdcdn.qpic.cn/MTY4ODg1ODMwNDM1NDE2NQ_109643_aoD6mnMoszYl0O7w_1769579708?w=1838&h=942&type=image/png)



## **2.2 插槽**



Profinet IO 设备总共有 10 个插槽，每个插槽对应一个模块，对于 10 个模块的简单说明下： R2P_State：机器人向 PLC 发送状态数据；



R2P_IO：机器人向 PLC 发送 IO 数据；



R2P_Joints：机器人向 PLC 发送关节数据；



R2P_TCP：机器人向 PLC 发送 TCP 数据；



R2P_BIT_REG：机器人向 PLC 发送输出布尔寄存器数据（0-63）；



R2P_INT_REG：机器人向 PLC 发送输出整型寄存器数据（0-23）；



R2P_FLOAT_REG：机器人向 PLC 发送输出浮点寄存器数据（0-23）；



P2R_IO：PLC 设置机器人 IO；



P2R_REG1：PLC 设置机器人输入整型寄存器；



P2R_REG2：PLC 设置机器人输入浮点型寄存器。



Profinet 收发数据是以字节流的方式，因此对每个模块都定义了一套数据格式



## **2.3用户定义的数据类型**



对于 PLC S7-1200 和 S7-1500 (PLC 固件 4.0 或更高版本)：Elite_datastruct.udt



# **3. Profinet配置方法**



## **3.1 启用 Profinet 功能**



1.将机器人 FB1 网口接入PLC交换机，点击“配置> 通讯> Profinet”，进入 Profinet 界面，启用 Profinet 功能。如下图所示：**增加网口说明**



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_565052_Kt-ndiWIrxXT7WAa_1713858057?w=1686&h=1051&type=image/png)



2. profinet界面功能配置



每台机器都有一个默认的设备名称“elite-pnet”，当一台PLC同时与多台机器人连接时，用户需要对设备名称进行更改，确保每台机器人的设备名称是唯一的



![](https://wdcdn.qpic.cn/MTY4ODg1MTI2MzE5MDc3MQ_823871_zTb1A4K0F5mwFx4t_1782207756?w=1278&h=796&type=image/png)



3.当通讯异常时，如连接失败、PLC未连接，用户可根据模块的状态配置对应程序是否需要暂停或者停止，防止通信异常对程序逻辑造成影响



IO模块 => P2R_IO 线圈输入模块



寄存器模块1 => P2R_REG1 整型寄存器输入模块



寄存器模块2 => P2R_REG2 浮点型寄存器输入模块



![](https://wdcdn.qpic.cn/MTY4ODg1MTI2MzE5MDc3MQ_126312_Iuw1f3ldyDLfRkbT_1782208064?w=1274&h=797&type=image/png)



## **3.2 设置 Profinet**



1. 在 TIA Portal 中添加设管理通用站描述文件（GSD）：在菜单栏选择“选项> 管理通用站描述文件(GSD)”，如图 3-1（a）所示；然后选择对应 GSD 文 件所在的目录，并选择对应的 GSD 文件，点击安装，如图 3-1（b）所示。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_84416_WtsgpRSGTF6EB5Ah_1713858308?w=1911&h=995&type=image/png)



3-1（a）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_157009_G-PdoRV04ZPr9yH4_1713858366?w=1919&h=995&type=image/png)



3-1（b）



2. 在项目中添加设备并配置：



1）双击左侧项目树中的“设备和网络”，如图 3-2（a）所示；双击或拖拽右侧硬件目录 中，具体路径为：“其他现场设备> PROFINET IO> IO> ELITE> ELITE CS> Elite Robot CS Device”，如图 3-2（b）所示。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_210505_h9wzGlIGcDekwSME_1713860194?w=1920&h=1040&type=image/png)



3-2（a）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_491270_sZ1c1ga5iaKyTCg7_1713860447?w=1920&h=1032&type=image/png)



3-2（b）



2）将“Elite CS Device”与 PLC 连接，如图 3-3 所示。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_599106_hP4F1N7EE8BsOICw_1713860499?w=1920&h=995&type=image/png)



3-3



3）双击 PLC 网口以配置 PLC 网络，注意需要将 PLC网络IP配置为和机器人 FB1网络同一网段下，如图 3-4所示。



注意：FB1 网络可通过点击状态及菜单栏右侧的艾利特Logo ，选择“设置> 系统> 网络”去查看。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_53269_8NTuYXd6q7wsPMIj_1713862107?w=1920&h=1029&type=image/png)



3-4



4）双击“elite-dev“去配置 IP 和设备名称，注意此处 IP 应和机器人 FB1 网络 IP 保持一 致，如图 3-5（a）和图 3-5（b）所示。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_508677_dCZNdGOo0K8AEX6i_1713924238?w=1920&h=1026&type=image/png)



3-5（a）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_969560_y86Aw3V19PiGv3Oy_1713862164?w=1912&h=994&type=image/png)



3-5（b）



5）添加模块：选择右侧“硬件目录> 模块”，选择需要模块插入，本处插入所有十个模 块，如图 3-6 所示。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_52233_KLlK-JlP_A19Yg--_1713925673?w=1920&h=1026&type=image/png)



3-6



3. 导入数据类型：



左侧项目树中选择“外部源文件> 添加新的外部文件> Elite_datastruct.udt”，如图 3-7（a） 所示；右键“Elite_datastruct.udt> 从源生成块”，对弹窗点击确定，如图 3-7（b）所示；左侧 项目树中展开 PLC 数据类型，可看到相关数据类型，如图 3-7（c）所示



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_302780_JqItphHqOW7JC5hW_1713928547?w=1920&h=996&type=image/png)



3-7（a）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_981040_RlbZQPl1O3v8uFXP_1713928575?w=1920&h=993&type=image/png)



3-7（b）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_659456_v2uYy6FRbrQsD04B_1713928615?w=1920&h=995&type=image/png)



3-7（c）



4. 添加变量：



1）左侧项目树中选择 PLC 变量，可“添加新变量表”或者直接选择“默认变量表”。随 后便可在相应变量表中添加变量：填入名称和选择数据类型，如图 3-8（a）所示，想要获取机 器人的状态，则选择"Elite_R2P_State"类型。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_857717_xXe7Rh5bYsPJby43_1713928735?w=1920&h=997&type=image/png)



3-8（a）



2）左侧项目树中双击“设备和网络”并双击“elite-dev”选择插槽 1 中“R2P_State_1”， 选择“IO 变量”，记下第一个变量的地址，如图 3-8（b）所示，是“%I10.0”。 3）回到变量表中，将刚刚记录下的地址填入变量地址，如图 3-8（c）所示。以此类推，可 以将十个插槽中的变量添加。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_995274_sCQ5RR-Gl4JCOOsR_1713928799?w=1920&h=947&type=image/png)



3-8（b）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_25630_ibbqPqA82iy04o86_1713928813?w=1920&h=993&type=image/png)



3-8（c）



5. 编译并下载到 PLC 中，然后转到在线模式。



6. 在设备视图中右键设备选择“分配设备名称”，搜索并更改设备名称，如图 3-10（a）和 如图 3-10（b）所示。



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_245326_uaakIASjg9pYxhAx_1713928972?w=1227&h=661&type=image/png)



3-10（a）



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_360427_Ek7tfS5KREFh5wH6_1713929011?w=1232&h=687&type=image/png)



3-10（b）



## **3.3 ****监视变量**



配置完成后所有设备与模块都会有绿色对钩：



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_963996_0AH-dF_Xoh88Zf5X_1713929773?w=1112&h=723&type=image/png)



按照上面介添加完变量表后，可参照数据格式表格查看对应变量



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_490089_V5pOY7jE7tHEcfr__1713930053?w=1045&h=785&type=image/png)



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_374656_jhQCzv9OZDbrjVkz_1713930157?w=1040&h=777&type=image/png)



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_520807_ccIoeOKY8LUgfsy3_1713930178?w=1043&h=810&type=image/png)



除了在博途上监视以外，还可以在示教器端监视：



如下图所示，在插件寄存监视器中可以查看到布尔寄存器、整数寄存器、浮点寄存器，也可以在此模拟强制输出到PLC



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_889026_PMksLSK0abzieA2a_1714292164?w=1280&h=797&type=image/png)



寄存器监视插件的使用可按连接下载文档安装：[寄存器监控器插件 | ES/CS技术文档](https://docs.elibot.cn/cs/3b5a8/0ffe3/cd3ed)



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_431351_Jgyk-Z-BFzhQdNo6_1714292009?w=1252&h=801&type=image/png)



若要接收或发送整数、浮点数，请查阅脚本手册Profinet篇脚本指令。



可以在配置-IO-机器人IO设置页面自定义名称，定义好名称后可直接在任务里使用，无需脚本，如下图所示：



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_296297_9moMzsGAIvQc8XHU_1715061452?w=1283&h=797&type=image/png)



如下图，选择设置指令，选择配置好的整数寄存器输出名称：



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_21350_dDTldmCQJZA1hSfc_1715061639?w=1285&h=798&type=image/png)



直接设置整数寄存器输为999



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_456981_KFd4_F-XrFkEAFww_1715061739?w=1278&h=803&type=image/png)



也可以等待布尔量为高/低电平



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_616199_32eYxGw2Jinx-0p-_1715061908?w=1281&h=802&type=image/png)



**等待定义好的布尔寄存器为高**



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_884967_MZIgBSbX9wXwEGsq_1715061958?w=1282&h=796&type=image/png)



若要等待浮点寄存器或者整数寄存器为指定数值则需使用函数，如下图选择等待，下拉input快捷栏找到定义好的浮点/整数寄存器：



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_237438_aEkOxwmZC8XwtRQX_1715062551?w=1231&h=802&type=image/png)



等待浮点寄存器等于3.14：



![](https://wdcdn.qpic.cn/MTY4ODg1NTgxOTQ0NjAyOQ_18607_RjEL1AgOoJOkn3hB_1715062724?w=1246&h=802&type=image/png)



# **4. 常见问题解答**



1. PLC端将GSD文件导入配置完成后无法连接机器人？



需要检查博途里机器人的IP、设备名称是否一直，刷新周期是否设置过低，IO刷新周期时间8ms以上，看门狗周期时间8ms以上，连接多台机器人时需要保证IP、设备名称的唯一性



2. 重新更改插槽模块后无法通讯上



如果配置参数都没有问题，可以尝试重启机器人控制器



3. PLC偶发报连接超时或者看门狗超时，自己重连恢复



更新到最新的机器人应用软件，使用最新的GSD文件



4. 在使用profinet总线过程中，机器人包E17S1 RTSI看门狗报警



此问题一般是CPU过载导致，需要检查程序内有无死循环



5. 配置后PLC程序能正常通讯，但是PLC断电重启后通讯不上



PLC在组态时不能设置成自动分配IP和自动分配设备名称



** **
