# references 说明

本目录是艾利特（Elibot）ES/CS 系列官方技术文档（https://docs.elibot.cn/cs/）的**主题化精华整理**，2026-08-07 抓取。

## 文件索引
| 文件 | 内容 |
|---|---|
| 01_产品与选型.md | 产品线（CS/CSF/CSH/CSA/防爆/CSR/ES/LS）、控制柜、示教器、选型资料 |
| 02_快速上手.md | 开机上电、模式、安装/负载设置、VNC/网页示教器/文件传输/虚拟机、备份升级、远程开机 |
| 03_坐标系与位姿.md | 基座/用户/工具坐标系、3点/4点示教、位姿单位、变换函数、偏移指令、可加减限制 |
| 04_图形化编程.md | 程序编写建议、跳转实现、深度复制、变量导入、点位修改、节拍优化、提前触发、轨迹复现、回原位、文件读写、力矩查看 |
| 05_硬件与接线.md | 标准/B1/MINI 柜 IO、急停与防护停止、末端 IO、485、抱闸、远程开机、大负载第二电源 |
| 06_通讯.md | 二次开发端口（29999/30001/30004/30020/40011/30011）、Modbus、EtherNet-IP、Profinet、Fins、Socket、RS485 |
| 07_二次开发.md | Python/C++/C# SDK、启动流程、端口文档 |
| 08_ROS2.md | CS_ROS2 驱动、控制器、MoveIt2、Gazebo、C++/Python 案例 |
| 09_应用工艺.md | 码垛、焊接、力控、涂胶、传送带跟踪、视觉引导、CNC |
| 10_故障处理.md | 故障代码、通用排查、密码/IP 重置、old 文件恢复、运维技巧 |
| 11_生态与插件.md | 插件安装卸载、IO 扩展、夹爪/视觉适配、工具类插件 |
| archive/ | 完整抓取的官方文章快照（Markdown，按 URL 层级命名），供查细节 |

## 官方原文（在线核对最新版本）
- 首页：https://docs.elibot.cn/cs/
- EC/EA 文档：https://docs.elibot.cn/ec ｜ FAQ：https://docs.elibot.cn/faq ｜ 官网：https://www.elibot.com/
- 各主题原文 URL 见 SKILL.md 第 0 节及各参考文件头部。

## 刷新本地快照
运行 `../scripts/fetch_elibot_docs.py` 重新抓取 docs.elibot.cn/cs 全部文章并更新 `archive/`（会覆盖 archive 内容，需联网）。
