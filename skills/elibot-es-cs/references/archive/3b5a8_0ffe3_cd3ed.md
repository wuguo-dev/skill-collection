# 寄存器监控器插件

URL: https://docs.elibot.cn/cs/3b5a8/0ffe3/cd3ed
发布时间: 2026-01-21

# 1. 简介



CS机器人在与外部设备进行通讯时，通常会使用机器人内部的寄存器进行信息交互，机器人自带可查看modbus寄存器，关于布尔寄存器、整数寄存器、浮点数寄存器的查看可安装寄存器监控器插件进行查看，插件文件询问艾利特人员方可获得，存放至U盘内，并插入机器人示教器或控制柜USB接口。



如果是机器人和PLC进行Profinet或Ethernet/IP通讯，请务必安装此插件！



# 2. 操作流程



寄存器监视器插件安装地址：



[RegisterMonitor-1.3.elico](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjYxNDAxLCJwYXRoIjoicmVnaXN0ZXJtb25pdG9yLTEuMy5lbGljbyIsInRpbWVzdGFtcCI6IjIwMjYtMDMtMDNUMTY6MTA6NTEuMDAyKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--fce9733af5059ded6895b8493f39b66db383eb25786ac266248047d9beac08b5/registermonitor-1.3.elico?disposition=attachment)38.1 KB



## 2.1 插件的安装



[下载插件安装包后，按插件安装流程章节安装插件。](https://docs.elibot.cn/cs/3b5a8/7a799/ce642#heading-menu-h2-2)



## 2.2 插件的使用



### 2.2.1 寄存器状态查看和强制



1. 点击示教器屏幕左侧底部插件按钮，再点击寄存器监视器进入插件界面；



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDg0LCJwYXRoIjoiMjAyNjAxMjItMjIwODU5OC12cTNmbjQiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjE3OjE3LjA3NSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--05454174955bcb0228eb709ffc734d31d3bbb32b89175d5852a538510227d598/20260122-2208598-vq3fn4)



插件界面分别有布尔寄存器、整数寄存器、浮点寄存器，根据地址查看；



2. 布尔寄存器输入输出数量各128个，保留为总线通讯的输入输出各范围是0-63，保留范围外部RTSI客户端通讯的输入输出范围为64-127，(1)查看状态，(2)输出强制为True；



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDg1LCJwYXRoIjoiMjAyNjAxMjItMjY1MjE1MS02YXhuajAiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjE3OjE3LjEyNSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--04bead5f92117ae1b1957f743fc4816bbbefce362c326b582604ee3bb26b797a/20260122-2652151-6axnj0)



3. 整数寄存器输入输出数量各47个，保留为总线通讯的输入输出各范围是0-23，保留范围外部RTSI客户端通讯的输入输出范围为23-47，(1)查看状态，(2)输出整数；



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDg2LCJwYXRoIjoiMjAyNjAxMjItMjU0NjMzNy14MGxmM28iLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjE3OjE3LjI3OSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--e482e47b2ebed5ac736cc95c9b9f06d9c01cfd63c3abc867b818a0a0280c0533/20260122-2546337-x0lf3o)



4. 浮点寄存器输入输出数量各47个，保留为总线通讯的输入输出各范围是0-23，保留范围外部RTSI客户端通讯的输入输出范围为23-47，(1)查看状态，(2)输出浮点数；



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDgyLCJwYXRoIjoiMjAyNjAxMjItMjY1NTMzMS00ajVnOWQiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjE3OjE2Ljk5OCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--9b204b44899e64076025c89a272181d999284d548b96bf55daa590f049d548e6/20260122-2655331-4j5g9d)



## 2.2.2 寄存器名称更改



1. 点击配置-通用-IO，选择需要更改的输入输出寄存器，选择后进行重命名；



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDgzLCJwYXRoIjoiMjAyNjAxMjItMjY4Mjk1OS0yazVzeDIiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjE3OjE3LjA5NSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--be253eaf16e24463b95f155d788cd6b65dbf4ffc642f0a2b241c85eb2b11508c/20260122-2682959-2k5sx2)



## 2.3 通讯使用范围说明



输入布尔寄存器（0-63），输出布尔寄存器（0-63）



输入整数寄存器（0-23），输出整数寄存器（0-23）



输入浮点寄存器（0-23），输出浮点寄存器（0-23）



保留为总线通讯扩展使用，例如EthernetIP，profinet通讯等；



输入布尔寄存器（64-127），输出布尔寄存器（64-127）



输入整数寄存器（24-47），输出整数寄存器（24-47）



输入浮点寄存器（24-47），输出浮点寄存器（24-47）



保留为外部RTSI客户端使用；



# 3. 常见问题解答



1. 机器人系统版本需在2.9.0及以上；



2. 插件安装需要重启后使用；



3. 插件版本的更新询问艾利特人员获悉。



#
