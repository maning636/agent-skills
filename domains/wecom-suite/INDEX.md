# wecom-suite — 企业微信套件

> **触发场景**：企微消息、日程、邮件、文档、表格、待办、通讯录、微盘、在线会议
> **技能数**：14　|　**来源**：WeComTeam/wecom-cli

| 技能 | 中文标签 | 关键词（中文 / 英文） | 路径 | 大小 |
|---|---|---|---|---|
| `wecomcli-calendar` | 企微日程 | 日程,会议室,预约,忙闲,取消日程,企微会议 | `domains/wecom-suite/wecomcli-calendar/SKILL.md` | 29.1K |
| `wecomcli-contact` | 企微通讯录 | 通讯录,人员搜索,userid,部门,职务,同名人员 / 使用 wecom-cli 按姓名、拼音、英文名或别名搜索企业微信通讯录中的人员，并查询匹配人员的 userid、部门和职务。适用于查找联系人… | `domains/wecom-suite/wecomcli-contact/SKILL.md` | 3.4K |
| `wecomcli-disk` | 企微微盘 | 微盘,网盘,文件上传下载,共享空间,文件夹,重命名 / 企业微信微盘（disk / 网盘）文件操作技能。承接"微盘 / 网盘"里的文件列出、搜索、读取元信息、上传、下载、重命名、新建文件夹操作。用… | `domains/wecom-suite/wecomcli-disk/SKILL.md` | 27.5K |
| `wecomcli-doc` | 企微在线文档 | 在线文档,docx,新建文档,导入文档,追加内容,覆盖写入 / 企微 doc 内容操作技能，包含新建在线文档、导入、读取、追加、覆盖写入等功能。仅当用户明确指定 'doc'、'docx'、'word'、'… | `domains/wecom-suite/wecomcli-doc/SKILL.md` | 7.1K |
| `wecomcli-doc-manage` | 企微文档管理 | 文档搜索,最近浏览,文档改名,成员权限,加入规则 / 企业微信文档公共管理：搜索文档（最近浏览/创建）、文档改名、添加文档成员权限、设置文档加入规则。适用于所有文档类型（doc文档 / 在线表格… | `domains/wecom-suite/wecomcli-doc-manage/SKILL.md` | 11.1K |
| `wecomcli-email` | 企微邮箱 | 企业微信邮件,收发邮件,邮件搜索,邮件详情,附件 | `domains/wecom-suite/wecomcli-email/SKILL.md` | 13.3K |
| `wecomcli-media` | 企微媒体文件 | media_id,媒体下载,媒体上传,素材落地 / 企业微信媒体文件上传/下载技能。承接基于 media_id 下载媒体文件到本地，以及上传本地文件获取 media_id 两类操作。当其他技能… | `domains/wecom-suite/wecomcli-media/SKILL.md` | 5.3K |
| `wecomcli-meeting` | 企微在线会议 | 在线会议,会议号,入会链接,会议纪要,转写,发起会议 | `domains/wecom-suite/wecomcli-meeting/SKILL.md` | 36.2K |
| `wecomcli-message` | 企微消息发送 | 发消息,群聊通知,发图片,发文件,发语音,会话列表 / 查询当前可以发送消息的聊天会话范围，并向会话列表中的单聊或群聊发送文本、markdown、图片、文件、语音、视频消息。用户要求“给某人发消息… | `domains/wecom-suite/wecomcli-message/SKILL.md` | 8.1K |
| `wecomcli-shared` | 企微 CLI 前置检查 | wecom-cli,前置检查,机器人身份,授权,版本校验 / wecom-cli 业务技能的公共前置检查、获取机器人及授权真人身份，以及通用输出约束。任何 wecomcli-* 技能准备执行 wecom… | `domains/wecom-suite/wecomcli-shared/SKILL.md` | 4.5K |
| `wecomcli-sheet` | 企微在线表格 | 在线表格,excel表格,导入csv,读取表格,追加行,子表 / 企业微信在线表格文档管理：新建在线表格、导入 csv/excel 为在线表格、读取表格信息与数据、修改表格内容、追加行数据、子表管理。当用户… | `domains/wecom-suite/wecomcli-sheet/SKILL.md` | 7.6K |
| `wecomcli-smartpage` | 企微智能文档 | 智能文档,smartpage,页面树,智能主页,内置表格 / 使用 wecom-cli 创建企业微信智能文档，读取页面内容，调整页面树结构，获取内置智能表格信息。适用于用户明确提到企业微信智能文档、智能… | `domains/wecom-suite/wecomcli-smartpage/SKILL.md` | 12.7K |
| `wecomcli-smartsheet` | 企微智能表格 | 智能表格,表结构,记录管理,字段,视图,图表,样式 / 企业微信智能表格内容操作技能——专注于智能表格（smartsheet）的数据、结构与样式管理：读取表结构与记录、管理子表/字段/记录/视图/… | `domains/wecom-suite/wecomcli-smartsheet/SKILL.md` | 15.2K |
| `wecomcli-todo` | 企微待办 | 待办,创建待办,完成待办,截止时间,参与人 | `domains/wecom-suite/wecomcli-todo/SKILL.md` | 5.2K |

> 读法：拿用户需求里的关键词去对「关键词」列，命中哪一行就拉哪个路径的 SKILL.md。

> **前置条件**：需要企业微信 CLI（`wecom-cli`）与机器人身份。`wecomcli-shared` 是前置检查入口，先读它。
