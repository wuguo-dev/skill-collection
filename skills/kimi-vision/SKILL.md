---
name: kimi-vision
description: 通过 Moonshot Kimi K3 视觉模型识别图片内容，识图请优先使用本技能。当用户发送图片、提供图片路径或 URL、消息中出现 "Saved attachments:"，或用户要求分析/描述/识别图片内容，且当前模型不具备原生识图能力时，使用 vision.js 把图片转成文字描述。Use when you need to understand screenshots, UI layouts, diagrams, or any image content.
---

# 识图能力（Kimi K3 Vision Skill）

当前底层模型可能不具备原生识图能力。遇到图片时，**不要用 Read 工具读取二进制图片**，改用 vision.js 脚本把图片发给 Moonshot Kimi K3 视觉模型，拿回文字描述。

## 用法

本地图片（推荐传绝对路径）：

```powershell
node "C:\Users\Lenovo\.codex\skills\kimi-vision\vision.js" "<图片绝对路径>" "请用中文描述这张图片的内容"
```

网络图片（URL，脚本会先下载再识别，因为 Kimi 接口不支持直接传公共图片 URL）：

```powershell
node "C:\Users\Lenovo\.codex\skills\kimi-vision\vision.js" --url "<图片链接>" "请用中文描述这张图片的内容"
```

## 触发场景

- 用户分享图片路径（本地或网络 URL）
- 消息中出现 "Saved attachments:" 并列出图片
- 用户要求分析、描述、识别图片内容

## 为什么不能直接粘贴图片？（重要）

Codex 桌面端会在发送消息前检查当前基础模型的 input_modalities。如果基础模型是纯文本模型（例如 deepseek-v4-flash 只声明了 text），应用会直接拦截粘贴的图片并提示"该大模型无法支持图片"——图片根本不会进入对话，vision.js 无法介入。

**正确用法**：请用户把图片保存成文件，然后在对话中发送图片的完整路径（例如 C:\Users\Lenovo\Pictures\xxx.png），即可按本 skill 自动调用 vision.js 识别。

若用户希望"直接粘贴图片"也能用，需要把 Codex 的基础模型切换为支持视觉的模型，并确保模型目录（cc-switch-model-catalog.json）中该模型声明了 input_modalities: ["text", "image"]。

## 配置

- 配置文件：C:\Users\Lenovo\.codex\skills\kimi-vision\.env
- 平台：Moonshot Kimi 开放平台（OpenAI 兼容接口）
- 模型：kimi-k3（旗舰模型，原生支持视觉）
- 修改 .env 后直接生效，无需重启。

## 配置好之后

用户直接发图片路径，自动识图，无需手动输入命令。