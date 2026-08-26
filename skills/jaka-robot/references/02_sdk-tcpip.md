# SDK 与 TCP/IP 控制

来源：[SDK 简介](https://www.jaka.com/docs/guide/V3/SDK/introduction.html)、[SDK 快速开始](https://www.jaka.com/docs/guide/V3/SDK/%E8%8A%82%E5%8D%A1%20SDK%20%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B%20-%20CN.html)、[TCP/IP 控制协议](https://www.jaka.com/docs/guide/V3/tcpip.html)。

## SDK 版本与调用顺序

- V3 文档适配 SDK V2.3.0+、控制器 V3.0.1+；支持 Linux x86/x64/arm64 和 Windows x86/x64。
- V3 控制器目前只支持 gRPC。控制器 >3.2 时，首次使用需在 JAKA App 设置 `jaka_sdk` 密码，并把控制源切换为 SDK。
- SDK 位移统一为 mm，角度统一为 rad，编码为 UTF-8。
- 调用任何接口前先 `login_in()`；控制命令前检查上一调用的返回值。
- 典型顺序：登录 → 读取版本/状态 → 上电 → 使能 → 设置负载/TCP/用户坐标系 → 可达性与模式检查 → 非阻塞运动 → 轮询完成/超时 → 停止或下使能 → 登出。
- 伺服模式中不能调用普通 `joint_move`、`linear_move`、`circle_move`；Servo 指令与滤波参数按独立章节配置。
- Python 中一个阻塞 SDK 调用会卡住其他 Python 线程；状态监控和运动并行时使用非阻塞运动并显式轮询。

各语言类名、参数顺序、布尔/枚举定义和动态库路径从对应官方 C/C++/C#/Python 页面复制，不凭记忆补全。升级 SDK 时先查废弃接口页。

## TCP/IP 端口

### 10001：控制请求/响应

```json
{"cmdName":"get_robot_state"}
```

```json
{"cmdName":"get_robot_state","errorCode":"0","errorMsg":"","enable":true,"power":1}
```

所有指令均为非阻塞。收到 `errorCode=0` 仅说明请求被接受或接口成功返回，运动/程序仍需通过 `get_motion_state`、`get_program_state`、`inpos` 等状态确认完成。

### 10000：状态推送

返回字符串化状态，可能包含包长、实际/指令关节位置、实际/指令 TCP 位姿、柜体/TIO/扩展 IO、程序状态、模式、倍率、软限位、急停、上电、运动中、保护性停止等。按 `len` 处理粘包/拆包，不假设一次 `recv` 就是一条完整 JSON；官方说明一般最大包长取决于内容，可接近 15000 字节。

发送周期和可选字段由 `optionalInfoConfig.ini` 及 10000/10004 配置接口控制。修改控制器配置前先读取当前值并保留回滚值。

## TCP/IP 特有约定

- 位姿 `[X,Y,Z,Rx,Ry,Rz]`：X/Y/Z 为 mm，姿态为固定坐标系 x-y-z 顺序的 RPY 分量，单位 degree。
- `errorCode` 可能是数字或字符串；`0`、`"0"` 都视为成功，Empty/Null 不是成功。
- TCP/IP IO 索引从 1 开始，SDK IO 索引从 0 开始。
- 10001 的命令 JSON 与返回 JSON 均使用 `cmdName`；保持请求命令与响应的关联，并记录 `errorMsg`。
- 网络层设置连接、读取和动作完成三类独立超时。断线时先停止继续下发，再查询机器人真实状态，禁止盲目重发运动命令。
