---
name: jaka-robot
description: JAKA（节卡）协作机器人 V3 官方技术文档知识库与操作指南。用于 JAKA 机器人图形化编程与 JKS 脚本、C/C++/C#/Python SDK、10000/10001 TCP/IP 控制、功能 IO、Modbus/PROFINET/EtherNet-IP、ROS 1/2、AddOn、JSI/SRCI 及事件码诊断。用户提到 JAKA、节卡、Zu/Pro/A/C/S/MiniCobo、JKS、JAKA SDK、jaka_ros2、JAKA AddOn 或相关端口与故障码时使用。
---

# JAKA 机器人技术文档

以 [JAKA V3 官方文档](https://www.jaka.com/docs/guide/V3/) 为准，帮助用户编写、核对和排查 JAKA 机器人应用。先识别接口与版本，再选择对应参考资料；不要把不同接口的单位、索引或控制方式混用。

## 先确认边界

在给出可执行方案前，确认现有信息中的机器人型号、控制器/系统版本、调用接口、控制源、工具与负载、TCP/用户坐标系、目标点来源、速度/加速度和现场安全条件。信息不足时保留明确占位符，并指出上机前必须核实的值。

涉及真实运动时，把首次验证限制为仿真、空载或低速单步：保持急停可达，清空工作区，先验证可达性、关节限位、奇异点、碰撞和 IO 联锁，再逐步提高速度。不要代填真实 IP、账号、密码或示教点。

## 不可混用的接口约定

| 接口 | 位置 | 姿态/关节角 | IO 索引 | 关键语义 |
|---|---|---|---|---|
| 图形化编程 / JKS | mm | degree | 按具体指令核对 | 六元素数组；`tol=0` 精确到点，正值允许轨迹混合 |
| TCP/IP JSON | mm | degree | 从 1 开始 | 10001 请求/响应；命令均非阻塞，需另查运动或程序状态 |
| JAKA SDK | mm | rad | 从 0 开始 | V3 控制器走 gRPC；先登录并逐次检查返回码 |
| ROS 2 服务示例 | mm | rad | 以消息定义为准 | 关节数组为 rad；真实机先 Plan，再 Execute |

转换接口时显式标注 `deg ↔ rad`，并逐项核对 `[x, y, z, rx, ry, rz]`、相对/绝对模式、用户/工具坐标系和 IO 偏移。TCP/IP 的 `errorCode` 可能是整数或字符串；统一归一化后再判断是否为 0。

## 按任务加载参考资料

- 图形化指令、JKS 语法、运动/位姿/线程/Socket：读 [references/01_programming-jks.md](references/01_programming-jks.md)。
- SDK 版本、登录、C/C++/C#/Python、10000/10001 端口：读 [references/02_sdk-tcpip.md](references/02_sdk-tcpip.md)。
- 功能 IO、Modbus、PROFINET、EtherNet/IP、PLC 对接：读 [references/03_io-industrial-bus.md](references/03_io-industrial-bus.md)。
- ROS 2、MoveIt 2、RViz、Gazebo、真实机驱动：读 [references/04_ros2.md](references/04_ros2.md)。
- AddOn 3.0、自定义指令/服务/页面、配置与发布：读 [references/05_addon.md](references/05_addon.md)。
- 故障码、事件码和排查：读 [references/06_errors.md](references/06_errors.md)。
- 需要核对版本、原始接口签名、地址表或未覆盖专题（ROS 1、JSI/SRCI、夹爪、码垛）时，读 [references/00_sources.md](references/00_sources.md) 并访问对应官方页面。

## 产出要求

1. 开头写明采用的接口、控制器/SDK 版本假设及单位。
2. 代码把连接、登录/控制权、状态检查、运动、完成条件、异常停止和登出/断开分开；每一步检查返回值。
3. 非阻塞命令必须给出完成判据，例如 `inpos`、运动状态、程序状态或超时；收到成功响应不等于动作完成。
4. 点位、速度、加速度、负载、TCP、用户坐标系和 IO 地址使用具名常量，不埋入业务逻辑。
5. 明确区分控制器拒绝、通讯失败、运动未完成、保护性停止和程序错误；附上应采集的状态与事件码。
6. 文档或接口签名与本技能摘要冲突时，以用户实际版本的官方页面为准，并说明差异。
