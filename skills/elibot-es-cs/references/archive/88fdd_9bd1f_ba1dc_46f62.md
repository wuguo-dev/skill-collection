# 力反馈设备控制机器人

URL: https://docs.elibot.cn/cs/88fdd/9bd1f/ba1dc/46f62
发布时间: 2026-04-27

# **一、简介**



**本案例使用序力智能 HFD-6 力反馈设备进行机器人控制
**需要的DLL和配方文件作为附件置于文末，运行时需要放置在同目录下



# **二、操作流程**



**1、**安装HFD-6力反馈设备USB驱动程序VCP-V1.3.1_Setup_x64.exe



[VCP_V1.3.1_Setup_x64.exe](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjgyNTA4LCJwYXRoIjoidmNwX3YxLjMuMV9zZXR1cF94NjQuZXhlIiwidGltZXN0YW1wIjoiMjAyNi0wNC0yNFQxNDowMDoyNC41MjUrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--eeb83130d60ae283a19d8bd1c5a7049cc1de0b85f8b4e8582f5f2d592ca4f896/vcp_v1.3.1_setup_x64.exe?disposition=attachment)6.2 MB



**2、**连接好设备的电源适配器与 USB 线后，启动电源，在计算机的设备管理器中，设备驱动描述符中出现如下名称：STMicroelectronic Virtual COM Port



**3、**下载附件中的文件，将他们和代码文件放在同一目录下。修改机器人的IP地址，以及port_dir文件目录



**4、**执行下方的python文件，此时机械臂会随摇杆一同运动。



# **三、常见问题**



**1、**Q:在计算机的设备管理器中，设备驱动描述符中出现黄色感叹号。



A:右键端口下面的设备描述符 STMicroelectronics Virtual COM Port，在弹出的快捷菜单中点**【更新驱动程序】**,在弹出的对话框中点击**【浏览我的电脑以查找驱动程序(R)】**,在接下来弹出的对话框中点击**【让我从计算机上的可用驱动程序列表中选取(L)】**,在驱动程序列表中选择【**STMicroelectronics Virtual COM Port**】，点击下一步, 如果看到**【Windows 已成功更新你的驱动程序】**，则更新完成，黄色感叹号消失。



# 四、代码和附件



代码流程图如下图所示：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjgyNTc0LCJwYXRoIjoiaW1hZ2UucG5nIiwidGltZXN0YW1wIjoiMjAyNi0wNC0yNFQxNjo1MzowNi4zMDArMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--d89131fc36de7888977bc061cdb3d169cdf9061341500a6c23f19d60342e852e/image.png)



**主要流程**：



- `Key_combination()` 初始化 HFD-6 摇杆
- 轮询 `hfdGetButton()` 等 0→1 上升沿
- 按下后：



- `rtsi(ROBOT_IP)` → `connect()` → `version_check()` → `controller_version()`
- `output_subscribe('actual_TCP_pose', 50)` → `start()` → `get_output_data_buffered(512)` 读 TCP 位姿 → `disconnect()`
- `calculate_xyz / calculate_rxryrz` 算基准 V5/V51
- `send_script(SCRIPT_PATH)` Socket 直连 30001，发送 `external_control_rocker.script`
- `get_inverse_kin(target_pose)` Socket 直连 40011，一次性 IK → 得初始关节角
- `_latest_joints = init_joints` 初始化



- 起 `rtsi_writer_thread(init_joints)`：



- `rtsi(ROBOT_IP)` → `connect()` → `version_check()` → `controller_version()`
- `output_subscribe('output_int_register0', 10)` 订阅脚本就绪信号
- `input_subscribe('input_double_register0~6')` 订阅 7 个输入寄存器（6 关节 + 1 flag）
- `start()` 启动 RTSI 数据流
- `get_output_data_buffered(512)` 等 `output_int_register0 == 1`（脚本就绪）
- 再连一次 `rtsi(ROBOT_IP)` → `output_subscribe('actual_joint_positions', 50)` → `start()` → `get_output_data_buffered` 读当前关节 → `disconnect()`
- **软启动**：`interpolate_joints(current, init, t)` 50 步 → `_write_joints(rt, in_data, joints, 1)` → `set_input(in_data)` 写寄存器
- **正常透传**：250Hz 从 `_latest_joints` 取关节 → `_write_joints(rt, in_data, joints, 1)` → `set_input(in_data)` 写寄存器
- 停止时 `_write_joints(rt, in_data, last_joints, 0)` 写 flag=0 → `disconnect()`



- 运行中每 4ms：



- `hfdGetPosition()` / `hfdGetOrientationRad()` 读摇杆 → 减原点
- `poseMul / userFrameToTcpFrame` 坐标变换链 → `get_inverse_kin(target_pose)` 40011 IK → 更新 `_latest_joints`



- 再按按钮：



- `stop_script()` Socket 直连 30001 发 `halt()` 停脚本
- `Key_combination_off()` 关摇杆力反馈



**涉及的接口**：



**组件****接口**HFD-6`hfdOpen / hfdInit / hfdCalibrateDevice / hfdGetPosition / hfdGetOrientationRad / hfdGetButton / hfdEnableForce / hfdEnableDevice / hfdSetGravityCompensation`RTSI (30004) 自研模块`rtsi(ip) / connect / version_check / controller_version / output_subscribe / input_subscribe / start / get_output_data_buffered / set_input / disconnect`30001 (Socket)`socket.connect → sendall(script) / sendall("halt()")`40011 (Socket)`socket.connect → sendall("req 1 get_inverse_kin([...])") → recv`坐标变换`euler_to_matrix / matrix_to_euler / pose_mul / pose_inv / base_pose_to_user_pose / user_frame_to_tcp_frame`



```
"""
CSRocker.py — 摇杆控制机器人

架构参考 touchuan_rtsi.py（E:\workspace\sub_touchuan\port）：

  - PC 端 250Hz 通过 RTSI 往 input_double_register 写入目标关节角
  - 机器人端 external_control_rocker.script 以 8ms 固定周期执行 servoj
  - 40011 端口仅用于启动前一次性获取初始关节角（IK 逆解）

对比原版改进：
  - 去掉 30020 解释器透传（延迟大、无周期保证）
  - 去掉每次循环的 40011 IK 查询（启动时仅一次）
  - RTSI 直驱：PC 端固定 4ms 周期写寄存器，机器人端 8ms servoj
  - 软启动：线性插值从当前关节到目标关节

依赖：rtsi.py, serialize.py（同目录下）
"""

import sys
import os
import time
import struct
import socket
import threading
import signal
import copy
import ast

# ── 复用参考目录的 RTSI 协议实现 ──────────────────────────────────────────
port_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        os.path.pardir, '..', 'sub_touchuan', 'port')
sys.path.insert(0, port_dir)
from rtsi import rtsi

import numpy as np
import transformations
from transformations.transformations import euler_from_matrix, inverse_matrix

import ctypes

# ============================================================================
# 常量
# ============================================================================
ROBOT_IP = "172.16.15.45"
RTSI_FREQ = 250.0
SERVOJ_TIME = 1.0 / RTSI_FREQ     # = 0.004s
SOFT_START_DURATION = 1.0          # 软启动时间（秒）
SOFT_START_STEPS = 50
SCRIPT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           "external_control_rocker.script"))

_running = True
_latest_joints = None
_lock = threading.Lock()

# ============================================================================
# HFD 摇杆驱动（与原版完全相同）
# ============================================================================
lib = ctypes.cdll.LoadLibrary('./HFD_API64.dll')

def hfdOpen():              return lib.hfdOpen()
def hfdInit():
    lib.hfdInit(-1); time.sleep(0.05)
def hfdCalibrateDevice():
    lib.hfdCalibrateDevice(-1); time.sleep(0.05)
def hfdGetPosition():
    fx = ctypes.pointer(ctypes.c_double())
    fy = ctypes.pointer(ctypes.c_double())
    fz = ctypes.pointer(ctypes.c_double())
    lib.hfdGetPosition(fx, fy, fz, -1)
    return [fx.contents.value, fy.contents.value, fz.contents.value]
def hfdGetOrientationRad():
    fx = ctypes.pointer(ctypes.c_double())
    fy = ctypes.pointer(ctypes.c_double())
    fz = ctypes.pointer(ctypes.c_double())
    lib.hfdGetOrientationRad(fx, fy, fz, -1)
    return [fx.contents.value, fy.contents.value, fz.contents.value]
def hfdEnableForce():       lib.hfdEnableForce(True, -1); time.sleep(0.05)
def hfdSetForce(x, y, z):   lib.hfdSetForce(ctypes.c_double(x), ctypes.c_double(y), ctypes.c_double(z), -1)
def hfdEnableExpertMode():  lib.hfdEnableExpertMode(); time.sleep(0.05)
def hfdEnableDevice():      lib.hfdEnableDevice(True, -1); time.sleep(0.05)
def hfdDisableExpertMode(): lib.hfdDisableExpertMode(); time.sleep(0.05)
def hfdSetGravityCompensation(): lib.hfdSetGravityCompensation(True, -1); time.sleep(0.05)
def hfdGetButton():         return lib.hfdGetButton(0, -1)

def Key_combination_on():
    hfdEnableExpertMode()
    lib.hfdEnableDevice(True, -1)
    hfdDisableExpertMode()
    lib.hfdSetGravityCompensation(True, -1)

def Key_combination_off():
    lib.hfdSetGravityCompensation(False, -1)
    hfdEnableExpertMode()
    lib.hfdEnableDevice(False, -1)
    hfdDisableExpertMode()

def Key_combination():
    a1 = hfdOpen()
    hfdInit()
    hfdCalibrateDevice()
    hfdEnableForce()
    hfdEnableExpertMode()
    hfdEnableDevice()
    hfdDisableExpertMode()
    hfdSetGravityCompensation()
    return a1

# ============================================================================
# 位姿运算（与原版完全相同）
# ============================================================================

def mm_deg_to_m_rad(pose):
    nn = copy.deepcopy(pose)
    nn[0] /= 1000; nn[1] /= 1000; nn[2] /= 1000
    nn[3] /= 57.2957; nn[4] /= 57.2957; nn[5] /= 57.2957
    return nn

def euler_to_matrix(pose):
    m = transformations.euler_matrix(pose[3], pose[4], pose[5])
    m[0][3], m[1][3], m[2][3] = pose[0], pose[1], pose[2]
    return m

def matrix_to_euler(mat):
    x, y, z = mat[0][3], mat[1][3], mat[2][3]
    mat = mat.copy()
    mat[0][3] = mat[1][3] = mat[2][3] = 0
    rx, ry, rz = euler_from_matrix(mat)
    return [float(x), float(y), float(z), float(rx), float(ry), float(rz)]

def pose_inv(pose):
    return matrix_to_euler(inverse_matrix(euler_to_matrix(pose)))

def pose_mul(pose1, pose2):
    return matrix_to_euler(np.matmul(euler_to_matrix(pose1), euler_to_matrix(pose2)))

def base_pose_to_user_pose(user, basepose):
    return pose_mul(pose_inv(user), basepose)

def user_frame_to_tcp_frame(user_pose, target):
    return pose_mul(user_pose, target)

def calculate_xyz(tcp, pose):
    V2 = pose_inv(mm_deg_to_m_rad([-pose[0], pose[2], pose[1], 0, 0, 0]))
    V1 = base_pose_to_user_pose(mm_deg_to_m_rad([-340.1, -171.1, 311.4, 0, 0, 0]), tcp)
    V4 = pose_mul(V2, [V1[0], V1[1], V1[2], 0, 0, 0])
    return V4

def calculate_rxryrz(tcp, pose):
    V21 = pose_inv([0, 0, 0, pose[3], pose[4], pose[5]])
    V1 = base_pose_to_user_pose(mm_deg_to_m_rad([-340.1, -171.1, 311.4, 0, 0, 0]), tcp)
    V41 = pose_mul(V21, [0, 0, 0, V1[3], V1[4], V1[5]])
    return V41

# ============================================================================
# 40011 明文请求（仅用于启动前一次性 IK）
# ============================================================================

def _send_40011(cmd_id, statement):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((ROBOT_IP, 40011))
    sock.sendall(f"req {cmd_id} {statement}\n".encode())
    resp = sock.recv(1024).decode('utf-8')
    sock.close()
    return resp

def get_inverse_kin(target_pose):
    """通过 40011 调用 get_inverse_kin，返回 6 关节角 list[float]（rad）"""
    pose_str = f"[{target_pose[0]},{target_pose[1]},{target_pose[2]},{target_pose[3]},{target_pose[4]},{target_pose[5]}]"
    resp = _send_40011(1, f"get_inverse_kin({pose_str})").strip()
    if '[failure]' in resp:
        print(f"[WARN] IK 失败: {resp}")
        return None
    parts = resp.split(' : ', 1)
    if len(parts) == 2:
        try:
            val = ast.literal_eval(parts[1].strip())
            if isinstance(val, list) and len(val) == 1:
                return val[0]
            return val
        except Exception as e:
            print(f"[WARN] 解析 IK 响应失败: {e}")
    return None

# ============================================================================
# 脚本发送（30001 端口），停止脚本（halt）
# ============================================================================

def send_script(script_path):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    sock.connect((ROBOT_IP, 30001))
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    sock.sendall(content.encode('utf-8'))
    resp = sock.recv(1024).decode('utf-8', errors='ignore').strip()
    sock.close()
    print(f"[INFO] 30001 响应: {resp}")
    return True

def stop_script():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    sock.connect((ROBOT_IP, 30001))
    sock.sendall(b"halt()\n")
    sock.close()

# ============================================================================
# 工具函数
# ============================================================================

def lerp(a, b, t):
    return a + (b - a) * t

def interpolate_joints(start, end, t):
    return [lerp(s, e, t) for s, e in zip(start, end)]

# ============================================================================
# RTSI 写入线程（250Hz 直驱）
# 对应 touchuan_rtsi.py 的 follow_writer_thread
# ============================================================================

def rtsi_writer_thread(init_joints):
    """
    init_joints: 软启动起点（机器人当前关节角）

    1. 连接机器人 RTSI（30004）
    2. 订阅 output_int_register0（确认脚本已就绪）
    3. 订阅 input_double_register0~6（用于写入）
    4. 等待脚本就绪
    5. 软启动：从当前关节角插值到 init_joints
    6. 正常透传：每 4ms 从 _latest_joints 写入寄存器
    """
    global _running, _latest_joints

    print(f"[INFO] 连接机器人 RTSI ({ROBOT_IP})...")
    rt = rtsi(ROBOT_IP)
    rt.connect()
    rt.version_check()
    version = rt.controller_version()
    print(f"[INFO] 控制器版本: {version}")

    # 订阅 output_int_register0（脚本就绪信号）
    rt.output_subscribe('output_int_register0', 10)

    # 订阅输入：6 个关节角 + 1 个 flag，共 7 个 input_double_register
    in_vars = ('input_double_register0,input_double_register1,'
               'input_double_register2,input_double_register3,'
               'input_double_register4,input_double_register5,'
               'input_double_register6')
    in_data = rt.input_subscribe(in_vars)

    rt.start()
    print("[INFO] RTSI 启动")

    # 等待脚本就绪（output_int_register0 == 1）
    print("[INFO] 等待 external_control_rocker 脚本就绪...")
    deadline = time.time() + 15
    ready = False
    while time.time() < deadline and _running:
        recv = rt.get_output_data_buffered(512)
        if recv and getattr(recv, 'output_int_register0', 0) == 1:
            ready = True
            print("[INFO] 脚本已就绪")
            break
        time.sleep(0.05)

    if not ready:
        print("[WARN] 脚本未就绪，继续（可能已超时）")

    # 获取机器人当前关节角（用于软启动）
    rt_snap = rtsi(ROBOT_IP)
    rt_snap.connect()
    rt_snap.version_check()
    rt_snap.output_subscribe('actual_joint_positions', 50)
    rt_snap.start()
    time.sleep(0.2)
    recv_snap = rt_snap.get_output_data_buffered(512)
    current_joints = list(recv_snap.actual_joint_positions) if recv_snap else init_joints[:]
    rt_snap.disconnect()

    print(f"[INFO] 机器人当前关节: {[round(v, 4) for v in current_joints]}")
    print(f"[INFO] 目标关节角: {[round(v, 4) for v in init_joints]}")

    # ─── 软启动阶段 ───
    print(f"[INFO] 软启动 ({SOFT_START_DURATION}s, {SOFT_START_STEPS}步)...")
    soft_interval = SOFT_START_DURATION / SOFT_START_STEPS
    for i in range(SOFT_START_STEPS + 1):
        if not _running:
            break
        t = i / SOFT_START_STEPS
        joints = interpolate_joints(current_joints, init_joints, t)
        _write_joints(rt, in_data, joints, 1)
        time.sleep(soft_interval)

    if not _running:
        rt.disconnect()
        return

    print("[INFO] 软启动完成，进入 RTSI 透传模式")

    # ─── 正常透传（250Hz）───
    interval = 1.0 / RTSI_FREQ
    while _running:
        t0 = time.perf_counter()

        with _lock:
            joints = _latest_joints

        if joints is not None:
            _write_joints(rt, in_data, joints, 1)

        elapsed = time.perf_counter() - t0
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    # 停止：写 flag=0，脚本停在最后位置
    with _lock:
        last_joints = _latest_joints or init_joints
    _write_joints(rt, in_data, last_joints, 0)
    rt.disconnect()
    print("[INFO] RTSI 线程已退出")


def _write_joints(rt, in_data, joints, flag):
    """将 6 个关节角 + flag 写入 input_double_register0~6"""
    in_data.input_double_register0 = joints[0]
    in_data.input_double_register1 = joints[1]
    in_data.input_double_register2 = joints[2]
    in_data.input_double_register3 = joints[3]
    in_data.input_double_register4 = joints[4]
    in_data.input_double_register5 = joints[5]
    in_data.input_double_register6 = float(flag)
    rt.set_input(in_data)

# ============================================================================
# 摇杆控制主循环
# ============================================================================

def rocker_control_loop():
    global _running, _latest_joints

    a1 = Key_combination()
    if a1 == 0:
        print("摇杆初始化异常")
        return

    last_button = hfdGetButton()
    running = False
    init_pos, init_ori = None, None
    V5, V51 = None, None
    t_writer = None

    while True:
        current_button = hfdGetButton()
        button_pressed = (current_button == 1 and last_button == 0)
        last_button = current_button

        # ── 按下按钮：启动 ──
        if button_pressed and not running:
            init_pos = hfdGetPosition()
            init_ori = hfdGetOrientationRad()

            # 获取当前 TCP 位姿（通过 RTSI）
            rt_tcp = rtsi(ROBOT_IP)
            rt_tcp.connect()
            rt_tcp.version_check()
            rt_tcp.output_subscribe('actual_TCP_pose', 50)
            rt_tcp.start()
            time.sleep(0.05)
            recv_tcp = rt_tcp.get_output_data_buffered(512)
            tcp = list(recv_tcp.actual_TCP_pose) if recv_tcp else [0, 0, 0, 0, 0, 0]
            rt_tcp.disconnect()

            pose_zero = [0, 0, 0, 0, 0, 0]
            V5 = calculate_xyz(tcp, pose_zero)
            V51 = calculate_rxryrz(tcp, pose_zero)
            print(f"[INFO] 基准 TCP: {[round(v, 4) for v in tcp]}")
            print(f"[INFO] 基准 V5: {[round(v, 4) for v in V5]}")
            print(f"[INFO] 基准 V51: {[round(v, 4) for v in V51]}")

            # 发送控制脚本到机器人
            if not send_script(SCRIPT_PATH):
                print("[ERROR] 脚本发送失败")
                break
            time.sleep(0.3)

            # 通过 40011 一次性 IK 获取初始关节角
            result2 = user_frame_to_tcp_frame(
                mm_deg_to_m_rad([-340.1, -171.1, 311.4, 0, 0, 0]), V5)
            result21 = user_frame_to_tcp_frame(
                mm_deg_to_m_rad([-340.1, -171.1, 311.4, 0, 0, 0]), V51)
            target_pose = [
                round(result2[0], 5), round(result2[1], 5), round(result2[2], 5),
                3.14, 0, round(result21[5], 5),
            ]
            init_joints = get_inverse_kin(target_pose)
            if init_joints is None:
                print("[ERROR] 无法获取初始关节角")
                break
            print(f"[INFO] 初始关节角: {[round(v, 4) for v in init_joints]}")

            # 启动 RTSI 写线程（软启动）
            _latest_joints = init_joints[:]
            t_writer = threading.Thread(target=rtsi_writer_thread,
                                        args=(init_joints,), daemon=True)
            t_writer.start()

            running = True
            print("[INFO] 开始运动")

        # ── 再次按下按钮：停止 ──
        elif button_pressed and running:
            print("[INFO] 停止运动")
            _running = False
            if t_writer:
                t_writer.join(timeout=5)
            stop_script()
            Key_combination_off()
            time.sleep(1)
            Key_combination_on()
            running = False
            _running = True

        # ── 运行中：读取摇杆，计算目标关节角 ──
        if running:
            cur_pos = hfdGetPosition()
            cur_ori = hfdGetOrientationRad()

            pose = [0, 0, 0, 0, 0, 0]
            pose[0] = cur_pos[0] - init_pos[0]
            pose[1] = cur_pos[1] - init_pos[1]
            pose[2] = cur_pos[2] - init_pos[2]
            pose[3] = cur_ori[0] - init_ori[0]
            pose[4] = cur_ori[1] - init_ori[1]
            pose[5] = cur_ori[2] - init_ori[2]

            # 平移
            V6 = pose_mul(mm_deg_to_m_rad([pose[0], pose[2], pose[1], 0, 0, 0]), V5)
            result2 = user_frame_to_tcp_frame(
                mm_deg_to_m_rad([-340.1, -171.1, 311.4, 0, 0, 0]), V6)

            # 旋转
            V61 = pose_mul([0, 0, 0, pose[3], pose[4], pose[5]], V51)
            result21 = user_frame_to_tcp_frame(
                mm_deg_to_m_rad([-340.1, -171.1, 311.4, 0, 0, 0]), V61)

            target_pose = [
                round(result2[0],  5),
                round(result2[1],  5),
                round(result2[2],  5),
                3.14,
                0,
                round(result21[5], 5),
            ]

            joints = get_inverse_kin(target_pose)
            if joints is not None:
                with _lock:
                    _latest_joints = joints

        time.sleep(0.004)

# ============================================================================
# 主入口
# ============================================================================

if __name__ == "__main__":
    def _signal_handler(sig, frame):
        global _running
        print("\n[INFO] 退出信号")
        _running = False
        stop_script()
        sys.exit(0)

    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)

    print("[INFO] 等待机器人上电、抱闸释放、REMOTE 模式...")
    rocker_control_loop()
    print("[INFO] 程序结束")

```



[HFD_API64.dll](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjgxNDU5LCJwYXRoIjoiaGZkX2FwaTY0LmRsbCIsInRpbWVzdGFtcCI6IjIwMjYtMDQtMjFUMTU6MDI6MzkuNjY2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--ffa3645ec2858beb78077007e0975cf1d9cff0b401026be1dd28621d818f5d8a/hfd_api64.dll?disposition=attachment)182.5 KB



[rtsi.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MTAwLCJwYXRoIjoicnRzaS5weSIsInRpbWVzdGFtcCI6IjIwMjYtMDQtMjlUMTA6MTE6MzcuNjMzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--cb20d219af36093bf3b57fb267170698dc9ae425b089685703841bd4cd9976c1/rtsi.py?disposition=attachment)14.6 KB



[serialize.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MDk4LCJwYXRoIjoic2VyaWFsaXplLnB5IiwidGltZXN0YW1wIjoiMjAyNi0wNC0yOVQxMDoxMTozNi4zODUrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--795f746bae4003051aa754f07432ecc082daa809290aa871ef4c69cd78054fec/serialize.py?disposition=attachment)5.3 KB



[external_control_rocker.script](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0NjQ1LCJwYXRoIjoiZXh0ZXJuYWxfY29udHJvbF9yb2NrZXIuc2NyaXB0IiwidGltZXN0YW1wIjoiMjAyNi0wNC0yOVQxNTozMDozMi40NTErMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--dc0c0e62efd9e46bd08861179aa868590bcd4210487172c738e8bcc28138d295/external_control_rocker.script?disposition=attachment)774 字节
