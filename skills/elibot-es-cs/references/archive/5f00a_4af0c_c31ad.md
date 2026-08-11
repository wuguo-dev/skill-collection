# 支持文件导出及分析

URL: https://docs.elibot.cn/cs/5f00a/4af0c/c31ad
发布时间: 2026-01-13

# 1. 简介



CS飞行日志分析



# 2. 操作流程



## 2.1机器人上插入U盘，u盘格式是应为FAT32,内存大小在32G以内



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjE2LCJwYXRoIjoiMjAyNjAxMTUtMzM3NjEyMy1wOHFmdGYiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjk4MiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--9a206f6da5e0e0e9cf298e35e9ef4702105a3c2ed54cca3e390c9b55fb807d80/20260115-3376123-p8qftf)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjA5LCJwYXRoIjoiMjAyNjAxMTUtMjc0MzMxOS12NW9ydm0iLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjEyOSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--d892b3b30c434be1f3f517b2cb2fdfdfa1ec220d7522def4f8f1714ee16c735b/20260115-2743319-v5orvm)![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NTk5LCJwYXRoIjoiMjAyNjAxMTUtMzI5NDk3Ny1xZWQ1ankiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5Ljc2MiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--16b90630078cef807f48d4d5dacfecd118f2919a93599a17bcda910639be9181/20260115-3294977-qed5jy)



## 2.2拷贝飞行日志并且解压：



支持文件拷贝：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjA4LCJwYXRoIjoiMjAyNjAxMTUtMzM1MTUzNy1lbmhzZ2YiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjIxMiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--e13c5c84c34c6d3ee291eb1a8c7274367c7c1a55a95458d349450bc01b48ac30/20260115-3351537-enhsgf)



飞行日志拷贝：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjExLCJwYXRoIjoiMjAyNjAxMTUtMjc2OTQzNC1jNGt6MjkiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjU5OCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--be74b7b31b5f7cf83fd8326ca37b0b93a33799288225d7133199737b91e5d4d4/20260115-2769434-c4kz29)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjA3LCJwYXRoIjoiMjAyNjAxMTUtMzM1MTUzNy1xZTV0cHkiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjI5MSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--480d0ace344f7808dff3e935f72ec81dd9361028f71298beac073c405323a530/20260115-3351537-qe5tpy)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjEwLCJwYXRoIjoiMjAyNjAxMTUtMzQ1MDIxNi13dnpyMWgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjQ1MiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--60829fc3954b0cf8587325bcff02d6107246808fc45db38c5fae758ffd1de2b2/20260115-3450216-wvzr1h)



## 2.3电脑端查看：



解压：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjAxLCJwYXRoIjoiMjAyNjAxMTUtMzMyMjAwMS1qNGsycXEiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5LjgzMiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--ba6ea0f0f4e002bbab49038e5669c77157f361b635b6b8aa22424dcce54e2749/20260115-3322001-j4k2qq)



解压完成：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NTk3LCJwYXRoIjoiMjAyNjAxMTUtMzQ1MDIxNi13cTdnZWwiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5LjUwNiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--f0bbbbb835238c4881a1a06c7ef58be3d43add9f0f02326f3c78834264f65100/20260115-3450216-wq7gel)



## 2.4注释：



EliRobot (上位机以及X86系统相关日志)



controller (上位机相关日志，记录上位机软件相关日志、任务文件等)



Program (当前系统所有配置、任务、脚本文件)



default.configuration (报警时的当前配置文件)



default.configuration.variables (报警时的当前配置变量文件)



test.task (报警时的当前任务文件)



audit.csv (审计日志：记录用户的重要操作)



elibot.log (软件运行日志：记录软件运行信息，如软件运行异常信息，记录较为全面，主要问题定位文件)



gui.properties (当前界面相关配置，主要用于记录系统设置->通用配置中的相关参数)



log_history.csv (用于记录软件的运行->日志页面的所有日志条目)



remoteControl.properties (当前远程控制配置)



histogram.properties (统计数据：统计数据的频率，主要内部使用)



system (X86系统相关日志，该部分日志主要用于研发深度排查问题使用)



df (系统硬盘挂载状态，用于排查是否存在系统硬盘占满等情况)



dmesg (系统状态日志，用于排查定位一些系统级的问题)



messages (系统状态日志，用于排查定位一些系统级的问题)



messages.0 (系统状态日志，用于排查定位一些系统级的问题)



ps (系统线程以及进程状态)



Runtime.txt (JAVA虚拟机的运行时状态)



top (系统线程以及进程状态)



version (系统ROOTFS版本号)



x11vnc.log (系统x11日志)



Xorg.0.log (系统Xrog日志)



Service



metadata.conf (上位机软件的版本信息，如版本号、编译时间等)



EliServer (下位机以及A9系统相关日志)



controller (下位机相关日志，该部分日志用于记录下位机软件相关日志状态等)



eli_log



elisafety.log (安全控制器日志，主要用于排查 E6S99 报警使用)



eliserver_d.06.log (下位机DEBUG日志文件备份)



eliserver_d.log (下位机DEBUG日志文件，记录统报警日志，执行的脚本等）



eliserver.02.log (下位机日志文件历史备份)



eliserver.log (下位机日志文件，记录操作日志、报警日志等)



eli_snapshot.log (快照文件，记录报警之前40ms的状态数据，如CPU使用率、 温度、电压等)



reboot.log (内部日志文件，一般不需关注)



simulation_robot.conf (仿真IO输入控制配置文件用于实现软件仿真的IO输入功能)



time.log (内部日志文件，一般不需关注)



motion_task.log (运动节点执行日志，用于记录运动节点数据（2.12.0版本添加）)



motion_task.0.log (运动节点执行历史日志，用于记录运动节点数据（2.12.0版本添加）)



eli_resource (系统相关资源文件，一般不需关注)



eli_robot_data (机器人相关配置文件，如绑定信息、传感器出厂配置等，一般不需关注)



eli_user_data (系统相关用户配置文件，一般不需关注)



eli_controller.conf (当前使用的机器人配置)



eli_robot_bind_config.ini (机器人绑定的数据信息，如零位脉冲等)



eli_robot_bind_config.ini.backup (机器人绑定的数据信息备份文件)



eli_robot_config.ini (机器人关机位置数据)



eli_safety.conf (当前使用的安全配置)



eli_system_config.ini (用户系统配置数据，如产测模式配置、关机时间等)



eli_user_config.conf (用户系统配置数据，如碰撞开关是否打开、碰撞百分比)



fc_params.xml (用户相关的力传感器相关配置)



start_eliserver.sh (控制脚本，一般不需关注)



stop_eliserver.sh (控制脚本，一般不需关注)



metadata.conf (下位机软件的版本信息，如版本号、编译时间等)



realtime_data



realtime_data.csv (飞行记录的实时数据，记录报警前25秒左右以及报警后5秒左右所有实时数据，如位置速度电流电压等)



system (A9系统相关日志，该部分日志主要用于研发深度排查问题使用)



dh (系统硬盘挂载状态，用于排查是否存在系统硬盘占满等情况)



dmesg (系统状态日志，用于排查定位一些系统级的问题)



ps (系统线程以及进程状态)



top (系统线程以及进程状态)



version (系统AB版本，内部使用，一般不需关注)



# 3. 示例



## 3.1使用支持文件查看30001端口接收的脚本：



如下图使用sockettool通过30001端口发送脚本给机器人：movel([0.1,0.12,0.123,0.1234,0.54321,0.54321],a=1,v=2,t=3,r=4)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjA1LCJwYXRoIjoiMjAyNjAxMTUtMjk4OTU4OC1ydzR5bDgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjAyOSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--5e9e66d99c4e0907c5d49436c9dbba92cacaea745b0212fef70086303ba8ae6f/20260115-2989588-rw4yl8)



发送后机器人应该会按照脚本指令运动，无论是否运动，我们都可以导出支持文件查看：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjE0LCJwYXRoIjoiMjAyNjAxMTUtMzM3NjEyMy14Zmo5NWkiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIxLjA3NSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--80eac873a8a9e293eb217f0c2a7adc341c7a72f85f42c34e690c8e20eea0d6dd/20260115-3376123-xfj95i)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjE1LCJwYXRoIjoiMjAyNjAxMTUtMjc0MzMxOS02b21xbHAiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjc4OCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--b8625897b50078d91624e0e2f4df743e03fb08191fcacb98c966659493788c84/20260115-2743319-6omqlp)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjA2LCJwYXRoIjoiMjAyNjAxMTUtMjc2OTQzNC15ZHcxNmciLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjA5OSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--d57a7c59c20ebd216ec145ddd9a9d1a9a50a2bbe8a7df7ced87832060a801d0b/20260115-2769434-ydw16g)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjE3LCJwYXRoIjoiMjAyNjAxMTUtMjc0MzMxOS00OTQ0NTYiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjg3NyswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--6a455c31ea6905bbf9f956cc1a46bbb2019ffd6efd71080e7d572c0d6dcef263/20260115-2743319-494456)



电脑端查看：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NTk4LCJwYXRoIjoiMjAyNjAxMTUtMjc2OTQzNC12MjBxdzgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5LjY2NiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--352eec8c3ef7f253b0139f057b760489df210e0015bfc7e1085400dbd0d396d6/20260115-2769434-v20qw8)



解压并打开，查找最新记录：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjA0LCJwYXRoIjoiMjAyNjAxMTUtMzM1MTUzNy12NHZha3UiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjExMiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--b1b47b4d3bb61857557faf20e18ddc7ab407c58678c94ba794350eeeb9662716/20260115-3351537-v4vaku)



找到该eliserver文件：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NTk2LCJwYXRoIjoiMjAyNjAxMTUtMzI5NDk3Ny1manlpNWwiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5LjU1NSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--96fa54f9b5da63dc0009c8463216007d1eb2c4075ad06be2afa803c828011690/20260115-3294977-fjyi5l)



使用快捷键ctrl+f搜索脚本关键词或全部，可查看已发送的脚本：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjAwLCJwYXRoIjoiMjAyNjAxMTUtMzQ1MDIxNi10bmk4d2YiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5Ljc2NyswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--9dcc91fa62cee1ad86cd3bb1ac68894fb4eb34e77cf2fc748307b7179de9da48/20260115-3450216-tni8wf)



## 3.2查看历史报警信息程序变更记录



路径：CS_BACKUP\EliRobot\log\log_history.scv



可以查看报警信息和程序变更记录



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NTk1LCJwYXRoIjoiMjAyNjAxMTUtMjk4OTU4OC0zdzdzeTAiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5LjM5NSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--b2134f41ac6c405901ebf30e131b0c5fd4f462e104e5f544d62a0ce7afc2070c/20260115-2989588-3w7sy0)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjAzLCJwYXRoIjoiMjAyNjAxMTUtMjk4OTU4OC1rY3Jkcm8iLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjE5LjkyMiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--45f990b97552ed7da565362871b1bf0407eafaca114e41dabea7650f9ff85142/20260115-2989588-kcrdro)



## 3.3查看系统磁盘挂载情况



路径：recording/ELIRobot/system/df



一般占用率超过80%则需着重注意



CPU占用超过80%就属于超负荷，机器人系统可能或报警主任务无限循环，线程里高速执行逻辑等都可能导致CPU超负荷，导致死机抖动等问题和风险。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjEyLCJwYXRoIjoiMjAyNjAxMTUtMzM3NjEyMy1tdGw1dzIiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjU4NCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--5e4d91d44c7fa8b84d898ef4d396805fb6449c0550926ce495ec8fc2740fe7c0/20260115-3376123-mtl5w2)



## 3.4查看报警瞬间的IO状态



路径：recording/ELIServe/controller/eli_log/eli_snapshot_log



可以查看机器人报警瞬间的io状态，可用于排查入碰撞报警瞬间是否由io误触发导致的末端工具撞击



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NjEzLCJwYXRoIjoiMjAyNjAxMTUtMzMyMjAwMS1ycWhqeGEiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDE0OjE4OjIwLjkwOSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--76a229dbc3212a31baede93661d0c973b0d9ee791fae430ea1315b978100a3f0/20260115-3322001-rqhjxa)
