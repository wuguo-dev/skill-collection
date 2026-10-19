# 请求、设备方法、动作链和通信

## 用户操作到方法

标准设备入口：`main/controller/JsonControler.java:devExec`，类级 `@At("/json")`，方法级 `/devExec/?/?`。

`JSP/common.ajax -> /<context>/json/devExec/<设备标识>/<方法> -> DeviceService.getDeviceFirst -> BaseDevice.invoke -> 设备代理/实现 -> Command/外部接口`。

- 入口用 `req.getParameterMap()`，取每个键第一个值；不是直接把任意 JSON body 当参数 map。
- 设备标识解析交给 getDeviceFirst，不能假定永远是数值 ID。确认设备类型匹配哪一个实例。
- 方法为 `$` 时从 `methodName` 请求参数取名；`#` 前缀代表动作组扩展调用。
- MainModule 的 `/dev/<dev>/<method>` 转发到同一入口。
- 返回 null 会包装成成功 DataRes；返回 boolean false 可能只是 `data=false`。UI 的 success 提示不一定表示硬件执行成功。
- 返回文件、图像、View、DataRes 时有专门分支。具体请求契约需核对调用方和方法返回值。

认证和过滤需同时查看 `ioc/chain.js`、`mvc/BaseProcessor`、`CheckLevel`、`CrossOriginFilter`、`UserService` 及配置脚本。MainModule 和 JsonControler 的注解不同，不能用一个类的注解概括全部入口。BaseProcessor 的 urlCheck 脚本可在方法执行前阻断请求。

## 动态入口

`MainModule.api` 的 `/*` 查找 SysUrl，进行角色相关自动登录检查，替换返回参数，执行命名 SysScript，再按配置类型渲染 JSP、JSON、转发、重定向、RawView、代理或 SQL 结果。

找不到字符串形式的 Java @At 时，继续查 SysUrl/SysScript。部署数据库缺失时，明确说“动态映射尚未取得”，不要编造控制器。

## 参数与方法代理

证据：`infc/BaseDevice.java:invoke/filter`。

- Map 参数按真实参数名映射、转换；CommonAction 类型参数从专用键注入。字符串支持 `~` 恢复逗号、JSON 对象等转换。
- 动作链旧接口的 args 是有序逗号分隔字符串，以方法参数顺序映射；`#...` 可用 EL 求值。
- 缺少 pid 时，动作链调用可能默认使用当前 ActionChain.id。截图“手动录入 pid=5263”需确认它是识别配置所属节点，不是导航点位 ID。
- BaseDevice.filter 在实现方法前后调用 DeviceObserver，workflow 类型还可由配置 Workflow 替代方法实现。因此定位根因时检查运行设备的前后拦截和工作流。

## 动作链的执行与层级

证据：`common/CommonAction.java`；`service/ConfigService.java:getAction`；`model/table/ActionChain.java`。

- 顶层动作匹配 `plass`（所属类全名）、`pid`（所属记录 ID），只选 parentId 为空/0、type 为 0/1 的条目；子链按 parentId 获取。
- 启用列表通过 BaseService 过滤 `isRemoved==0`，再按 TBaseSeq.sequence/ID 排序。
- `chainRun(List)` 顺序执行；某项返回真值时进入它的子链。false 主要影响该项子链，不是默认终止整个后续列表。
- variable 可把返回值放入 CommonAction.args；`return` 变量影响链的返回值。
- 工作流设备 ID 特殊值 -2 有独立分支；普通项调用 BaseDevice.invoke。
- TBaseAction 还可按 actionType 分派到动作组、命名脚本、GraphAction、Workflow。普通 NavPoint/NavPath 基于 TBaseSeq，通常走其类名/ID 对应的动作链。
- 异常策略由 ignoreException/outException 等控制。void/null 返回不天然等价于业务失败；不能把 `chainRun(...) != null` 的局部变量当严格的执行成功判据。

## 并发与取消

证据：`plugin/device/actionChain/ActionChainDevice.java`；`CommonAction.stop`。

- actionGroupThread 另建 CommonAction 和线程；父动作返回不表示该线程已经完成。waitThreadEnd 仅针对该动作设备统计的线程且有等待上限。
- waitMSecond 每 5 ms 检查所属 CommonAction.isChainRun，具有协作中断能力。
- stop 只改变链继续执行的标志。正在执行的方法只有主动检查对应标志才会及时退出。
- 不同链对象、NavRunThread.THREAD_SET_DIE、后台服务 RUNNING 是不同控制域。检查一处 stop 不足以认定所有线程已停。

## 通信边界

证据：`service/CommuService.java`；`common/CommuncationThread.java`；`common/Command.java`。

1. Communication.klass/uri 决定传输实现，例如 UDPServer、TCP、JSerialPort、MQTT、Modbus 等。
2. 监听模式 open 后注册观察者并 receive；数据到 CommuService.listen 后分派至绑定该通道的设备及匹配命令。无模板时可以直接 comRx。
3. 轮询模式为通道创建 CommuncationThread，维护优先队列；队列空时收集该通道设备的 comPoll 命令。
4. 命令发送后设置 RX，再执行解析；DeviceCommand/DeviceAnalysis 和具体 comRx 共同决定解析。
5. BaseDevice.put 更新属性，按 DeviceAction 计算告警，按 DeviceProperty 注入字段、记录历史、通知或触发联动。

检查顺序：业务调用是否发生 -> 命令是否进入正确通道 -> 响应/超时 -> 解析及属性更新时间 -> 业务是否收到状态。协议响应只证明到该接口层，不自动证明车体完成位移。

例如 PlcDriveDevice.comDrive 返回 Command；comDriveResponse 等待协议响应，二者都不能仅凭名称推断会等待距离执行完毕。动作链在驱动后固定延时，只说明经过该时长，是否到位仍看里程反馈。

## 日志和前端反馈

WebsocketRoom 暴露 `/websocket`，分 root、设备、通信等房间。CommonAction 日志包含线程名和链对象标识；PlcDriveDevice 生成命令时还把调用栈放入 remark，可用于追踪意外驱动指令来源。

检查 BaseDevice.sendSocket 的 isLog 和部署日志配置，避免把只推给浏览器的消息当作一定保存在服务器上的日志。

前端控制接入或修改可配合既有 `station-device-ui-integration` 技能；此知识库提供该系统机制与入口，具体页面交互和请求契约仍需逐个核对。
