# 异常监控线程

URL: https://docs.elibot.cn/cs/88fdd/9bd1f/ba1dc/58e59
发布时间: 2026-07-03

# 一、简介



**本案例****基于原生 socket 二进制协议解析实现机器人状态实时监控（30001 端口），同时通过 30020 解释器端口以 125Hz 频率发送 servoj 指令控制机器人关节运动。监控线程可检测急停、保护停止、温度/电压/电流越限等 11 类异常并实时告警。****
**需要的脚本文件作为附件置于文末，运行时需要放置在同目录下



# **二、操作流程**



- 修改代码顶部 `ROBOT_IP` 为机器人真实 IP
- 修改 `INITIAL_JOINT_TARGET` 六关节目标角度（弧度），作为 demo 正弦运动的基准位置
- 如需调整异常检测阈值，修改 `THRESHOLD_TEMP` / `THRESHOLD_CURRENT` 等参数
- 如需调整伺服频率，修改 `SERVOJ_FREQ`（默认 125Hz）和对应的 `SERVOJ_T` / `LOOKAHEAD_TIME` / `GAIN`
- 执行代码文件，机器人开始正弦摆动，同时终端每 10 秒打印一次状态摘要



# **三、常见问题**



- Q：为什么程序启动后机器人不动？



A：先确认机器人已上电、释放抱闸、处于远程模式。其次查看终端日志，如果出现连接失败，检查 IP 是否可达、30001 和 30020 端口是否未被占用。



- Q：为什么监控报警但机器人仍在运动？



A：监控线程仅负责告警，不会自动停止机器人。如需异常自动停机，请在 `detect_anomalies` 的调用处增加 `stop_event.set()` 逻辑。



- Q：servoj 频率设为 125Hz 是什么含义？



A：125Hz 表示控制线程每 8ms 通过 30020 端口发送一帧 `servoj` 脚本。实际伺服平滑度还取决于 `lookahead_time`（前向平滑 0.1s）和 `gain`（增益 300）参数，可酌情调整。



# 四、代码和附件



**主要流程**：



- `socket.connect((ROBOT_IP, 30001))` 连 30001 端口（监控用），设置 2s 超时
- 起 `monitor_thread_fn()` 监控子线程：



- `sock.recv(4)` 读长度头 → `struct.unpack(">I", hdr)` 解大端 uint32
- 按长度读 payload → 取首字节 `msg_type`，仅处理 `MESSAGE_TYPE_ROBOT_STATE(16)`
- `parse_robot_state(state_data)` 按子消息 ID 逐段分发解析：
- `parse_robot_mode_data(48字节)` → 时间戳/模式/急停/速度倍率
- `parse_joint_data(6×57字节)` → 6 关节的实测/目标位置、速度、电流、温度、力矩、关节模式
- `parse_masterboard_data(83字节)` → IO 位、模拟量、主板温度、整机电压/电流、安全模式
- `parse_safety_state(38字节)` → 安全 CRC、操作模式、肘部位置
- `parse_additional_info(5字节)` → Freedrive 按钮/碰撞检测状态
- `parse_tool_data(25字节)` → 末端工具电压/电流/温度
- `detect_anomalies(state, thresholds)` 检测 11 类异常（急停/保护停止/模式异常/温度/速度/电压/电流/Freedrive 等）
- `state_summary(state)` 每 10 帧打印一次状态摘要



- 起 `servoj_thread_fn()` 控制子线程：



- `socket.connect((ip, 30001))` → `sendall("interpreter_mode(clearQueueOnEnter=True, clearOnEnd=True)\n")` 通过 30001 开启解释器模式
- `socket.connect((ip, 30020))` 连解释器端口 → `setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)` 禁用 Nagle 降低延迟
- `_send_servoj(sock, joints)` → 拼接 `def a():\n servoj([j0..j5], t=0.008, lookahead_time=0.1, gain=300)\nend\n` → `sendall(script.encode())` 通过 30020 逐帧发送
- 125Hz 定频从 `cmd_queue` 取目标关节



- 起 `demo_joint_generator(initial_joints)` 演示线程：



- 每 100ms 对 6 关节做独立正弦插值（幅值 0.3rad × 频率 0.2Hz × 各关节相位偏移）→ `cmd_queue.put_nowait(current)` 推入命令队列



- 主线程每秒检查 `latest_state` → 调 `detect_anomalies` 打印异常或 `state_summary` 打印状态
- Ctrl+C → `stop_event.set()` → 队列推 `None` → 各线程 `sock.close()` 退出



**涉及的接口**：



**组件****接口****用途**30001 (Socket)`socket.connect → recv` 二进制 `struct.unpack(">I", hdr)` 解长度头 + 按长度收 payload + 首字节取 msg_type持续接收机器人状态包30001 (Socket)`socket.connect → sendall("interpreter_mode(...)")`开启解释器模式30020 (Socket)`socket.connect → setsockopt(TCP_NODELAY) → sendall("def a():\n servoj(...)")`解释器端口逐帧发送 servoj 脚本struct.unpack`">Q???????BBdddB??I"` (48B) / `">dddiiiffffBI"` (每关节57B×6) / `">II BBB ddd BBB ddd ffff BBBBB"` (83B) / `">IBBdddd"` (38B) / `">BBBBB"` (5B) / `">BBddBfBB"` (25B)大端二进制逐字段解包detect_anomalies检查 is_emergency_stopped / is_protective_stopped / is_task_paused / robot_mode / safety_mode / joint_mode / temperature / velocity / voltage / current / masterboard_temp / is_freedrive_button_pressed11 类异常实时检测Queue`put_nowait / get(timeout=0.5)`关节生成器 → 控制线程的解耦管道



```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elite CS 系列机器人状态监控 + 伺服控制双线程脚本

监控线程：连接 30001 端口，持续解析 ROBOT_STATE 并检测异常。
控制线程：先通过 30001 端口发送 interpreter_mode() 开启解释器模式，
          再通过 30020 端口定时发送 servoj 指令控制机器人运动。

用法：
  改脚本顶部配置（机器人 IP、目标关节角度），直接运行。
  python elite_servoj_control.py
"""

import json
import queue
import socket
import struct
import sys
import threading
import time
from collections import defaultdict
from datetime import datetime

# =====================================================================
# 配置
# =====================================================================
ROBOT_IP = "172.16.101.122"
ROBOT_PORT = 30001

# 监控线程配置
MONITOR_TIMEOUT = 2.0
THRESHOLD_TEMP = 80.0
THRESHOLD_CURRENT = 10.0
THRESHOLD_TORQUE = 50.0
THRESHOLD_VELOCITY = 3.0
THRESHOLD_ROBOT_VOLTAGE = 60.0
THRESHOLD_ROBOT_CURRENT = 20.0
THRESHOLD_MASTERBOARD_TEMP = 70.0
SUMMARY_EVERY = 10

# 控制线程配置
SERVOJ_PORT = 30020           # 发送 servoj 的端口（需先用 30001 开启解释器模式）
SERVOJ_FREQ = 125             # servoj 控制频率 Hz
SERVOJ_T = 1.0 / SERVOJ_FREQ  # 每帧时间
LOOKAHEAD_TIME = 0.1          # servoj lookahear_time 参数 (s)
GAIN = 300                    # servoj gain 参数

# 初始目标关节角度（弧度），6 个关节
# 改这里可以改变机器人目标位置
INITIAL_JOINT_TARGET = [0.0, -1.57, 1.57, 0.0, 1.57, 0.0]


# =====================================================================
# 枚举与常量
# =====================================================================
MESSAGE_TYPE_ROBOT_STATE = 16
MESSAGE_TYPE_ROBOT_MESSAGE = 20

SUB_ROBOT_MODE_DATA = 0
SUB_JOINT_DATA = 1
SUB_CARTESIAN_INFO = 4
SUB_MASTERBOARD_DATA = 3
SUB_ADDITIONAL_INFO = 8
SUB_TOOL_DATA = 2
SUB_SAFETY_STATE = 10

ROBOT_MODE = {
    0: "DISCONNECTED", 1: "CONFIRM_SAFETY", 2: "BOOTING",
    3: "POWER_OFF", 4: "POWER_ON", 5: "IDLE",
    6: "BACKDRIVE", 7: "RUNNING", 8: "UPDATING_FIRMWARE",
    9: "WAITING_CALIBRATION",
}
SAFETY_MODE = {
    1: "NORMAL", 2: "REDUCED", 3: "PROTECTIVE_STOP",
    4: "RECOVERY", 5: "SAFEGUARD_STOP", 6: "SYSTEM_EMERGENCY_STOP",
    7: "ROBOT_EMERGENCY_STOP", 8: "VIOLATION", 9: "FAULT",
    10: "VALIDATE_JOINT_ID", 11: "UNDEFINED_SAFETY_MODE",
    12: "AUTOMATIC_MODE_SAFEGUARD_STOP",
    13: "SYSTEM_THREE_POSITION_ENABLING_STOP",
}
JOINT_MODE = {
    235: "RESET", 236: "SHUTTING_DOWN", 238: "BACKDRIVE",
    239: "POWER_OFF", 240: "READY_FOR_POWEROFF",
    245: "NOT_RESPONDING", 246: "MOTOR_INITIALISATION",
    247: "BOOTING", 249: "BOOTLOADER",
    251: "VIOLATION", 252: "FAULT", 253: "RUNNING", 255: "IDLE",
}
OK_ROBOT_MODES = {4, 5, 7}
OK_SAFETY_MODES = {1, 2}
# 255 表示未初始化/空闲，不报异常
IGNORE_SAFETY_MODES = {255}
BAD_JOINT_MODES = {245, 246, 247, 249, 251, 252}


# =====================================================================
# 解析函数（索引取值）
# =====================================================================

def parse_robot_mode_data(data: bytes):
    if len(data) < 48:
        return None
    vals = struct.unpack(">Q???????BBdddB??I", data[:48])
    return {
        "timestamp": vals[0],
        "is_robot_power_on": bool(vals[3]),
        "is_emergency_stopped": bool(vals[4]),
        "is_robot_protective_stopped": bool(vals[5]),
        "is_task_running": bool(vals[6]),
        "is_task_paused": bool(vals[7]),
        "robot_mode": vals[8],
        "robot_control_mode": vals[9],
        "target_speed_fraction": vals[10],
        "speed_scaling": vals[11],
        "target_speed_fraction_limit": vals[12],
        "robot_speed_mode": vals[13],
        "is_in_package_mode": bool(vals[15]),
    }


def parse_joint_data(data: bytes):
    joints = []
    per_joint = 57
    for i in range(6):
        off = i * per_joint
        if off + per_joint > len(data):
            break
        vals = struct.unpack(">dddiiiffffBI", data[off:off + per_joint])
        joints.append({
            "index": i,
            "actual_joint": vals[0],
            "target_joint": vals[1],
            "actual_velocity": vals[2],
            "current": vals[6],
            "voltage": vals[7],
            "temperature": vals[8],
            "torque": vals[9],
            "joint_mode": vals[10],
        })
    return {"joints": joints}


def parse_masterboard_data(data: bytes):
    if len(data) < 83:
        return None
    vals = struct.unpack(">II BBB ddd BBB ddd ffff BBBBB", data[:83])
    return {
        "digital_input_bits": vals[0],
        "digital_output_bits": vals[1],
        "standard_analog_input_domain0": vals[2],
        "standard_analog_input_domain1": vals[3],
        "tool_analog_input_domain": vals[4],
        "standard_analog_input_value0": vals[5],
        "standard_analog_input_value1": vals[6],
        "tool_analog_input_value": vals[7],
        "standard_analog_output_domain0": vals[8],
        "standard_analog_output_domain1": vals[9],
        "tool_analog_output_domain": vals[10],
        "standard_analog_output_value0": vals[11],
        "standard_analog_output_value1": vals[12],
        "tool_analog_output_value": vals[13],
        "masterboard_temperature": vals[14],
        "robot_voltage": vals[15],
        "robot_current": vals[16],
        "io_current": vals[17],
        "safety_mode": vals[18],
        "is_robot_in_reduced_mode": bool(vals[19]),
        "operational_mode_selector_input": bool(vals[20]),
        "threeposition_enabling_device_input": bool(vals[21]),
        "internal_use": vals[22],
    }


def parse_safety_state(data: bytes):
    if len(data) < 38:
        return None
    vals = struct.unpack(">IBBdddd", data[:38])
    return {
        "safety_crc_num": vals[0],
        "safety_operational_mode": vals[1],
        "current_elbow_position_x": vals[3],
        "current_elbow_position_y": vals[4],
        "current_elbow_position_z": vals[5],
        "elbow_radius": vals[6],
    }


def parse_additional_info(data: bytes):
    if len(data) < 5:
        return None
    vals = struct.unpack(">BBBBB", data[:5])
    return {
        "is_freedrive_button_pressed": bool(vals[0]),
        "is_freedrive_io_enabled": bool(vals[2]),
        "is_dynamic_collision_detect_enabled": bool(vals[3]),
    }


def parse_tool_data(data: bytes):
    if len(data) < 25:
        return None
    vals = struct.unpack(">BBddBfBB", data[:25])
    return {
        "tool_analog_output_domain": vals[0],
        "tool_analog_input_domain": vals[1],
        "tool_analog_output_value": vals[2],
        "tool_analog_input_value": vals[3],
        "tool_voltage": vals[4],
        "tool_output_voltage": vals[5],
        "tool_current": vals[6],
        "tool_temperature": vals[7],
        "tool_mode": vals[8],
    }


def parse_robot_state(data: bytes):
    offset = 0
    result = {}
    while offset + 4 <= len(data):
        sub_len = struct.unpack(">I", data[offset:offset + 4])[0]
        offset += 4
        if sub_len < 4:
            break
        content = data[offset:offset + sub_len - 4]
        offset += sub_len - 4
        if not content:
            continue
        sub_type = content[0]
        sub_data = content[1:]
        try:
            if sub_type == SUB_ROBOT_MODE_DATA:
                parsed = parse_robot_mode_data(sub_data)
            elif sub_type == SUB_JOINT_DATA:
                parsed = parse_joint_data(sub_data)
            elif sub_type == SUB_CARTESIAN_INFO:
                continue  # 不解析，用 joint_data 的 target
            elif sub_type == SUB_MASTERBOARD_DATA:
                parsed = parse_masterboard_data(sub_data)
            elif sub_type == SUB_ADDITIONAL_INFO:
                parsed = parse_additional_info(sub_data)
            elif sub_type == SUB_TOOL_DATA:
                parsed = parse_tool_data(sub_data)
            elif sub_type == SUB_SAFETY_STATE:
                parsed = parse_safety_state(sub_data)
            else:
                parsed = None
        except Exception:
            parsed = None
        if parsed is not None:
            result[sub_type] = parsed
    return result


def detect_anomalies(state: dict, thresholds: dict):
    anomalies = []
    mode = state.get(SUB_ROBOT_MODE_DATA)
    master = state.get(SUB_MASTERBOARD_DATA)
    joints = state.get(SUB_JOINT_DATA)
    additional = state.get(SUB_ADDITIONAL_INFO)

    if mode:
        if mode.get("is_emergency_stopped"):
            anomalies.append("[EMERGENCY] 机器人处于急停状态")
        if mode.get("is_robot_protective_stopped"):
            anomalies.append("[PROTECTIVE] 机器人处于保护停止状态")
        if mode.get("is_task_paused"):
            anomalies.append("[PAUSED] 任务已暂停")
        robot_mode = mode.get("robot_mode")
        if robot_mode not in OK_ROBOT_MODES:
            anomalies.append(f"[ROBOT_MODE] 模式异常: {ROBOT_MODE.get(robot_mode, f'UNKNOWN({robot_mode})')} ({robot_mode})")

    safety_mode = None
    if master and "safety_mode" in master:
        safety_mode = master["safety_mode"]
    safety = state.get(SUB_SAFETY_STATE)
    if safety and "safety_operational_mode" in safety:
        safety_mode = safety["safety_operational_mode"]
    if safety_mode is not None and safety_mode not in OK_SAFETY_MODES and safety_mode not in IGNORE_SAFETY_MODES:
        anomalies.append(f"[SAFETY] 安全模式异常: {SAFETY_MODE.get(safety_mode, f'UNKNOWN({safety_mode})')} ({safety_mode})")

    if joints:
        for j in joints["joints"]:
            idx = j["index"]
            jm = j["joint_mode"]
            if jm in BAD_JOINT_MODES:
                anomalies.append(f"[JOINT_MODE] 关节{idx} 异常: {JOINT_MODE.get(jm, f'UNKNOWN({jm})')} ({jm})")
            if j["temperature"] > thresholds["temp"]:
                anomalies.append(f"[TEMP] 关节{idx} 温度过高: {j['temperature']:.1f}C")
            if abs(j["actual_velocity"]) > thresholds["velocity"]:
                anomalies.append(f"[VELOCITY] 关节{idx} 速度过大: {j['actual_velocity']:.3f}rad/s")

    if master:
        if master.get("robot_voltage", 0) > thresholds["robot_voltage"]:
            anomalies.append(f"[VOLTAGE] 电压过高: {master['robot_voltage']:.1f}V")
        if master.get("robot_current", 0) > thresholds["robot_current"]:
            anomalies.append(f"[CURRENT] 电流过大: {master['robot_current']:.2f}A")
        if master.get("masterboard_temperature", 0) > thresholds["masterboard_temp"]:
            anomalies.append(f"[TEMP] 主板温度过高: {master['masterboard_temperature']:.1f}C")

    if additional:
        if additional.get("is_freedrive_button_pressed"):
            anomalies.append("[FREEDRIVE] 自由驱动按钮被按下")

    return anomalies


def state_summary(state: dict):
    parts = []
    mode = state.get(SUB_ROBOT_MODE_DATA)
    master = state.get(SUB_MASTERBOARD_DATA)
    joints = state.get(SUB_JOINT_DATA)
    if mode:
        rm = mode.get("robot_mode")
        sm = master.get("safety_mode") if master else None
        parts.append(f"Mode={ROBOT_MODE.get(rm, rm)}")
        parts.append(f"Safety={SAFETY_MODE.get(sm, sm) if sm is not None else 'N/A'}")
        parts.append(f"TaskRunning={mode.get('is_task_running')}")
    if master:
        parts.append(f"V={master.get('robot_voltage'):.1f}V I={master.get('robot_current'):.2f}A")
    if joints and joints["joints"]:
        j0 = joints["joints"][0]
        parts.append(f"J0={j0['actual_joint']:.3f}rad speed={j0['actual_velocity']:.3f}")
    return "  ".join(parts)


# =====================================================================
# 监控线程
# =====================================================================

def monitor_thread_fn(ip: str, port: int, timeout: float,
                      latest_state: dict, state_lock: threading.Lock,
                      stop_event: threading.Event, log_fn):
    """持续读取 30001 端口，解析状态，写入 latest_state"""
    sock = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        log_fn(f"[Monitor] 已连接 {ip}:{port}")

        while not stop_event.is_set():
            # 读取 4 字节长度头
            hdr = b""
            try:
                while len(hdr) < 4:
                    chunk = sock.recv(4 - len(hdr))
                    if not chunk:
                        log_fn("[Monitor] 连接断开")
                        return
                    hdr += chunk
            except socket.timeout:
                continue
            except Exception as e:
                log_fn(f"[Monitor] 读取头异常: {e}")
                continue

            total_len = struct.unpack(">I", hdr)[0]
            if total_len < 4:
                continue

            # 读取 payload
            payload = b""
            try:
                while len(payload) < total_len - 4:
                    chunk = sock.recv(total_len - 4 - len(payload))
                    if not chunk:
                        log_fn("[Monitor] 连接断开")
                        return
                    payload += chunk
            except socket.timeout:
                continue
            except Exception as e:
                log_fn(f"[Monitor] 读取 payload 异常: {e}")
                continue

            if len(payload) < 1:
                continue

            msg_type = payload[0]
            if msg_type != MESSAGE_TYPE_ROBOT_STATE:
                continue

            state_data = payload[1:]
            state = parse_robot_state(state_data)
            with state_lock:
                latest_state["data"] = state
                latest_state["timestamp"] = time.time()
    except Exception as e:
        log_fn(f"[Monitor] 线程异常: {e}")
    finally:
        if sock:
            sock.close()
        log_fn("[Monitor] 线程结束")


# =====================================================================
# 控制线程：servoj 运动控制
# =====================================================================

def servoj_thread_fn(ip: str, port: int,
                     joint_cmd_queue: queue.Queue,
                     latest_state: dict, state_lock: threading.Lock,
                     stop_event: threading.Event, log_fn):
    """
    控制线程：
      1) 连 30001 发送 interpreter_mode() 开启解释器模式
      2) 连 30020 持续从队列取目标关节角度，发送 servoj
    队列可传 None 表示停止。
    """
    sock_30001 = None
    sock_30020 = None
    try:
        # 1) 用 30001 开启解释器模式
        sock_30001 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_30001.settimeout(2.0)
        sock_30001.connect((ip, 30001))
        log_fn(f"[Servoj] 已连接 {ip}:30001，准备开启解释器模式")

        init_script = b"interpreter_mode(clearQueueOnEnter = True, clearOnEnd = True)\n"
        sock_30001.sendall(init_script)
        log_fn("[Servoj] 已通过 30001 发送 interpreter_mode")
        time.sleep(0.2)

        # 2) 连接 port 发送 servoj
        sock_30020 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_30020.settimeout(2.0)
        sock_30020.connect((ip, port))
        sock_30020.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        log_fn(f"[Servoj] 已连接 {ip}:{port}")

        # 发送第一帧 servoj（防止首帧丢失）
        first_target = joint_cmd_queue.get(timeout=2.0)
        if first_target is None:
            return
        _send_servoj(sock_30020, first_target, log_fn)
        time.sleep(SERVOJ_T)

        while not stop_event.is_set():
            try:
                target = joint_cmd_queue.get(timeout=0.5)
            except queue.Empty:
                # 队列空，继续用上一帧
                continue

            if target is None:
                log_fn("[Servoj] 收到停止信号")
                break

            _send_servoj(sock_30020, target, log_fn)

            # 控制频率
            time.sleep(SERVOJ_T)

    except Exception as e:
        log_fn(f"[Servoj] 线程异常: {e}")
    finally:
        if sock_30020:
            sock_30020.close()
        if sock_30001:
            sock_30001.close()
        log_fn("[Servoj] 线程结束")


def _send_servoj(sock: socket.socket, joints: list, log_fn):
    """发送一帧 servoj 命令。joints 为 6 个弧度值的列表。"""
    if len(joints) != 6:
        raise ValueError(f"servoj 需要 6 个关节，当前: {len(joints)}")

    j0, j1, j2, j3, j4, j5 = joints
    script = (
        f"def a():\n"
        f"servoj([{j0},{j1},{j2},{j3},{j4},{j5}],"
        f"t={SERVOJ_T},"
        f"lookahead_time={LOOKAHEAD_TIME},"
        f"gain={GAIN})\n"
        f"end\n"
    )
    try:
        sock.sendall(script.encode("utf-8"))
    except Exception as e:
        log_fn(f"[Servoj] 发送异常: {e}")


# =====================================================================
# 演示：周期性更新目标角度（正弦插值）
# =====================================================================

def demo_joint_generator(initial_joints: list, stop_event: threading.Event,
                         cmd_queue: queue.Queue, log_fn):
    """演示：每个关节做独立正弦运动，定时 put 到队列"""
    import math
    amplitude = 0.3  # 弧度
    freq = 0.2       # Hz
    t = 0.0
    dt = 0.1         # 每步 0.1s

    current = list(initial_joints)

    while not stop_event.is_set():
        # 正弦更新
        for i in range(6):
            current[i] = initial_joints[i] + amplitude * math.sin(2 * math.pi * freq * t + i * 0.8)

        try:
            cmd_queue.put_nowait(list(current))
        except queue.Full:
            pass

        time.sleep(dt)
        t += dt


# =====================================================================
# 主程序
# =====================================================================

def main():
    # 日志
    def log(line: str):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[{ts}] {line}")

    thresholds = {
        "temp": THRESHOLD_TEMP,
        "current": THRESHOLD_CURRENT,
        "torque": THRESHOLD_TORQUE,
        "velocity": THRESHOLD_VELOCITY,
        "robot_voltage": THRESHOLD_ROBOT_VOLTAGE,
        "robot_current": THRESHOLD_ROBOT_CURRENT,
        "masterboard_temp": THRESHOLD_MASTERBOARD_TEMP,
    }

    # 共享状态
    latest_state = {"data": None, "timestamp": 0.0}
    state_lock = threading.Lock()
    stop_event = threading.Event()

    # 命令队列
    cmd_queue: queue.Queue = queue.Queue(maxsize=2)

    # 启动监控线程
    mon = threading.Thread(
        target=monitor_thread_fn,
        args=(ROBOT_IP, ROBOT_PORT, MONITOR_TIMEOUT,
              latest_state, state_lock, stop_event, log),
        daemon=True,
        name="MonitorThread"
    )
    mon.start()

    # 等待监控线程先跑起来
    time.sleep(0.5)

    # 启动控制线程
    ctrl = threading.Thread(
        target=servoj_thread_fn,
        args=(ROBOT_IP, SERVOJ_PORT,
              cmd_queue, latest_state, state_lock, stop_event, log),
        daemon=True,
        name="ServojThread"
    )
    ctrl.start()

    # 启动演示关节生成器
    demo = threading.Thread(
        target=demo_joint_generator,
        args=(INITIAL_JOINT_TARGET, stop_event, cmd_queue, log),
        daemon=True,
        name="JointGenerator"
    )
    demo.start()

    log(f"双线程已启动: 监控={ROBOT_IP}:{ROBOT_PORT}, 控制={ROBOT_IP}:{SERVOJ_PORT}")
    log(f"目标关节: {[f'{j:.3f}' for j in INITIAL_JOINT_TARGET]}")
    log("按 Ctrl+C 停止")

    packet_count = 0
    try:
        while True:
            time.sleep(1.0)
            with state_lock:
                state = latest_state.get("data")
                ts = latest_state.get("timestamp")

            if state is None:
                continue

            anomalies = detect_anomalies(state, thresholds)
            packet_count += 1

            if anomalies:
                log("=" * 50)
                log(f"检测到 {len(anomalies)} 项异常:")
                for a in anomalies:
                    log(f"  - {a}")
                log("=" * 50)
            elif packet_count % SUMMARY_EVERY == 0:
                log(f"[OK] {state_summary(state)}")

    except KeyboardInterrupt:
        log("收到中断信号，停止...")
    finally:
        stop_event.set()
        # 通知控制线程停止
        try:
            cmd_queue.put_nowait(None)
        except queue.Full:
            pass
        time.sleep(0.5)
        log("已停止")


if __name__ == "__main__":
    main()

```
