<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ba-tools

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/hanasa2023/nonebot-plugin-ba-tools.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-ba-tools">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-ba-tools.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
</div>

## 📖 介绍

目标是做 BlueArchive 最好用的工具箱

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-ba-tools

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-ba-tools

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_ba_tools"]

</details>

## 🎉 使用

### 💡 资源文件

本项目在 [Schale DB]() 的基础上新增了 l2d 文件夹，请在 release 中下载相应文件并解压至相应目录下

- 默认路径为项目根目录
- 如需更改资源文件路径，请自行更改插件配置中的`asserts_path`属性

### ✨ 功能介绍

- [x] 每日 00:00 在以订阅的群聊中自动推送学生生日信息
- [ ] 获取当月过生日的学生列表
- [ ] 获取学生详细信息
- [ ] 获取活动列表
