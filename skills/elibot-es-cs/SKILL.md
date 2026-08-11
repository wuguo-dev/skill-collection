---
name: elibot-es-cs
description: 艾利特（Elibot/ELITE ROBOTS）ES/CS 系列协作机器人的官方技术文档知识库与操作指南。使用场景：编写/优化 ES/CS 机器人图形化编程（任务树）程序、示教坐标系与TCP、使用偏移/赋值/循环等指令、配置IO与硬件接线、配置 Modbus/Profinet/EtherNet-IP/Socket/Fins 等通讯、使用 29999/30001/30004/30020/40011 端口二次开发、Python/C++/C# SDK、ROS2 驱动与 MoveIt2、码垛/焊接/力控/涂胶/传送带跟踪/视觉引导等工艺包、故障代码与排查、插件安装与生态适配。当用户提到艾利特机械臂、ES/CS系列、示教器、任务树、图形化编程、二次开发端口、CS_ROS2、E6Sxx 故障码等时使用本技能。
---

# 艾利特 ES/CS 协作机器人技术文档

本技能汇总艾利特官方 ES/CS 技术文档（docs.elibot.cn/cs）的核心知识，用于指导 ES/CS 系列协作机器人的编程、调试、二次开发与故障处理。详细资料见 `references/`（按主题整理的精华文档 + `archive/` 完整抓取快照），并附官方原文 URL 供核对最新版本。

## 0. 文档地图（先读这里）

| 主题 | 精华文档 | 官方原文 |
|---|---|---|
| 产品与选型 | references/01_产品与选型.md | docs.elibot.cn/cs/97375/af7fa |
| 快速上手/开机/模式/工具 | references/02_快速上手.md | docs.elibot.cn/cs/97375/cf056 等 |
| 坐标系、TCP、偏移 | references/03_坐标系与位姿.md | docs.elibot.cn/cs/97375/30661、/cs/d9b09/fcc78 |
| 图形化编程（任务树） | references/04_图形化编程.md | docs.elibot.cn/cs/d9b09/8e2b0 等 |
| 硬件与接线 | references/05_硬件与接线.md | docs.elibot.cn/cs/ab632 |
| 通讯（端口/Modbus/Profinet/EIP/Fins/Socket） | references/06_通讯.md | docs.elibot.cn/cs/e61bf |
| 二次开发 SDK/端口 | references/07_二次开发.md | docs.elibot.cn/cs/88fdd |
| ROS2 | references/08_ROS2.md | docs.elibot.cn/cs/1ffff |
| 应用工艺（码垛/焊接/力控/涂胶/传送带/视觉） | references/09_应用工艺.md | docs.elibot.cn/cs/1b89f |
| 故障处理 | references/10_故障处理.md | docs.elibot.cn/cs/5f00a |
| 生态与插件 | references/11_生态与插件.md | docs.elibot.cn/cs/3b5a8 |

## 1. 关键硬性约束（官方明确要求，违反会出问题）

- **单位**：位姿 XYZ 一律为**米(m)**，RX/RY/RZ 为**弧度(rad)**；数组顺序固定 `[x, y, z, rx, ry, rz]`。脚本里判断/偏移必须换算（`var[0]`=X，`[1]`=Y，`[2]`=Z）。
- **死循环必须加延时**：每个死循环体内必须加 **≥0.1s 延时**（如 `sleep(0.1)`），否则机器人 CPU 过载卡死。
- **Move 指令下只放路点**，不允许嵌套其他指令（赋值/判断/IO/延时放在循环或判断层）。
- **主程序只写逻辑指令**（不写运动指令），并建议在主程序里加循环，防止误改循环模式导致程序无法运行。
- **程序命名**：`程序名称（工站/工件型号）+ 日期`，如 `Main_墙面4x4网格打点_20260806`。
- **偏移指令（V2.13.0+）**：以**位姿**偏移生成的点必须用 **MoveL** 运行（用 MoveJ 会撞机）；以**关节数据**偏移才用 MoveJ。偏移后的点位都基于**基座**运行。
- **数组赋值**：数组间赋值建议勾选**深度复制**，否则 a、b 引用同一对象、b 改变 a 同步变。
- **CS 图形化编程无跳转指令**：用 `while` 循环 + `if` 判断/`switch` 开关 + 计数器（CNT）实现"跳转"。

## 2. 坐标系与位姿（示教、偏移、变换）

- 三类坐标系：**基座标系**（机器人安装基座，右手系）、**用户坐标系**（作业空间自定义，3 点法示教：原点→X+→Y+，Z 按右手定则=平面法向）、**工具坐标系 TCP**（4 点法示教位置，姿态用"示教姿态"对齐）。
- 位姿变换函数：`pose_trans(p1, p2)` 复合变换、`pose_inv(p)` 逆变换、`get_actual_tcp_pose()` 取当前 TCP 位姿（m/rad）。
- 常用换算：`pose_trans(pose_inv(用户坐标系), get_actual_tcp_pose())` = 基座位姿转用户坐标系下位姿；反方向用 `pose_trans(用户坐标系, 点位)`。
- **可加减限制**：基座/用户坐标系下只能直接加减 x/y/z/rz 四项，rx/ry 不能直接加减；工具坐标系下六项均可加减。
- 用户坐标系偏移（自定义 `Offs` 函数）：`pose_trans(pose_inv(user), p)` → 加偏移 → `pose_trans(user, ...)` 转回基座。
- **指令中设置 TCP**（2.11.0+）：`设置TCP` 指令只改变配置了"使用激活的 TCP"的路点；测试按钮仅作用于手动模式，自动运行按路点指令设置的 TCP。
- 负载重心设置、安装方式设置（正装/倒装/侧装）、奇异点说明见 references/03。

## 3. 图形化编程要点（任务树）

- 常用指令：MoveJ/MoveL/MoveP、偏移（复合）、赋值、判断/while 循环/switch、延时、数字/模拟 IO、设置（速度/TCP/坐标）、线程、脚本（def/sec）。
- 脚本类型：**def 脚本=主程序**（同时仅一个，新的 def 会强制停止旧的）；**sec 脚本=并行**（可与 def 同跑，但**不支持运动指令**，不允许耗时指令如 sleep/串口/socket 超时）。
- 偏移指令：基准路点（须先示教才会出现在列表）+ 常量偏移 / 变量偏移（6 元素数组 `[0.1,0,0,0,0,0]` 即 X+100mm）。
- 快速修改点位：复制粘贴保持关联（home 点）、编辑位姿方向箭头 ±mm、可变路点直接在全局变量改数组。
- 快速修改全局变量：示教器只能单个建 → 用 SFTP（root/elibot）改 `xxx.configuration.variables`；或写 `.variable` 文件（name,value,remarks,favorite）≥2.15 用「配置-全局变量-导入变量」，导入时任务会停止。
- 轨迹节拍优化：转接半径（默认 50，工艺关键点禁设）、速度上限（关节 230°/s、1200°/s²；直线 1500mm/s、10000mm/s²）、真实速度=设定速度×运行倍率、姿态变化大用 MoveJ、仅位移用 MoveL、规避 6 轴 180°/360° 大旋转。
- 运动到达提前触发：`point_dist()`（直线距离）或 `pose_dist()`（含姿态）+ 事件/线程 + 标志位。
- 轨迹复现：复合-轨迹记录（喷涂等），最大 141330 点，复现时速度必须 100%。
- 初始化判断自动回原位：`get_actual_tcp_pose()` 判断工作区域 → 直接安全高度（把安全点 Z 赋给当前 Z，不要 Z+ 偏移抬升）→ 直线 100mm/s 回安全点。
- 读写内部文件：A9 柜共享目录 `/rbctrl/EliRobot_share/program/`（对应 x86 的 /home/elite/user/program，≥2.5）；D9 柜 `/rbctrl/RT_CONTROLLER/ROBOT/program/`；用 Python 文件 API（open/write）注意缩进。
- 数字 IO 组合成寄存器：机器人内建 4 个端口寄存器（0=标准DI 可读不可写、1=可配置DI+工具DI、2=标准DO 可读可写、3=可配置DO+工具DO），`read_port_register(0)` / `write_port_register(2,3)`，必须按 DI0-15/DO0-15 顺序接线且占用后不可他用；≥2.13.1 可用 `bit_list_to_integer([DI0,DI1,...])` / `integer_to_bit_list`（≥2.12.1 用 byte_list_to_integer / integer_to_byte_list）。

## 4. 硬件与接线（速查）

- 控制柜：标准柜（A9 3网口 / D9 1网口）、B1 柜、MINI 柜（外部 DC 45-55V，必须配置供电方式：未配置/外部DC/电池，否则 E6S52 上电失败报警）。
- IO：标准柜 16DI/16DO（PNP）、8 组可配置输入+8 组可配置输出（成对使用、时间差校验）、模拟 IO（0-10V 或 4-20mA）、IO 电源（内部 24V 最大 2A，外部最大 6A）。默认内部供电。
- 安全 IO：急停（EI0-EI1）与防护停止（SI0-SI1）均**双通道冗余**，两通道信号中断允许时间差 **80ms**；只接通一路会触发安全违规报警；防护重置按钮需配置可配置安全输入。
- 末端 IO：CS 系列数字输入仅 PNP；数字输出可配 PNP/NPN（1A）；1/2 号引脚可配 485+/485- 或模拟量（ES/LS 固定 485）；双针电源模式最大 2000mA、持续 1s、占空比 10%、平均 ≤1000mA；多针模式会占用 IO。
- 485：标准柜 4 号引脚→485+、3 号引脚→485-；B1/MINI 柜 485A→+、485B→-、485G→GND；最大波特率 500Kbps；末端 485 与控制柜 485 除脚本指令外无区别。
- 抱闸：电磁式 vs 插销式（0x7E：0=插销/弹杆、1=电磁）；0x0A 先写 30000 再写 1（电磁）或 2（插销），断电重启生效；专家模式入口：右上角连点 5-8 次，密码 `elibot`。
- 远程开机：远程 ON/OFF 端子提供 12V 辅助电源；ON 有效脉冲 100-2000ms；通电自启动/远程开关机需 2.14+（详见 references/05）。
- 大负载（CS520H/530H/620/625/630）末端第二路 24V 电源：专家模式-伺服参数-末端I/O 0x53 写 11（勾 keep）、0x32 写 5；脚本 `set_tool_second_power_on(True/False)` 需 V2.16+。

## 5. 通讯与二次开发端口（TCP/IP，均可用 socket 同时连接）

- **29999 Dashboard**：上/下电、加载任务/配置、play/pause/stop、查询状态。命令以 `\n` 结尾。常用：`robotControl -on`（返回 Powering on）、`brakeRelease`（Brake is released）、`play`（Starting task）、`task -r`（Task is running）、`stop`、`pause`、`speed -v 50`、`robotMode`、`unlockProtectiveStop`。
- **30001**：机器人以 10Hz 推送状态报文（关节角/速度/力矩、TCP、IO、模式等）；可发送脚本/运动指令。远程模式下才允许外部控制，本地模式会强制断开外部连接。
- **30004 RTSI**：实时数据交互，按指定频率订阅指定数据，最快 250Hz；大端；协议=版本校验→设置→同步循环。
- **30020 解释器**：把实时计算的脚本排队到当前任务后执行（不打断），队列上限 8500；含 skipbuffer、statelastexecuted 等状态命令；`interpreter_mode` / `end_interpreter` / `clear_interpreter`。
- **40011 明文请求**：一问一答式；调用规则同 SEC（不能运动指令/耗时指令/死循环）。
- **30011**：另一数据/指令端口（详见 references/06）。
- SDK：Python（`Elite_Robots_CS_SDK_Python`，pybind11+CMake，需 CS 2.13.4+/2.14.2+、python3.6+）、C++（`Elite_Robots_CS_SDK`）、C#（`Elite_Robots_CS_SDK_CSharp`），见 GitHub Elite-Robots。
- 二次开发启动流程：29999 连接 → `robotControl -on` → `brakeRelease` → `play` → `task -r`，保持远程模式。
- Modbus：机器人可做 TCP 从站/主站、RTU 主站（末端/控制柜端口）；EtherNet/IP（欧姆龙/汇川/codesys 双机）、Profinet（西门子）、Fins（欧姆龙，插件 fins-2.13.elico，RPC xmlrpc http://IP:9601，`memoryAreaReadInt16("dm100")` 等）、Socket 插件、RS485 脚本通讯 —— 详细配置见 references/06。

## 6. ROS2（CS_ROS2）

- 环境：Ubuntu22.04 + ROS2；clone `Elite_Robots_CS_SDK`（cmake/make/sudo make install）与 `Elite_Robots_CS_ROS2_Driver`；rosdep + colcon build；连接 FB1+FB2 网口。
- 启动：`ros2 launch eli_cs_robot_driver elite_control.launch.py robot_ip:=<FB1 IP> local_ip:=<PC IP> cs_type:=cs63 launch_rviz:=false headless_mode:=true`；MoveIt2：`ros2 launch eli_cs_robot_moveit_config cs_moveit.launch.py cs_type:=cs66`；Gazebo：`eli_cs_robot_simulation_gz` 的 cs_sim_control / cs_sim_moveit。
- 控制器（ros2_control）：推荐 `scaled_joint_trajectory_controller`（按机器人实际速度缩放同步轨迹），另有 `forward_position_controller`、`forward_velocity_controller`、`freedrive_controller`；同一时间只能一个关节运动控制器 active。
- 关节名：`shoulder_pan_joint, shoulder_lift_joint, elbow_joint, wrist_1_joint, wrist_2_joint, wrist_3_joint`。
- 常用：`ros2 action send_goal /scaled_joint_trajectory_controller/follow_joint_trajectory ...`；上电 `ros2 service call /dashboard_client/power_on std_srvs/srv/Trigger "{}"`、`brake_release`、`play`；监控 `/io_and_status_controller/io_states`、`/joint_states`、`/speed_scaling_state_broadcaster/speed_scaling`。

## 7. 应用工艺（速查）

- **码垛工艺包**：任务-复合-码垛；排样=直线/矩阵/自定义；层、隔离层（隔离器）、每个工件处（ApproachPoint/ToolActionPoint/工具动作/ExitPoint）；矩阵四点须按顺/逆时针环形示教，列数=1-2 点间、行数=2-3 点间；参考点取第一层第一工件。内置变量 pallet_lct/pallet_lno/pallet_sep/pallet_tct。视觉偏移：方法一偏移用户坐标系（仅 XY，pose_trans），方法二脚本偏移目标点（码垛指令临时生成用户坐标系，须新插入 movel 并把点转 base+补偿再转回临时用户坐标系）。
- **焊接工艺包**（CS 2.13+，插件 WeldingTools）：TCP Z+ 必须朝下与焊枪出丝方向一致；模式=线性/管形/多层多道/点焊；摆动=月牙/圆圈/锯齿/梯型；JOB 模式（Bit0-3 二进制选任务）；焊机匹配=通用IO/脚本/总线；时序=预送气→起弧(送丝+防粘丝)→稳定→滞后送气；寻位需焊机支持；3D 查看轨迹（红=焊接、蓝=非焊接）。
- **力控**：CSF 系列内致力控模块（无需外挂）；CS 标准系列需 SensorAdapter 插件+外接力传感器；流程=工具IO 配置（RS485）→力传感器空载标定→负载辨识（4 姿态，只需动 4/5/6 轴）→（第三方传感器需安装角辨识，负载建议 ≥3kg）→开启力传感器碰撞检测（初始 10-15N）。
- **涂胶/轨迹平滑**：getpoes.script 采集点位生成 .ml 文件 + remotetcp 插件微段插补（时间间隔调大减抖动）。
- **传送带跟踪**（≥2.12）：增量编码器接 B4 高速 IO，正交式需 AB 两路输入；单机最多 2 条传送带。
- **2D 相机视觉引导上下料**：详见 references/09（Halcon/插件对接流程）。

## 8. 故障与运维速查

- 专家模式入口：右上角连点 5-8 次，密码 `elibot`；可在专家模式查看急停/防护停止状态（≥2.13）、伺服参数（0x51 传动比/0x62 额定转矩/0x64 额定电流/0x74 固件版本/0x7E 抱闸类型）。
- 常见故障码：E6S42 机器人连接断开、E12S75{joint} 关节编码器读取异常、E12S21{joint} 关节驱动器过流、E6S100 安全违规、E2S2 急停无法消除、E6S48 上电失败、E12S903 关节开抱闸异常、E6S25 主板急停输入切换不一致 —— 处理步骤见 references/10。
- 通用排查：不运动（检查模式/速度缩放/任务状态/急停）、抖动（转接半径/加速度/时间间隔）、碰撞报警（灵敏度 40-80%）、撞击卡死（references/10）。
- 忘记密码：魔术文件（U 盘根目录 `elimagic/` 文件夹放 .sh）或 SFTP 删除 `/home/elite/EliRobot/conf` 下 elipass（操作模式）/ elisafetypass（安全密码）后重启。
- 强制改 IP：魔术文件 elimagic_change_ip.sh（默认 192.168.1.110，≥2.10）。
- 任务恢复：≥2.12 保存后同目录生成 `xxx.number.old`（number 越小越新，最多 10 个），改后缀 .old→.task 或用示教器打开另存。
- 文件访问：SFTP root/elibot；网页示教器 `http://<IP>:5800/`；VNC 远程桌面；备份/升级（U盘/无U盘）见 references/02。

## 9. 工作方式建议

1. 先确认机器人型号（CS/ES/LS/CSF）、控制柜类型（标准 A9/D9、B1、MINI）与**软件版本**（偏移指令、导入变量、设置TCP、末端第二电源等功能有版本门槛）。
2. 写图形化编程方案时：初始化文件夹 → 测距/测量预留 → 主循环（while+if）→ 结束；Move 下只放路点；循环内 ≥0.1s 延时；偏移用变量数组 `[x,y,z,rx,ry,rz]`（m/rad）。
3. 涉及坐标系偏移：优先用官方**偏移指令**（V2.13+），位姿偏移配 MoveL、关节偏移配 MoveJ，落点统一基座。
4. 需要细节（接线图、完整脚本、协议报文）时，加载对应 `references/` 文档；需要最新版本时访问官方原文 URL。
5. 需要刷新本地文档快照：运行 `scripts/fetch_elibot_docs.py`（会自动重新抓取 docs.elibot.cn/cs 全部文章到 references/archive）。
