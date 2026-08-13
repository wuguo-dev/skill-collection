# 示例：从真实 .task 逆向出的结构

## 示例1：主任务（Main_ActionDispatche_2026-8-11.task）
简化骨架：
```
EliTask (name, robotType=CS612, toolType=7, version 2.16.0.964)
├─ InitVariables
└─ MainTask (isTaskAlwaysLoops=true)
   ├─ FolderNode "文件夹1_初始化"
   │   ├─ SetNode  → resultCode = 0
   │   ├─ AssignmentNode → last_n = -1   (定义变量，第1个)
   │   └─ AssignmentNode → n = 0         (定义变量，第2个)
   └─ FolderNode "文件夹2_主循环"
      ├─ LoopNode (LOOP_EXPRESSION, 条件 True, 循环变量 循环_1)
      │   └─ children
      │       ├─ AssignmentNode → n = task_no (读信号，引用n)
      │       └─ IfNode (n ≠ last_n)
      │           └─ children
      │               ├─ SetNode → resultCode = 255
      │               ├─ AssignmentNode → last_n = n (引用last_n)
      │               └─ SwitchNode (n)
      │                   └─ children
      │                       ├─ CaseNode case_1 → ScriptNode(Action_0)
      │                       ├─ CaseNode case_2 → ScriptNode(Action_1)
      │                       ├─ CaseNode case_3 → ScriptNode(Action_2)
      │                       ├─ CaseNode case_4 → ScriptNode(Action_3)
      │                       ├─ CaseNode case_5 → ScriptNode(Action_4)
      │                       └─ CaseNode default case → ScriptNode(Default_Result99)
      └─ ScriptNode → Delay_01.script (sleep 0.1)
```
要点：
- 变量 `last_n`/`n` 在初始化文件夹里定义，后面全部用 XPath 引用；
- case_1~case_5 顺序对应任务号 0~4，default 兜底；
- 脚本节点内嵌完整脚本内容（cachedFileContents）。

## 示例2：test.task（指令集覆盖）
```
MainTask
├─ MoveNode MoveJ (JOINT_MOVEMENT) + WaypointNode 路点_2
├─ MoveNode MoveL (LINEAR_MOVEMENT) + DirectionNode(方向) + UntilNode
│     └─ WaypointNode 路点_1
├─ IfNode  digital_in[5] == True  → children
│     └─ IfNode  digital_in[6] ≠ False → children
│           ├─ PlaceHolder 占位节点
│           └─ MoveNode MoveP (PROCESS_MOVEMENT, 带 inheritedProcessMoveTransitionRadius) + WaypointNode 路点_3
├─ WaitNode 等待 0.3s
└─ LoopNode (LOOP_ALWAYS)
    └─ children
        └─ AssignmentNode → 偏移插件(TaskExtensionNode Offset)
            └─ dataModel: offsetPose / offsetJoints / sourceVariable(gb_p2) / resultVariable / frame
（MainTask 之后）
SubTaskNode 子任务_1
  └─ children → PopupNode 弹出窗口
```

## 生成器 round-trip 校验
`python scripts/task_generator.py` 会：
1. 读取 `D:\WorkSpace\Main_ActionDispatche_2026-8-11.task`，按 case 顺序提取脚本；
2. 用 TaskBuilder 重建同一任务；
3. 对比原始/生成的元素指纹（tag+属性顺序），输出 `指纹一致: True/False`。
开发时改过生成器后务必跑一次确认。