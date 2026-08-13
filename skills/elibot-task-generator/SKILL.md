---
name: elibot-task-generator
description: Generate Elibot ES/CS robot graphical-programming .task files (XML) that can be dragged directly into the teach pendant. Use when the user asks to create, generate, or modify an Elibot (艾利特) graphical programming task file (.task), such as a PLC-triggered action dispatcher main task, when they want to skip manual teach-pendant editing, or when a new/updated task requirement should be produced as a .task file. Covers folders, assignment, register/signal output, loops, if/switch, embedded script nodes, wait, popup, subtask, and variable reference serialization.
---

# 艾利特图形化任务生成器（.task 文件）

## 概述
把用户的"图形化编程需求"转成艾利特 ES/CS 机器人的 `.task` XML 文件，用户直接拖进示教器即可运行，无需手工搭树。核心依据是逆向自真实 `.task` 文件的序列化格式（见 `references/xml-schema.md`）。

## 工作流
1. **确认需求**：任务名、整体结构（初始化/主循环/开关分支）、每个 case 要执行的脚本（文件名+完整内容）、用到的信号名（如 `task_no`/`resultCode`）、变量。
2. **组装节点树**：用 `scripts/task_generator.py` 的 `TaskBuilder` 按需求生成 XML：
   - 容器节点（文件夹/循环/判断/开关/case/子任务）用 `body` 回调传子节点，深度自动处理；
   - 变量在"初始化文件夹"用 `assignment(..., define="名")` 定义，之后引用自动生成 XPath；
   - 表达式引用变量用 `b.expr_var_cell("名", <Expression深度>)`，读信号用 `pin_cell("信号名")`；
   - 脚本节点 `script_node(深度, "文件名.script", 脚本内容)`，内容会完整内嵌并 XML 转义。
3. **生成并写出**：`b.build(main_children)` 返回 XML 字符串；以 **UTF-8（无 BOM）** 写出 `.task`。
4. **校验**：
   - 用 XML 解析器确认 well-formed；
   - 如可访问现有任务文件，跑 `python scripts/task_generator.py` 做 round-trip 指纹对比；
   - 核对 `cachedFileContents` 脚本、`scriptFile.path`、信号名、机器人参数（robotType/toolType/version/robotSN 照抄用户机器人的值）。
5. **交付**：把 `.task` 放到用户目录（如 `D:\WorkSpace\`），提醒：先上传配套脚本文件到机器人本地盘、首次在示教器打开确认节点树，再替换旧任务。

## 关键规则（务必遵守）
- 序列化格式细节：读 `references/xml-schema.md`（每种节点 XML、表达式单元格、变量 XPath 规则、单位、转义）。
- 脚本**内容内嵌**在 `<cachedFileContents>`，`&<>"'` 都要转义；`path` 用机器人本地盘里的脚本文件名。
- **变量**全部在初始化文件夹（第一个文件夹）里用赋值定义；第一个 `AssignmentNode` 引用时 XPath 不带索引（`AssignmentNode`），第二个起带 `[2]`。
- **switch case** 按顺序 `case_1~case_N` 对应匹配值（当前依据：case_1↔0、case_2↔1……），`default case` 兜底。
- **单位**：图形化路点 XML 里是 mm/rad，脚本里是 m/rad。
- 结构示例：见 `references/examples.md`。

## 待验证/扩展（遇到再补）
- 数字输出（写布尔信号）的 `SetNode` 精确写法、TCP 设置节点——需要用户提供样例后补进生成器；
- Move 节点的路点需要实机示教数据；建议动作仍用"脚本节点"里的 movel/movej，图形化 Move 节点仅在用户明确要求时生成；
- case 匹配值的含义以现场示教器显示为准。