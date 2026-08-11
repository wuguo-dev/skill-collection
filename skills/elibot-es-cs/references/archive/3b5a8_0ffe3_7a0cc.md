# 干涉区插件

URL: https://docs.elibot.cn/cs/3b5a8/0ffe3/7a0cc
发布时间: 2026-03-03

# 1. 简介



借助干涉区插件，既能划定机器人周边空间区域，也可设置各关节活动范围作为干涉区；一旦机器人末端驶入划定区域，系统便会输出对应信号，该信号可实现多机器人互锁避让、自动回零等联动控制。



# 2安装插件



• 机器人系统版本： >= V2.14.0



• 干涉区插件版本：3.1.1



[InterferenceZone-3.1.1-SNAPSHOT.elico](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQ3LCJwYXRoIjoiaW50ZXJmZXJlbmNlem9uZS0zLjEuMS1zbmFwc2hvdC5lbGljbyIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NDc6MjkuNTAwKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--f2924cc86b888998a8d3a4ed1a152a1fcb9c0da707ac591059a9d6c9b770fca1/interferencezone-3.1.1-snapshot.elico?disposition=attachment)293.9 KB



[下载插件安装包后，按插件安装流程章节安装插件。](https://docs.elibot.cn/cs/3b5a8/7a799/ce642#heading-menu-h2-2)



# 3. 干涉区配置



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQxLCJwYXRoIjoiMjAyNjA3MjgtMTA1LWI5dmZ0MyIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NDQ6MzQuNjY5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--f3fc1d3613ad69148bdc481dd04ce77fa1e0f671c4e618ed3261c5fa78242eb8/20260728-105-b9vft3)



首先需要确认干涉区的类型：轴干涉、立方体、球体；并点击创建。



## 3.1基础属性



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjM3LCJwYXRoIjoiMjAyNjA3MjgtMTE3LW0xaGh1ZiIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NDQ6MzIuNTYyKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--dc6f61603d003c67c3d2bc49f6c82237386a3efaa4521a93a0acde10f31383b0/20260728-117-m1hhuf)



类型：轴干涉、立方体、球体



坐标系：可选择基座或用户坐标系



输出I/O:数字输出、可配置IO、布尔寄存器（布尔寄存器需要先在配置—I/O—布尔寄存器重命名后才会显示）



触发状态：高电平、低电平



启动模式：禁用、上电后启用（手摸模式也有效）、运行时启用。



使能I/O：（可不配置）关联使能信号【数字输入、可配置IO、布尔寄存器（布尔寄存器需要先在配置—I/O—布尔寄存器重命名后才会显示）】



触发动作：仅输出信号、暂停任务并输出信号、停止任务并输出信号



触发时机：进入区域时、离开区域时



约束肘部：不仅监控机器人末端（TCP），也同时监控肘部关节：只要肘部进入 / 穿过干涉区边界，就触发限制（减速、停止或互锁信号）



## 3.2干涉区属性



设置干涉区信号触发区域。



轴干涉：关节范围模式、基准位置模式。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQyLCJwYXRoIjoiMjAyNjA3MjgtMTE3LWd0bXdjbCIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NDQ6MzUuMTg0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--2b8aafb1c86d863d482a49956491f87aa40f0767984ad0bd5672970ac43749cf/20260728-117-gtmwcl)![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQ5LCJwYXRoIjoiMjAyNjA3MjgtOTMtNzBvaXM5IiwidGltZXN0YW1wIjoiMjAyNi0wNy0yOFQxNDo1MDowMy42NjErMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--4c27b09dbe9a9d5d4bc772d69cfa2de1b3c924348b2c898b896c6234566eea92/20260728-93-70ois9)



立方体：顶点模式、中心点模式。（注意单位为毫米）



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjM4LCJwYXRoIjoiMjAyNjA3MjgtOTMtNmptMGM5IiwidGltZXN0YW1wIjoiMjAyNi0wNy0yOFQxNDo0NDozMy4zNzQrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--23108035b20382fefdd125ed1bbd78394acf0c63db5add9c4f17673b6aacc65b/20260728-93-6jm0c9)![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQ0LCJwYXRoIjoiMjAyNjA3MjgtOTMtaGg0Zng3IiwidGltZXN0YW1wIjoiMjAyNi0wNy0yOFQxNDo0NDozNi4xNjErMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--6b1c51c4c264d544bea69a64b0a8e7669b13234bf2b81f7e5d7451997299cece/20260728-93-hh4fx7)



球体：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjM1LCJwYXRoIjoiMjAyNjA3MjgtNjktaXNlNWhpIiwidGltZXN0YW1wIjoiMjAyNi0wNy0yOFQxNDo0NDozMS41NTkrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--b92662e18f8e9e954012e75941828c6f1d1f50c0ce3cbe3478ad2bb4001412c1/20260728-69-ise5hi)



## 3.3工具属性



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQwLCJwYXRoIjoiMjAyNjA3MjgtNjktd3NrMm9uIiwidGltZXN0YW1wIjoiMjAyNi0wNy0yOFQxNDo0NDozNC45MjQrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--7af8c4d40478196d65e480001d511c906f2d8f733c1dc192cd79a1ed5f88c943/20260728-69-wsk2on)



工具半径：若末端加工件也有一定的工作范围，可添加工具半径。



工具偏移：末端工具TCP点



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQzLCJwYXRoIjoiMjAyNjA3MjgtMTA1LXJ5dzZ3eSIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NDQ6MzUuNTcxKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--8d1119aa9bb7756f4e9ef6cda7be918803ca18c7af1acc221e61cc0b6482a58c/20260728-105-ryw6wy)



激活的TCP：沿用配置—TCP内配置的工具属性。



# 4. 示例



干涉区配置完成后首先干涉区插件的UI界面会有干涉区3D视图；并且配置的信号也会输出信号。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjQ1LCJwYXRoIjoiMjAyNjA3MjgtMTA1LTh5ZHgzNSIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NDQ6MzYuNDc2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--9b6079df133863dbfc36c34845317528769eaf939846136d6c5b91d684fd5034/20260728-105-8ydx35)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzE3NjUwLCJwYXRoIjoiMjAyNjA3MjgtMTA1LWVtdGJzOCIsInRpbWVzdGFtcCI6IjIwMjYtMDctMjhUMTQ6NTA6MDQuNDY3KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--f10c9962298a9e25298214ac87662ae0f8505c4ab7f668d93b00ac72d1a46df3/20260728-105-emtbs8)



# 5. 常见问题



1、 为什么我干涉信号不输出？



检查触发状态是否为高电平，是否已经启用，信号配置是否正确。



2、 多个干涉区可以重叠吗？



可以，每个干涉区独立生效，多个信号可同时触发。
