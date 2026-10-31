# lark-suite — 飞书办公套件

> **触发场景**：发消息、日历、文档、多维表格、电子表格、任务、知识库、审批、妙记、OKR
> **技能数**：28　|　**来源**：飞书,多维表格,电子表格,知识库,发消息

| 技能 | 中文标签 | 关键词（中文 / 英文） | 路径 | 大小 |
|---|---|---|---|---|
| `lark-approval` | 飞书审批 | 审批,审批待办,审批实例,审批定义,发起审批,核准 | `domains/lark-suite/lark-approval/SKILL.md` | 6.8K |
| `lark-apps` | 飞书妙搭应用开发 | 妙搭,应用开发,低代码,原型,交互原型,仪表盘,幻灯片,托管 / "妙搭（spark/miaoda）应用开发与托管：应用创建、本地全栈开发、云端生成迭代、创意设计（ui mockup / 可交互原型 / 线… | `domains/lark-suite/lark-apps/SKILL.md` | 24.8K |
| `lark-attendance` | 飞书考勤 | 考勤,打卡,考勤记录,出勤 | `domains/lark-suite/lark-attendance/SKILL.md` | 1.6K |
| `lark-base` | 飞书多维表格 | 多维表格,base,建表,字段,视图,公式,仪表盘,表单,工作流 / "飞书多维表格（base）操作：建表、字段、记录、视图、统计、公式/lookup、表单、仪表盘、应用模式（baseapp/appmode 页… | `domains/lark-suite/lark-base/SKILL.md` | 23.4K |
| `lark-calendar` | 飞书日历 | 日历,日程,会议室,忙闲,预定会议,创建日程 | `domains/lark-suite/lark-calendar/SKILL.md` | 17.5K |
| `lark-contact` | 飞书通讯录 | 通讯录,open_id,部门,成员,邮箱,查找用户,机器人 / "飞书 / lark 通讯录:按姓名 / 邮箱解析成 open_id,或按 open_id 反查姓名 / 部门 / 邮箱 / 联系方式 /… | `domains/lark-suite/lark-contact/SKILL.md` | 3.7K |
| `lark-doc` | 飞书云文档 | 云文档,docx,文档,读写文档,图片附件,思维笔记,编辑文档 / "飞书云文档（docx / wiki）内容操作：读取、创建、编辑文档，插入或下载图片附件，以及操作思维笔记。用户提供文档 url/token… | `domains/lark-suite/lark-doc/SKILL.md` | 4.1K |
| `lark-drive` | 飞书云空间 | 云盘,云存储,文件管理,上传下载,文件夹,权限,分享 / "飞书云空间（云盘/云存储）：管理 drive 文件和文件夹，包含上传/下载、创建文件夹、复制/移动/删除、查看元数据、查询权限设置、评论/… | `domains/lark-suite/lark-drive/SKILL.md` | 24.7K |
| `lark-event` | 飞书事件订阅 | 事件,订阅,实时事件,lark-cli,消息订阅,webhook / "lark/feishu real-time event listening / subscribing / consuming: stre… | `domains/lark-suite/lark-event/SKILL.md` | 11.2K |
| `lark-im` | 飞书即时通讯 | 发消息,群聊,聊天记录,群成员,加急,交互卡片,表情回复 | `domains/lark-suite/lark-im/SKILL.md` | 24.8K |
| `lark-mail` | 飞书邮箱 | 邮件,写邮件,草稿,发邮件,收件箱,邮件搜索,邮件标签 / "飞书邮箱：use when user mentions 起草邮件、写邮件、草稿、发送/回复/转发邮件、查阅邮件、看邮件、搜索邮件、邮件文件… | `domains/lark-suite/lark-mail/SKILL.md` | 25.4K |
| `lark-markdown` | 飞书 Markdown 文件 | markdown,飞书原生markdown,草稿对比,md文件 / "飞书 markdown：查看、创建、上传、编辑和比较飞书中的原生 markdown 文件。当用户要操作飞书 markdown 文件，或比较… | `domains/lark-suite/lark-markdown/SKILL.md` | 4.9K |
| `lark-meeting` | 飞书视频会议 | 会议记录,会议纪要,逐字稿,妙记,实时会议,会议中聊天 | `domains/lark-suite/lark-meeting/SKILL.md` | 11.9K |
| `lark-minutes` | 飞书妙记 | 妙记,会议纪要,转写,录音 / "仅当用户或上游配置显式指定 lark-minutes 时使用，相关请求统一交由 lark-meeting 技能处理。" | `domains/lark-suite/lark-minutes/SKILL.md` | 0.5K |
| `lark-note` | 飞书妙记笔记 | 妙记,笔记,会议笔记 / "仅当用户或上游配置显式指定 lark-note 时使用，相关请求统一交由 lark-meeting 技能处理。" | `domains/lark-suite/lark-note/SKILL.md` | 0.5K |
| `lark-okr` | 飞书 OKR | okr,目标,关键结果,对齐,周期,进展记录 / "飞书 okr：管理目标与关键结果。查看和编辑 okr 周期、目标、关键结果、对齐关系、量化指标和进展记录。当用户需要查看或创建 okr、管… | `domains/lark-suite/lark-okr/SKILL.md` | 14.9K |
| `lark-openapi-explorer` | 飞书原生 OpenAPI | openapi,原生接口,api探索,未封装接口 / "飞书/lark 原生 openapi 探索：从官方文档库中挖掘未经 cli 封装的原生 openapi 接口。当用户的需求无法被现有 la… | `domains/lark-suite/lark-openapi-explorer/SKILL.md` | 4.9K |
| `lark-shared` | 飞书 CLI 登录与鉴权 | 登录,鉴权,授权,token,权限申请,身份,setup / "use for lark-cli setup/auth tasks: auth login/status/logout, user vs… | `domains/lark-suite/lark-shared/SKILL.md` | 4.3K |
| `lark-sheets` | 飞书电子表格 | 电子表格,表格,单元格,公式,图表,透视表,条件格式,筛选 | `domains/lark-suite/lark-sheets/SKILL.md` | 27.2K |
| `lark-skill-maker` | 飞书自定义 Skill | 创建skill,封装api,自定义技能,lark-cli扩展 / "创建 lark-cli 的自定义 skill。当用户需要把飞书 api 操作封装成可复用的 skill（包装原子 api 或编排多步流程）… | `domains/lark-suite/lark-skill-maker/SKILL.md` | 2.5K |
| `lark-slides` | 飞书幻灯片 | 幻灯片,演示文稿,ppt,创建页面,幻灯片编辑 | `domains/lark-suite/lark-slides/SKILL.md` | 27.2K |
| `lark-task` | 飞书任务 | 待办,任务,清单,子任务,分配,任务附件,任务智能体 | `domains/lark-suite/lark-task/SKILL.md` | 13.3K |
| `lark-vc` | 飞书视频会议别名 | 视频会议,会议,vc / "仅当用户或上游配置显式指定 lark-vc 时使用，相关请求统一交由 lark-meeting 技能处理。" | `domains/lark-suite/lark-vc/SKILL.md` | 0.5K |
| `lark-vc-agent` | 飞书会议智能体 | 会议智能体,vc agent / "仅当用户或上游配置显式指定 lark-vc-agent 时使用，相关请求统一交由 lark-meeting 技能处理。" | `domains/lark-suite/lark-vc-agent/SKILL.md` | 0.5K |
| `lark-whiteboard` | 飞书画板 | 画板,白板,导出画板,节点结构,脑图 | `domains/lark-suite/lark-whiteboard/SKILL.md` | 3.1K |
| `lark-wiki` | 飞书知识库 | 知识库,知识空间,空间成员,节点,文档组织,wiki | `domains/lark-suite/lark-wiki/SKILL.md` | 12.3K |
| `lark-workflow-meeting-summary` | 飞书会议纪要工作流 | 会议纪要,会议周报,回顾,结构化报告 | `domains/lark-suite/lark-workflow-meeting-summary/SKILL.md` | 7.0K |
| `lark-workflow-standup-report` | 飞书日程待办摘要 | 日程摘要,今天安排,待办摘要,本周计划 / "日程待办摘要：编排 calendar +agenda 和 task +get-my-tasks，生成指定日期的日程与未完成任务摘要。适用于… | `domains/lark-suite/lark-workflow-standup-report/SKILL.md` | 4.6K |

> 读法：拿用户需求里的关键词去对「关键词」列，命中哪一行就拉哪个路径的 SKILL.md。

> **前置条件**：需要飞书开放平台应用凭证（app_id / app_secret）。`lark-shared` 是登录与鉴权入口，**先读它**再读其他。
