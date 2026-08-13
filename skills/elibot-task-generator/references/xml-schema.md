# .task 文件 XML 序列化参考（艾利特 ES/CS 图形化编程）

> 依据两份真实文件逆向整理：
> - `Main_ActionDispatche_2026-8-11.task`（主任务：文件夹/赋值/写寄存器/循环/判断/开关/脚本/延时）
> - `test.task`（MoveJ/MoveL/MoveP/等待/循环/偏移插件/If读数字输入/弹出窗口/子任务/占位）
> 生成时必须遵循这里的元素名、属性、子元素顺序。

## 0. 根结构与机器人参数（照抄你的机器人）

```xml
<EliTask name="任务名" installationName="default" robotType="CS612" toolType="7"
         createdVersion="2.16.0.964" lastSavedVersion="2.16.0.964"
         robotSN="0726A416A10013" savedTime="YYYY-MM-DD HH:MM:SS"
         typeName="机器人主任务">
  <InitVariables typeName="初始化变量"/>
  <MainTask isTaskAlwaysLoops="true" hasBeforeStart="false" hasInitVariables="true" typeName="机器人主任务">
    ...节点...
  </MainTask>
  ...子任务（可选，在 </MainTask> 之后）...
</EliTask>
```
- `isTaskAlwaysLoops="true"` = 主任务自动循环。
- robotType/toolType/版本/robotSN 直接复制用户机器人当前值（不确定就问）。

## 1. 通用表达式（Expression）单元

表达式由若干"单元格"顺序拼接，单元格类型：
| 单元格 | XML | 说明 |
|---|---|---|
| 数字/字符 | `<ExpressionCharCell char="X"/>` | 每个字符一个；如 255 → 3 个 cell：2、5、5；-1 → `-`、`1` |
| 变量 | `<ExpressionVariableCell><TaskVariable reference="相对XPath"/></ExpressionVariableCell>` | 引用已定义变量 |
| 信号/IO | `<ExpressionPinCell><pin referenceName="信号名"/></ExpressionPinCell>` | `digital_in[5]`、`task_no`、`start` 等 |
| 关键字 | `<ExpressionTokenCell token=" True " scriptCode=" True "/>` | `token` 是界面显示，`scriptCode` 是生成的脚本代码 |
| 比较符 | `==`：`<ExpressionTokenCell token=" ?= " scriptCode="==" />`；`≠`：`<ExpressionCharCell char="≠"/>` | |

## 2. 常用节点

### 文件夹
```xml
<FolderNode display="文件夹名" isHideSubtree="false" typeName="文件夹">
  ...子节点...
</FolderNode>
```

### 赋值（定义变量 / 引用变量）
```xml
<AssignmentNode valueSourceType="EXPRESSION" deepCopy="false" typeName="赋值">
  <TaskVariable name="last_n" type="Default" prefersPersistentValue="false" favorite="false" describe=""/>
  <Expression>
    <ExpressionCharCell char="-"/><ExpressionCharCell char="1"/>
  </Expression>
</AssignmentNode>
```
- 变量首次出现用 `name=`（定义），之后用 `reference="相对XPath"`（见第 3 节）。
- 读信号赋给变量：Expression 里放 `<ExpressionPinCell><pin referenceName="task_no"/></ExpressionPinCell>`。

### 设置/写输出（寄存器或信号）
```xml
<SetNode type="EXPRESSION_OUTPUT" tcpSettingEnabled="false" typeName="设置">
  <expressionOutputPinName>resultCode</expressionOutputPinName>
  <Expression><ExpressionCharCell char="2"/><ExpressionCharCell char="5"/><ExpressionCharCell char="5"/></Expression>
</SetNode>
```

### 循环
```xml
<!-- 条件循环 while 表达式 -->
<LoopNode type="LOOP_EXPRESSION" loopCount="0" isCheckConditionInSeparateThread="false" isPostTestLoop="false" typeName="循环">
  <TaskVariable name="循环_1" type="Loop" prefersPersistentValue="false" favorite="false" describe=""/>
  <Expression><ExpressionTokenCell token=" True " scriptCode=" True "/></Expression>
  <children>...子节点...</children>
</LoopNode>
<!-- 无条件循环 -->
<LoopNode type="LOOP_ALWAYS" ...>（其余同上）</LoopNode>
```

### 判断 If
```xml
<!-- 变量比较 -->
<IfNode checkExpressionContinuous="false" typeName="If">
  <Expression>
    <ExpressionVariableCell><TaskVariable reference="...n..."/></ExpressionVariableCell>
    <ExpressionCharCell char="≠"/>
    <ExpressionVariableCell><TaskVariable reference="...last_n..."/></ExpressionVariableCell>
  </Expression>
  <children>...子节点...</children>
</IfNode>
<!-- 读数字输入 == True -->
<IfNode checkExpressionContinuous="false" typeName="If">
  <Expression>
    <ExpressionPinCell><pin referenceName="digital_in[5]"/></ExpressionPinCell>
    <ExpressionTokenCell token=" ?= " scriptCode="==" />
    <ExpressionTokenCell token=" True " scriptCode=" True "/>
  </Expression>
  <children>...</children>
</IfNode>
```

### 开关 switch + 情况 case
```xml
<SwitchNode typeName="开关">
  <Expression>
    <ExpressionVariableCell><TaskVariable reference="...n..."/></ExpressionVariableCell>
  </Expression>
  <children>
    <CaseNode caseName="case_1" typeName="情况">...该 case 的节点...</CaseNode>
    ...
    <CaseNode caseName="default case" typeName="情况">...default...</CaseNode>
  </children>
</SwitchNode>
```
- 匹配规则（待现场确认）：按顺序 case_1↔任务号0、case_2↔1……default 兜底。生成时按此顺序。

### 脚本节点（内容内嵌，最重要）
```xml
<ScriptNode scriptType="FILE_TYPE" typeName="脚本">
  <cachedFileContents>整段脚本，XML转义，保留换行</cachedFileContents>
  <scriptFile pathRootType="TASK_PATH" path="Action_0_Standby_20260810.script"/>
</ScriptNode>
```
- 脚本内容**完整内嵌**在 `cachedFileContents`，.task 自包含。
- 转义：`&`→`&amp;`、`<`→`&lt;`、`>`→`&gt;`、`"`→`&quot;`、`'`→`&apos;`。
- `path` 是脚本文件名（机器人本地盘里的名字，建议和脚本一致）。

### 等待
```xml
<WaitNode type="WAIT_TIME" timeoutEnable="false" typeName="等待">
  <waitTime value="0.3" unit="S"><valueInSi>0.3</valueInSi><siUnit class="cn.elibot.robot.plugin.domain.value.Time$Unit">S</siUnit></waitTime>
</WaitNode>
```

### 弹出窗口（textmsg 类）
```xml
<PopupNode dialogType="WARNING" contentType="TEXT" message="提示文字" blockWhenPopup="false" typeName="弹出窗口"/>
```

### 子任务（放 </MainTask> 之后）
```xml
<SubTaskNode name="子任务_1" isHideSubtree="false" isSynchronized="false" isTracking="false" typeName="子任务">
  <children>...节点...</children>
</SubTaskNode>
```

### 占位节点（空分支）
```xml
<PlaceHolder typeName="占位节点"/>
```

## 3. 变量 XPath 引用规则（重要）

- 变量都在"初始化文件夹"里定义（`MainTask > FolderNode` 下的 `AssignmentNode`，按出现顺序编号 `AssignmentNode[1]`、`[2]`…）。
- 引用写法：`<TaskVariable reference="../..(N次)/FolderNode/AssignmentNode[k]/TaskVariable"/>`。
- `N` = 从"引用处 TaskVariable 元素"向上到 `MainTask` 的层数。
  - 例：主任务里的 If 表达式内引用 → `../../../../../../../FolderNode/AssignmentNode[2]/TaskVariable`（7 层）；
  - Loop children 里的赋值引用 → `../../../../../FolderNode/AssignmentNode[2]/TaskVariable`（5 层）。
- 生成器（task_generator.py）会自动按嵌套深度计算，不需要手算。

## 4. 运动节点（MoveJ/MoveL/MoveP）

```xml
<MoveNode movementType="JOINT_MOVEMENT" positionType="CARTESIAN_POSE" tcpType="ACTIVE_TCP" describe="" typeName="MoveJ">
  <frameReference>Ctrl_base_frame</frameReference>
  <jointSpeed value="1.0471975511965976" unit="RAD_S"><valueInSi>...</valueInSi><siUnit class="cn.elibot.robot.plugin.domain.value.AngularSpeed$Unit">RAD_S</siUnit></jointSpeed>
  <jointAcceleration value="..." unit="RAD_S2">...</jointAcceleration>
  <WaypointNode name="路点_2" positionNodeType="FIXED_POSITION" kinematicFlag="-1" customTransitionRadius="false" advancedPositionOptionType="INHERITED_PARAMETERS" typeName="路点">
    <transitionRadius value="0.0" unit="M">...</transitionRadius>
    <internalPosition>
      <jointPositions joints="j1,j2,j3,j4,j5,j6"/>
      <toolPose X="mm" Y="mm" Z="mm" RX="rad" RY="rad" RZ="rad"/>
      <flangePose .../>
      <fromPosition>...</fromPosition>
      <jointSpeed .../><jointAcceleration .../><cartesianSpeed value="0.25" unit="M_S">...</cartesianSpeed><cartesianAcceleration value="1.2" unit="M_S2">...</cartesianAcceleration>
      <nextMotionTime value="2.0" unit="S">...</nextMotionTime>
      <Pose key="baseToFrame">...单位阵...</Pose>
    </internalPosition>
  </WaypointNode>
</MoveNode>
```
- MoveL：`movementType="LINEAR_MOVEMENT"`，速度用 `cartesianSpeed/cartesianAcceleration`。
- MoveP：`movementType="PROCESS_MOVEMENT"`，多一个 `<inheritedProcessMoveTransitionRadius value="0.025" unit="M">`。
- **坐标单位**：XML 里 `toolPose` 是 **mm/rad**；脚本里是 m/rad。注意换算。
- 路点坐标需要**实机示教**的数据；建议动作仍用"脚本节点"里的 movel/movej（你们现有做法），图形化 Move 节点仅在确实需要时才生成。

## 5. XML 转义速查
| 原字符 | 转义 |
|---|---|
| `&` | `&amp;` |
| `<` | `&lt;` |
| `>` | `&gt;` |
| `"` | `&quot;` |
| `'` | `&apos;` |

## 6. 生成后必做检查
1. 用 XML 解析器校验格式（well-formed）；
2. `cachedFileContents` 里的脚本和 `path` 文件名一致；
3. 变量引用路径正确（参考第 3 节）；
4. 编码 UTF-8（无 BOM 更好）；
5. 首次使用前，在示教器打开确认节点树正确，再替换旧任务。