# 3D 雷达数据与辅助定位

## 真实调用链

`Communication(UDP监听) -> CommuService.listen -> LivoxMid360Device.comRx -> 滚动点队列 -> Slam3DDevice.getXYZ -> getMinZInRange -> RobotAccurateDevice.slamMoveWith3D -> RobotNavDevice.go -> AbstractDriveDevice.comDrive`。

RobotAccurateDevice 经 RobotNavDevice.getSlamDevice 获取前置 SlamDevice，再对 `getUseRp()` 结果强转 Slam3DDevice。因此要核对真实设备树及 useRpFlag；选择到其他 InfcLidar 实现时可能发生类型转换错误。

## MID360 驱动

证据：`plugin/device/hardware/lidar/LivoxMid360Device.java`。

- 注释提供 UDP HEX 监听、56301 和接收包大小等集成提示；这是仓库说明，不等于现场 Communication.uri。
- comRx 从报文读取数据类型和点数。类型1按每点14字节、偏移36解出 int x/y/z 和强度，写入 CriQueue；类型3目前主要为球坐标调试输出，不可当成等效完整点云转换。
- fps 注解写“帧数”，实际 init 用来建立点队列容量，默认50000，不能按每秒帧率解释。
- getXYZ 返回滚动队列逆序快照；队列容量控制历史保留，而不是严格按时间淘汰。旧点在没有足够新点覆盖时可能继续存在。
- isTimeOut 以距最后接收时间是否超过200ms判断；下游 getMinZInRange 没有先强制检查这个状态。
- scan 当前直接返回 true，stop 只修改扫描标志；它们在此实现中不能被解释为已发出雷达硬件启停指令。

另一驱动 `standard/LidarRsHeliosDevice` 也是 InfcLidar，但不是当前 Slam3DDevice 的直接点云来源。回答型号和协议问题时跟随运行实例，不能混用类。

## 坐标与旋转

Slam3DDevice 的 livoxMid360Device 字段是实际下级设备。get3DSlamData 调它的 getXYZ；getXYZ 依次绕 X、Y、Z 按安装角度旋转，输出 `double[]{x,y,z,intensity}`。

getMinZInRange 在旋转后的坐标上过滤：

```text
frontStart <= X <= frontEnd
leftRange  <= Y <= rightRange
startHeight <= Z <= endHeight
```

全部边界包含端点。leftRange/rightRange 是 Y 的下/上界，不能擅自改成负左正右的绝对距离。相对地面的高度含义需要结合安装位置和旋转配置；区间本身在雷达校正坐标系中，未见此方法另加安装高度平移。

有符合条件的点则返回最小Z；没有则 null。它既不直接返回沿路径里程，也不把区间宽度当移动距离。

导航投影的 zMin/zMax、disXMin/disYMin 等属于另外的数据处理分支；getMinZInRange 直接在 getXYZ 结果上按方法参数筛选，不能默认它继承投影过滤结果。

## “沿路径行走指定区间检测停止”

证据：`plugin/device/nav/RobotAccurateDevice.java:slamMoveWith3D`。

循环每轮：取选中3D雷达 -> 查区间最小Z -> 满足条件就 break -> 否则 go(pathId,false) -> finally 等300ms。退出后发 comDrive(0,0,0)。

| checkType | UI名称 | 实际停止条件 |
|---|---|---|
| 0 | 从无到有 | 本轮 rel != null |
| 1 | 从有到无 | 本轮 rel == null |

当前实现没有记录“先无后有/先有后无”的历史状态，启动就满足条件可以立即停；“从有到无”也没有要求先稳定观测到物体。空点云、数据格式异常与真实消失应分别分析。

循环为 while(true)，没有显式超时或 CommonAction/NavRunThread 取消条件；捕获 Throwable 后打印并继续。若误选设备导致强转异常，或区间永远不满足条件，可能一直循环。通用“停止所有”能否使该动作退出不能由按钮名称保证，须核对具体代码路径。

## 用户 F3 区间

这些是用户截图的配置快照，不是仓库内默认值：

| 点位动作 | X范围 | Y范围 | Z范围 | 条件 |
|---|---:|---:|---:|---|
| ID16 | 0～500 | 1000～2000 | 1900～3000 | 有点即停 |
| ID56 | 50～4000 | 0～3000 | -300～-100 | 无点即停 |

二者检查不同空间区域。ID16 后续还前进350再重设里程7000；ID56 后续重设里程14430。检测停止时的车体位置、缓停位移、等待期间点云历史，都影响重新赋值的物理参考点。

## 排查方法

先核对 Communication 收包时间、包格式/点数、设备树及 useRpFlag，再看原始点云、旋转后的点云和区间内点数。将“雷达坐标空间”与“路径里程空间”分开记录。

需要离线验证时，用用户提供的同一时刻点云、安装角度和参数计算筛选结果；只验证空间判定，不能声称因此证明整车动态过程。缺少现场数据时不要凭高度正负改区间。
