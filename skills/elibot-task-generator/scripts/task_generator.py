#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成艾利特 ES/CS 机器人图形化编程 .task 文件。

用法（在 Codex 中）：
1. 用 TaskBuilder 组装节点树（容器节点用 body 回调传子节点）；
2. b.build(main_children) 得到 .task XML 字符串；
3. 以 UTF-8（无 BOM）写出 .task 文件，交付用户拖入示教器。

支持节点：文件夹、赋值(定义/引用变量/读信号)、设置(写寄存器/信号)、循环(条件/无条件)、
判断(变量比较/数字输入)、开关+case、脚本节点(内容内嵌)、等待、弹出窗口、子任务、占位。

变量 XPath 引用自动计算：所有任务变量在"第一个文件夹(初始化)"里定义，
引用按"引用处深度 -> MainTask -> FolderNode/AssignmentNode[k]/TaskVariable"生成。
"""
from datetime import datetime

IND = "  "

def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&apos;'))

# ---------------- 表达式单元格 ----------------
def char_cell(c):        return '<ExpressionCharCell char="%s"/>' % esc(c)
def token_cell(t, c):    return '<ExpressionTokenCell token="%s" scriptCode="%s"/>' % (esc(t), esc(c))
def pin_cell(name):      return '<ExpressionPinCell><pin referenceName="%s"/></ExpressionPinCell>' % esc(name)
def var_cell(ref):       return '<ExpressionVariableCell><TaskVariable reference="%s"/></ExpressionVariableCell>' % ref
def number_cells(v):     return "".join(char_cell(c) for c in str(v))
def true_cell():         return token_cell(" True ", " True ")
def false_cell():        return token_cell(" False ", " False ")
def eq_cell():           return token_cell(" ?= ", "==")
def ne_cell():           return char_cell("\u2260")

def _val(tag, value, unit, cls):
    return ('<%s value="%s" unit="%s">' % (tag, value, unit) +
            '<valueInSi>%s</valueInSi>' % value +
            '<siUnit class="%s">%s</siUnit></%s>' % (cls, unit, tag))


class TaskBuilder:
    MAIN_DEPTH = 2   # EliTask=1, MainTask=2

    def __init__(self, task_name, robot_type="CS612", tool_type="7",
                 version="2.16.0.964", robot_sn="", saved_time=None):
        self.task_name = task_name
        self.robot_type = robot_type
        self.tool_type = tool_type
        self.version = version
        self.robot_sn = robot_sn
        self.saved_time = saved_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.var_order = []
        self.lines = []

    # ---------- 变量 ----------
    def define_var(self, name):
        if name not in self.var_order:
            self.var_order.append(name)

    def var_ref(self, name, tv_depth):
        idx = self.var_order.index(name) + 1
        ups = tv_depth - self.MAIN_DEPTH
        target = "FolderNode/AssignmentNode" + ("" if idx == 1 else "[%d]" % idx) + "/TaskVariable"
        return "../" * ups + target

    def expr_var_cell(self, name, expr_depth):
        """在 Expression 深度为 expr_depth 的表达式里引用变量（TaskVariable 在 ExpressionVariableCell 内，深 2 层）。"""
        return var_cell(self.var_ref(name, expr_depth + 2))

    def emit(self, depth, s):
        self.lines.append(IND * (depth - 1) + s)

    # ---------- 叶子节点 ----------
    def assignment(self, depth, expr_cells, define=None, ref=None):
        self.emit(depth, '<AssignmentNode valueSourceType="EXPRESSION" deepCopy="false" typeName="赋值">')
        if define is not None:
            self.define_var(define)
            self.emit(depth + 1, '<TaskVariable name="%s" type="Default" prefersPersistentValue="false" favorite="false" describe=""/>' % esc(define))
        else:
            self.emit(depth + 1, '<TaskVariable reference="%s"/>' % self.var_ref(ref, depth + 1))
        self.emit(depth + 1, '<Expression>')
        for c in expr_cells:
            self.emit(depth + 2, c)
        self.emit(depth + 1, '</Expression>')
        self.emit(depth, '</AssignmentNode>')

    def set_pin(self, depth, pin_name, expr_cells):
        self.emit(depth, '<SetNode type="EXPRESSION_OUTPUT" tcpSettingEnabled="false" typeName="设置">')
        self.emit(depth + 1, '<expressionOutputPinName>%s</expressionOutputPinName>' % esc(pin_name))
        self.emit(depth + 1, '<Expression>')
        for c in expr_cells:
            self.emit(depth + 2, c)
        self.emit(depth + 1, '</Expression>')
        self.emit(depth, '</SetNode>')

    def script_node(self, depth, path, content):
        self.emit(depth, '<ScriptNode scriptType="FILE_TYPE" typeName="脚本">')
        self.emit(depth + 1, '<cachedFileContents>')
        for ln in content.split("\n"):
            self.emit(depth + 2, esc(ln))
        self.emit(depth + 1, '</cachedFileContents>')
        self.emit(depth + 1, '<scriptFile pathRootType="TASK_PATH" path="%s"/>' % esc(path))
        self.emit(depth, '</ScriptNode>')

    def wait(self, depth, seconds):
        self.emit(depth, '<WaitNode type="WAIT_TIME" timeoutEnable="false" typeName="等待">')
        self.emit(depth + 1, _val('waitTime', seconds, 'S', 'cn.elibot.robot.plugin.domain.value.Time$Unit'))
        self.emit(depth, '</WaitNode>')

    def popup(self, depth, message, dialog="INFO"):
        self.emit(depth, '<PopupNode dialogType="%s" contentType="TEXT" message="%s" blockWhenPopup="false" typeName="弹出窗口"/>' % (dialog, esc(message)))

    def placeholder(self, depth):
        self.emit(depth, '<PlaceHolder typeName="占位节点"/>')

    def subtask(self, depth, name, body):
        self.emit(depth, '<SubTaskNode name="%s" isHideSubtree="false" isSynchronized="false" isTracking="false" typeName="子任务">' % esc(name))
        self.emit(depth + 1, '<children>')
        for fn in body:
            fn(depth + 2)
        self.emit(depth + 1, '</children>')
        self.emit(depth, '</SubTaskNode>')

    # ---------- 容器节点（body = 子节点回调列表，fn(child_depth)） ----------
    def folder(self, depth, display, body):
        self.emit(depth, '<FolderNode display="%s" isHideSubtree="false" typeName="文件夹">' % esc(display))
        for fn in body:
            fn(depth + 1)
        self.emit(depth, '</FolderNode>')

    def loop(self, depth, loop_type, cond_cells, body, loop_name="循环_1"):
        self.emit(depth, '<LoopNode type="%s" loopCount="0" isCheckConditionInSeparateThread="false" isPostTestLoop="false" typeName="循环">' % loop_type)
        if loop_type == "LOOP_EXPRESSION":
            self.emit(depth + 1, '<TaskVariable name="%s" type="Loop" prefersPersistentValue="false" favorite="false" describe=""/>' % esc(loop_name))
            self.emit(depth + 1, '<Expression>')
            for c in cond_cells:
                self.emit(depth + 2, c)
            self.emit(depth + 1, '</Expression>')
        self.emit(depth + 1, '<children>')
        for fn in body:
            fn(depth + 2)
        self.emit(depth + 1, '</children>')
        self.emit(depth, '</LoopNode>')

    def if_node(self, depth, expr_cells, body):
        self.emit(depth, '<IfNode checkExpressionContinuous="false" typeName="If">')
        self.emit(depth + 1, '<Expression>')
        for c in expr_cells:
            self.emit(depth + 2, c)
        self.emit(depth + 1, '</Expression>')
        self.emit(depth + 1, '<children>')
        for fn in body:
            fn(depth + 2)
        self.emit(depth + 1, '</children>')
        self.emit(depth, '</IfNode>')

    def switch(self, depth, expr_cells, body):
        self.emit(depth, '<SwitchNode typeName="开关">')
        self.emit(depth + 1, '<Expression>')
        for c in expr_cells:
            self.emit(depth + 2, c)
        self.emit(depth + 1, '</Expression>')
        self.emit(depth + 1, '<children>')
        for fn in body:
            fn(depth + 2)
        self.emit(depth + 1, '</children>')
        self.emit(depth, '</SwitchNode>')

    def case(self, depth, case_name, body):
        self.emit(depth, '<CaseNode caseName="%s" typeName="情况">' % esc(case_name))
        for fn in body:
            fn(depth + 1)
        self.emit(depth, '</CaseNode>')

    # ---------- 组装 ----------
    def build(self, main_children, subtasks=None, always_loops=True):
        self.lines = []
        self.emit(1, '<EliTask name="%s" installationName="default" robotType="%s" toolType="%s" createdVersion="%s" lastSavedVersion="%s" robotSN="%s" savedTime="%s" typeName="机器人主任务">' % (
            esc(self.task_name), self.robot_type, self.tool_type, self.version, self.version, self.robot_sn, self.saved_time))
        self.emit(2, '<InitVariables typeName="初始化变量"/>')
        self.emit(2, '<MainTask isTaskAlwaysLoops="%s" hasBeforeStart="false" hasInitVariables="true" typeName="机器人主任务">' % ("true" if always_loops else "false"))
        for fn in main_children:
            fn(3)
        self.emit(2, '</MainTask>')
        if subtasks:
            for fn in subtasks:
                fn(2)
        self.emit(1, '</EliTask>')
        return "\n".join(self.lines) + "\n"


# ================= 演示/校验：重建主任务并 round-trip 对比 =================
def demo_main_dispatcher(b, cases):
    """cases: [(case_name, script_path, script_content), ...]，按 case 顺序。"""
    def init_folder(d):
        b.folder(d, "文件夹1_初始化", [
            lambda dd: b.set_pin(dd, "resultCode", [char_cell("0")]),
            lambda dd: b.assignment(dd, [char_cell("-"), char_cell("1")], define="last_n"),
            lambda dd: b.assignment(dd, [char_cell("0")], define="n"),
        ])
    def main_folder(d):
        def loop_body(dd):
            b.assignment(dd, [pin_cell("task_no")], ref="n")
            def if_body(e):
                b.set_pin(e, "resultCode", [char_cell("2"), char_cell("5"), char_cell("5")])
                b.assignment(e, [b.expr_var_cell("n", e + 1)], ref="last_n")
                def sw_body(c):
                    for (cname, cpath, ccontent) in cases:
                        b.case(c, cname, [lambda x, p=cpath, ct=ccontent: b.script_node(x, p, ct)])
                b.switch(e, [b.expr_var_cell("n", e + 1)], [sw_body])
            b.if_node(dd, [b.expr_var_cell("n", dd + 1), ne_cell(), b.expr_var_cell("last_n", dd + 1)], [if_body])
        def loop_node_fn(dd):
            b.loop(dd, "LOOP_EXPRESSION", [true_cell()], [loop_body], loop_name="循环_1")
        def delay_fn(dd):
            b.script_node(dd, "Delay_01.script", "sleep(0.1)\n")
        b.folder(d, "文件夹2_主循环", [loop_node_fn, delay_fn])
    return [init_folder, main_folder]


if __name__ == "__main__":
    import xml.etree.ElementTree as ET
    import os

    orig = r"D:\WorkSpace\Main_ActionDispatche_2026-8-11.task"
    tree = ET.parse(orig)
    root = tree.getroot()

    # 1) 按原任务 case 顺序提取 (caseName, scriptPath, scriptContent)
    cases = []
    for case in root.iter("CaseNode"):
        sn = case.find("ScriptNode")
        if sn is not None:
            path = sn.find("scriptFile").attrib["path"]
            content = "".join(sn.find("cachedFileContents").itertext())
            cases.append((case.attrib["caseName"], path, content))
    print("提取 case 顺序:", [c[0] for c in cases])
    print("脚本路径:", [c[1] for c in cases])

    b = TaskBuilder("MainActionDispatche_2026-8-11", robot_sn=root.attrib["robotSN"],
                    saved_time=root.attrib["savedTime"])
    xml = b.build(demo_main_dispatcher(b, cases))

    out = os.path.join(os.environ.get("TEMP", "."), "gen_Main_ActionDispatche.task")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(xml)
    print("生成文件:", out)
    print("生成长度:", len(xml))

    # 2) 结构指纹对比（tag + 属性顺序），忽略空白文本
    def fingerprint(root):
        out = []
        def walk(el):
            out.append((el.tag, tuple(sorted(el.attrib.items()))))
            for ch in el:
                walk(ch)
        walk(root)
        return out

    fp_orig = fingerprint(ET.parse(orig).getroot())
    fp_gen = fingerprint(ET.parse(out).getroot())
    print("指纹一致:", fp_orig == fp_gen)
    if fp_orig != fp_gen:
        for i, (a, b_) in enumerate(zip(fp_orig, fp_gen)):
            if a != b_:
                print("首个差异位置", i)
                print("  原 :", a)
                print("  生成:", b_)
                break
        print("长度 原/生成:", len(fp_orig), len(fp_gen))