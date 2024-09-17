<div align="center">

# nonebot-plugin-ba-tools

![NoneBotPluginBaToolsLogo](./logo.png)

[![license](https://img.shields.io/github/license/hanasa2023/nonebot-plugin-ba-tools.svg)](./LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-ba-tools.svg)](https://pypi.python.org/pypi/nonebot-plugin-ba-tools)
[![NoneBot](https://img.shields.io/badge/nonebot-2.3.0+-red.svg)](https://nonebot.dev)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)

</div>

## 📖 介绍

目标是做 BlueArchive 最好用的工具箱

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>

在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```sh
    nb plugin install nonebot-plugin-ba-tools
```

</details>

<details>
<summary>使用包管理器安装</summary>

在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```sh
  pip install nonebot-plugin-ba-tools
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

```python
    plugins = ["nonebot_plugin_ba_tools"]
```

</details>

## 🎉 使用

### 💡 资源文件

~~本项目在 [Schale DB](https://github.com/SchaleDB/SchaleDB) 的基础上新增了 l2d 文件夹，请在 release 中下载相应文件并解压至相应目录下~~ v0.1.6 已实现网络请求资源文件，无需再自行配置资源文件

- 资源文件请求详见 [Ba Tools Api](https://api.hanasaki.tech)

- ~~默认路径为项目缓存路径，使用[nonebot_plugin_localstore](https://github.com/nonebot/plugin-localstore)进行管理，你可以使用`nb localsotre`查看默认缓存路径~~

#### 插件配置

🔧 请在你的 bot 根目录下的`.env` `.env.*`中添加以下字段

|      字段      | 默认值 |   可选值   |         描述         |
| :------------: | :----: | :--------: | :------------------: |
| LOADING_SWITCH | false  | true/false | 是否开启图片加载通知 |

### ✨ 功能介绍

- [x] 每日 00:00 在以订阅的群聊中自动推送学生生日信息
- [x] 获取当月过生日的学生列表
- [ ] 获取学生详细信息
- [x] 获取活动列表
- [x] 获取 ba 千里眼
- [x] 获取关卡攻略
- [ ] 好感度计算
- [x] 获取/抽取 ba 漫画(目前只能获取到（二创？）漫画，将来可能会支持更多的漫画)
- [ ] 获取 ba 表情包
- [ ] 自动推送总力战/大决战信息 ~~基于 bilibili 动态~~（目前只做了国际服）

### 🤖 指令表

⚠️ 此处示例中的"/"为 nb 默认的命令开始标志，若您设置了另外的标志，则请使用您设置的标志作为开头

|      指令       |           权限            | 需要@ |                 说明                 |             示例              |
| :-------------: | :-----------------------: | :---: | :----------------------------------: | :---------------------------: |
| ba 学生生日订阅 | 管理员/群主以及 SUPERUSER |  无   |   在此群订阅/取消订阅学生生日推送    |  /ba 学生生日订阅 开启/关闭   |
|  ba 总力战订阅  | 管理员/群主以及 SUPERUSER |  无   | 在此群订阅/取消订阅总力战/大决战推送 |   /ba 总力战订阅 开启/关闭    |
|    ba 千里眼    |            无             |  无   |          获取 ba 千里眼信息          |    /ba 千里眼 国服/国际服     |
|   ba 活动一览   |            无             |  无   |           获取 ba 活动信息           | /ba 活动一览 国服/国际服/日服 |
|   ba 关卡攻略   |            无             |  无   |           获取 ba 关卡攻略           |      /ba 关卡攻略 H25-1       |
|     ba 漫画     |            无             |  无   |        获取 ba（二创？）漫画         |    /ba 漫画 抽取/第 104 话    |
|  ba 学生生日表  |            无             |  无   |         获取某月的学生生日表         |   /ba 学生生日表 当月/9 月    |

## 👥 参与共建

请加入 QQ 群`991680169`进行交流

# 🧐 TODO

- [ ] 使用 nonebot-plugin-orm 重构插件数据
