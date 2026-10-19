# 源码入口与版本复核

默认根目录 `D:/WorkSpace/code/station`。下表使用相对根目录的路径，符号后为2026-10-19读取时的行号提示。查阅时以当前方法定义为准。

## 主干入口

| 主题 | 文件 | 关键符号/位置 |
|---|---|---|
| 容器 | src/main/webapp/WEB-INF/web.xml | Nutz NutFilter、main.MainModule |
| 启动 | src/main/java/main/MainSetup.java | init:32，外部配置、DB、异步初始化 |
| 动态路由 | src/main/java/main/MainModule.java | api，SysUrl/SysScript |
| 设备请求 | src/main/java/main/controller/JsonControler.java | devExec:793 |
| 配置缓存 | src/main/java/service/BaseService.java | daoSave:266，getTCache:799/817 |
| 动作选择 | src/main/java/service/ConfigService.java | getAction:155，initScript:78 |
| 设备构造 | src/main/java/service/DeviceService.java | getInstance:147，loadDev:193，getDeviceChild:305 |
| 方法代理 | src/main/java/infc/BaseDevice.java | filter:280，invoke:329/736，put:537 |
| 通信服务 | src/main/java/service/CommuService.java | commuStart:79，listen:151 |
| 通信队列 | src/main/java/common/CommuncationThread.java | run:58，addPoll:94 |
| 通信命令 | src/main/java/common/Command.java | sendCommand、analysiser |
| 后台服务 | src/main/java/service/SyService.java | startService |
| 定时服务 | src/main/java/service/CronService.java | add:48，exec:79 |
| 推送 | src/main/java/service/WebsocketRoom.java | /websocket，sendDevice |
| 动作引擎 | src/main/java/common/CommonAction.java | chainRun:59/76/126/179，stop:217 |
| 线程/延迟 | src/main/java/plugin/device/actionChain/ActionChainDevice.java | actionGroupThread:83，waitMSecond:133 |

## 导航入口

| 文件（src/main/java/ 后） | 关键符号/位置 |
|---|---|
| plugin/device/nav/RobotNavDevice.java | goWithPathAndDisc:173；setRobotAtThisPoint:286 |
| 同上 | go:321；stopAndInitParamsAndRun:650；renderId2SlamPoint:701 |
| 同上 | getRobotCurPoint:760；p2p:873；navToPoint:1159 |
| 同上 | changeToOtherPathPoint:1268；fixPostionPreAction:1304；fixPostion:1336；goHome:1614 |
| plugin/device/nav/threads/NavRunThread.java | call:68，子路线执行:92 |
| plugin/device/nav/param/point/RobotNavRunPoint.java | compareTo:28，comparePointId:53 |
| plugin/device/nav/PlcPostionDevice.java | setRobotPathAndPathPostion:74，getPathPostion:144/216 |
| plugin/device/nav/RobotAccurateDevice.java | slamMoveWith3D:338 |
| plugin/device/nav/model/NavPoint.java | postion:15，isAccurate:21 |
| plugin/device/nav/model/NavPath.java | 路径字段与继承sequence |
| plugin/device/nav/model/NavPointMap.java | 路径点映射 |
| plugin/device/nav/model/NavPathMulti.java | 关联/备用策略字段 |
| plugin/device/nav/enums/NavPointTypeEnum.java | TASK/MUST/MUST_BACK/P2P/CHARGE |
| plugin/device/nav/enums/NavPathTypeEnum.java | 策略和参数类映射 |
| plugin/device/nav/RobotNavConfigDevice.java | init，动态参数UI |
| plugin/device/nav/param/path/PathParamAbstract.java | xzLevels / moveStep |
| plugin/device/robotWheeled/PlcDriveDevice.java | comDrive:74，mmCount:295 |
| plugin/deviceInfc/AbstractDriveDevice.java | 驱动契约、单位 |

对应页面：`src/main/webapp/WEB-INF/pc/plugin/nav/navPoint.jsp`，isRemoved:77、No:80、列表sequence:151、设置位置:162、前往:182、停止:232。

## 雷达与巡检入口

| 文件（src/main/java/ 后） | 关键符号/位置 |
|---|---|
| plugin/device/hardware/lidar/LivoxMid360Device.java | comRx:93，getXYZ:145，isTimeOut:182 |
| plugin/device/slamNav/Slam3DDevice.java | getXYZ:222，getMinZInRange:463 |
| plugin/device/slamNav/SlamDevice.java | getUseRp:104 |
| plugin/device/standard/LidarRsHeliosDevice.java | 另一型号驱动，非MID360 |
| plugin/device/robotWheeled/Plc.java | init:285，execTask:689，导航分派:777 |
| plugin/device/robotWheeled/sysService/RobotTaskExecService.java | run，控制模式门槛 |
| plugin/device/task/TaskDevice.java | startUpInit:128，getPointByImgFuncMapList:502，taskEnd:534 |
| plugin/device/autoConfig/RobotAutoConfigDevice.java | receiveTask:422，toAutoPoints:451，stopAndClearCurTaskQueue:1493 |
| plugin/device/ocr/OcrDevice.java | doUserInput:684，saveImgDataMain:1799 |
| plugin/device/ocr/model/ImgFunction.java | positionId |
| plugin/device/ocr/model/ImgHistory.java | 结果记录 |
| plugin/device/liangchang/LiangChangJianCeDevice.java | createTask:82，startSize:397，httpJson:714 |

## 重新定位相关源码

```powershell
rg -n '目标标签|方法名' D:/WorkSpace/code/station/src/main/java
rg -n 'isAccurate|setRobotAtThisPoint|postion' D:/WorkSpace/code/station/src/main/java/plugin/device/nav
rg -n 'URL片段' D:/WorkSpace/code/station/src/main/webapp/WEB-INF
```

通过 `source-index.json` 记录已读关键文件的SHA-256和具体锚点。用 `scripts/source_probe.py --check` 检查全部，或 `--topic architecture/runtime/navigation/radar/inspection` 缩小范围。默认只读输出当前定位，`--check` 仅输出差异摘要；没有扫描文件内容中的配置值到输出。

基线Git HEAD若可从本地元数据读取则记录在清单中；这不证明工作树干净。文件哈希才是本次分析源码内容的版本依据。现场部署WAR的版本尚未比对。

新增源码版本后，先重新阅读变化的方法并更新受影响参考，再更新清单。不要仅重算哈希使“检查通过”，那会丢失知识过期信号。
