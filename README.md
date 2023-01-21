

# CUIT_XiaoXingCampus_QQBot

## 1 版本更新

### V 1.0

- 实现了整体框架
- 实现了基本的消息转发功能
  - **私聊消息** 可以参考 nonebot_plugin_smart_reply
  - **转发消息** 可参考插件商店的 nonebot_plugin_forwarder 转发姬插件

![image-example](assets/example.jpg)

### V 1.1

- 修改发布人的信息展示方式

  ```
  20.菜鸟裹裹查
  来源：发发[1315000000]
  ```

### V 2.0

- 使用```GitHub```托管代码

- 修改发布人的信息展示方式

  ```
  提交来源：xxxxxx
  提交QQ：xxxx
  ```

- 添加回复与艾特功能

  - 转发时将发送消息中**回messageID**，即添加回复的源信息

    ```python
    # 发送消息
    回111，太强了
    
    # 转发消息
    112.回111，太强了
    --------------------
    111.我是废物
    --------------------
    提交来源：阿巴阿巴
    提交QQ：123456789
    ```

  - 转发时将发送消息中的**艾特messageID**更改为**@nickname**

    ```python
    # 发送消息
    你好强啊艾特111，太强了
    
    # 转发消息
    112.你好强啊 @发发 ，太强了
    --------------------
    提交来源：阿巴阿巴
    提交QQ：123456789
    ```

- 添加消息撤回功能

  撤回发送给小杏的消息，小杏会撤回群里面的消息

- 发送群文件功能

  给小杏发送文件，小杏会发送到群文件

- 添加帮助功能

  给小杏发送关键词**帮助**，小杏会回复帮助信息，关于机器人的功能点与```GitHub```地址

### V 3.0

> 待完善 等我学sql

- 使用```sql```本地化数据
- 可自定义昵称

## 2 安装

https://www.bilibili.com/video/BV1aZ4y1f7e2

### 2.1 依赖库

- https://github.com/mrs4s/go-cqhttp/releases

- ```linux```可能要单独安装下面这个

  pip install nonebot-adapter-onebot

### 2.2 备忘记录

> 快跑 这个甲方不懂技术 预算低

- 选择 反向 Websocket 通信

- config.yml

  - uin: xxxx # QQ账号
  - 端口
    - universal: ws://your_websocket_universal.server   ->   ws://127.0.0.1:27182/onebot/v11/ws/   (10000-60000随机数)

- 登录不畅可删除 session.token

- 之后运行都是.bat文件

- 打开 windows Powershell

  - nb create
  - src
  - echo
  - v11

- .env 改成 prod

- .env.prod

  ```json
  # 好像这里面一定要双引号
  HOST=127.0.0.1  # 主机名
  PORT=27182  # 监听的端口
  # SUPERUSERS=["123456"]  # 超级用户
  NICKNAME=["小杏"]  # 机器人昵称
  COMMAND_START=["/"]  # 命令起始字符   "" 会把所有都视为命令
  # COMMAND_SEP=["."]  # 命令分割符 一般不用
  ```

- 运行 bot.py 与 go-cqhttp.bat 文件即可

- ```screen```基本操作

  退出screen

  ```
  Ctrl+A+D
  ```

  创建screen

  ```
  screen -R name
  ```

  进入screen

  ```
  screen -r name
  ```

