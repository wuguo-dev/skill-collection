# 四点法脚本函数码垛功能

URL: https://docs.elibot.cn/cs/1b89f/bf71f/c79ac
发布时间: 2026-01-13

# **1. 简介**



interpolate_pose() 此指令适用于有规律/等间距的矩阵只需示教四个顶点点位即可完成矩阵取放物料，可以用于外部设备随机发送矩阵取料/放料位置机械手实现矩阵抓取



# **2. 操作流程**



(1) ：指令说明如图2-1



![](https://wdcdn.qpic.cn/MTY4ODg1NzczNDQyNjQyMA_13398_w5WR1durw74iuw4Y_1721750194?w=643&h=654&type=image/png)



（图2-1）



[录制_2024_07_24_00_31_06_90.mp4](https://drive.weixin.qq.com/s?k=AJ0AaActAA0J5j0hBBATQALwZWANU)



(2) 举例：矩阵为3行4列（图2-2）机械手如何走到6号位置



![](https://wdcdn.qpic.cn/MTY4ODg1NzczNDQyNjQyMA_162313_YRH5qUDNcpxPRGen_1721750593?w=452&h=380&type=image/png)



（图2-2）



[录制_2024_07_24_00_52_19_183.mp4](https://drive.weixin.qq.com/s?k=AJ0AaActAA04hOuRMtATQALwZWANU)



（3）：举例：矩阵为3行4列（图2-2）外部设备（PLC）发送2行2列机械手如何走



![](https://wdcdn.qpic.cn/MTY4ODg1NzczNDQyNjQyMA_231212_Y5gEm8-u4T1USqxN_1721790232?w=1281&h=827&type=image/png)



```
lie0=read_input_integer_register(0)
hang0=read_input_integer_register(1)
lie0=lie0-1
hang0=hang0-1
lie0=lie0*0.333
hang0=hang0*0.5
lie1=interpolate_pose(A1,A4,lie0)
lie2=interpolate_pose(A9,A12,lie0)
mi=interpolate_pose(lie1,lie2,hang0)

```



[录制_2024_07_24_10_57_56_582.mp4](https://drive.weixin.qq.com/s?k=AJ0AaActAA0li91L0pATQALwZWANU)



# **3. 常见问题解答**



(1) 注意事项：如一列有11个点位不是用1/11而是1/10因为第一个点是从0开始



(2) 此指令只适用于等间距有规律的矩阵



(3) 本次演示使用默认基座坐标系TCP夹具任意姿态安装 此指令只是用终止点-起始点除以点位间隔无需在意末端姿态



#
