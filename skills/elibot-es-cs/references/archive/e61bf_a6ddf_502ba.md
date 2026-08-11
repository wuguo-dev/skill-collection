# 与外部设备通过TCPIP通讯（插件）

URL: https://docs.elibot.cn/cs/e61bf/a6ddf/502ba
发布时间: 2026-03-12

# 1. 简介



机器人本身的TCPIP通讯只有脚本这一种方式，用户编写脚本通讯耗时较多，不能开机自动连接。此插件提供用户以图形化的形式编写、提供开机自启动，能自动连接的服务端或打开服务器监听，并且提供数据处理的图形化指令。



# 2. 操作流程



## 2.1. 环境准备



版本信息：



●  机器人应用版本v2.11及以上



●  扩展socket插件 exsocket-5.10.elico



[exsocket-5.10.0.elico](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MzEwNzI4LCJwYXRoIjoiZXhzb2NrZXQtNS4xMC4wLmVsaWNvIiwidGltZXN0YW1wIjoiMjAyNi0wNy0wN1QxNzowOTo0NC45NDUrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--2e0d5bb4b17446d3549a68bc8ecfdb3293c9a51562bbac1d6e63e4ee2c8b5d3f/exsocket-5.10.0.elico?disposition=attachment)351.5 KB



## 2.2. 插件导入



[下载插件安装包后，按插件安装流程章节安装插件。](https://docs.elibot.cn/cs/3b5a8/7a799/ce642#heading-menu-h2-2)



## 2.3. 插件使用



### 2.3.1. 机器人设置IP



该插件适用于本机器人的FB1网口，在机器人设置→网络→FB1网络里的IP地址



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDA3LCJwYXRoIjoiMjAyNjAxMTYtMTk0LThkNnZ2MCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuNzczKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--05eb36a1285871b8ba11bd6e055712e2728c1bb6e142e2a7db218be1a7de2b2e/20260116-194-8d6vv0)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDA0LCJwYXRoIjoiMjAyNjAxMTYtMjQyLXZ0czFzMCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuNTgwKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--bc45acce54fc151dd9395593834ac7b78409d9cc9627583e2acd979dd1dafd3b/20260116-242-vts1s0)



### 2.3.2. socket配置



点击新建，可以建立多个socket配置。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDEzLCJwYXRoIjoiMjAyNjAxMTYtMjU0LXY0MDZ2cSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MjguNjU0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--e0676b7a517186762d2614df3e51a129688257be485eecc0cf4821612186f875/20260116-254-v406vq)



点击下拉按键，可以选择已建立的socket配置



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDA1LCJwYXRoIjoiMjAyNjAxMTYtMTk0LTlmcTg3eCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuNTE5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--93dfaeb3286b67f431099a456a350756955c1cb902b6ae7246fd3ed8336a0dc9/20260116-194-9fq87x)



点击下拉按键后，可以在选择框内选择不需要的socket配置，点击删除按钮删掉



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDAwLCJwYXRoIjoiMjAyNjAxMTYtMjU0LWV6c3lsYSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuMjgzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--3c338e2018756572858f4b9988549830b044befdc3d61db43a2747d066ef5e74/20260116-254-ezsyla)



### 2.3.3. 机器人做客户端



#### 2.3.3.1. 客户端连接



### 方法1：自启动



在导入拓展socket插件之后，在“配置”-“socket配置”里可以设置客户端的参数。



“类型” 选择CLIENT，输入对应的 “”地址、“端口”，点击 “连接” 按钮界面上会有连接状态反馈。



socket插件的“socket配置”中我们可以一些便捷功能能使用。



“自启动”(只需勾选上)，机器人开机后，会自动连接对应地址的服务器。



“信号” 选择指定的输出（DO(0)-DO(15)）。连接服务器成功后，对应的DO会对外输出信号。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDAzLCJwYXRoIjoiMjAyNjAxMTYtMTgyLXhtdmFrYyIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuNTg1KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--25425def088081755f90dd7f26860a981d9bdf7740885138ddc34827e0632c9a/20260116-182-xmvakc)



此图-表示已经连接上对应服务器



### 方法2：通过任务连接



指令栏选择 “插件”，1. 点击"Socket Client" 2. 勾选“连接” 3. 选择对应的socket配置



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDAxLCJwYXRoIjoiMjAyNjAxMTYtMjMwLXZteWgxOCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuNDExKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--3baac330c2e103efa9beabca41060ff6ecb2cd344d5c97020ba6fc98868034c7/20260116-230-vmyh18)



1. 点击右侧的运行按钮。运行任务时，通过该行指令，连接至对应地址的服务器



2. 点击左侧的“连接”按钮，在任务运行前，先连接至对应地址的服务器。已连接后，不影响该行指令的正常运行



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDAyLCJwYXRoIjoiMjAyNjAxMTYtMjMwLXQwNGRxciIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuNTY0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--3b55f0615fd958cd1c73c41731a307b40098c612b2b52c98c84ff141fc3e7142/20260116-230-t04dqr)



#### 2.3.3.2. 客户端发送



指令栏选择“插件”，1. 点击"Socket Client" 2. 选择对应的socket配置 3. 勾选“发送” 4. 输入需要发送的内容



可以手动点击”发送“（必须是已连接的状态），也可以直接”运行任务“来发送



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzk5LCJwYXRoIjoiMjAyNjAxMTYtMjA2LTFoZ29idSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuMjI5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--569d301ebcaeb5ccc2795eaadbd4cef3fdbcfca3956cd66b60ae9264e4262548/20260116-206-1hgobu)



可以选择“输入”或 “变量”。选择变量，可以在任务中，给变量赋不同的值，动态调整发送的内容



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDE1LCJwYXRoIjoiMjAyNjAxMTYtMjA2LWZjbGRsciIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NTA6MzUuODU0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--4462ed21981bacc9fd714b49a7a12eed274b331c8987242bad27265c2fc9171b/20260116-206-fcldlr)



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzk4LCJwYXRoIjoiMjAyNjAxMTYtMTY3LWlwN2gzbiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuMjU1KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--d11b7fd1e08b17ab7326c79b25efc69eb8a9c081cc45e5a4da3a1691892507fa/20260116-167-ip7h3n)



针对服务端的需求，可以选择发送不同类型的数据



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzc4LCJwYXRoIjoiMjAyNjAxMTYtMjA2LXJ4MnByeCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTguODE1KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--d5fd61bf9c84eeab921bc1377557ea79eaf7c789567cfc7d1f317dca0ddd3600/20260116-206-rx2prx)



#### 2.3.3.3. 客户端接收



指令栏选择“插件”，1. 点击"Socket Client" 2. 勾选“接收” 3. 选择对应的变量 4. 选择接收的数据类型。



可以手动点击”接收“（必须是已连接的状态），也可以直接”运行任务“来接收。



超时时间，默认：0表示一直等待接收值。



接收到的值的数据类型，如果如果发送的数据，无法变成对应选择类型会弹出错误弹窗。



比如；发送的值为[1，2，3]数组，选择的是整数类型就会发生弹窗错误。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzgzLCJwYXRoIjoiMjAyNjAxMTYtMjU0LWttcm50IiwidGltZXN0YW1wIjoiMjAyNi0wMS0xNlQxNTo0Nzo1OS4zNDYrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--f2fa009bec5aff6752fae92897e4731d1148de0687fe83e7741cc9ea92b0635a/20260116-254-kmrnt)



注：无论是发送还是接收，都要选择对应的socket配置



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzc5LCJwYXRoIjoiMjAyNjAxMTYtMjMwLXhkYzVucSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTguODUxKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--99c097821cee90ff2f908b54a6c234667fad627714b569d1fb01e433a40dcc84/20260116-230-xdc5nq)



### 2.3.4. 机器人做服务端



#### 2.3.4.1. 服务端开启监听



### 方法1：自启动



在导入拓展socket插件之后，在“配置”-“socket配置”里可以设置服务端的参数。



“类型” 选择CLIENT，输入对应的 “”地址、“端口”，点击 “监听” 按钮，界面上会有监听状态反馈。



socket插件的“socket配置”中我们可以一些便捷功能能使用。



“自启动”(只需勾选上)，机器人开机后，会自动打开监听。



“信号” 选择指定的输出（DO(0)-DO(15)）。打开监听后，对应的DO会对外输出信号。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzkyLCJwYXRoIjoiMjAyNjAxMTYtMjQyLXZhaHhrMyIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuNjkwKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--78d67afdf66bf0de59494ee2e355702b16689b796ce0d39699ba98e93153d36d/20260116-242-vahxk3)



### 方法2：在任务里直接添加



指令栏选择 “插件”，点击"Socket Server"-勾选“监听”-选择对应的socket配置，“运行任务”或点击"监听"



注：每次任务运行监听指令会让客户端连接断开，所以无特殊需求方法2不建议使用。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzg0LCJwYXRoIjoiMjAyNjAxMTYtMTY3LW95eGEyOSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuMTc2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--8e339f774ec49df8c8d8d22ac0b12152cf0afc3cc3c2675e53b227088ee938ce/20260116-167-oyxa29)



#### 2.3.4.2. 服务端发送



指令栏选择“插件”，1. 点击"Socket Server" 2. 选择对应的socket配置 3. 勾选“发送” 4. 输入需要发送的内容。



可以手动点击”发送“（必须客户端已连接的状态），也可以直接”运行任务“来发送



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzkwLCJwYXRoIjoiMjAyNjAxMTYtMTk0LTl1azB3NiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuNDkwKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--8a17460e04904d65ef32d00dc41cfe9ada12c65827360267be8dbb6685b3a3ee/20260116-194-9uk0w6)



可以选择“输入”或 “变量”。选择变量，可以在任务中，给变量赋不同的值，动态调整发送的内容



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzg5LCJwYXRoIjoiMjAyNjAxMTYtMTgyLWN5NG04eSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuODg3KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--b735dfdebf30062541c630dceb81bbce97f47cba7fc1eb6efaee336004e20625/20260116-182-cy4m8y)



针对客户端的需求，可以选择发送不同类型的数据



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzg2LCJwYXRoIjoiMjAyNjAxMTYtMjE4LXh4ZzF2MSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuNDAzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--ffee78554d272e9769636e6a2ce65c478fc583143d816a931db5e05cfe0cb047/20260116-218-xxg1v1)



#### 2.3.4.3. 服务端接收



指令栏选择“插件”，1. 点击"Socket Server" 2. 勾选“接收” 3. 选择对应的变量 4. 选择接收的数据类型。



可以手动点击”接收“（必须是已连接的状态），也可以直接”运行任务“来接收。



超时时间，默认：0表示一直等待接收值。



接收到的值的数据类型，如果如果发送的数据，无法变成对应选择类型会弹出错误弹窗。比如；发送的值为[1，2，3]数组，选择的是整数类型就会发生弹窗错误。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzk0LCJwYXRoIjoiMjAyNjAxMTYtMjA2LTdwcTJicCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuODg4KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--2b540010adf909362e1837d61915fd8fb9a9f8acb67caad34e250909ff38fa45/20260116-206-7pq2bp)



注：无论是发送还是接收，都要选择对应的socket配置



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzg4LCJwYXRoIjoiMjAyNjAxMTYtMjQyLW5udG5xOSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuNDYwKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--b60d57aa11c71f80fc74c36719bd32849a96368183aa5fb1af6aeec42ae2f4d9/20260116-242-nntnq9)



### 2.3.5. socket插件便捷指令



#### 2.3.5.1. 字符串拆分



该指令可以把接收的字符串型数据用符号进行分割。



指令栏选择“插件”。1. 点击"字符串拆分" 2. 选择需要处理的字符串变量 3. 选择处理后，用于接收结果的变量 4. 选择分割符。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzg3LCJwYXRoIjoiMjAyNjAxMTYtMTk0LTc5NjR3YiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuMzczKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--1659822659f4077629a32e882250350beaca921f05cd9cc37502f7dc5432ae1d/20260116-194-7964wb)



字符串中的数字，会自动转换成整型或者浮点型，可以直接用于计算等操作。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzg1LCJwYXRoIjoiMjAyNjAxMTYtMjU0LWlxdGZ1NCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuMTg5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--ce84314b4aaacc25d9a62093ce2e3923c2f3118c463a3382269f458a9be591e6/20260116-254-iqtfu4)



#### 2.3.5.2. 字符串拼接



该指令可以将两串字符串，拼接成一串字符串。



指令栏选择“插件”。1. 点击"字符串拼接" 2. 选择需要拼接的字符串变量 3. 选择需要拼接的字符串变量 4. 选择拼接后，用于接收结果的变量。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzgyLCJwYXRoIjoiMjAyNjAxMTYtMTgyLWlsZTR6MyIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuMDU2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--2317d2a0ddf4f936fa69ee642e4fda187180ea986458e4438333aaa76bd069bf/20260116-182-ile4z3)



拼接后的效果



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzkzLCJwYXRoIjoiMjAyNjAxMTYtMjE4LTF5YTBxOCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuNzUyKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--3f643fcd283521c0cfce493ba02cc9a1d5db83d974908cfc861d4d825beac15c/20260116-218-1ya0q8)



#### 2.3.5.3. 数组赋值



该指令可以直接把数组里的数据拆分赋值到变量里，下标代数组里的第几位数据（从0开始计算）



指令栏选择“插件”。1. 点击"数组赋值" 2. 选择对应的数组变量 3. 用于接收结果的变量 4. 填写下标



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDEwLCJwYXRoIjoiMjAyNjAxMTYtMjMwLTZsY3VzbiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDEuNDczKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--c0d43b374aca6de19f33949841c9f594a93cb3e43500bca3e1338cf751bb48f5/20260116-230-6lcusn)



赋值后的效果



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzc3LCJwYXRoIjoiMjAyNjAxMTYtMTY3LXV2dWt0cyIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTguNzY5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--7fd80e84dedaece07a3a52133540236ec3a6c58241e0fd886ee34c7e489c6e43/20260116-167-uvukts)



#### 2.3.5.4. 清除缓存



该指令用于“服务器” 或 “客户端”发送数据后，清除未接收处于缓存区的数据。



指令栏选择“插件”。1. 点击"“Flush Socket" 2. 选择对应socket配置



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzgwLCJwYXRoIjoiMjAyNjAxMTYtMjA2LXYzY2h2bCIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTguODYzKzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--7ac1df8887d8631f0e2707d54842b7340f5a5b157396decd1ece94b4d02e1294/20260116-206-v3chvl)



假设机器人处于未运行状态，通讯助手作为客户端，向机器人发送了数据



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzgxLCJwYXRoIjoiMjAyNjAxMTYtMjMwLWVxcjRkZSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTguOTA0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--5469e58095f46196bcd6b22458826315248992f6104fba8370c25f7b75186a4d/20260116-230-eqr4de)



在这种情况下，未接收的数据会保存在缓存区。机器人一但执行任务，立刻就会收到保存在缓存区的数据。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDEyLCJwYXRoIjoiMjAyNjAxMTYtMjE4LTVvbGpzIiwidGltZXN0YW1wIjoiMjAyNi0wMS0xNlQxNTo0ODowMS44MjYrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--5ca14d1160085b72ec31f5383c20c77583a7835f91d1c9574f98454d4a0ddc13/20260116-218-5oljs)



执行“清除缓存”指令后，会清除掉处于缓存区的数据，就不会出现刚执行任务，客户端还没发送数据，机器人这边就已经接收到数据的情况。



机器人会一直处于运行状态，等待客户端发送数据。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1MzkxLCJwYXRoIjoiMjAyNjAxMTYtMTY3LW1ucTAwYiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuNzI0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--01a9fda2739e8d4e3c1a0c0d06e037d1120c01b83dae6414a034bd22b16ab626/20260116-167-mnq00b)



#### 2.3.5.5. 检查连接状态



该指令用于检测 “客户端” 或 “服务端” 的连接状态



指令栏选择“插件”，点击"Check Socket"-选择对应的socket配置-选择需要赋值的变量



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1NDA5LCJwYXRoIjoiMjAyNjAxMTYtMjU0LWt5MzllOSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDEuMzM2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--7532a596e4bbaa8dcebf91f7d82799d7fec5ac03ea5a391ed84d4ee5ad2cc4fc/20260116-254-ky39e9)



该指令会反馈对应socket配置的连接状态，会返还 “True” 或 “False”，并赋值到对应的变量



“True”是已连接，“False”是未连接。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzk1LCJwYXRoIjoiMjAyNjAxMTYtMTk0LXF3eWVoNSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuMDA2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--86e7ec4e671f14117b21d7fa96880d6e462b04a00d3339ae863fda7b63666db0/20260116-194-qwyeh5)



# 3. socket日志解析



socket插件版本必须要5.9.8以上



socket插件在运行时，会生成一个日志文件，该日志如果通过备份导出则文件路径：CS_BACKUP\EliRobot\log\extend_socket_（server或client）.log客户端和服务器的日志分开。



也可以通过Win SCP等途径直接登录机器人并读取，路径为：



/home/elite/user/log/extend_socket_（server或client）.log



注意：该日志无法通过支持文件导出。



日志文件打开如下：日志中会显示端口的连接状态以及发送接收数据的日志。



该日志可以保存4万条以上。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjYwNDcxLCJwYXRoIjoiMjAyNjAyMjgtMzg5Njk2MC1icWxybWEiLCJ0aW1lc3RhbXAiOiIyMDI2LTAyLTI4VDE3OjI4OjAzLjc1MCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--d318b3473afadcd5bdcdfc6af511f2257308162f81d56e475835c71d74787d00/20260228-3896960-bqlrma)



# 4. 常见问题解答



### 4.1.客户端/服务端连接不上？



机器人为客户端时查看对应的IP地址是否填错，是否是同一网段，是否可以ping通，是否网线插在在FB1网口。



### 4.2.常见的报错



报错码：socket.timeout



原因：接收数据超时，在接收里设定了超时时间。超时时间等于0，该指令会一直等待，直到接收到数据为止



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzk2LCJwYXRoIjoiMjAyNjAxMTYtMjQyLTFkZms5YiIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDc6NTkuOTY5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--2cd8e3c9dee492ccd0460ba667dc399c13ce3b6df1330e533389fd091299df59/20260116-242-1dfk9b)



报错码：ValueError



原因：数据类型不一致。图中的案例，“接收”设定的“数据类型”是整形，实际收到的数据是字符串“abc”



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ1Mzk3LCJwYXRoIjoiMjAyNjAxMTYtMTgyLXE5amw3MSIsInRpbWVzdGFtcCI6IjIwMjYtMDEtMTZUMTU6NDg6MDAuMDI2KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--05c37953e2b4ccb29d863ee97a77b2b2f14ca7950c5fe9090689a45b0c598fcc/20260116-182-q9jl71)



#
