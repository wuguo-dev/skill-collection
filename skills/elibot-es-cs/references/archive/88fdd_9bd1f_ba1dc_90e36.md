# 双机器人协同透传

URL: https://docs.elibot.cn/cs/88fdd/9bd1f/ba1dc/90e36
发布时间: 2026-04-28

# 一、简介



**本案例使用俩台机器人，其中从机器人跟随主机器人的运动，进行同步运动
**需要的脚本文件作为附件置于文末，运行时需要放置在同目录下



# **二、操作流程**



**1、**将代码与附件章节的代码放置到同一目录下，此时文件夹中应有四份文件



**2、**确保俩台机器人有充足的运动空间，程序启动时，从属机器人会先运动到主机器人的相同位姿



**3、**修改代码中两台机器人的IP地址，**MASTER_IP**是主动机器人的地址，**FOLLOW_IP**是从动机器人的地址



**4、**执行下方的python文件，此时从属机器人会监听主机器人的运动，并保持跟随。



# **三、常见问题**



**1、**Q:为什么从属机器人运动更慢，无法跟上主机器人的运动速度。



A:优先确保俩台机器人的速度滑块设定的全局速度是一致的。如果俩台机器人全局速度一致仍然有滞后，可以再适度加大**RTSI_FREQ**的值。



# 四、代码和附件



代码流程图如下图所示：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MTAxLCJwYXRoIjoiaW1hZ2UucG5nIiwidGltZXN0YW1wIjoiMjAyNi0wNC0yOVQxMDoyMzoxMi42MzQrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--415149e0778e71319ad4facd9e610f32594eabba0dd48a5d960a219ef1612ee4/image.png)



**主要流程**：



- `send_script_to_follow(script_path)` Socket 直连 `(FOLLOW_IP, 30001)` → `sendall(script)` 发 `follow_ema.script` 到从机
- 起子线程 `master_reader_thread()`：



- `rtsi(MASTER_IP)` → `connect()` → `version_check()` → `controller_version()`
- `output_subscribe('actual_joint_positions', 250)` 订阅关节角 @ 250Hz
- `start()` → 循环 `get_output_data()` 读关节 → 加锁写 `_latest_joints`
- `disconnect()`



- 主线程等 master 第一帧
- 起子线程 `follow_writer_thread()`：



- `rtsi(FOLLOW_IP)` → `connect()` → `version_check()` → `controller_version()`
- `output_subscribe('output_int_register0', 10)` 订阅脚本就绪信号
- `input_subscribe('input_double_register0~6')` 订阅 7 个输入寄存器
- `start()` → 等 `output_int_register0 == 1`（脚本就绪）
- 再连一次 `rtsi(FOLLOW_IP)` → `output_subscribe('actual_joint_positions', 50)` → `start()` → `get_output_data_buffered` 读当前关节 → `disconnect()`
- **软启动**：`interpolate_joints(current, target, t)` 50 步 → 写寄存器 `input_double_register0~5 = joints` + `input_double_register6 = 1` → `set_input()`
- **正常透传**：250Hz 从 `_latest_joints` 取 → 写寄存器 → `set_input()`
- 停止时写 `flag=0` → `disconnect()`



- 退出：`stop_follow_script()` Socket 直连 30001 发 `halt()`



**涉及的接口**：



**组件****接口**RTSI (master)`rtsi(ip) / connect / version_check / controller_version / output_subscribe / start / get_output_data / disconnect`RTSI (follow)`rtsi(ip) / connect / version_check / controller_version / output_subscribe / input_subscribe / start / get_output_data_buffered / set_input / disconnect`30001 (Socket)`socket.connect → sendall(script) / sendall("halt()\n")`



```
"""
透传控制：纯 RTSI 直驱，follow 跑脚本监听寄存器 + EMA 外推
master -> PC(30004 read) -> PC(30004 write) -> follow(30001 script reads register)

依赖：rtsi.py, serialize.py（同目录下）
"""

import sys
import os
import time
import struct
import threading
import signal
import math
import socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ServoJ_RTSI联合', 'python'))
from rtsi import rtsi

# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────
MASTER_IP = "192.168.254.138"
FOLLOW_IP = "172.16.15.45"

RTSI_FREQ = 250.0              # Hz
SERVOJ_TIME = 1.0 / RTSI_FREQ  # = 0.004s

SOFT_START_DURATION = 1.0      # 软启动时间（秒）
SOFT_START_STEPS = 50

_running = True
_latest_joints = None
_lock = threading.Lock()

def _signal_handler(sig, frame):
    global _running
    print("\n[INFO] 收到退出信号，正在停止...")
    _running = False

    # 发送 halt() 停止 Follow 脚本
    stop_follow_script()

# ──────────────────────────────────────────────
# 停止 Follow 脚本（30001 端口发送 halt）
# ──────────────────────────────────────────────
def stop_follow_script():
    """通过 30001 端口发送 halt() 停止 Follow 机器人脚本。"""
    script_port = 30001
    try:
        print(f"[INFO] 发送 halt() 到 Follow ({FOLLOW_IP}:{script_port})...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5.0)
        sock.connect((FOLLOW_IP, script_port))
        sock.sendall(b"halt()\n")
        sock.close()
    except Exception as e:
        print(f"[WARN] 停止 Follow 脚本失败: {e}")

# ──────────────────────────────────────────────
# 线性插值 & 软启动
# ──────────────────────────────────────────────
def lerp(a, b, t):
    return a + (b - a) * t

def interpolate_joints(start, end, t):
    return [lerp(s, e, t) for s, e in zip(start, end)]

def joints_diff(a, b):
    return max(abs(ai - bi) for ai, bi in zip(a, b))

# ──────────────────────────────────────────────
# Master 读取线程（30004 订阅 actual_joint_positions）
# ──────────────────────────────────────────────
def master_reader_thread():
    """以 RTSI_FREQ Hz 持续读取 master 关节位置，写入 _latest_joints。"""
    global _latest_joints, _running

    print(f"[INFO] 连接 master RTSI ({MASTER_IP})...")
    rt_master = rtsi(MASTER_IP)
    try:
        rt_master.connect()
    except Exception as e:
        print(f"[ERROR] 无法连接 master RTSI: {e}")
        _running = False
        return

    rt_master.version_check()
    version = rt_master.controller_version()
    print(f"[INFO] Master 控制器版本: {version}")

    # 订阅输出：actual_joint_positions（6个关节角）
    out_vars = 'actual_joint_positions'
    out_data = rt_master.output_subscribe(out_vars, RTSI_FREQ)

    rt_master.start()
    print(f"[INFO] Master RTSI 启动，订阅 {out_vars} @ {RTSI_FREQ}Hz")

    interval = 1.0 / RTSI_FREQ
    try:
        while _running:
            t0 = time.perf_counter()

            # 接收 master 数据 (buffer=4 约 16ms 延迟)
            recv_out = rt_master.get_output_data()
            if recv_out and recv_out.actual_joint_positions:
                joints = list(recv_out.actual_joint_positions)
                with _lock:
                    _latest_joints = joints

            elapsed = time.perf_counter() - t0
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    finally:
        rt_master.disconnect()
        print("[INFO] Master RTSI 已断开")

# ──────────────────────────────────────────────
# Follow 写入线程（30004 写 input_double_register）
# ──────────────────────────────────────────────
def follow_writer_thread():
    """以 RTSI_FREQ Hz 将 master 关节位置写入 follow 的寄存器。"""
    global _running

    print(f"[INFO] 连接 follow RTSI ({FOLLOW_IP})...")
    rt_follow = rtsi(FOLLOW_IP)
    try:
        rt_follow.connect()
    except Exception as e:
        print(f"[ERROR] 无法连接 follow RTSI: {e}")
        _running = False
        return

    rt_follow.version_check()
    version = rt_follow.controller_version()
    print(f"[INFO] Follow 控制器版本: {version}")

    # 订阅 follow 的 output_integer_register0（确认 follow 脚本已启动）
    out_follow_data = rt_follow.output_subscribe('output_int_register0', 10)

    # 订阅输入：6个关节角 + 1个 flag，共 7 个 input_double_register
    in_vars = 'input_double_register0,input_double_register1,input_double_register2,input_double_register3,input_double_register4,input_double_register5,input_double_register6'
    in_data = rt_follow.input_subscribe(in_vars)

    rt_follow.start()
    print("[INFO] Follow RTSI 启动")

    # 先等待 follow 脚本启动（output_int_register0 == 1）
    print("[INFO] 等待 follow 脚本启动...")
    deadline = time.time() + 15
    reg_ready = False
    while time.time() < deadline and _running:
        recv = rt_follow.get_output_data_buffered(512)
        if recv and recv.output_int_register0 == 1:
            reg_ready = True
            print("[INFO] Follow 脚本已就绪")
            break
        time.sleep(0.05)

    if not reg_ready:
        print("[WARN] Follow 脚本未就绪，继续尝试写入（可能已等待超时）")

    # 等待 master 读到第一帧
    with _lock:
        master_target = _latest_joints

    if master_target is None:
        print("[ERROR] 无法获取 master 目标位置")
        _running = False
        return

    print(f"[INFO] Master 初始关节: {[round(v, 4) for v in master_target]}")

    # 读取 follow 当前实际关节位置（软启动用）
    rt_master_snapshot = rtsi(FOLLOW_IP)
    rt_master_snapshot.connect()
    rt_master_snapshot.version_check()
    out_follow_snapshot = rt_master_snapshot.output_subscribe('actual_joint_positions', 50)
    rt_master_snapshot.start()
    time.sleep(0.2)
    recv_snap = rt_master_snapshot.get_output_data_buffered(512)
    follow_current = list(recv_snap.actual_joint_positions) if recv_snap else [0.0] * 6
    rt_master_snapshot.disconnect()

    print(f"[INFO] Follow 当前关节: {[round(v, 4) for v in follow_current]}")
    diff = joints_diff(follow_current, master_target)
    print(f"[INFO] 初始位置差: {diff:.4f} rad")

    # ─── 软启动阶段 ───
    print(f"[INFO] 开始软启动 ({SOFT_START_DURATION}s, {SOFT_START_STEPS}步)...")
    soft_interval = SOFT_START_DURATION / SOFT_START_STEPS
    for i in range(SOFT_START_STEPS + 1):
        if not _running:
            break
        t = i / SOFT_START_STEPS
        joints = interpolate_joints(follow_current, master_target, t)

        in_data.input_double_register0 = joints[0]
        in_data.input_double_register1 = joints[1]
        in_data.input_double_register2 = joints[2]
        in_data.input_double_register3 = joints[3]
        in_data.input_double_register4 = joints[4]
        in_data.input_double_register5 = joints[5]
        in_data.input_double_register6 = 1  # flag=1 表示有新数据
        rt_follow.set_input(in_data)

        time.sleep(soft_interval)

    if not _running:
        rt_follow.disconnect()
        return

    print("[INFO] 软启动完成，进入正常透传模式")

    # ─── 正常透传（250Hz）───
    interval = 1.0 / RTSI_FREQ
    last_sent = time.perf_counter()

    try:
        while _running:
            t0 = time.perf_counter()

            with _lock:
                joints = _latest_joints

            if joints is not None:
                in_data.input_double_register0 = joints[0]
                in_data.input_double_register1 = joints[1]
                in_data.input_double_register2 = joints[2]
                in_data.input_double_register3 = joints[3]
                in_data.input_double_register4 = joints[4]
                in_data.input_double_register5 = joints[5]
                in_data.input_double_register6 = 1   # flag=1 → 有新数据
                rt_follow.set_input(in_data)
                last_sent = t0

            elapsed = time.perf_counter() - t0
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    finally:
        # 发送停止信号（flag=0，follow 脚本会停在最后位置）
        in_data.input_double_register6 = 0
        rt_follow.set_input(in_data)
        rt_follow.disconnect()
        print("[INFO] Follow RTSI 已断开")

# ──────────────────────────────────────────────
# 发送脚本到 follow（30001 端口）
# ──────────────────────────────────────────────
def send_script_to_follow(script_path):
    """通过 30001 端口发送脚本到 follow 机器人。"""

    script_port = 30001  # Elite 机器人的脚本端口
    
    # 读取脚本文件
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
    except Exception as e:
        print(f"[ERROR] 读取脚本失败: {e}")
        return False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10.0)
        sock.connect((FOLLOW_IP, script_port))
        print(f"[INFO] 已连接 follow 脚本端口")

        # 发送脚本内容
        sock.sendall(script_content.encode('utf-8'))
        print(f"[INFO] 脚本已发送 ({len(script_content)} 字节)")

        # 等待确认
        response = sock.recv(1024)
        print(f"[INFO] Follow 响应: {response.decode('utf-8', errors='ignore').strip()}")

        sock.close()
        return True

    except Exception as e:
        print(f"[ERROR] 发送脚本失败: {e}")
        return False

# ──────────────────────────────────────────────
# 主函数
# ──────────────────────────────────────────────
def main():
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    port_dir = os.path.dirname(__file__)
    script_path = os.path.abspath(os.path.join(port_dir, 'follow_ema.script'))

    if not send_script_to_follow(script_path):
        print("[ERROR] 脚本发送失败，退出")
        sys.exit(1)

    # 等待脚本启动
    time.sleep(0.5)

    t_master = threading.Thread(target=master_reader_thread, daemon=True, name="master-reader")
    t_master.start()

    print("[INFO] 等待 master 第一帧数据...")
    deadline = time.time() + 10
    while _latest_joints is None and _running:
        if time.time() > deadline:
            print("[ERROR] 等待 master 数据超时")
            sys.exit(1)
        time.sleep(0.05)

    print(f"[INFO] Master 初始关节: {[round(v, 4) for v in _latest_joints]}")

    t_follow = threading.Thread(target=follow_writer_thread, daemon=True, name="follow-writer")
    t_follow.start()

    try:
        while _running and t_master.is_alive() and t_follow.is_alive():
            time.sleep(0.5)
    except KeyboardInterrupt:
        _signal_handler(None, None)

    stop_follow_script()

    t_master.join(timeout=3)
    t_follow.join(timeout=5)
    print("[INFO] 透传已停止，程序退出")

if __name__ == "__main__":
    main()

```



[serialize.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MDk4LCJwYXRoIjoic2VyaWFsaXplLnB5IiwidGltZXN0YW1wIjoiMjAyNi0wNC0yOVQxMDoxMTozNi4zODUrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--795f746bae4003051aa754f07432ecc082daa809290aa871ef4c69cd78054fec/serialize.py?disposition=attachment)5.3 KB



[follow_ema.script](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MDk5LCJwYXRoIjoiZm9sbG93X2VtYS5zY3JpcHQiLCJ0aW1lc3RhbXAiOiIyMDI2LTA0LTI5VDEwOjExOjM2LjQ4OCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--b52a3da1cf3ef2771f753e8fd3a7d0be555e1a380b16bcc624412212c57da184/follow_ema.script?disposition=attachment)1.3 KB



[rtsi.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MTAwLCJwYXRoIjoicnRzaS5weSIsInRpbWVzdGFtcCI6IjIwMjYtMDQtMjlUMTA6MTE6MzcuNjMzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--cb20d219af36093bf3b57fb267170698dc9ae425b089685703841bd4cd9976c1/rtsi.py?disposition=attachment)14.6 KB
