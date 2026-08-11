# 用户坐标系下运动控制

URL: https://docs.elibot.cn/cs/88fdd/9bd1f/ba1dc/acdcf
发布时间: 2026-05-07

# 一、简介



**本案例基于用户坐标系下笛卡尔坐标位姿，计算基坐标系的关节姿态，并调用servoj移动到目标点
**需要的脚本文件作为附件置于文末，运行时需要放置在同目录下



# **二、操作流程**



**1、**将代码与附件章节的代码放置到同一目录下，此时文件夹中应有四份文件



**2、**修改代码中**DEFAULT_ROBOT_IP **为机器人真实IP，**USER_X，USER_Y，USER_Z，USER_RX，USER_RY，USER_RZ**设置为坐标系偏移值，单位是mm和deg



**3、**示例里设置了5个点位，写在**targets**里，请将点位修改为需要的点位，并且如果存在自己的线程，可以删除**main**函数里的循环代码，只在需要运动的时候调用**servo.set_target**即可



**4、**执行代码文件，机器人基于用户坐标系运动



# **三、常见问题**



**1、**Q:为什么机器人没有运动，然后打印里有“逆解失败”的字样。



A:这基本都是因为逆解的目标是奇异点，导致机器人无法到达，自然逆解失败，机器人没有运动。这一点可以通过示教器的日志看到，会打印“目标位姿为奇异位姿，机器人不可达”。解决方法首先要确认传递的点位是否正确，单位是否一致。



**2、**Q:为什么寄存器的值一直在变？



A:因为实现逻辑会通过端口修改机器人浮点数寄存器0-5的值，分别对应机器人六个关节的位姿，所以如果有修改寄存器的需求，请跳过前五个浮点数寄存器。



# 四、代码和附件



**主要流程**：



- `UserCoordServo(robot_ip, user_frame, freq_hz)` 构造，`atexit.register(self.stop)` 注册退出清理
- `servo.start()`：



- `_send_follow_script()` → Socket 直连 `(robot_ip, 30001)` 发 `follow_ema.script`
- 起 `_rtsi_reader_loop` 子线程：
- `rtsi(ip)` → `connect()` → `version_check()` → `output_subscribe("actual_joint_positions", 250)` → `start()` → 循环 `get_output_data()` 读 `_latest_joints`
- 等第一帧数据
- `_setup_rtsi_writer()` → `rtsi(ip)` → `connect()` → `version_check()` → `output_subscribe('output_int_register0', 10)` + `input_subscribe('input_double_register0~6')` → `start()`
- `_wait_follow_script_ready()` → 轮询 `get_output_data()` 等 `output_int_register0 == 1`
- `_compute_and_set_target_joints()` 算初始 IK，直接写 `set_input()` 一次
- 起 `_rtsi_writer_loop` 子线程：250Hz 循环 → 读 `_target_joints` → `set_input()` 写 `input_double_register0~5 = joints` + `register6 = 1`



- 外部调 `servo.set_target(ux=100, uy=200, uz=50)` → 更新目标 → 设 `_ik_dirty = True`
- `_compute_and_set_target_joints()`：



- `user_to_base(ip, user_frame, target)` → 内部调 40011 `pose_trans`，用户坐标系 → 基坐标系
- `pose_to_joints(ip, base_pose, ref_joints)` → 内部调 40011 `get_inverse_kin`
- IK 失败时优先用上一次成功的 `_target_joints` 做参考，不行再回退到实际关节



- `servo.stop()` → `flag=0` + `_halt_follow_script()` 30001 发 `halt()` + 断开 RTSI



**涉及的完整接口**：



**组件****接口**30001 (Socket)`socket.connect → sendall(script) / sendall("halt()\n")`RTSI Reader`rtsi(ip) / connect / version_check / output_subscribe("actual_joint_positions", 250) / start / get_output_data / disconnect`RTSI Writer`rtsi(ip) / connect / version_check / output_subscribe / input_subscribe / start / get_output_data / set_input / disconnect`40011 (Socket)`send_40011(ip, "pose_trans(...)")` 位姿变换 + `send_40011(ip, "get_inverse_kin(...)")` 逆解



```
"""
用户坐标系下的 servoj 运动控制（持续线程模式）

架构：
  PC 端：计算 IK → 写 input_double_register0~5（关节角）+ register6（flag=1）
  机器人端：跑脚本读寄存器 → servoj 执行

依赖：rtsi.py, serialize.py（同目录下）

用法：
  from user_coord_servo import UserCoordServo
  servo = UserCoordServo(robot_ip="192.168.254.138")
  servo.start()
  servo.set_target(ux=100, uy=200, uz=50, urx=0, ury=0, urz=0)
  servo.stop()
"""

import sys
import os
import time
import socket
import threading
import math
import atexit

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'ServoJ_RTSI联合', 'python'))
from rtsi import rtsi

# ──────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────
DEFAULT_ROBOT_IP = "192.168.254.138"

RTSI_FREQ = 250.0
SERVOJ_TIME = 1.0 / RTSI_FREQ

# 用户坐标系参数
USER_X = -300.0   # mm
USER_Y = 600.0    # mm
USER_Z = -300.0   # mm
USER_RX = 0.0     # deg
USER_RY = -45.0   # deg
USER_RZ = 0.0     # deg

# 默认目标点（用户坐标系下，单位mm/rad）
DEFAULT_TARGET = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

# ──────────────────────────────────────────────
# 40011 明文请求
# ──────────────────────────────────────────────
_req_lock = threading.Lock()
_req_id = 1


def send_40011(ip, cmd, timeout=5.0):
    """向 40011 端口发送请求，返回 (result_list, error_str)"""
    global _req_id
    with _req_lock:
        cur_id = _req_id
        _req_id += 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((ip, 40011))
        sock.sendall(f"req {cur_id}{cmd}\n".encode())
        resp = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
            if b"\n" in resp:
                break
    finally:
        sock.close()

    resp_str = resp.decode("utf-8", errors="replace").strip()
    if "failure" in resp_str.lower():
        return None, resp_str

    parts = resp_str.split(":", 1)
    if len(parts) < 2:
        return None, f"unexpected response: {resp_str}"

    val_str = parts[1].strip()
    try:
        val = eval(val_str)
        if isinstance(val, list):
            if len(val) == 1 and isinstance(val[0], list):
                return [float(x) for x in val[0]], None
            return [float(x) for x in val], None
        return float(val), None
    except Exception:
        return None, f"parse error: {val_str}"


# ──────────────────────────────────────────────
# 位姿变换工具
# ──────────────────────────────────────────────
def pose_inv(ip, p):
    p_native = [float(x) for x in p]
    return send_40011(ip, f"pose_inv({p_native})")


def pose_trans(ip, p1, p2):
    p1_native = [float(x) for x in p1]
    p2_native = [float(x) for x in p2]
    return send_40011(ip, f"pose_trans({p1_native},{p2_native})")


def deg_to_rad(deg):
    return deg * math.pi / 180.0


def build_user_frame():
    """构建用户坐标系位姿（m, rad）"""
    return [
        USER_X / 1000.0,
        USER_Y / 1000.0,
        USER_Z / 1000.0,
        deg_to_rad(USER_RX),
        deg_to_rad(USER_RY),
        deg_to_rad(USER_RZ),
    ]


def user_to_base(ip, user_frame, target):
    """
    用户坐标系位姿 → 基坐标系位姿
    target: [ux, uy, uz, urx, ury, urz] (mm, rad)
    返回: [x, y, z, Rx, Ry, Rz] (m, rad)
    """
    ux, uy, uz, urx, ury, urz = target
    user_target = [ux / 1000.0, uy / 1000.0, uz / 1000.0, urx, ury, urz]
    base_pose, err = pose_trans(ip, user_frame, user_target)
    if err:
        return None, f"pose_trans failed: {err}"
    return base_pose, None


def pose_to_joints(ip, base_pose, ref_joints):
    """基坐标系位姿 → 关节角度"""
    pose_native = [float(x) for x in base_pose]
    ref_native = [float(x) for x in ref_joints]
    return send_40011(ip, f"get_inverse_kin({pose_native}, {ref_native})")


# ──────────────────────────────────────────────
# 主类
# ──────────────────────────────────────────────
class UserCoordServo:
    """
    用户坐标系 servoj 控制类

    架构：
      1. PC 通过 30001 发送 follow 脚本（读寄存器 → servoj）
      2. PC 通过 RTSI 30004 写 input_double_register0~6
         - register0~5: 目标关节角 (rad)
         - register6: flag (1=有新数据, 0=停止)
      3. 机器人端脚本持续读寄存器执行 servoj

    用法：
        servo = UserCoordServo(robot_ip="192.168.254.138")
        servo.start()
        servo.set_target(ux=100, uy=200, uz=50)
        servo.stop()
    """

    def __init__(
        self,
        robot_ip=DEFAULT_ROBOT_IP,
        user_frame=None,
        freq_hz=250,
    ):
        self.robot_ip = robot_ip
        self.user_frame = user_frame if user_frame is not None else build_user_frame()
        self.freq_hz = freq_hz

        self._running = False
        self._target = list(DEFAULT_TARGET)  # [ux, uy, uz, urx, ury, urz]
        self._target_lock = threading.Lock()

        self._target_joints = None           # 当前生效的目标关节角
        self._target_joints_lock = threading.Lock()

        self._latest_joints = None           # 机器人当前实际关节角
        self._latest_joints_lock = threading.Lock()

        self._rtsi_reader_thread = None
        self._rtsi_reader_running = False
        self._rtsi_writer_thread = None
        self._rtsi_writer_running = False

        # RTSI 写入连接（writer 线程专用）
        self._rt_writer = None
        self._in_data = None

        self._ik_dirty = True

        atexit.register(self.stop)

    # ──────────────────────────────────────────
    # 公共接口
    # ──────────────────────────────────────────

    def set_target(self, ux=None, uy=None, uz=None, urx=None, ury=None, urz=None):
        """
        设置目标点（用户坐标系下，位置mm / 姿态rad）
        线程安全，可随时调用。只传需要修改的分量。
        """
        with self._target_lock:
            t = self._target
            if ux is not None: t[0] = float(ux)
            if uy is not None: t[1] = float(uy)
            if uz is not None: t[2] = float(uz)
            if urx is not None: t[3] = float(urx)
            if ury is not None: t[4] = float(ury)
            if urz is not None: t[5] = float(urz)
        self._ik_dirty = True

    def get_target(self):
        """获取当前目标点（用户坐标系下，位置mm / 姿态rad）"""
        with self._target_lock:
            return self._target[:]

    def start(self):
        """启动控制"""
        if self._running:
            print("[WARN] 已在运行")
            return

        print(f"[INFO] 启动 UserCoordServo，robot={self.robot_ip}, freq={self.freq_hz}Hz")
        print(f"[INFO] 用户坐标系: x={USER_X}, y={USER_Y}, z={USER_Z}, rx={USER_RX}°, ry={USER_RY}°, rz={USER_RZ}°")

        # Step 1: 通过 30001 发送 follow 脚本
        self._send_follow_script()
        time.sleep(0.5)

        # Step 2: 启动 RTSI reader 线程
        self._rtsi_reader_running = True
        self._rtsi_reader_thread = threading.Thread(target=self._rtsi_reader_loop, daemon=True, name="rtsi-reader")
        self._rtsi_reader_thread.start()

        # 等待第一帧
        deadline = time.time() + 10
        while self._latest_joints is None and self._rtsi_reader_running:
            if time.time() > deadline:
                raise RuntimeError("等待机器人数据超时")
            time.sleep(0.05)

        print(f"[INFO] 机器人已就绪，当前关节: {[round(v, 4) for v in self._latest_joints]}")

        # Step 3: 建立 RTSI writer 连接
        self._setup_rtsi_writer()

        # Step 4: 等待 follow 脚本就绪
        self._wait_follow_script_ready()

        # Step 5: 计算初始 IK 并直接写入
        if self._compute_and_set_target_joints():
            # 初始位置：直接写一次寄存器，让机器人从当前位置出发
            with self._target_joints_lock:
                joints = self._target_joints
            if joints is not None and self._in_data is not None:
                self._in_data.input_double_register0 = joints[0]
                self._in_data.input_double_register1 = joints[1]
                self._in_data.input_double_register2 = joints[2]
                self._in_data.input_double_register3 = joints[3]
                self._in_data.input_double_register4 = joints[4]
                self._in_data.input_double_register5 = joints[5]
                self._in_data.input_double_register6 = 1
                self._rt_writer.set_input(self._in_data)
            print(f"[INFO] 初始目标关节: {[round(v, 4) for v in joints]}")

        # Step 6: 启动 RTSI writer 线程
        self._rtsi_writer_running = True
        self._rtsi_writer_thread = threading.Thread(target=self._rtsi_writer_loop, daemon=True, name="rtsi-writer")
        self._rtsi_writer_thread.start()

        self._running = True
        print("[INFO] 控制已启动")

    def stop(self):
        """停止控制"""
        self._running = False
        self._rtsi_reader_running = False
        self._rtsi_writer_running = False

        # flag=0 告诉机器人脚本停住
        if self._in_data is not None and self._rt_writer is not None:
            try:
                self._in_data.input_double_register6 = 0
                self._rt_writer.set_input(self._in_data)
            except Exception:
                pass

        # 停止 follow 脚本
        self._halt_follow_script()

        if self._rtsi_reader_thread and self._rtsi_reader_thread.is_alive():
            self._rtsi_reader_thread.join(timeout=3)
        if self._rtsi_writer_thread and self._rtsi_writer_thread.is_alive():
            self._rtsi_writer_thread.join(timeout=5)

        # 断开 writer
        if self._rt_writer:
            try:
                self._rt_writer.disconnect()
            except Exception:
                pass
            self._rt_writer = None

        print("[INFO] UserCoordServo 已停止")

    # ──────────────────────────────────────────
    # 内部方法
    # ──────────────────────────────────────────

    def _send_follow_script(self):
        """通过 30001 发送 follow 脚本到机器人"""
        port_dir = os.path.dirname(__file__)
        script_path = os.path.abspath(os.path.join(port_dir, 'follow_ema.script'))

        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_content = f.read()
        except Exception as e:
            raise RuntimeError(f"读取 follow 脚本失败: {e}")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10.0)
            sock.connect((self.robot_ip, 30001))
            sock.sendall(script_content.encode('utf-8'))
            sock.close()
            print(f"[INFO] Follow 脚本已发送 ({len(script_content)} 字节)")
        except Exception as e:
            raise RuntimeError(f"发送 follow 脚本失败: {e}")

    def _halt_follow_script(self):
        """发送 halt() 停止机器人脚本"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((self.robot_ip, 30001))
            sock.sendall(b"halt()\n")
            sock.close()
            print("[INFO] 已发送 halt()")
        except Exception as e:
            print(f"[WARN] 发送 halt() 失败: {e}")

    def _setup_rtsi_writer(self):
        """建立 RTSI 写入连接"""
        rt = rtsi(self.robot_ip)
        try:
            rt.connect()
        except Exception as e:
            raise RuntimeError(f"RTSI writer 连接失败: {e}")

        rt.version_check()
        version = rt.controller_version()
        print(f"[INFO] RTSI writer 控制器版本: {version}")

        rt.output_subscribe('output_int_register0', 10)

        in_vars = (
            'input_double_register0,'
            'input_double_register1,'
            'input_double_register2,'
            'input_double_register3,'
            'input_double_register4,'
            'input_double_register5,'
            'input_double_register6'
        )
        self._in_data = rt.input_subscribe(in_vars)

        rt.start()
        self._rt_writer = rt
        print("[INFO] RTSI writer 已启动")

    def _wait_follow_script_ready(self):
        """等待 follow 脚本就绪（output_int_register0 == 1）"""
        print("[INFO] 等待 follow 脚本就绪...")
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                recv = self._rt_writer.get_output_data()
                if recv and recv.output_int_register0 == 1:
                    print("[INFO] Follow 脚本已就绪")
                    return
            except Exception:
                pass
            time.sleep(0.05)

    def _rtsi_reader_loop(self):
        """RTSI 读取线程：持续获取机器人当前关节位置"""
        rt = rtsi(self.robot_ip)
        try:
            rt.connect()
        except Exception as e:
            print(f"[ERROR] RTSI reader 连接失败: {e}")
            self._rtsi_reader_running = False
            return

        rt.version_check()
        rt.output_subscribe("actual_joint_positions", RTSI_FREQ)
        rt.start()

        interval = 1.0 / RTSI_FREQ
        try:
            while self._rtsi_reader_running:
                t0 = time.perf_counter()
                recv = rt.get_output_data()
                if recv and recv.actual_joint_positions:
                    with self._latest_joints_lock:
                        self._latest_joints = list(recv.actual_joint_positions)
                elapsed = time.perf_counter() - t0
                sleep_time = interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
        finally:
            rt.disconnect()
            print("[INFO] RTSI reader 已断开")

    def _rtsi_writer_loop(self):
        """RTSI 写入线程：持续将目标关节角写入寄存器"""
        interval = 1.0 / self.freq_hz

        try:
            while self._rtsi_writer_running:
                t0 = time.perf_counter()

                # ── IK 更新 ──
                if self._ik_dirty:
                    self._compute_and_set_target_joints()
                    self._ik_dirty = False

                # ── 写寄存器 ──
                with self._target_joints_lock:
                    joints = self._target_joints

                if joints is not None and self._in_data is not None:
                    self._in_data.input_double_register0 = joints[0]
                    self._in_data.input_double_register1 = joints[1]
                    self._in_data.input_double_register2 = joints[2]
                    self._in_data.input_double_register3 = joints[3]
                    self._in_data.input_double_register4 = joints[4]
                    self._in_data.input_double_register5 = joints[5]
                    self._in_data.input_double_register6 = 1  # flag=1
                    self._rt_writer.set_input(self._in_data)

                # ── 定时 ──
                elapsed = time.perf_counter() - t0
                sleep_time = interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)
        finally:
            # 退出时 flag=0
            if self._in_data is not None and self._rt_writer is not None:
                try:
                    self._in_data.input_double_register6 = 0
                    self._rt_writer.set_input(self._in_data)
                except Exception:
                    pass

    def _compute_and_set_target_joints(self):
        """
        计算目标关节角度（用户坐标 → 基坐标 → IK）
        优先用上一次成功的 target_joints 做 IK 参考，
        失败则回退到当前实际关节做参考。
        IK 失败时保留旧目标，不覆盖。
        """
        with self._target_lock:
            target = self._target[:]

        # 优先用上一次成功的 target_joints 做 IK 参考（比 actual 更稳定）
        with self._target_joints_lock:
            ref_joints = self._target_joints

        if ref_joints is None:
            with self._latest_joints_lock:
                ref_joints = self._latest_joints[:]

        base_pose, err = user_to_base(self.robot_ip, self.user_frame, target)
        if err:
            print(f"[ERROR] 坐标变换失败: {err}")
            return False

        ik_joints, err = pose_to_joints(self.robot_ip, base_pose, ref_joints)
        if err:
            # IK 失败：尝试用 actual joints 再算一次
            with self._latest_joints_lock:
                ref_joints_actual = self._latest_joints[:]
            if ref_joints_actual != ref_joints:
                print(f"[WARN] IK 失败(用 target_joints 参考)，尝试用 actual joints 重算...")
                ik_joints, err = pose_to_joints(self.robot_ip, base_pose, ref_joints_actual)
                if err:
                    print(f"[ERROR] 逆解失败: {err}，保留旧目标")
                    return False
            else:
                print(f"[ERROR] 逆解失败: {err}，保留旧目标")
                return False

        with self._target_joints_lock:
            self._target_joints = ik_joints

        return True


# ──────────────────────────────────────────────
# 便捷函数
# ──────────────────────────────────────────────
_instance = None


def start(robot_ip=DEFAULT_ROBOT_IP):
    """快捷启动：启动全局单例"""
    global _instance
    if _instance is None:
        _instance = UserCoordServo(robot_ip=robot_ip)
    _instance.start()
    return _instance


def set_target(ux=None, uy=None, uz=None, urx=None, ury=None, urz=None):
    """快捷接口：设置目标点（用户坐标系，位置mm / 姿态rad）"""
    if _instance is None:
        raise RuntimeError("请先调用 user_coord_servo.start()")
    _instance.set_target(ux=ux, uy=uy, uz=uz, urx=urx, ury=ury, urz=urz)


def stop():
    """快捷停止"""
    global _instance
    if _instance:
        _instance.stop()
        _instance = None


# ──────────────────────────────────────────────
# 演示
# ──────────────────────────────────────────────
if __name__ == "__main__":

    servo = UserCoordServo(robot_ip="192.168.254.138")
    servo.start()

    targets = [  #点位需要密集，间距要小，单位是mm 和 rad
        (0, 0, 0, 0, 0, 0),
        (90, 80, 166, 0.138, 0.154, -0.138),
        (0, 100, 0, 0, 0, 0),
        (-50, 50, 100, 0, 0, 0),
        (0, 0, 0, 0, 0, 0),
    ]

    for i, target in enumerate(targets):
        ux, uy, uz, urx, ury, urz = target
        print(f"\n[演示] 设置目标点 {i+1}: ({ux}, {uy}, {uz}, {urx}, {ury}, {urz}) mm/rad")
        servo.set_target(ux=ux, uy=uy, uz=uz, urx=urx, ury=ury, urz=urz)
        time.sleep(1)

    servo.stop()
```



[rtsi.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MTAwLCJwYXRoIjoicnRzaS5weSIsInRpbWVzdGFtcCI6IjIwMjYtMDQtMjlUMTA6MTE6MzcuNjMzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--cb20d219af36093bf3b57fb267170698dc9ae425b089685703841bd4cd9976c1/rtsi.py?disposition=attachment)14.6 KB



[follow_ema.script](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MDk5LCJwYXRoIjoiZm9sbG93X2VtYS5zY3JpcHQiLCJ0aW1lc3RhbXAiOiIyMDI2LTA0LTI5VDEwOjExOjM2LjQ4OCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--b52a3da1cf3ef2771f753e8fd3a7d0be555e1a380b16bcc624412212c57da184/follow_ema.script?disposition=attachment)1.3 KB



[serialize.py](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg0MDk4LCJwYXRoIjoic2VyaWFsaXplLnB5IiwidGltZXN0YW1wIjoiMjAyNi0wNC0yOVQxMDoxMTozNi4zODUrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--795f746bae4003051aa754f07432ecc082daa809290aa871ef4c69cd78054fec/serialize.py?disposition=attachment)5.3 KB
