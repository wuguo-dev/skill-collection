---
name: station-system
description: 基于本地 station 智能巡检系统源码，分析系统运行逻辑、设备接入、巡检任务、复合导航与里程、动作链及雷达点云定位。用户询问 station 系统、F3 路径倒退、精确修正、必经点、设置机器人位置或梁场检测接入时使用。纯前端设备按钮集成优先使用 station-device-ui-integration。
---

# Station 智能巡检系统

基于源码回答问题，并定位到真正控制行为的配置与方法。默认仓库 `D:/WorkSpace/code/station`，知识基线为 2026-10-19 本地源码；外部数据库和设备配置未被快照收录。

## 使用方法

1. 确认当前源码根目录及其适用的 AGENTS.md。需要引用某个机制时，打开下表对应参考，再核对当前源码的相关方法。引用中的行号是基线定位提示，方法名比行号稳定。
2. 区分三类证据：源码确定的行为；用户提供的配置/日志；由二者推演、尚未现场验证的原因。把缺少的部署配置具体说清楚。
3. 追踪用户入口到设备边界；涉及异常动作时记录“当前路径、当前里程及单位、目标点、执行中的动作、重定位前后数值”。根据实际导航实现选用对应逻辑。
4. 给出直接结论、源码依据、最小必要的后续验证。修改配置前重建执行顺序与坐标变化；若用户只要求分析，则交付证据与待确认项。

| 问题 | 读取参考 |
|---|---|
| 系统结构、启动、插件设计、配置和缓存 | [architecture.md](references/architecture.md) |
| HTTP/JSP、动态路由、设备方法、动作链、通信 | [runtime.md](references/runtime.md) |
| 路径、点位、必经点、排序、里程、倒退、精确修正 | [navigation.md](references/navigation.md) |
| MID360、点云、安装角、检测区间、雷达等待不结束 | [radar.md](references/radar.md) |
| 任务调度、自动巡检、识别、报告、梁场检测主机 | [inspection.md](references/inspection.md) |
| 运行异常、无动作、停止、返航、部署/构建 | [troubleshooting.md](references/troubleshooting.md) |
| 用户此前 F3 配置案例及证据边界 | [f3-case.md](references/f3-case.md) |
| 精确源码入口及复查 | [source-map.md](references/source-map.md) |

## 必须保留的语义

- 这是 Nutz MVC/IoC 的 Maven WAR，业务由数据库配置、插件 Java、脚本和工作流共同决定。源码中的默认值不等于现场值。
- `plugin.device.nav`、`robotWheeled.NavCore`、`slamNav.LaserNavCore`、`seerNav`、`robotTrack` 是不同实现。截图中的“复合导航/沿路径前进指定距离/设置机器人位置”对应 `plugin.device.nav.RobotNavDevice`。
- 点位表的 `No` 是显示行号；导航目标优先队列按路径 `sequence`、点位 `postion` 排序。启用点位不等于所有点位都自动成为任务目标，规划器另外插入必经点。
- `NavPoint.postion` 是毫米，PLC 路径里程是脉冲，以 `drive.mmCount()` 换算。把两者写清楚再比较。
- `setRobotAtThisPoint` 改 PLC 路径/原点，不行驶到指定点，也不自动删除尚未执行的目标。`navToPointById` 才是发起前往点位。
- 精确修正在缓停后根据误差发出反向补偿；普通定位也能因当前里程大于目标而倒退。先识别调用分支再判断原因。
- `slamMoveWith3D` 的“从无到有/从有到无”是当前状态判断，非带历史记忆的边沿检测。它的取消与超时能力必须看方法体，不能由 UI 名称推定。
- 方法拦截器、DeviceObserver、动态 SysScript、线程动作组都可能改变单看方法体得到的结论。

## 源码变化检查

`scripts/source_probe.py` 只读取源码和清单，不启动系统，也不连接数据库或硬件：

```powershell
python <技能目录>/scripts/source_probe.py --topic navigation
python <技能目录>/scripts/source_probe.py --root D:/WorkSpace/code/station --topic radar --check
```

输出包含真实文件路径、SHA-256 是否与基线一致、关键方法当前行号。退出码 0 表示选定文件与基线一致，1 表示缺失、变化或锚点不匹配，2 表示清单/参数错误。变化是重新阅读源码的信号，不等于故障。详见 [source-map.md](references/source-map.md)。

## 验证边界与维护

静态阅读或离线推演不能证明现场故障已复现或修复。读取日志、分析配置和编写补丁，与下发真实设备命令是不同范围的工作；仅在用户授权的环境和操作范围内执行。

更新知识时，把通用运行机制放在对应主题参考，把特定点位 ID 和现场现象留在案例文件，并更新源码清单。文档只保留必要的配置字段名，不复制账号、令牌、密钥或现场连接凭证。
