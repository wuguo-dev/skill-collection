# 复合导航、里程与点位

本文只适用于 `plugin.device.nav.RobotNavDevice`。行号详见 source-map.md。

## 数据模型与界面

- NavPath：pathType、pathName、pathSpeed、params、mapPathId，继承 sequence。
- NavPoint：pid 是所属 NavPath.id；pointType、pointName、`postion`、params、isAccurate、seerCode，继承 sequence。源码拼写 postion 应保留。
- NavPointMap：pathId/pointId -> toPathId/toPointId，是路径关联边，其记录也能配置动作链。
- NavPathMulti：关联路径和备用导航策略；选用不同策略不一定意味着 PLC pathId 被重写，应检查具体调用。
- pointType 枚举：TASK 任务点、MUST 正向基准/必经点、MUST_BACK 后退必经点、P2P 路径关联点、CHARGE 充电桩。
- `navPoint.jsp` 按 sequence 展示，No 为 rownum。开关绑定 isRemoved 并反向显示；No 与业务执行优先级不同。
- “设置机器人在该点位”的定位图标调用 setRobotAtThisPoint；“前往点位”调用 navToPointById。

## 从目标列表到路线

`stopAndInitParamsAndRun -> renderId2SlamPoint -> NavRunThread -> p2p -> navToPoint`。

1. 先置 THREAD_SET_DIE，停止当前 CommonAction，等待旧 NavRunThread 退出。
2. 把目标 ID 转为 NavPoint，按路径 sequence、同路径 postion 排序。
3. 放入 PriorityBlockingQueue，RobotNavRunPoint.compareTo 再按路径 sequence、postion 比较。
4. 每取一个顶层目标，用 getRobotCurPoint 重新确定当前位置，规划它的子路线。
5. 子路线依次消费。一个子点动作结束后，不会自动把这条子路线剩余项全部重新规划；坐标跳变必须与尚未执行的项一起分析。

启用只表示允许被配置系统取到，不等于所有点都加入任务。普通巡检任务可从表计关联反推目标列表，手动前往可以只有一个目标。MUST 是规划器补入的点，TASK/P2P 的行为取决于被选为目标或关联路径。

## p2p 的规则

证据：RobotNavDevice.p2p。

- 同一路径且当前 `s <= t`：插入严格满足 `s < postion < t` 的 MUST，升序，再加入目标。CHARGE 起点会先加入，以执行出库动作。
- 同一路径且当前 `s > t`：插入严格区间内 MUST_BACK，降序，再加入目标。不会自动插入普通 MUST。
- 跨路径：建立当前点到可达关联点、NavPointMap、目标路径入口到目标点的边，用 ShortestPathCalc 计算路线，再插入相应段的必经点。
- 跨路径起点超过关联点时还有显式回退重规划分支：`comDrive(-50,-50,endPostionP2PValue)`。不是所有倒退都来自 isAccurate。
- 当前版跨路径分段补点代码使用普通 MUST 的升序区间判断；不要把同路径逆行 MUST_BACK 的规则无条件推广到所有分段。
- P2P 点到达后执行映射动作，再以目标点的路径/里程重设 PLC。映射按待执行点过滤，匹配多条时报错。

## 到点的内部顺序

`navToPoint`：路径前置动作链 -> 行驶定位 -> 点位动作链 -> 若为 P2P 则映射动作及路径重定位。

RobotNavDevice 本身还有 navType 分支：默认 YN 使用本文的 PLC 里程定位；XG 用 Seer 点位代码请求导航，getRobotCurPoint 也按 seerCode 映射当前位置。即使设备类相同，也要确认 navType 后才能套用 fixPostion 的前后退判断。

- MUST 使用独立的 CommonAction；其他点一般用导航设备持有的 action。
- nav_debug 时会跳过点位动作；到达充电桩的末尾点通常不执行出库动作。
- 连续同路径 TASK 可能异步预处理下一个目标；lastConfirmPoint 可缓存方向和点。涉及动作期间改坐标时要连同预处理一起检查。
- 路径前置动作返回值保存在局部 result，当前代码未据其布尔值阻断后续定位。具体动作异常仍可能中断调用。

## 里程的三种数值

| 数值 | 单位/含义 | 代码 |
|---|---|---|
| NavPoint.postion | mm，业务路径坐标 | getPostion4mc 转目标脉冲 |
| PlcPostionDevice.getPathPostion | 脉冲，PLC 当前路径坐标 | HD24 属性解析量 |
| drive.getXRunSync | 脉冲，驱动累计计数 | 用于计算路径原点 |

`目标脉冲 = round(目标毫米 * mmCount)`；`当前毫米 = 当前脉冲 / mmCount`。

设置位置：`setRobotAtThisPoint(id) -> setRobotPathAndPathPostion(pathId, mm) -> startPulse = XRun - targetPulse -> setRobotPathAndStarPostion`。写入路径 ID/原点，等待通信响应；不在该方法内进行物理行驶，也不重排任务队列。上层方法不检查这里返回的 boolean，需验证写入响应及随后反馈值。

路径 ID、路径起点、路径绝对里程的同步读取默认等待新时间戳，最多约30秒；超时仍可能返回现有缓存，不等于明确失败。还需核对 Data 更新时间。

## 普通定位与精确修正

证据：RobotNavDevice.fixPostionPreAction/fixPostion。

1. 验证 PLC 当前路径与目标路径相同，否则抛异常。
2. nearPostionValue>0 且绝对误差小于该值时直接返回；这处比较发生在脉冲层，不能直接当毫米。
3. 当前脉冲 <= 目标脉冲：设置前进限制；否则 isBack=true，设置后退限制。
4. 循环按方向比较里程，调用 go；接近目标时可按 postionSubSpeed 减速。循环约200ms一次以控制通信负载，还可能调用绕障/跌落处理。
5. moveStop、清前后里程限制，读取实际停止位置。
6. isAccurate=true 且误差绝对值>0、线程未取消时，前进行驶后发速度 -20；后退行驶后发 +20，以误差换算的毫米距离补偿，并按距离估计等待。

这不是一个重新闭环确认最终误差为零的过程；源码直接取误差绝对值，并按原行驶方向选择补偿方向。不要把注释“后退”解释为所有情况下必为负速度。

## go：路径策略到轮速

RobotNavDevice.go 按 NavPathTypeEnum 将 params JSON 解析成对应参数类并执行策略，得到修正 level，再合成基础速度、左右轮速度或舵轮角度。

- 路径类型覆盖二维码、视觉巡线、目标追踪、激光、路面、陀螺仪、直接驱动、3D 路面等，以枚举为准。
- NavPathMulti 允许按里程选择关联策略，或主策略无结果时尝试备用策略，并可限制备用策略行驶距离。
- pathSpeed 经 speedRate 缩放；isBack 时变号。当前代码没有在这处强制 pathSpeed 为正，异常负值也需检查。
- xzLevels、moveStep、kp、实际策略 level 决定轮速。level=null 或参数异常时有只记录并返回的分支，不能用“导航循环还在运行”推断持续下发正确指令。
- 差速模式与舵轮模式、PID与分级修正分支不同。最终物理正反向还受驱动实现及左右轮倍率影响。

## 分析倒退的最小证据

先区分：目标在当前位置后方；缓停后的精确补偿；跨路径恢复；路径前置/点位动作显式驱动；负速度/驱动方向配置。

记录同一时间段的 pathId、XRun、路径原点、当前/目标脉冲、mmCount、当前目标点ID和动作链ID。日志“机器人执行后退消除缓停里程”对应精确补偿；“前往点位”目标较小配合负基础速度对应普通逆行；“设置当前路径和起始里程”揭示坐标重设。
