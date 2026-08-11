# 传送带跟踪使用

URL: https://docs.elibot.cn/cs/1b89f/fddac/33ae2
发布时间: 2026-01-13

# 1. 简介



本文介绍cs机器人用写脚本去实现传送带功能(增量式），单台机器人最多支持2个传送带跟踪。



# 2.前期准备



2.1机器人版本要求：2.12.0及以上



2.2硬件连接



机器人连接控制柜B4高速io



本文以西克编码器示列



选择编码器类型：增量式



模式：正交式，升降式，上升，下降



A输入：高速输入



B输入：高速输入



注意：正交式，需要接入两个输入及AB，其他的模式，只需要接A输入即可。



使用正交式模式



+US---24V



GND---0V



A---DI16-19（A,B分两个io段子接）



B---DI16-19



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NDY0LCJwYXRoIjoiMjAyNjAxMTUtMjc2OTQzNC1hcmcyN3YiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDEzOjU2OjM1LjcxOSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--1d2f51013bc9e63485ba5621798e457120511ba770b706bc39d491afdb92ebe5/20260115-2769434-arg27v)



其他模式



+US---24V



GND---0V



A---DI16-19



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NDYyLCJwYXRoIjoiMjAyNjAxMTUtMzI5NDk3Ny16ZXE1ZnUiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDEzOjU2OjM1LjU2OSswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--a2c4a469694f0d3cdbac297c73119149659011f42cc64bdf272987276d193a1e/20260115-3294977-zeq5fu)



# 3.脚本指令介绍



1：初始化设置：encoder_enable_pulse_decode()



encoder_enable_pulse_decode(0, 1, 16, 17)



第一个参数：0 表示传送带0 ，1表示传送带1



第二个参数：1 正交，2 升降，3 上升，4 下降



第三个参数：高速IO ，16 表示高速IO 16， 17 表示 高速IO 17



第四个参数：高速IO. 除了 正交模式是 需要配置，其他模式是不需要配置，可以直接设置成0.



停止传送带跟踪： stop_conveyor_tracking()



功能： 该指令用于停止由追踪线性或追踪圆形触发的传送带跟踪功能



追踪圆形传送带：track_conveyor_circular(center, ticks_per_revolution, rotate_tool=False, encoder_index =0)



参数：



center：姿态矢量，用于确定机器人基座坐标系中传送带的中心位置，list型数据；



ticks_per_revolution：传送带移动一圈时编码器变化的刻度数，foat型数据；rotate_tool：工具应当与传送带一起旋转，或者停留在轨迹（movel()等）规定的方位。不指定布尔值时，使用默认布尔值为False，boolean型数据（可选参数）；encoder_index：与传送带跟踪相联系的编码器序号，序号值必须为0或者1。不指定序号值时，使用默认序号值为0，integer型数据（可选参数）。



功能： 该指令用于使机器人运动（movej() 等）追踪圆形传送带



2：追踪线性传送带： track_conveyor_linear(direction, ticks_per_meter, encoder_index=0)



参数：



direction：姿态矢量，用于确定机器人基座坐标系中传送带的方向，list型数据；ticks_per_meter：传送带移动一米时编码器变化的刻度数，foat型数据；encoder_index：与传送带跟踪相联系的编码器序号，序号值必须为0或者1。不指定序号值时，使用默认序号值为0，integer型数据（可选参数）。



功能： 该指令用于使机器人运动（movej() 等）追踪线性传送带。



![](/cs/-/dam/assets/organization_78ncz3z--main-version/eyJfcmFpbHMiOnsiZGF0YSI6eyJpZCI6MjQ0NDYzLCJwYXRoIjoiMjAyNjAxMTUtMzM3NjEyMy1pamJiaXIiLCJ0aW1lc3RhbXAiOiIyMDI2LTAxLTE1VDEzOjU2OjM1LjY5MCswODowMCIsInRva2VuIjoiIn0sImV4cCI6IjIwMjYtMDgtMDlUMTU6NTk6NTkuOTk5WiIsInB1ciI6Im9yZ2FuaXphdGlvbl83OG5jejN6LS1tYWluLXZlcnNpb24ifX0--cf7333aa96e8e07b0240d52b6d0d181d4b045fc7a88d66ff6c255a33983f04a8/20260115-3376123-ijbbir)



**前3个数组是不是代表着xyz。+1代表正方向，-1代表反方向，后三位是补零，都是0就行。



3：获取编码器滴答计数：encoder_get_tick_count(encoder_index)



参数：



该指令用于返回选定编码器的嘀嗒计数。



encoder_index：被访问的编码器序号，序号值必须是0或者1，integer型数据。foat型数据，传送带编码器的嘀嗒计数。



功能： 该指令用于返回选定编码器的嘀嗒计数。



# 4.示列



```
#增量式
def unnamed():
  encoder_enable_pulse_decode(0, 1, 16, 17)
  def start_conveyor_tracking0():
    #线性
    track_conveyor_linear([1.0,0.0,0.0,0.0,0.0,0.0],2000, 0)
    #圆形
    #track_conveyor_circular([0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 222, False, 0)
  end
  # 跟踪: 传送带 0
  start_conveyor_tracking0()
  movej(xxxx)
  
 # movej(xxxx)
  stop_conveyor_tracking()
end
```
