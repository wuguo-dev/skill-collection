# 30004端口使用

URL: https://docs.elibot.cn/cs/88fdd/9bd1f/12e52/6aeba
发布时间: 2026-02-11

# 1. 简介



RTSI 全称为实时数据交互(Real-Time Sychronization Interface), 该协议提供了标准的TCP/IP 链接, 用于与外部程序进行实时的数据交互。RTSI 的网络端口为 30004。交互的数据内容例如：



- 输出：机器人输出整型寄存器的值、末端负载等



- 输入：机器人浮点输入寄存器、数字输入 IO 的状态设置



# 2. 操作流程



RTSI 分为协议检查、设置、同步循环三个步骤。



具体流程分为：



1.校验协议版本；



2.请求控制器的主版本，次版本，bug-fix 版本，编译版本



3.设置订阅需求(这里设置输出定阅和输入订阅)；



4.发送开始信号以开始同步循环;



5.循环接收控制器返回的数据包并解析出来。



### 2.1 校验协议版本



报文头：86(RTSI_REQUEST_PROTOCOL_VERSION)



上位机向控制柜发送数据格式：



数据总长度(2byte)+报文头(1byte)+协议版本(当前版本都为 01，2byte)



上位机收到控制柜返回的数据格式:



数据总长度(2byte)+报文头(1byte)+校验是否成功(成功为 1，失败为 0，1byte)



### 2.2 请求控制器的主版本，次版本，bug-fix 版本，编译版本



报文头：118(RTSI_GET_ELITECONTROL_VERSION)



上位机向控制柜发送数据格式：



数据总长度(2byte)+报文头(1byte)



上位机收到控制柜返回的数据格式:



数据总长度(2byte)+报文头(1byte)+主版本(4byte)+次版本(4byte)+ bug-fix 版本



(4byte)+编译版本(4byte)



### 2.3 设置订阅需求(这里设置输出定阅和输入订阅)



##### 2.3.1 订阅输出需求



报文头：79(RTSI_CONTROL_PACKAGE_SETUP_OUTPUTS)



上位机向控制柜发送数据格式：



数据总长度(2byte)+报文头(1byte)+输出频率(8byte)+订阅变量名(string 类型)



上位机收到控制柜返回的数据格式:



数据总长度(2byte)+报文头(1byte)+订阅 ID(1byte)+订阅变量名类型(string 类型)



##### 2.3.2 订阅输入需求



报文头：73(RTSI_CONTROL_PACKAGE_SETUP_INPUTS)



上位机向控制柜发送数据格式：



数据总长度(2byte)+报文头(1byte) +订阅变量名(string 类型)



上位机收到控制柜返回的数据格式:



数据总长度(2byte)+报文头(1byte)+订阅 ID(1byte)+订阅变量名类型(string 类型)



### 2.4 发送开始信号以开始”同步循环



报文头：83(RTSI_CONTROL_PACKAGE_START)



上位机向控制柜发送数据格式：



数据总长度(2byte)+报文头(1byte)



上位机收到控制柜返回的数据格式:



数据总长度(2byte)+报文头(1byte)+是否开始(1byte)



### 2.5 循环接收控制器返回的数据包



报文头：85(RTSI_DATA_PACKAGE)



上位机向控制柜发送数据格式(控制订阅输入时发送)：



数据总长度(2byte)+报文头(1byte)+订阅 ID(1byte)+值(bytes)



上位机收到控制柜返回的数据格式(循环接收订阅输出):



数据总长度(2byte)+报文头(1byte)+订阅 ID(1byte)+值(bytes)



说明：可以同时多次订阅输出和输入，每次增加订阅，ID 号会加 1，第一次订阅时 ID 号为 1，在收取订阅输出和控制订阅输入时，可以根据 ID 来区分属于哪次的订阅。



# 3. 示例



完整程序查看 **章节4 附件** 中 ***30004.py*** 文件



程序订阅输出和输入订阅如下



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0MTk0LCJwYXRoIjoiMjAyNjAxMTUtMjk4OTU4OC05Mmxwc3ciLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDEzOjA4OjAzLjk3NyswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--40d6be398eb6e6c78eb7f7b1d9a4d371c1f5429d39b9561a87fecb709668b01a/20260115-2989588-92lpsw)



运行打印如下



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0MTkzLCJwYXRoIjoiMjAyNjAxMTUtMzMyMjAwMS11czMyNGUiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDEzOjA4OjAzLjY4NiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--863c7ff3fc3b674e6ebc45985f296c97bc4164a344975b3339f39be1e7bc1807/20260115-3322001-us324e)



机器人数据



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0MTk1LCJwYXRoIjoiMjAyNjAxMTUtMzMyMjAwMS1weTJtMXciLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDEzOjA4OjAzLjg5OCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--b8430f781a7e02e933b29a537ab0c5d216520f553220c0f7d28b4c76507a6bf6/20260115-3322001-py2m1w)



# 4. 附录



python程序实例 ：



[30004.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjY4ODcxLCJwYXRoIjoiMzAwMDQucHkiLCJ0aW1lc3RhbXAiOiIyMDI2LTAzLTMwVDExOjIzOjA5LjExMSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--f0c500f90fee7e7ddc77b3e64dd311d2fbe0775b596ad9dd756480431c3860bd/30004.py?disposition=attachment)8.8 KB



RTSI订阅内容表：



[RTSI.md](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjY4ODcyLCJwYXRoIjoicnRzaS5tZCIsInRpbWVzdGFtcCI6IjIwMjYtMDMtMzBUMTE6MjM6MzUuNjM1KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--dd93dc3784420cbd0438b0d005e50d65ba6c2e4e7116eb55fc0493fd531008e5/rtsi.md?disposition=attachment)17.6 KB



#
