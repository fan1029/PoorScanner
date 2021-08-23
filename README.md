# PoorScanner使用说明书

![](https://img.shields.io/badge/Version-1.0.1%20Beta-yellow)
![](https://img.shields.io/badge/Date-2021--8--22-blue)
[![图片名称](https://img.shields.io/badge/%E5%8F%8D%E9%A6%88-%E7%82%B9%E6%88%91-brightgreen)](https://github.com/fan1029/PoorScanner/issues/new)

-工具在不同环境下可能不怎么稳定，如果有什么问题恳请大家反馈。说明书有什么错误的地方也大家欢迎指正。

## 更新记录 2021.8.23

**修复了云函数主程序 gitee上传文件接口写错了的BUG（之前把自己的上传地址写死进去了，没从配置文件里读）**

**更新了说明书**


PoorScanner是一款依托腾讯云serverless云函数服务的目录扫描器，由于腾讯云云函数每次网络请求会有不同的出网IP(大概三四十个) 可以依靠此特性来实现简单的扫目录防封功能。适用于扫描中小型字典，不想花钱买代理的用户。(球球给孩子颗星星吧)

![QQ截图20210822220928.png](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/QQ%E6%88%AA%E5%9B%BE20210822220928.png)

## 使用

服务端环境 python 3.6 

客户端环境 python 3.8（三点几的都应该可以）

需要安装的依赖

客户端：

```java
pip install requests
pip install colorama
pip install tencentcloud-sdk-python
```

服务端：

服务端各依赖已经打包好，直接上传就行。这边只是说明下。

```java
aiohttp
```

使用说明

```java
python poorscanner.py -h    //获取帮助信息
```

e.g

```java
python poorscanner.py -u http://www.baidu.com/
python poorscanner.py -u http://www.baidu.com/ -d php.txt  自定义字典(需放在dictionary目录下)
python poorscanner.py -u http://www.baidu.com/ -s 60    自定义速度
python poorscanner.py -u http://www.baidu.com/  -t hidden 隐蔽扫描

```

```java
-h, --help            show this help message and exit
  -u U                  输入扫描的目标 e.g http://www.baidu.com/
  -d D                  输入要使用的自定义字典名(请放在dictionary目录下)
  -s S                  扫描速度
  -m M                  请求方式 head(这个快点) get 默认为get
  -t T                  模式默认为普通模式扫描 传参为hidden为隐蔽扫描
  -cut_times CUT_TIMES  隐蔽扫描模式下使用，讲字典切割的片段数，默认为 10个
  -wait_time WAIT_TIME  每个片段扫描完成后延时的时间默，认为60S
  --getid GETID         获取requestID的报告 (占坑 这个没写好懒得删了)
```

注意：

- 扫描速度为并发的协程数 默认为30 意思时可以同时异步执行请求的数量网站封的严就慢点平时没事扫可以调高点 100啥的
- url请使用标准点的格式  [http://www.baidu.com/](http://www.baidu.com/)
- 扫描用的字典需要放在dictionary目录下面，自定义使用字典时只要输入文件名就行了
- 默认字典为Dirsearch的默认字典
- 如果指定head方式扫描速度会快 不过如果有些站不支持的这请求方式就会报错
- **轮询时会在那边等待云函数结果，没加进度条 放那边等吧，如果长时间没结果可以去腾讯云函数日志模块下看看报错原因**

### 扫描模式

-t 指定扫描模式  

- normal 正常模式  字典长度过大会自动拆分分批发送
- hidden 隐蔽模式（我也不知道有没有用） 这个就是按照要求把一个字典分成好多个小字典 然后间隔指定时间发送 只有第一个小字典扫完以后才会第二个小字典。使用时如果不指定cut_times 和wait_time 默认时切分10个小字典 每个扫完等一分钟

## 环境部署

### 创建云函数

腾讯云搜索云函数

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled.png)

进去以后新建个python空白模板，不要点一键创建

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%201.png)

点击高级配置勾选异步执行，然后再改执行超时时间，内存可以稍微调高点。然后chuang

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%202.png)

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%203.png)

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%204.png)

解压server.zip文件 点击上传文件夹，上传server文件夹（点上传zip会出错我也不知道为啥），然后点击部署。

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%205.png)

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%206.png)

### 填写配置文件

```java
config.ini 客户端
[Server]
id=腾讯云的API密钥 SecretId
key=腾讯云的API密钥 SecretKey
function_name=poorscanner  创建的云函数的名字
reigon=ap-shanghai   创建的云函数地区

[Gitee]
owner=Gitee用户的名字
repo=创建的项目名子（用来中转扫描结果）
brach=master（分支）

[Dir]
cut_size=100000 （普通模式扫描时单次扫描字典最大长度上限）
cycle_time=15（结果轮询周期）

```

```java
server.ini 服务端的
[Gitee]
access_token= GITEE的私人令牌
owner=同上
repo=同上
```

- 腾讯云的密钥请在账号中心→访问管理→访问密钥处生成

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%207.png)

- 你需要创建一个gitee用户 并且创建一个项目用来中转扫描结果（腾讯云的云函数日志功能太拉了没办法。。。。）

注意 用户名是@后面的那个不要填错

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%208.png)

创建个仓库

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%209.png)

看见上面的仓库地址了吗？

[https://gitee.com/maple_10101/](https://gitee.com/maple_10101/mapletest)poorscanner

maple_10101对应owner

poorscanner 对应配置文件中的 repo

然后去申请个gitee私人令牌，然后记住令牌，填写在配置文件中。

![Untitled](https://raw.githubusercontent.com/fan1029/PoorScanner/main/IMG/Untitled%2010.png)

**将配置文件填写到客户端服务端的配置文件中就完成了  服务端填写完成后要保存下然后点击部署**
### 配置完成！
