# 远程桌面VNC的使用

URL: https://docs.elibot.cn/cs/fd2cf/ed9bb
Published: 发布时间: 2025-12-24

# 1. 简介



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_529801_PibsC282PirGkzp__1713708084?w=204&h=184&type=image/png)



VNC是一款开源的远程控制软件，功能强大且高效实用，其性能不逊色同类软件，它的工作原理和WIN远程控制软件类似。



也可以直接使用网页示教器，参考链接：[https://docs.elibot.cn/cs/fd2cf/62671#heading-menu-h1-0](https://docs.elibot.cn/cs/fd2cf/62671#heading-menu-h1-0)



# 2. 工作流程



整个 VNC 一般运行的工作流程如下：



(1) VNC 客户端通过浏览器或 VNC Viewer 连接至 VNC Server。



(2) VNC Server 传送一对话窗口至客户端，要求输入连接密码（可能为空），以及存取的 VNC Server 显示装置。



(3) 在客户端输入连接密码后，VNC Server 验证客户端是否具有存取权限。



(4) 若是客户端通过 VNC Server 的验证，客户端即要求 VNC Server 显示桌面环境。



(5) 被控端将画面显示控制权交由 VNC Server 负责



# 3. 操作流程



## 3.1VNC下载



1. 官网下载连接：Download VNC Viewer | VNC® Connect



2. 选择对应的操作平台点击下载即可



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_374066_lCe4WNuqDzTg2ogR_1713709251?w=2489&h=1373&type=image/png)



## 3.2VNC安装



##### 双击下载好的安装包



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_139117_QHkYPR_M5wBCPFo-_1713709669?w=176&h=214&type=image/png)



##### 第一步-选择语言（官网不支持中文），语言确定点击“OK”



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_808091_QzzOHlnV9ZH8l9yM_1713709749?w=450&h=239&type=image/png)



##### 第二步-点击“Next”



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_577065_qW-ng_Jf8wgkBrC5_1713709876?w=776&h=602&type=image/png)



##### 第三步-点击勾上“我接受许可协议中的条款“——点击“Next”



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_715053_qR-hNk9riQPkqq6s_1713710052?w=776&h=602&type=image/png)



##### 第四步-选择你安装的路径——点击“Next”



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_551954_O9fpWrQY2lKRF47I_1713710328?w=776&h=602&type=image/png)



##### 第五步-点击“Install”



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_315721_r2ViJpJVyOXkccVM_1713710406?w=776&h=602&type=image/png)



##### 第六步-等待安装完成——点击”finsh“



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_81637_fTsuKLlOR24lvMl8_1713710582?w=776&h=602&type=image/png)



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_16131_-s3Q-SfwHUrLIxZ2_1713710638?w=776&h=602&type=image/png)



## 3.3机器人配置



##### 第一步-机器人与PC通过网线连接（标准控制柜连接接口为FB1口，D9控制柜只有一个网口，直接连接即可，通过交换机中转也可以实现）



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_49036_yx_2GcnwtkpZAQeI_1713781293?w=591&h=444&type=image/png)



##### 第二步-在机器人示教器上点击右上角菜单——点击设置



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_10924_OVa-wv_xgIHdriFh_1713781303?w=830&h=515&type=image/png)



##### 第三步-选择网络——FB1网络（静态地址)——输入（IP地址，子网掩码，默认网关）——点击“应用“（FB1网络显示网络已连接则表示连上）



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_437607_vNRH-hsSWb4BuvBY_1713781567?w=830&h=522&type=image/png)



## 3.4VNC连接



##### 第一步-打开VNC



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_716608_Z9RKg9kFE-wjb3JG_1713782023?w=1350&h=960&type=image/png)



##### 第二步-输入机器人设定的IP地址——点击下方连接（快捷键”Enter“）



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_959475_kwTTEqR5FcRNc9Gw_1713782259?w=831&h=591&type=image/png)



##### 第三步-点击”Continue“



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_209621_L_aMu47W2YwYC0-s_1713782453?w=831&h=591&type=image/png)



##### 第四步-远程操作机器人示教器界面



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_136310_oA7eAKy3s7OBXlw-_1713782592?w=830&h=546&type=image/png)



# 4. 示例



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjcyMDA3LCJwYXRoIjoicmVhbHZuY192aWV3ZXJfaW50ZXJmYWNlIiwidGltZXN0YW1wIjoiMjAyNi0wNC0wN1QxNTozMToxNi4wODcrMDg6MDAiLCJ0b2tlbiI6IiJ9LCJleHAiOiIyMDI2LTA4LTA5VDE1OjU5OjU5Ljk5OVoiLCJwdXIiOiJvcmdhbml6YXRpb25fNzhuY3ozei0tbWFpbi12ZXJzaW9uIn19--221a3552303376874f803e45b8060643e8549fbfa29e4cb2338e96ab9cc5a1f0/realvnc_viewer_interface)



# 5. 常见问题解答



1. 错误界面提示连接超时



![](https://wdcdn.qpic.cn/MTY4ODg1NjU4NjUwNTY0MA_222962_-8bEB_7FtH6h1lzy_1713782866?w=750&h=540&type=image/png)



请检查网络通讯有无断开，地址有无输错，网口有无插错，电脑IP有无修改至同一网段



2.用电脑远程操作的时候不要同时操作示教器。



#
