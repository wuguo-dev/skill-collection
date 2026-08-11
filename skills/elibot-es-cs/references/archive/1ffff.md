# ROS

URL: https://docs.elibot.cn/cs/1ffff
Published: 发布时间: 2025-12-24

# 1.  简介



ROS（Robot Operating System）是适用于机器人的开源元操作系统。ROS 集成了大量的工具、库、协议，提供类似 OS 所提供的功能，可以实现对机器人的控制。



# 2.  操作流程



#### 2.1硬件准备



需要设置IP以及FB1以及FB2，将网口连接到上位机



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjM2NzIwLCJwYXRoIjoiMjAyNTEyMjQtMzkyMTYxMi10c25hNWoiLCJ0aW1lc3RhbXAiOiIyMDI1LTEyLTI0VDEwOjU1OjU0LjY0NCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--2e7b304c5720d04d55b47cc54fef5b7f573b975affd029f82f7d3ed99f01c345/20251224-3921612-tsna5j)



设置步骤如下：



设置网口IP



1、步骤1



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjM2NzE4LCJwYXRoIjoiMjAyNTEyMjQtMzg0NzkxLXNyYTZpMyIsInRpbWVzdGFtcCI6IjIwMjUtMTItMjRUMTA6NTQ6MDguMjg0KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--fd8e3b524c8af7edda6905b1f5a2600fa7250116a81ef50b49d8016c17ad16f2/20251224-384791-sra6i3)



2、  步骤2



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjM2NzE5LCJwYXRoIjoiMjAyNTEyMjQtMzg0Ni14OHJkeWkiLCJ0aW1lc3RhbXAiOiIyMDI1LTEyLTI0VDEwOjU0OjA4LjMxOSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--f66ea9f26a377e2a70624f1371d3a49723f25d6d48d9ef17298e70263fb0e2f2/20251224-3846-x8rdyi)



3、  步骤3，设置-网络-设置FB1以及FB2



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjM2NzE3LCJwYXRoIjoiMjAyNTEyMjQtMzg0NzkxLWxscHVxYyIsInRpbWVzdGFtcCI6IjIwMjUtMTItMjRUMTA6NTQ6MDguNDA5KzA4OjAwIiwidG9rZW4iOiIifSwiZXhwIjoiMjAyNi0wOC0wOVQxNTo1OTo1OS45OTlaIiwicHVyIjoib3JnYW5pemF0aW9uXzc4bmN6M3otLW1haW4tdmVyc2lvbiJ9fQ--b88aaaafafc4be2f588dd57c1761184c977bd6ecf76aed434e9d49707c81fe15/20251224-384791-llpuqc)



4、  步骤4，尽量把远程控制关闭，如果打开必须在远程控制



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjM2NzE2LCJwYXRoIjoiMjAyNTEyMjQtMzg0Ni1iM29wYWciLCJ0aW1lc3RhbXAiOiIyMDI1LTEyLTI0VDEwOjU0OjA3LjIzNCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--7cab88e1d2d707aff4c3550c3fa61c39f33fd178af0cbf6b98e129052df1d391/20251224-3846-b3opag)



#### 2.2 所需环境



艾利特CS机器人支持ROS2的控制，下面进行操作手册



首先需要自行安装Ubuntu22.04，ROS2，以及各类工具



安装ROS2完成后，将ELITESDK文件下载拷贝下来，地址：GitHub - Elite-Robots/Elite_Robots_CS_SDK



注意：执行下方下载等步骤需要联网并且由于国内网络访问github速度过慢可能导致失败，需多次尝试



下载步骤如下：



打开终端输入命令，git clone后跟复制的GitHub内HTTPS的网址



```
git clone https://github.com/Elite-Robots/Elite_Robots_CS_SDK

```



下载拷贝SDK文件



逐行执行以下指令，注意：cd打开的是SDK文件夹，并且Ros2源码与SDK不建议放在一起，编译时容易出错，可以将EliteSDK放到桌面。



```
cd <clone of this repository>
mkdir build && cd build
cmake ..
make -j
sudo make install

```



进行SDK安装使用



可以在桌面新建文件夹elite_ros_ws，并在此文件夹下创建一个src文件夹，打开文件夹，并打开命令行输入以下代码



下载ROS2源代码文件，地址： GitHub - Elite-Robots/Elite_Robots_CS_ROS2_Driver



```
git clone
https://github.com/Elite-Robots/Elite_Robots_CS_ROS2_Driver.git

```



#### 2.3配置 ROS 环境



##### 1.在elite_ros_ws目录下打开终端运行，初始化 rosdep 的配置文件



```
sudo rosdep init

```



##### 2.下载和更新最新的依赖项数据，确保在安装 ROS 包时可以正确地解决所有依赖。



```
rosdep update

```



注意：执行此步骤需要联网并且由于国内网络访问github速度过慢可能导致失败，需多次尝试。



##### 3.在 ROS 工作空间中自动安装所有 ROS 包的系统级别依赖项，确保你可以顺利构建和运行这些 ROS 包



```
rosdep install --ignore-src --rosdistro $ROS_DISTRO --from-paths src -y

```



完成后，会显示All required rosdeps installed successfully



##### 4.编译工作空间中的 ROS 2 包



```
colcon build

```



如果在编译时出现colcon：未找到命令，可以



```
sudo apt update
sudo apt install python3-colcon-common-extensions

```



##### 5.在终端中加载 ROS 2 工作区的环境设置。它会配置你的终端环境，以便在当前会话中正确地使用 ROS 2 包和相关工具



```
source install/set.bash

```



##### 6.  运行ROS Driver



次步骤开始需连接机器人，注意需连接FB1以及FB2两个网口，



```
ros2 launch eli_cs_robot_driver elite_control.launch.py robot_ip:=172.16.11.109 local_ip:=172.16.11.20 cs_type:=cs63 launch_rviz:=false headless_mode:=true

```



- robot_ip:=填写机器人IP（FB1）
- local_ip:=填写电脑IP
- cs_type:=填写机器人型号
- launch_rviz:=是否打开可视化页面。true为显示rviz页面，:=false为不显示
- headless_mode:=是否需要控制插件，true为不使用，不写为使用



注意：首次连接机器人时建议launch_rviz改为true，确实移动机器人，监视页面有反应，如监控页面与实际机器人姿态不一致，需多次重启，确保没有问题后，将launch_rvuz改为false，因为之后在启动MoveIt2会再次打开一个可视化窗口。



##### 7.  运行MoveIt2



首先在elite_ros_ws目录重新建立一个终端，输入步骤5，一样的命令，再输入下面命令



```
ros2 launch eli_cs_robot_moveit_config cs_moveit.launch.py cs_type:=cs63 launch_rviz:=true headless_mode:=true

```



机器人示教器上显示机器人在运行中，就可以通过运行MoveIt2来控制机器人了



#### 2.3卸载SDK



由于一些特殊情况，需要卸载现有SDK



##### 下面操作非必需



##### 删除 SDK 安装文件



1.  查找 SDK 安装文件位置



首先确认 SDK 安装的位置（例如/usr/local/lib）



```
sudo find /usr/local /usr /opt -name "*elite*"

```



2.  删除共享库和静态库



根据查找结果，删除 SDK 的库文件



```
sudo rm-rf /usr/local/lib/libelite-cs-series-sdk.so 
sudo rm-rf /usr/local/lib/libelite-cs-series-sdk.a

```



3.  删除 CMake 配置文件



删除 CMake 生成的配置文件



复制编辑



```
sudo rm-rf /usr/local/lib/cmake/elite-cs-series-sdk

```



4.  更新动态链接库缓存



清理动态链接缓存，防止系统加载已删除的库文件



```
sudo ldconfig

```



##### 删除 SDK 源文件



1.  定位 SDK 源文件所在路径



SDK 源文件一般位于~/elite_ros_ws/src/ 下。



确认位置



```
ls~/elite_ros_ws/src/

```



2.  删除 SDK 源文件



删除 SDK 的源代码



```
rm-rf ~/elite_ros_ws/src/Elite_Robots_CS_SDK

```



##### 删除生成的构建文件



1.  删除编译生成的 build/, install/, log/ 文件夹



这些是colcon build 或 cmake 生成的文件



```
rm-rf ~/elite_ros_ws/build ~/elite_ros_ws/install ~/elite_ros_ws/log

```



##### 删除 CMake 配置缓存（可选）



如果生成的 CMake 配置文件未完全删除，可以清理缓存



```
rm-rf ~/.cmake

```



##### 检查是否卸载干净



1.  再次查找系统中是否残留 SDK 文件



如果输出为空，说明已彻底删除



```
sudo find /usr/local /usr /opt -name "*elite*"

```



2.  检查 ROS 环境变量中是否还有 SDK 相关的路径



```
printenv| grep elite

```
