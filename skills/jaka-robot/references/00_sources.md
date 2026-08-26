# 官方资料地图

本技能于 2026-08-26 根据 JAKA V3 中文官方文档整理。摘要用于快速决策；接口签名、版本门槛、地址表和事件码以在线原文为准。

| 主题 | 官方页面 |
|---|---|
| V3 总目录 | https://www.jaka.com/docs/guide/V3/ |
| 图形化指令 | https://www.jaka.com/docs/guide/V3/cmdhelp.html |
| JKS 编程脚本 | https://www.jaka.com/docs/guide/V3/jks.html |
| TCP/IP JSON 控制协议 | https://www.jaka.com/docs/guide/V3/tcpip.html |
| SDK 总览与版本 | https://www.jaka.com/docs/guide/V3/SDK/introduction.html |
| SDK 快速开始 | https://www.jaka.com/docs/guide/V3/SDK/%E8%8A%82%E5%8D%A1%20SDK%20%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B%20-%20CN.html |
| SDK C / C++ / C# / Python | https://www.jaka.com/docs/guide/V3/SDK/C.html · https://www.jaka.com/docs/guide/V3/SDK/Cpp.html · https://www.jaka.com/docs/guide/V3/SDK/Csharp.html · https://www.jaka.com/docs/guide/V3/SDK/Python.html |
| SDK 废弃接口与 Servo 滤波 | https://www.jaka.com/docs/guide/V3/SDK/%E5%BA%9F%E5%BC%83%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E.html · https://www.jaka.com/docs/guide/V3/SDK/Filter%20setting.html |
| 功能 IO | https://www.jaka.com/docs/guide/V3/funcIO.html |
| 工业总线与 PLC 实例 | https://www.jaka.com/docs/guide/V3/bus.html |
| Modbus 地址表 | https://www.jaka.com/docs/guide/V3/modbus.html |
| ROS 1 / ROS 2 | https://www.jaka.com/docs/guide/V3/ROS/ROS1.html · https://www.jaka.com/docs/guide/V3/ROS/ROS2.html |
| AddOn 开发 | https://www.jaka.com/docs/guide/V3/addOn/ |
| JSI / SRCI | https://www.jaka.com/docs/guide/V3/jsi/ · https://www.jaka.com/docs/guide/V3/jsi/SRCI.html |
| 事件码及含义 | https://www.jaka.com/docs/guide/V3/errinfo.html |
| 大寰夹爪 / 码垛 | https://www.jaka.com/docs/guide/V3/dh/ · https://www.jaka.com/docs/guide/V3/Palletizers/ |

## 版本核对顺序

1. 从控制器/App 获取完整系统版本、架构（X32/X64）和机器人型号。
2. 确认所用文档分支是 V3，而不是官网仍保留的 1.7.2 文档。
3. SDK 再核对 SDK 版本、控制器适配表和废弃接口页。
4. 工业总线再核对控制器版本、机柜类型及匹配的 EDS/GSDML 文件。
5. AddOn 再核对 convention、控制器架构和 AddOn 代际。
