# 巡检任务、识别和业务集成

## 普通巡检任务主干

`TaskDevice 创建任务/Quartz触发 -> TaskExec队列 -> RobotTaskExecService -> Plc.execTask -> 获取导航目标 -> 具体导航实现 -> 点位动作 -> OcrDevice/其他检测 -> 历史记录 -> TaskDevice.taskEnd -> 复核/报告`。

### 创建和排队

- TaskDevice 初始化任务表、菜单。createTask 保存任务及 TaskImgFuncMap 等关联，并按条件入队。
- startUpInit 从 state=0、issystem=0 的任务中恢复待执行项，排除已存在 ImgHistory 的表计项。
- TaskDevice.execute 是 Quartz 回调，读取 SysCrontab 后调用 execTask。
- execTaskNow 通过修改执行时间并重建队列实现优先执行，不等于绕过 Plc 的工作时间/电量等门槛。
- 状态：0待执行，1执行中，2中途取消/失败，3完成。恢复逻辑还会结合历史、当前任务ID和电量/工作状态。

### 执行门槛

证据：`robotWheeled/sysService/RobotTaskExecService.java`、`robotWheeled/Plc.java:execTask`。

RobotTaskExecService 是注册到 SysServices 的后台服务，循环调用 Plc.execTask，要求控制模式为任务模式。Plc 进一步检查反序列化完成、工作时间、低电量恢复、最低充电时间和当前电量。然后按 execTime 取最早到期任务，标记执行中。

源码有注释/占位逻辑，例如 execTask 局部 hasBarrier 当前固定为 false；不能只凭“虚拟墙检查”的注释声称实际启用了该拦截。

### 任务怎样变成导航点

证据：TaskDevice.getPointByTaskId/getPointByImgFuncMapList；Plc.execTask。

`TaskImgFuncMap.imgFuncId -> ImgFunction.positionId -> ActionChain -> ActionChain.pid -> 导航点ID`。按 isQrCodeNav 的兼容分支，动作链层级可能不同。

- isQrCodeNav 为 true 时还根据 navDevice 的实际类分流：NavCore 调 PathService.taskToStart；RobotNavDevice 调 stopAndInitParamsAndRun。
- 另一分支通过 metroDevice 反推点位，进入 LaserNavCore 的 SlamService。
- 任务只给导航目标，必经点由导航规划补入。禁用状态、表计项是否已完成、动作链层级都会改变最终点列表。
- 不能把同一屏中全部启用点当成任务目标，也不能把普通巡检 Task 和外部梁场主机 taskNo 当作同一个标识。

## 自动配置巡检是另一套编排

`autoConfig/RobotAutoConfigDevice` 维护 ROBOT_EXEC_DEQUE、RobotTaskPoint、RobotAutoPoint 等；receiveTask/toAutoPoints 处理点位编码和历史，按 robotType 和 inspectionNavMode 选择策略。还有单独的任务持久化/恢复、异步识别队列和停止方法。

普通 TaskDevice.ROBOT_TASK_DEQUE、NavRunThread 优先队列、RobotAutoConfigDevice 的任务队列并非同一队列。检查“停止后继续跑/重启后恢复”要明确是哪套入口和哪个恢复开关，不能只清一个列表就推断全停。

## 到点动作与图像识别

证据：`plugin/device/ocr/OcrDevice.java`；`ocr/model/ImgFunction.java`；`ocr/model/ImgHistory.java`。

- ImgFunction 是表计/巡检项配置，不只是图像算法；positionId 通常关联到动作节点。
- OcrDevice 根据方法选择相机/图像输入、目标结果和识别 SDK。拍照、可见光、红外、手动录入各有不同流程，不能由设备名称“图像识别”推断一定运行了 OCR 算法。
- 截图“手动录入”对应 doUserInput(pid,value,bytes,res,ytBytes)，查该 pid 下的 ImgFunction 并保存值；value=1 是录入结果，不能直接当作导航到位确认。
- saveImgDataMain 生成 ImgHistory、设置告警等级、更新识别缓存、保存记录，并通知观察者。
- TaskDevice.update 在普通任务分支给收到的 ImgHistory 补当前 taskId，按复核配置校验/处理重复记录，再保存并转发事件。识别记录先保存、任务关联后补，需沿观察者链看完整状态。
- Plc.init 注册 TaskDevice 观察 OcrDevice，MQTT/告警灯等又观察任务或识别事件；结果可能继续触发业务联动。
- BaseDevice.put 的普通属性历史/告警与 ImgHistory 的巡检图像结果是两条数据机制。

## 任务完成与报告

TaskDevice.taskEnd 清当前任务标识。成功分支调用 imgHistoryCheck 复核记录，可能安排补巡；其他结束类型更新为2，低电量结束可覆盖原因。随后保存结束时间/备注，通知观察者，按 backOcr 等条件后台生成报告。

NavRunThread 当前 execSuccessFlag 初始化后未由每次 navToPoint 返回结果汇总，navToPoint 的动作返回值也存在仅记录局部变量的情况。因此“导航线程正常结束”“任务状态完成”“每个业务动作成功”“报告内容有效”应分别验证。

报告入口 TaskDevice.docReport/roundPoll，图片压缩与记录查询也在 TaskDevice。识别异常先看 ImgHistory、配置关联和原始图片，而不是仅看最终报告。

## 梁场检测主机

`plugin/device/liangchang/LiangChangJianCeDevice` 通过 HTTP 接外部主机，提供创建任务、同步任务号、回弹/钢筋/尺寸/外观检测及结束任务等方法。真实主机地址/超时来自 ConfigParam。

- startSize 先 syncTaskNo，再 POST `/api/size/start`，按响应字段 `ok` 判断成功，记录 sessionNo。
- captureSize 获取 photoId，测距后 uploadSizeDistance 回填；setSizeValue、stopSize 结束/提交相应尺寸过程。
- 该主机任务会话与 station 普通巡检任务不同，重启后本地 taskNo 丢失也可能需要同步。
- RobotAccurateDevice 的点云定位控制行走；LiangChangJianCeDevice 的尺寸检测控制外部会话。只有动作链显式编排时，两者才形成业务流程。
- 截图中未勾选的脚本、机械臂、点云下载等不纳入本次实际执行推演；脚本名“梁长-首检测”的实际内容属于现场 SysScript，源码没有该数据库内容就不能补写其算法。

## 其他项目模块

轨道巡检看 robotTrack，第三方导航看 seerNav/seerV2，多设备项目看 ynen/metro/centralize 等。此基线只建立主入口地图；遇到具体问题仍追踪对应项目调用链，不将普通轮式巡检规则推广为全系统统一规则。
