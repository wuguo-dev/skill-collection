# 架构、启动和配置

基线：2026-10-19，`D:/WorkSpace/code/station`。本文定位主干，不声称穷尽全部 1073 个 Java 文件或所有项目定制。

## 系统设计思路

系统把“设备实现”和“现场编排”分开：Java 插件提供能力，配置表决定实例及依赖，动作链/脚本/工作流编排业务，后台服务不断消费通信与任务状态。理解行为时要同时看这四层。

| 层 | 主要入口 | 决定什么 |
|---|---|---|
| Web | MainModule、main/controller、JSP、mvc | 页面、接口、过滤、动态 URL |
| 配置/数据 | BaseService、ConfigService、model/table | 配置缓存、保存通知、脚本、动作与字典 |
| 插件/通信 | DeviceService、BaseDevice、CommuService | 设备实例、方法代理、参数注入、硬件协议 |
| 业务调度 | SyService、CronService、task/nav/autoConfig/ocr 等 | 常驻服务、定时任务、巡检、定位、识别与报告 |

## 启动顺序

证据：`src/main/webapp/WEB-INF/web.xml`；`src/main/java/main/MainModule.java`；`MainSetup.java:init`。

1. Servlet 容器加载 Nutz NutFilter，以 MainModule 为主模块。
2. MainModule 声明 MainSetup、`ioc/chain.js`、JavaScript IoC 配置和 `service`/`plugin.crontab` 注解扫描，启用事务和异步支持。
3. MainSetup 取得 IoC、PropertiesProxy。外部 HOME_PATH 由配置基础目录加 HOME_PATH_SUB 或 servlet context 名称形成，通常落在独立 station 运行目录。
4. 加入 JNI/JNA 库目录，加载外部 `station.properties`，注册类型转换和 JSON 处理器，确定数据库 URL。非 `jdbc:` 字符串按外部 HOME_PATH 下的 SQLite 文件解释。
5. 初始化 BaseService、ConfigService、DeviceService，加载基础 JavaScript 和脚本绑定。
6. 后台线程依次请求 `initDevice()`、CommuService、CronService、SyService。注意每个 `DeviceService.loadDev` 还会另起线程执行设备 `init()`，不能推断所有设备初始化已经完成。
7. 记录启动日志并执行初始化钩子。退出调用 StationService.destroy、注销 JDBC 驱动。

依赖初始化与服务就绪之间存在异步边界。排查“刚启动时偶发为空”需看具体设备线程/服务状态，不能只凭“系统启动”日志认定全部就绪。

## 设备如何被创建

证据：`service/DeviceService.java:getInstance/loadDev`；`infc/BaseDevice.java:setEnv/filter`。

- `Device` 是实例配置；`DeviceType.klass` 决定 Java 实现类。未配置实现类时可能使用 BaseDevice。
- DeviceService 构造设备及 ASM 拦截代理，保存到以 ID 为键的实例映射。
- `@AoStation(type=param)` 字段从 ConfigParam 注入。
- 子设备通过 Device.parentId、目标类型及字段名表达式解析并注入。required 子设备缺少时，某些情况下会自动创建配置记录。
- BaseDevice 的 `getParent()` 沿配置设备树解析，不应只用类的 Java 继承关系推断父设备。
- `@AoStation` 同时驱动设备标签、方法/参数 UI、通信命令、解析量等元数据。不同 AstEnum 语义不同。
- 方法代理允许 Workflow 或 DeviceObserver 介入。详细见 runtime.md。

`resources/conf/device.json` 是设备类型/命令/属性种子，不是部署现状的完整导出；loadDeviceConfig 对已有类型有保留逻辑。修改种子文件不意味着已有数据库中的设备类型随之改变。

## 配置与运行数据

| 模型/入口 | 用途 |
|---|---|
| Device / DeviceType / ConfigParam | 设备树、实现类、参数 |
| Communication / DeviceCommand / DeviceAnalysis | 通道、命令模板、响应解析 |
| DeviceProperty / DeviceReflect | 属性、记录策略、属性与外部点表映射 |
| DeviceAction / DeviceObserver | 条件联动、方法/动作组前后拦截 |
| ActionChain / ActionChainGroup | 命令编排、动作组 |
| SysUrl / SysScript / TWorkflow / TArtboard | 动态入口、脚本、工作流、图形流程 |
| SysServices / SysCrontab | 后台循环、Quartz 任务 |
| NavPath / NavPoint / NavPointMap / NavPathMulti | 复合导航路径、点位、映射与关联策略 |
| Task / TaskImgFuncMap / ImgFunction / ImgHistory | 巡检任务、表计项、识别配置和结果 |

源代码是机制，外部数据库是实例。只拿到源码时，F3、点位 16/56/77、动作组 pid、设备 ID 等现场记录不能由类名反推出来。

## 缓存与启用状态

证据：`service/BaseService.java:daoSave/getTCacheStream/getTCache`；`model/table/TBaseSeq.java:compareTo`。

- 缓存列表 `getTCacheStream` 过滤 `isRemoved == 0`；`getTCache(..., predicate)` 对 TBaseSeq 按 sequence 排序，相同时按 ID。
- `getTCache(Class, id)` 是直接查 Map，不走列表的启用过滤；禁用项仍可能被显式 ID 引用获取。
- 返回对象是缓存原始对象。直接改字段而不 daoSave，可能让缓存与持久化状态不一致。
- daoSave 更新缓存并通知观察者；设备/通信/服务等观察者可以响应配置变化。但并非所有参数变化都保证重新初始化整个设备，需检查相应 update 方法。

## 主题边界

- `nav` 是复合导航；`slamNav` 既含老 LaserNavCore，也含共享雷达处理；不能看到 slamNav 就认定业务跑在 LaserNavCore。
- `robotWheeled` 包含 Plc 宿主、驱动、控制、电量和服务，NavCore 是另一套导航实现。
- `seerNav`、`seerV2`、`robotTrack`、`autoConfig` 有各自状态机与队列。先核实 DeviceType.klass、Plc.navDevice、robotType/inspectionNavMode 再选路径。
- `liangchang`、`ynen`、`metro` 等代表不同业务集成。以真实方法调用链决定相关性。
