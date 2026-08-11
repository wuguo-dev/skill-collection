# Modbus客户端插件

URL: https://docs.elibot.cn/cs/3b5a8/66cb1/b5dca
发布时间: 2026-01-16

# 1. 简介



为了提升ModbusRTU在任务中使用的便捷性，减少用户直接使用脚本编程的情况，降低现场任务编写难度以及降低异常情况发生的概率，在和一些简单的外部ModbusRTU设备通信时，可以使用Modbus客户端插件简单快速的实现对外部设备的控制。



[ModbusClient-2.0.4.elico](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzEyMzM2LCJwYXRoIjoibW9kYnVzY2xpZW50LTIuMC40LmVsaWNvIiwidGltZXN0YW1wIjoiMjAyNi0wNy0xM1QxMToxMjozOC4zODErMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--85be6be402c13f1a6a22e4d1a6448a6210e225b8f41a23b4ac43bf348e55e8bf/modbusclient-2.0.4.elico?disposition=attachment)218.2 KB



# 2. 操作流程



## 2.1 插件的安装



[下载插件安装包后，按插件安装流程章节安装插件。](https://docs.elibot.cn/cs/3b5a8/7a799/ce642#heading-menu-h2-2)



## 2.2 插件的使用



工具I/O锁选择“ModbusClient”插件。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDcxLCJwYXRoIjoiMjAyNjAxMTYtMTI4Mzg3LXBrdzU5NCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTY6MzM6NTcuNzk2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--4bbb995f0a99b51c4355e57778571fe77c5b8ff9ddb7c801328389be0765407f/20260116-128387-pkw594)



### 2.2.1 从站参数设定



左侧导航栏配置 >> 插件 >> Modbus客户端 设置好从站的参数后点击连接； 端口选 /dev/ttyTCI0 。



注：如果端口已经连接，在选端口时会自动识别。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDYzLCJwYXRoIjoiMjAyNjAxMTYtMjQyLW8wNXVyeSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTY6MzM6NTUuNTk5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--9a4403c386a0361a3e459648fe7713171367602488180952c5ae3d6144db520c/20260116-242-o05ury)



### 2.2.2 指令添加



任务 >> 插件 >> Modbus，在任务树上添加Modbus插件节点 ；



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDY4LCJwYXRoIjoiMjAyNjAxMTYtMjE4LWJiZXVwayIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTY6MzM6NTcuMTgzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--b42c7e4e771b73ed38d95e923d62137ddfbf42adaae894dfb64da4b1d83cf635/20260116-218-bbeupk)



### 2.2.3 读取操作



在插件界面点击添加按钮来新增读取指令，输入正确的从站ID，在 功能码列里选择读的操作，例如“读保持寄存器”，然后在地址列输入读取的开始 地址，在数据列的方括号中输入要读取的寄存器个数。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDY2LCJwYXRoIjoiMjAyNjAxMTYtMTk0LWt4NDgzYiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTY6MzM6NTYuODYwKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--3121f3528a5990a162b40b7a2669947c76f36b4a265c55015966cb3e7a80924f/20260116-194-kx483b)



1、 选择变量，在变量列中选择要将读取到的数据赋值的变量，读取的返回值类型为列表。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDY1LCJwYXRoIjoiMjAyNjAxMTYtMjQyLXRjZnQwaSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTY6MzM6NTYuODE3KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--54053448d9ef838ee95ba5de520a68d8c762911c5be73bdb9c5472cd879b2efb/20260116-242-tcft0i)



### 2.2.4 写入操作



在插件界面点击添加按钮来新增写入指令，输入正确的从站ID，在 功能码列里选择写的操作，例如“写保持寄存器”，然后在地址列输入读取的开始 地址，在数据列的方括号中输入写入的数据，以逗号作为分割。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDY5LCJwYXRoIjoiMjAyNjAxMTYtMTI4Mzg3LWEwcTF6aCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTY6MzM6NTcuMjk5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--e778698df8d99477ceef3936064b69c196e73cbea8b7f83df279c133d1b2c734/20260116-128387-a0q1zh)



# 3. 常见问题解答



1. Modbus客户端插件目前支持末端modbusRTU、控制柜USB转RTU；若控制柜是标准控制柜，则支持控制柜485直连。



2. 添加插件后需要重启机器人后插件才激活。
