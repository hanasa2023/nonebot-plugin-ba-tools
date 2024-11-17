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

### 💡 数据来源

~~本项目在 [Schale DB](https://github.com/SchaleDB/SchaleDB) 的基础上新增了 l2d 文件夹，请在 release 中下载相应文件并解压至相应目录下~~ v0.1.6 已实现网络请求资源文件，无需再自行配置资源文件

- 资源文件请求详见 [Ba Tools Api](https://api.hanasaki.tech)

- 默认路径为项目缓存路径，使用[nonebot_plugin_localstore](https://github.com/nonebot/plugin-localstore)进行管理，你可以使用`nb localsotre`查看默认缓存路径

- [AronaBot](https://tutorial.arona.diyigemt.com/home)

- 涩图功能使用[自建pixiv数据库](https://github.com/hanasa2023/ba-image-db)

#### 插件配置

🔧 请在你的 bot 根目录下的`.env` `.env.*`中添加以下字段

|      字段      | 类型 |        默认值        |   可选值   |            描述            |
| :------------: | :--: | :------------------: | :--------: | :------------------------: |
| LOADING_SWITCH | bool |        false         | true/false |    是否开启图片加载通知    |
| BA_MAX_PIC_NUM | int  |          10          |     -      |   单次最多发送的图片数量   |
|  PIXIV_NGINX   | str  | "https://i.pixiv.re" |     -      |       pixiv图床反代        |
| SEND_PIC_INFO  | bool |        false         | true/false | 发送涩图是是否发送图片信息 |
|   R18_SWITCH   | bool |        false         | true/false |     r18开关，防爆按钮      |

### ✨ 功能介绍

- [x] 每日 00:00 在以订阅的群聊中自动推送学生生日信息
- [x] 获取当月过生日的学生列表
- [ ] 获取学生详细信息
- [x] 获取活动列表
- [x] 获取 ba 千里眼
- [x] 获取攻略(关卡攻略/总力战攻略/大决战攻略/竞技场攻略/火力演习攻略)
- [ ] 好感度计算
- [x] 获取/抽取 ba 漫画(目前只能获取到（二创？）漫画，将来可能会支持更多的漫画)
- [ ] 获取 ba 表情包
- [x] 自动推送总力战/大决战信息 ~~基于 bilibili 动态~~（目前只做了日服）⚠️api接口似乎发生了变动，该功能可能暂时无法使用
- [x] 获取 ba 涩图（基于自建的数据库）
- [x] 获取 ba meme（基于自建的图库，质量尽可能高了）
- [x] 获取ba人权
- [x] 获取ba总力战档线

### 🤖 指令表

⚠️ 此处示例中的"/"为 nb 默认的命令开始标志，若您设置了另外的标志，则请使用您设置的标志作为开头

|       指令       |           权限            | 需要@ |                      说明                       |              示例              |
| :--------------: | :-----------------------: | :---: | :---------------------------------------------: | :----------------------------: |
|  ba学生生日订阅  | 管理员/群主以及 SUPERUSER |  无   |         在此群订阅/取消订阅学生生日推送         |  `/ba学生生日订阅 开启/关闭`   |
|   ba总力战订阅   | 管理员/群主以及 SUPERUSER |  无   |      在此群订阅/取消订阅总力战/大决战推送       |   `/ba总力战订阅 开启/关闭`    |
|     ba千里眼     |            无             |  无   |               获取 ba 千里眼信息                |    `/ba千里眼 国服/国际服`     |
|    ba活动一览    |            无             |  无   |                获取 ba 活动信息                 | `/ba活动一览 国服/国际服/日服` |
|      ba攻略      |            无             |  无   |                  获取 ba 攻略                   |  `/ba攻略 关卡2-1/国服大决战`  |
|      ba漫画      |            无             |  无   |              获取 ba（二创？）漫画              |     `/ba漫画 抽取/第104话`     |
|   ba学生生日表   |            无             |  无   |              获取某月的学生生日表               |    `/ba学生生日表 当月/9月`    |
|      ba涩图      |            无             |  无   |         获取 ba 涩图，使用方法详见下方          |  `/ba涩图 num 2`或者`/ba涩图`  |
| ba涩图上传 <pid> |            无             |  无   |        上传涩图至数据库，参数为图片的pid        |    `/ba涩图上传 124081225`     |
|      bameme      |            无             |  无   | 获取 ba meme，参数为要获取的数目，不填默认 1 张 |  `/bameme num 2`或者`/bameme`  |
|    ba角色简评    |            无             |  无   |                  获取角色简评                   |   `/ba角色简评 日服/国际服`    |
|      ba人权      |            无             |  无   |                   获取ba人权                    |     `/ba人权 日服/国际服`      |
|    ba总力档线    |            无             |  无   |                  获取总力档线                   |  `/ba总力档线 日服/官服/b服`   |

- 各指令(不支持所有服的指令)参数可用列表如下

```
ba攻略：关卡<关卡号>/国际服总力/日服总力/国际服大决战/日服大决战/国际服火力演习/日服火力演习/国际服竞技场/日服竞技场
ba人权：国际服/日服
ba总力档线：日服/国服官服/官服/国服B服/国服b服/b服/B服
```

- ba涩图的具体使用方法

|  参数名  |       参数值类型       | 是否必须 | 默认值 |
| :------: | :--------------------: | :------: | :----- |
|   num    |          int           |    否    | 1      |
|   tags   |       list[str]        |    否    | -      |
|   isAI   |          bool          |    否    | false  |
| restrict | Literal["safe", "r18"] |    否    | "safe" |

例：

```
/ba涩图
/ba涩图 num 2 tags [BlueArchive] isAI true restrict safe
/ba涩图 num 2
/ba涩图 tags [小鸟游星野, BlueArchive]
/ba涩图 isAI true restrict r18
```

## 👥 参与共建

请加入 QQ 群`991680169`进行交流

## 🚩 TODO

- [ ] 使用 nonebot-plugin-orm 重构插件数据
