# CUIT_XiaoXingCampus_QQBot

## 1 版本信息

### V 1.0

- 实现了整体框架
- 实现了基本的消息转发功能
- 修改发布人的信息展示方式

### V 2.0

- 使用```GitHub```托管代码

- 修改发布人的信息展示方式

- 发送群文件功能

- 添加帮助功能

  私发 ‘帮助’ 即可获得帮助

### [V 3.0](./版本文档/V3.md)

> 2023-05-11

- 自定义昵称

  私发 Bot ‘昵称：xxx’ 即可更改昵称为 xxx

- 消息撤回

  撤回发给 Bot 的消息 Bot 也会撤回

- 消息回复

  私发 Bot 的消息以 ‘回132’ 开头，Bot 会在群里面回复消息编号为132的消息

- 艾特

  私发 Bot 的消息包含 ‘艾特132’，Bot 会在群里面艾特消息编号为132的发送者

- 使用```sql```本地化数据

### V 4.0

- 修复了艾特的bug
- 数据库更换为MySQL
- 使用`springboot`和`vue-admin-template-master`开发管理端
  - 可以随时更改目标群和黑名单
  - 可调过管理端一键修复等

## 2 学习路线

### 2.1 入门

https://www.bilibili.com/video/BV1aZ4y1f7e2

#### 2.1.1 依赖库

- https://github.com/mrs4s/go-cqhttp/releases

- ```linux```可能要单独安装下面这个

  pip install nonebot-adapter-onebot

- 安装适配器解决

  `pip install nonebot-adapter-onebot`

- 如果还是报这个错，上大招，卸载重装

  ```
  pip uninstall nonebot
  pip uninstall nonebot2
  pip uninstall nb-cli
  pip install nb-cli
  pip install nonebot-adapter-onebot
  ```

#### 2.1.2 备忘记录

> 快跑 这个甲方不懂技术 预算低
>
> 憨憨甲方 GitHub 链接都不准留

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

  ```python
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

### 2.2 文档

- [官方文档](https://nb2.baka.icu/docs/api/index)
- [github大佬](https://github.com/botuniverse/onebot-11)
- [```go-cqhttp```](https://docs.go-cqhttp.org/api)
