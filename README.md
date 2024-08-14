<div align="center">

# nonebot-plugin-ba-tools

![NoneBotPluginBaToolsLogo](https://github.com/hanasa2023/nonebot-plugin-ba-tools/blob/main/logo.png)

[![license](https://img.shields.io/github/license/hanasa2023/nonebot-plugin-ba-tools.svg)](./LICENSE)
[![PyPI](https://img.shields.io/pypi/v/nonebot-plugin-ba-tools.svg)](https://pypi.python.org/pypi/nonebot-plugin-ba-tools)
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
- ~~如需更改资源文件路径，请自行更改插件配置中的`asserts_path`属性~~

### ✨ 功能介绍

- [x] 每日 00:00 在以订阅的群聊中自动推送学生生日信息
- [ ] 获取当月过生日的学生列表
- [ ] 获取学生详细信息
- [ ] 获取活动列表

### 🤖 指令表

|     指令      |           权限            | 需要@ |              说明               |            示例             |
| :-----------: | :-----------------------: | :---: | :-----------------------------: | :-------------------------: |
| birthday_info | 管理员/群主以及 SUPERUSER |  无   | 在此群订阅/取消订阅学生生日推送 | /ba_birthday_info on 或 off |

## 👥 参与共建

请加入 QQ 群`991680169`进行交流
