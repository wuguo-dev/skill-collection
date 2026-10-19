# 排查入口与证据边界

## 静态分析到现场验证

先说明能确定的机制，再列与该机制有关的运行证据。源码支持某条分支，并不代表现场已走到该分支。能运行离线逻辑时使用离线样本；涉及数据库、服务启动和真车动作时先确认用户授权范围及环境。

| 现象 | 优先证据 | 源码入口 |
|---|---|---|
| 点位执行顺序与页面不同 | 实际任务点ID、路径sequence、点位postion、规划日志 | renderId2SlamPoint / RobotNavRunPoint / p2p |
| 刚进路径便倒退 | 转换点映射、当前/目标里程、路径前置动作、轮速 | changeToOtherPathPoint / fixPostionPreAction / go |
| 到点后短距离倒退 | 实际停止脉冲、isAccurate、补偿日志 | fixPostion |
| 重设位置后返回旧点 | 坐标跳变前后值、未消费子路线/目标 | setRobotAtThisPoint / NavRunThread |
| 雷达动作立即完成 | 首轮区间点数、checkType、旧点/空点云 | slamMoveWith3D / getMinZInRange |
| 雷达动作长期不结束 | 真正选择的设备、异常、点云新鲜度、区间 | getUseRp / Livox.comRx / slamMoveWith3D |
| 页面成功但设备未响应 | DataRes封装、实际data值、Command响应、反馈更新时间 | JsonControler.devExec / BaseDevice.invoke / Command |
| 定时任务未动 | Cron状态、控制模式、工作时间、电量、恢复标志 | CronService / RobotTaskExecService / Plc.execTask |
| 到点后任务仍未完成 | ImgFunction关联、ImgHistory、复核、异步识别 | TaskDevice / OcrDevice |
| 停止后仍有动作 | 活跃线程、各停止标志、阻塞方法、异步动作组 | CommonAction.stop / NavRunThread / RobotAccurateDevice |

## 里程问题记录格式

```text
时间 / 线程 / 当前动作链ID / 设备ID和实现类
当前pathId / 目标pathId / 目标点ID和名称
XRun(脉冲) / 路径原点(脉冲) / 路径当前值(脉冲)
mmCount(脉冲/mm) / 当前路径里程(mm) / 目标里程(mm)
isBack / isAccurate / 左右轮指令 / 重设位置事件
```

优先使用已有日志：`NavRunThread start`、`机器人当前在`、`路径规划成功`、`前往点位`、`设置当前路径和起始里程`、`机器人运动到点位`、`机器人执行后退消除缓停里程`、`差速运动`。先按线程/动作链关联，再按时间串联。系统多个线程输出会交错，肉眼相邻行不等于因果相邻。

## 停止、返航和清限制

- navPoint.jsp“停止所有”调用 stopAndInitParamsAndRun 空参：停止/清理导航和部分自动配置流程，等待旧线程结束。它不是已证明可抢占所有设备方法的通用中断。
- goHome 异步停止当前流程、选择充电桩并规划返航，含30秒重复调用抑制。返航本身会产生移动。
- clearPlcLimit 只是把前后里程限制写为0，不能用“解除限制”替代停止，也不能推断它取消了后台导航。
- moveStop/comDrive(0,0,0) 是当前驱动接口的停止请求；电气急停能力需要硬件/PLC证据，不能由普通停止按钮名称判断。

## 构建与部署

证据：pom.xml、README.md、MainSetup、Constants、PathEnum。

- 构建目标 Java8，WAR 部署到 Servlet/Tomcat。Constants 使用 Nashorn，运行JDK需验证是否带兼容脚本引擎；仅设置编译target并不证明任意较新JDK可直接启动。
- pom 引用了 libs 下厂商本地 JAR，另有 JNI/JNA、OpenCV、视频/相机等本地依赖；检查所需平台和外部lib目录。
- 外部 station.properties、数据库和设备表决定现场行为。不要为了理解源码直接启动整个系统，启动流程会自动初始化通信、定时任务和后台服务。
- 运行路径由 HOME_PATH/HOME_PATH_SUB/context 组合；外部目录不必等于源码目录或Tomcat webapp目录。
- README 同时包含部署示例和敏感配置示例。摘录时保留键名和机制，遮蔽账号、令牌和加密材料。
- 不要把仓库中测试/演示代码、target 编译产物或注释掉的历史服务当成当前业务入口。源码和现场WAR的版本差异必须单独确认。

## 当前覆盖范围

已读主干：启动/IoC、缓存、插件注入/代理、路由、通信、动作链、普通任务、Plc调度、复合导航、3D定位、MID360、识别结果、梁场检测。

未进行：部署数据库读取、运行服务连接、真车实验、全仓编译、所有项目插件逐类审计、现场WAR与源码一致性确认。这些边界不妨碍回答已追踪机制，但具体故障根因仍需对应数据。
