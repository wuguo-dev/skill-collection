# vscode编写程序

URL: https://docs.elibot.cn/cs/fd2cf/0ab86/d763a
发布时间: 2026-01-15

# 1. 简介



通过 VS Code 编辑器实现机器人脚本的高效开发，支持脚本文件直接下发至机器人控制系统，替代传统 U 盘拷贝方式，简化部署流程，提高调试效率



# 2. 操作流程



## 2.1.软件插件下载安装



VS Code 软件官网下载安装https://code.visualstudio.com/



插件清单：



中文汉化包-Chinese (Simplified) Language Pack for Visual Studio Code



ELITE CS Script插件



SFTP



(Ctrl+shift+X)打开扩展，搜索并安装以下插件包。重启VSCode



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_653502_PT0j5Jwh6yYEn3HM_1735882513?w=1099&h=511&type=image/png)



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_822122_3N_3E98r0MOgTR_G_1715327139?w=1334&h=600&type=image/png)



## 2.2.配置端口



### 2.2.1.sftp使用



配置SFTP：配置SFTP参数，必须建立一个文件夹，在该文件夹下配置的参数只对该文件夹生效打开vscode命令面板(CTRL+SHIFT+P)，输入SFTP：config 配置参数输入



### 2.2.2.SFTP：List打开远端设备对应配置路径的列表



步骤：首先创建新文件夹命名WorkSpace – 右击文件夹选择通过code打开



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_344760_qZ80T6CbzHBG4q3o_1715328904?w=341&h=336&type=image/png)



打开vscode命令面板(CTRL+SHIFT+P)，输入SFTP：config 配置参数输入。并将下面参数复制到参数栏。



```
{
    "name": "My Server",
    "host": "192.168.1.200",
    "protocol": "sftp",
    "port": 22,
    "username": "root",
    "password": "elibot",
    "remotePath": "/home/elite/user/program",
    "uploadOnSave": true
}

```



## 2.3.下载或者上传文件



注意：需保证当前文件夹下有创建的SFTP配置文件夹



步骤：安装插件后点击右上角新建文本文件



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_496306_lQjgpB31Ms3HuERx_1715328298?w=376&h=318&type=image/png)



点击选择语言



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_459056_icDy1frr3QggC6hj_1715328373?w=1110&h=407&type=image/png)



注：URScript中，关键字需要使用end结尾，例如以下代码



```
def test11():
    while i < 10:
      
    end
 
end

```



在艾利特CS机器人中，可以使用原生python格式，即以上代码的end均可不写。但需注意代码的缩进格式



```
def test11():
    while i < 10:
        #### comment 

```



## 2.4.从电脑下载到远端设备



修改后保存即可自动下载（或使用快捷键ctrl+s保存），保存后左下角显示字样 done 文件名称 即成功



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_211789_qLuAUDase2ndzs2y_1715329643?w=620&h=94&type=image/png)



右击下载点击upload file进行下载，保存后左下角显示字样 done 文件名称 即成功



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_76592_xYN_67TN6R_qO3x4_1715329736?w=532&h=642&type=image/png)



## 2.5.从远端设备上传至电脑



步骤：首先右击文件打开



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_987634_NNi81DlItG2pBT3q_1715329173?w=186&h=270&type=image/png)



并打开并输入快捷键ctrl+shift+p打开命令行，输入sftp：list，选择对应ip地址，以及文件夹，选择对应文件



## 2.6.使用侧边栏打开



点击侧边栏，打开对应文件夹，上载既可



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_824911_znL8BVdS70-9K4v7_1715329937?w=419&h=421&type=image/png)



上载后找到你想要的文件右击进行下载即可



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_559780_NwWrW04s1zEa3Drp_1718602975?w=665&h=794&type=image/png)



# 3. 常见问题解答



![](https://wdcdn.qpic.cn/MTY4ODg1NDU2ODQwNTgzOQ_363946_CIe1paO6GPmDembW_1717392217?w=762&h=161&type=image/png)



如出现上述报警，有可能是电脑ip不对，以及sftp参数设置不对



#
