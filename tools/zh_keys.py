# -*- coding: utf-8 -*-
"""每个技能的中文标签 + 中文关键词 —— 由 gen_zh_keys.py 自动生成，请勿手工编辑。
手工维护请改 curated_zh.py，然后重跑 python tools/gen_zh_keys.py
"""

ZH = {

# ---- agent-toolkit ----
"agent-toolkit/agent-reach": ("Agent 触达能力", "联网能力,触达,agent reach,获取信息渠道"),
"agent-toolkit/calibrate": ("校准", "校准,置信度校准,自检,结果校准,calibration"),
"agent-toolkit/cognitive-guard": ("认知防护", "认知偏差,防护,思维陷阱,避免误导,cognitive guard"),
"agent-toolkit/computer-use": ("电脑操作", "操作电脑,鼠标键盘,截图操作,ui自动化,computer use"),
"agent-toolkit/find-skills": ("技能发现", "找技能,skill发现,技能搜索,有什么技能,安装技能,怎么装技能,装技能,技能列表"),
"agent-toolkit/gidlin-law": ("吉德林法则顾问", "1) 用户说帮我理清思路,我很迷茫,我说不清楚问题在哪,吉德林,情绪和事实交织,第一性原理,私董会）之前需要先定义问题"),
"agent-toolkit/minimax": ("MiniMax 能力", "minimax,海螺,音视频,多模态,minimax模型"),
"agent-toolkit/officecli": ("Office 文档处理", "word,excel,ppt,office文档,表格处理,文档分析"),
"agent-toolkit/optimize-skill-md": ("按照《Skills MD 标准书写格式》", "优化SKILL.md,改进skill,标准化skill格式,skill格式检查,skill优化,需要优化"),
"agent-toolkit/orca-cli": ("Orca CLI", "orca,截图工具,界面识别,视觉定位,cli"),
"agent-toolkit/release-skills": ("技能发布", "发布技能,打包技能,技能分发,release"),
"agent-toolkit/sandcastle-verify": ("沙盒校验", "沙盒,验证环境,试运行,沙盒测试,sandbox"),
"agent-toolkit/skill-update": ("技能更新", "更新技能,升级skill,同步上游,skill更新"),
"agent-toolkit/slidecraft": ("幻灯片精修", "幻灯片打磨,ppt美化,版式调整,slidecraft"),
"agent-toolkit/tweak": ("微调优化", "微调,微调代码,小改,调参,tweak"),

# ---- cowork-plugin-management ----
"cowork-plugin-management/cowork-plugin-customizer": ("定制组织插件", "定制插件,组织适配,改插件,接mcp"),
"cowork-plugin-management/create-cowork-plugin": ("从零建插件", "创建插件,新建插件,插件脚手架"),

# ---- customer-support ----
"customer-support/customer-escalation": ("升级处理", "客诉升级,升级工单,打包上报"),
"customer-support/customer-research": ("客户问题调研", "客户问题研究,多源调研,溯源"),
"customer-support/draft-response": ("客服回复起草", "回复客户,客服话术,答复草稿"),
"customer-support/kb-article": ("知识库文章", "知识库,自助文档,faq,沉淀文章"),
"customer-support/ticket-triage": ("工单分级", "工单,问题分级,优先级,分诊"),

# ---- data ----
"data/analyze": ("数据分析", "数据问题,分析问题,洞察,算指标"),
"data/build-dashboard": ("交互式仪表盘", "仪表盘,dashboard,看板,交互式报表"),
"data/create-viz": ("数据可视化", "图表,画图,matplotlib,seaborn,可视化"),
"data/data-context-extractor": ("数据隐性知识提取", "数据字典,隐性知识,分析师访谈,口径沉淀"),
"data/data-visualization": ("图表设计", "图表选型,可视化方案,图表规范"),
"data/explore-data": ("数据探查", "数据剖析,数据质量,字段分布,缺失值,摸底"),
"data/sql-queries": ("多方言 SQL", "sql方言,snowflake,bigquery,databricks,数仓"),
"data/statistical-analysis": ("统计分析", "统计,假设检验,离群点,趋势分析,显著性"),
"data/validate-data": ("数据校验", "数据校验,口径核对,偏差检查,准确性"),
"data/write-query": ("SQL 编写", "sql,写查询,取数,数仓查询"),

# ---- design ----
"design/accessibility-review": ("无障碍审计", "无障碍,a11y,wcag,读屏,适老化,可访问性"),
"design/design-critique": ("设计评审", "设计评审,设计稿点评,可用性,视觉层级,设计反馈"),
"design/design-handoff": ("设计交付规格", "设计交付,开发交付,设计标注,切图,还原稿,交付规范"),
"design/design-system": ("设计系统", "设计系统,设计规范,组件库,token,命名一致性,设计标准"),
"design/research-synthesis": ("研究结论综合", "研究结论,主题归纳,用户洞察,研究综合"),
"design/user-research": ("用户研究方案", "用户研究,访谈提纲,可用性测试,问卷设计,调研方案"),
"design/ux-copy": ("UX 文案", "微文案,界面文案,错误提示,空状态,按钮文案,提示语"),

# ---- engineering ----
"engineering/debug": ("结构化调试", "调试,debug,排查问题,定位bug,复现,修bug"),
"engineering/standup": ("站会同步", "站会,日报,进度同步,晨会,工作汇报"),

# ---- enterprise-search ----
"enterprise-search/digest": ("活动摘要", "日报,周报摘要,每日简报,自动汇总"),
"enterprise-search/knowledge-synthesis": ("多源知识综合", "知识综合,多源合并,去重,可信度"),
"enterprise-search/search": ("跨源检索", "搜索,一次查询,多系统搜索"),
"enterprise-search/search-strategy": ("检索策略", "查询分解,检索编排,查询改写,搜索策略"),
"enterprise-search/source-management": ("检索源管理", "搜索源,数据源接入,源优先级"),

# ---- finance ----
"finance/audit-support": ("内审支持", "sox,内控测试,审计底稿,抽样"),
"finance/close-management": ("月结流程管理", "月结,结账流程,结账任务,结账进度"),
"finance/financial-statements": ("财务报表", "利润表,资产负债表,现金流量表,三表,财务报表"),
"finance/journal-entry": ("记账凭证", "记账,凭证,借贷,分录,做账"),
"finance/journal-entry-prep": ("月结记账准备", "月结,凭证准备,分录明细,结账凭证"),
"finance/reconciliation": ("账目核对", "对账,银行对账,子账,勾稽,账实核对"),
"finance/sox-testing": ("SOX 控制测试", "sox404,控制测试,样本选择,工作底稿"),
"finance/variance-analysis": ("差异归因分析", "差异分析,波动分析,归因,瀑布图,预算差异"),

# ---- human-resources ----
"human-resources/comp-analysis": ("薪酬对标分析", "薪酬,调薪,薪酬带,股权,人力成本,benchmark"),
"human-resources/draft-offer": ("offer 拟稿", "offer,录用通知,录用信,薪酬方案,入职通知"),
"human-resources/interview-prep": ("面试准备与评分卡", "面试,面试题,评分卡,结构化面试,能力模型"),
"human-resources/onboarding": ("入职引导", "入职,新人,试用期,第一周,入职清单"),
"human-resources/org-planning": ("组织与编制规划", "组织架构,编制,人员规划,团队结构,扩编"),
"human-resources/people-report": ("人力数据报告", "人员报告,离职率,员工结构,组织健康,人头统计"),
"human-resources/performance-review": ("绩效评估", "绩效,考核,绩效面谈,自评,校准会"),
"human-resources/policy-lookup": ("公司政策查询", "制度,政策,假期,报销政策,远程办公,员工手册"),
"human-resources/recruiting-pipeline": ("招聘管道管理", "招聘,候选人,简历,人才,招聘漏斗,候选人管道"),

# ---- hyperframes ----
"hyperframes/hyperframes": ("HyperFrames 动效引擎", "hyperframes,动效,网页动画,转场,动效视频,动画引擎"),
"hyperframes/hyperframes-cli": ("HyperFrames 命令行", "hyperframes cli,命令行,渲染,build,导出视频"),
"hyperframes/hyperframes-helper": ("HyperFrames 辅助工具", "hyperframes,辅助,调试,安装,排查"),
"hyperframes/hyperframes-registry": ("动效注册表", "registry,注册表,动效库,预设"),
"hyperframes/website-to-hyperframes": ("网页转 HyperFrames 视频", "网页转视频,网站转动效,录屏,promo视频,网站做成视频"),

# ---- legal ----
"legal/brief": ("法务简报", "法律简报,案情摘要,专题研究,事件法律分析"),
"legal/compliance-check": ("合规检查", "合规,监管,法规适用,合规校验"),
"legal/legal-response": ("法务标准回复", "法律问询回复,模板回复,法务答疑"),
"legal/legal-risk-assessment": ("法律风险评估", "风险分级,严重度,法律风险,升级标准"),
"legal/meeting-briefing": ("法务会议准备", "法务会前准备,法律会议,行动项"),
"legal/review-contract": ("合同审查", "合同审核,合同条款,红线,谈判手册,偏离项"),
"legal/signature-request": ("签署发起", "电子签,签署,签约,盖章,签字流程"),
"legal/triage-nda": ("NDA 三色分级", "保密协议,nda,分级,快速判断,保密协议审查"),
"legal/vendor-check": ("供应商合同状态", "供应商,合作方合同,协议台账,尽调"),

# ---- local-tooling ----
"local-tooling/local-ocr": ("本地离线 OCR 识文", "ocr,截图识文,离线识别,图片转文字,发票识别,文字提取"),
"local-tooling/skill-tuner": ("Skill 调优评测", "skill调优,优化skill,技能测试,skill评分,技能评测"),

# ---- marketing ----
"marketing/brand-review": ("品牌一致性检查", "品牌,品牌调性,口吻,style guide,文案审校"),
"marketing/campaign-plan": ("营销活动方案", "活动策划,投放方案,营销方案,campaign,活动日历"),
"marketing/email-sequence": ("邮件序列", "邮件营销,EDM,培育序列,邮件自动化,召回邮件"),

# ---- operations ----
"operations/capacity-plan": ("容量规划", "产能,资源规划,负载预测,利用率"),
"operations/change-request": ("变更申请", "变更管理,影响分析,回滚方案,变更单"),
"operations/compliance-tracking": ("合规跟踪", "合规要求,审计准备,合规台账"),
"operations/process-doc": ("流程文档化", "流程图,sop,raci,流程梳理,操作手册"),
"operations/process-optimization": ("流程优化", "瓶颈,提效,流程改进,价值流"),
"operations/risk-assessment": ("运营风险评估", "运营风险,风险识别,缓解措施"),
"operations/runbook": ("运行手册", "runbook,操作手册,值守手册,应急手册"),
"operations/status-report": ("运营状态报告", "运营周报,kpi,风险与行动项"),
"operations/vendor-review": ("供应商评估", "供应商评估,成本分析,供应商风险,推荐结论"),

# ---- pdf-viewer ----
"pdf-viewer/view-pdf": ("PDF 交互查看", "pdf,批注,填表,签名,标注pdf"),

# ---- product-management ----
"product-management/metrics-review": ("产品指标复盘", "指标,数据复盘,留存,转化,北极星指标,效果分析"),
"product-management/roadmap-update": ("路线图维护", "路线图,roadmap,排期,优先级,版本规划,迭代规划"),
"product-management/stakeholder-update": ("干系人同步", "周报,汇报,向上汇报,同步进展,干系人,状态同步"),

# ---- productivity ----
"productivity/memory-management": ("双层记忆", "记忆,长期记忆,偏好记忆,工作记忆,上下文"),
"productivity/start": ("启动生产力系统", "初始化,首次启动,引导配置,工作初始化"),
"productivity/task-management": ("任务管理", "待办,todo,任务清单,任务追踪"),
"productivity/update": ("同步任务与记忆", "同步,刷新记忆,更新状态"),

# ---- sales ----
"sales/account-context": ("客户全景", "客户档案,360视图,客户历史,往来记录"),
"sales/account-plan": ("客户战略计划", "大客户计划,客户经营,覆盖策略,干系人覆盖"),
"sales/account-research": ("目标公司调研", "客户调研,目标公司,背景调查,甲方背景"),
"sales/account-tiering": ("客户分层", "客户分级,ICP打分,客户优先级,名单排序"),
"sales/call-prep": ("通话准备", "通话前准备,会前简报,会议准备,客户背景"),
"sales/call-summary": ("通话纪要", "通话总结,会议纪要,跟进邮件,通话笔记"),
"sales/close-plan": ("成交方案", "成交计划,行动计划,ROI论证,关闭计划"),
"sales/competitive-intelligence": ("竞争情报", "竞对,竞争对手分析,赢单丢单模式,竞争格局"),
"sales/create-an-asset": ("客户材料制作", "客户材料,单页页,deck,提案材料,客户方案"),
"sales/crm-hygiene-check": ("CRM 数据体检", "crm检查,字段缺失,阶段错乱,数据卫生"),
"sales/customer-health": ("客户健康度", "客户风险,续约风险,qbr,客户活跃度"),
"sales/customer-voice": ("客户原声", "客户声音,客户反馈,原话引用,客户评价"),
"sales/daily-briefing": ("晨间简报", "今日会议,每日简报,晨会,待跟进客户"),
"sales/deal-advance-gap": ("商机推进缺口", "还差什么,推进条件,下一阶段,缺口检查"),
"sales/deal-review": ("商机深度复盘", "商机复盘,单子体检,赢单风险,推进卡点"),
"sales/deal-signals": ("商机异动监控", "商机预警,单子停滞,冠军换人,续约窗口,风险信号"),
"sales/deal-slip-scenario": ("丢单影响模拟", "丢单影响,配额缺口,业绩影响,情景推演"),
"sales/draft-outreach": ("外联邮件起草", "外联,开发信,触达邮件,跟进邮件"),
"sales/end-of-day": ("收尾复盘", "下班收尾,当日总结,承诺追踪"),
"sales/expansion-whitespace": ("增购空间挖掘", "增购,交叉销售,扩容机会,空白市场"),
"sales/forecast": ("业绩预测", "预测,commit,销售预测,管道预测,1v1"),
"sales/handle-objection": ("异议处理", "客户异议,反对意见,竞争威胁,异议应对"),
"sales/inbox-sweep": ("邮件批量处理", "批量邮件,未读邮件,邮件分类,邮件批处理"),
"sales/log-activity": ("活动回填 CRM", "补录,活动记录,写入crm,通话记录"),
"sales/pipeline-review": ("管道健康度", "销售管道,漏斗,转化率,管道覆盖,阶段健康"),
"sales/renewal-radar": ("续约雷达", "续约,续费,到期提醒,续约机会"),
"sales/rep-context": ("销售一对一准备", "销售1v1,组长的辅导,销售汇报,个人管道"),
"sales/route-lead": ("线索分配", "线索分配,归属,转交,交接"),
"sales/sales-lead-triage": ("线索分级排序", "线索打分,线索优先级,ICP,线索质量,分级"),
"sales/schedule-meeting": ("约会安排", "约会议,日历,发起会议,安排会议"),
"sales/setup": ("销售首次配置", "销售初始化,连接工具,首次运行,配置向导"),
"sales/stakeholder-map": ("决策链地图", "决策人,影响力,关键人物,干系人地图,联系人角色"),
"sales/team-pipeline": ("团队管道汇总", "团队管道,销售团队,组长视图,辅导"),
"sales/update-opportunity": ("商机更新", "商机阶段,更新商机,赢单概率,预计成交日"),
"sales/weekly-wrap": ("周度小结", "周报,本周总结,下周计划"),
"sales/win-loss-review": ("赢单丢单复盘", "赢单分析,丢单分析,赢单复盘,输单原因"),

# ---- small-business ----
"small-business/ad-manager": ("广告投放管理", "广告,投放,adwords,广告优化"),
"small-business/ap-processor": ("应付账款处理", "账单处理,供应商对账,应付流程"),
"small-business/brand-style": ("品牌风格设定", "品牌风格,视觉偏好,色调,排版偏好"),
"small-business/build-agent": ("把手工活变成技能", "做成技能,自动化流程,沉淀流程,自建技能"),
"small-business/build-connector": ("给工具接连接器", "连接器,接入工具,接口对接"),
"small-business/business-pulse": ("经营快照", "经营快照,一页纸经营,业务概览,经营状况"),
"small-business/call-list": ("今日呼叫清单", "打电话清单,今日外呼"),
"small-business/canva-creator": ("海报物料生成", "canva,配图,物料,营销图"),
"small-business/cash-flow-snapshot": ("现金流快照", "现金流,资金状况,应收应付,账期"),
"small-business/close-month": ("正式结账", "结账,关账,月度结账"),
"small-business/content-strategy": ("内容策略", "内容规划,爆款分析,内容打法"),
"small-business/contract-review": ("小微企业合同审查", "合同审查,msa,供应商合同,简易合同"),
"small-business/crm-autopilot": ("CRM 自动化", "crm,客户记录,自动录入"),
"small-business/grant-rfp-writer": ("投标书撰写", "投标,标书,基金申请,rfp"),
"small-business/grow-pipeline": ("管道增长", "漏斗增长,拓客,填充管道"),
"small-business/growth-pulse": ("增长体检", "增长有效性,拉新效果"),
"small-business/hiring-screener": ("简历筛选", "简历筛选,候选人打分,招聘筛选"),
"small-business/inbox-manager": ("收件箱管理", "收件箱,邮件处理,待办筛选"),
"small-business/inventory-planner": ("补货计划", "库存,补货,订货,库存规划"),
"small-business/invoice-chase": ("催收发票", "催发票,逾期发票,催款"),
"small-business/job-post-builder": ("招聘包制作", "招聘启事,jd,面试评分表,offer信"),
"small-business/lead-finder": ("找潜在客户", "找客户,潜客,目标客户,拓客"),
"small-business/marketing-monday": ("周一增长简报", "周一增长简报,营销周报"),
"small-business/monday-brief": ("周一经营简报", "周一简报,经营简报"),
"small-business/month-end-prep": ("月结准备", "月结准备,对账准备,账目核对,结账前"),
"small-business/outreach-composer": ("外联话术", "外联文案,开发信文案,像本人写的"),
"small-business/pay-the-bills": ("付款处理", "付账单,付款,账单处理,应付账款"),
"small-business/payroll-prep": ("工资准备", "工资准备,工时表,发薪核对"),
"small-business/plan-payroll": ("发薪规划", "发薪计划,工资发放,薪资规划"),
"small-business/proposal-builder": ("方案书制作", "方案书,提案,报价方案,标书"),
"small-business/reactivate": ("客户唤醒", "唤醒客户,回购,流失客户"),
"small-business/report-builder": ("报表定义", "报表,定期报表,指标定义"),
"small-business/report-pack": ("报表包交付", "报表包,定期交付,报表组合"),
"small-business/restock": ("补货决策", "补货,进货,补货下单"),
"small-business/review-reputation": ("口碑监测", "评价监测,口碑,差评,客户反馈监控"),
"small-business/seo-ai-visibility": ("搜索与AI可见性", "ai搜索,被ai引用,seo可见度"),
"small-business/smb-lead-triage": ("线索打分排序", "线索打分,线索排序,hubspot线索"),
"small-business/smb-onboard": ("新员工培训", "培训,带新人,员工上手"),
"small-business/smb-router": ("小企业总入口", "小企业,总入口,路由,开始"),
"small-business/social-content-engine": ("社媒内容流水线", "社交媒体,内容日历,发帖计划"),
"small-business/speed-to-lead": ("线索不漏接", "响应速度,线索响应,别漏线索"),
"small-business/tax-prep": ("报税材料准备", "报税,税务材料,纳税准备"),
"small-business/tax-season-organizer": ("报税季整理", "报税季,年度报税,税务整理"),
"small-business/ticket-deflector": ("工单自动应答", "工单自动处理,退款查询,订单状态,自动应答,工单拦截"),

# ---- understand ----
"understand/understand": ("语义理解引擎", "understand,理解,语义分析,读懂"),
"understand/understand-chat": ("对话式理解", "对话,chat,提问,问答理解"),
"understand/understand-dashboard": ("理解看板", "仪表盘,dashboard,概览,总览"),
"understand/understand-diff": ("差异理解", "diff,差异,变更对比,改了哪里"),
"understand/understand-domain": ("领域语义建模", "领域,domain,领域模型,业务语义"),
"understand/understand-explain": ("通俗解释生成", "解释,explain,通俗解释,讲明白"),
"understand/understand-knowledge": ("知识结构化理解", "知识,knowledge,知识图谱,知识抽取"),
}
