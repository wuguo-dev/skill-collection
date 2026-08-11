# 自定义脚本函数插件

URL: https://docs.elibot.cn/cs/3b5a8/0ffe3/5ffdf
发布时间: 2026-01-21

# 1. 简介



ScritptFunction是一款支持函数库自定义的插件，用于用户直接在插件中定义好脚本函数，可以直接通过示教器表达式键盘插入函数功能，实现函数调用，减少现场工程师编写任务树的工作量，如坐标变换、等待超时、 位姿偏移等，语法需支持Python格式。



[ScriptFunction-1.0.4.elico](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6Mjg5NDg0LCJwYXRoIjoic2NyaXB0ZnVuY3Rpb24tMS4wLjQuZWxpY28iLCJ0aW1lc3RhbXAiOiIyMDI2LTA1LTE1VDA5OjQwOjQ0LjA2MCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--4db69739481296064c77883992bae9d1ac45174735369691b7ad1f0484759376/scriptfunction-1.0.4.elico?disposition=attachment)87.8 KB



# 2.插件安装



[下载插件安装包后，按插件安装流程章节安装插件。](https://docs.elibot.cn/cs/3b5a8/7a799/ce642#heading-menu-h2-2)



# 3. 使用



在使用中有两种方法，用户可根据自己的需求选不同的方式实现。



## 3.1 直接导入脚本方式



### 3.1.1导入脚本函数



点击配置 >> 插件 >>脚本函数，点击导入在外部写好的文件，选择.script后缀的文件，插件可 以自动加载文件并解析文件中的函数。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDk4LCJwYXRoIjoiMjAyNjAxMjItMjU1MjEyNi01M2htZmgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI1LjU3NSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--2773a956c24c348b92103f45deb9dd0d691ab1657f2d1c6f44dfe2053c175583/20260122-2552126-53hmfh)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDk2LCJwYXRoIjoiMjAyNjAxMjItMjY4Mjk1OS04b2I1bzgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI1LjQyOSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--5739396d59bcbb915e05901324f506e1a26cc3046cec4b6e3dd276b5873da054/20260122-2682959-8ob5o8)



导入的函数，可以选中查看函数体：



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDk5LCJwYXRoIjoiMjAyNjAxMjItMjU0NjMzNy1jMTBkbXgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI1Ljg2NCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--8c40abd484353f473907312a284ae93db681452d6ec7ce157af9dd00cf158992/20260122-2546337-c10dmx)



### 3.1.2注册函数



点击函数名称前的选择框，可以将函数注册到键盘函数中，反之，可以取消注册。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MTAxLCJwYXRoIjoiMjAyNjAxMjItMjU0NjMzNy0zcjJveW4iLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI1LjcxNyswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--d59515aa36d2f31e7aae9293823f9a06f16ddf1cf8b588ba7ea9594419594c49/20260122-2546337-3r2oyn)



### 3.1.3任务中使用



如图，会出现在输入法快捷栏中，方便使用。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MTAwLCJwYXRoIjoiMjAyNjAxMjItMjY0MDI5NS1lOTVuaTgiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI1LjgwNyswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--7f91a4e516b566c758369b7c0921fb74d0b3ca8b6d5e2cd8841e849d54055a8b/20260122-2640295-e95ni8)



## 3.2 添加自定义函数方式



点击添加按钮，在键盘中输入函数的签名，只支持添加函数签名并可以添加到键盘函数中，函数体需要在任务树的脚本中补全。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MDk3LCJwYXRoIjoiMjAyNjAxMjItMjY0MDI5NS1sc3huNHkiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI1LjYzNiswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--c630ed83c9cccd48952a4382f7a6e95065c30bfd10f493b7c7e925cf86c733df/20260122-2640295-lsxn4y)



在任务中新创建脚本函数体，用同一名字保存命名脚本。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ3MTAyLCJwYXRoIjoiMjAyNjAxMjItMjY1MjE1MS15ODM2amciLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTIyVDEzOjM5OjI2Ljc3NCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--a3547efebfcf39f4165fd4218d34749dcdbdb98fb5d89ad0f00ed2d6d15bf719/20260122-2652151-y836jg)



### 3.2.2注册函数



同2.1.2章节相同。



### 3.2.3任务中使用



同2.1.3章节相同。
