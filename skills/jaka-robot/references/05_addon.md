# AddOn 3.0 开发

来源：[AddOn 目录](https://www.jaka.com/docs/guide/V3/addOn/)、[关于 AddOn](https://www.jaka.com/docs/guide/V3/addOn/1.1-AboutAddOn.html)、[配置文件说明](https://www.jaka.com/docs/guide/V3/addOn/7.1-IniConfig.html)。

## 版本与用途

- 当前教程默认 AddOn 3.0，支持控制器 1.7.1.x `_X64`；AddOn 1.0/2.0 已停止维护与开发支持。
- AddOn 用于封装自定义指令、自定义服务、自定义网页，或组合成复合插件，适合第三方设备与工艺包。
- 名称仅使用英文字母和下划线，不含空格或特殊字符。

开始前按用户实际控制器核对 [关于开发](https://www.jaka.com/docs/guide/V3/addOn/1.2-AboutDev.html) 与 [开发环境搭建](https://www.jaka.com/docs/guide/V3/addOn/3-EnvironmentInstall.html)。不要因为文档位于 V3 目录就假设 AddOn 版本与 V3 控制器天然兼容。

## 运行机制

- 自定义服务基于 Node-RED，在控制器内运行，可为指令和网页提供中间层。
- 自定义指令由属性、编辑页面和脚本组成；App 保存或运行时把参数交给 AddOn 服务，服务生成脚本返回给 App。
- 自定义网页通常部署到控制器并由 Nginx 代理，也可部署到外部设备；通过官方 App API 与 JAKA App 交互。

## 包结构与配置

- 服务/指令流通常保存在 `flows.json` 或自定义名称的 Node-RED 流文件。
- 任何 AddOn 包都必须包含 `xxx_config.ini`；配置文件指向服务入口并声明类型、端口、URL、语言和启动策略。
- 自定义页面工程建议使用 `client/`，构建产物使用 `dist/`。

```ini
[AddOnInfo]
convention=3.0
name=JAKA_Command
description="在日志中输出信息"
version=1.0
type=1
portal=10006
url=http://localhost/myAddOnUi
languagetype=node-red
service=AddOn.json
serviceenabled=1
```

字段含义和 `type` 枚举从当前配置文件说明页核对，不复用旧代 AddOn 示例。

## 开发路径

1. 选择服务、指令、网页或复合类型，定义对外输入/输出与错误模型。
2. 搭建官方 Node-RED/AddOn 环境，先完成最小服务调用。
3. 指令脚本只接收经过校验的参数；把单位、坐标系、范围和默认值写进属性定义。
4. 网页调用使用官方 App API，并为控制权、超时和错误状态提供可见反馈。
5. 按配置规范组包，在兼容控制器上安装；先验证安装/启动/停止/卸载，再验证真实工艺。
6. 发布前阅读 [发布](https://www.jaka.com/docs/guide/V3/addOn/5-Release.html) 和 [说明手册编写](https://www.jaka.com/docs/guide/V3/addOn/4.5-UserGuide.html)。
