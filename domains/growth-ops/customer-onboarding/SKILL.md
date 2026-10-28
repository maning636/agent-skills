---
id: growth-ops/customer-onboarding
domain: growth-ops
name: customer-onboarding
description: 新客户入职流程。基于标准 CRM 三段式 API 模式（POST /companies → POST /contacts → POST /deals），不绑定特定后端。触发场景：用户说"有新客户"、问"入职流程是什么"、生成入职检查清单。⚠️ v1.2 修订：先调用 crm-discover 发现后端 schema；重复 email 用 POST /contacts/search 做 exact match 查重；环境不可达时降级到文档化输出。
origin: 本机自研
license: 见来源
---


# 客户入职 (customer-onboarding)

## 1. 适用边界

### 1.1 适用场景
- 新客户签约后启动入职流程
- 老客户加购需要新增 contact
- 内部团队入职 SOP 自动化
- 第三方合作方接入流程

### 1.2 不适用
- 销售线索转化（属 `sales-funnel` skill）
- 长期客户成功（属 `customer-success` skill）
- 客户支持工单（属 `support-tickets` skill）

## 2. 标准 CRM 接入模式（不绑定后端）

### 2.1 发现后端能力（首次接入）

**必须**先做 schema 发现：
```
- POST /companies 的字段（name, industry, size, ...）
- POST /contacts 的字段（email, phone, role, companyId, ...）
- POST /deals 的字段（stage, amount, ownerId, contactIds, companyId, ...）
- Stage 初始值（如创建 deal 时默认 stage）
- 主键生成策略（UUID / autoincrement / 外部 ID）
```

典型 CRM 三段式 API 模式：

| 操作 | 标准 REST 模式 | 备注 |
|------|---------------|------|
| 创建公司 | `POST /companies` | 必须返回 company.id |
| 创建联系人 | `POST /contacts` | 必须返回 contact.id，含 email |
| 关联 deal | `POST /deals` | 关联 contactId + companyId |

### 2.2 三段式入职流程

```
Step 1: 创建公司
  POST /companies { name, industry, size, website, ... }
  → company.id (UUID 或 自增)

Step 2: 创建主联系人（可能多个）
  POST /contacts { email, firstName, lastName, role, companyId, ... }
  → contact.id

Step 3: 验证重复（见 §3）
Step 4: 创建 deal
  POST /deals { stage, amount, ownerId, contactIds: [contact.id], companyId: company.id, ... }
  → deal.id

Step 5: 触发自动 follow-up（如果有）
  POST /tasks { type: 'welcome_call', dueAt, ownerId, ... }
```

## 3. 重复 Email 处理（v1.1 + v1.2 强化）

### 3.1 Exact Match 查重流程

```
Step 1: 在创建 contact 前，先调用 POST /contacts/search
  body: { "email": "exact@email.com", "exact": true }
  （不同 CRM 的 exact match 字段名不同：Salesforce 用 `=` 表达式，HubSpot 用 filters）

Step 2: 若返回 1 条记录 → 复用该 contact 的 id，不创建新 contact
Step 3: 若返回 0 条记录 → 创建新 contact（POST /contacts）
Step 4: 若返回 ≥ 2 条记录 → 报错「数据脏：同一 email 多次注册」，需人工清理
```

### 3.2 跨 CRM 的查重方式

| CRM | 查重接口 | 关键参数 |
|-----|---------|---------|
| Salesforce | `GET /services/data/vXX/query/?q=SELECT+Id+FROM+Contact+WHERE+Email='...'` | `Email` exact match |
| HubSpot | `POST /crm/v3/objects/contacts/search` | `{ filterGroups: [{ filters: [{ propertyName: 'email', operator: 'EQ', value: '...' }] }] }` |
| Pipedrive | `GET /v1/persons/search?term=email@example.com&fields=email` | `fields=email` |
| Trycompai/crm | `POST /contacts/search` | `{ email, exact: true }` |
| 通用 REST | `GET /contacts?email=...` 或 `POST /contacts/search` | 视具体 API 而定 |

## 4. 降级模式（API 不可达）

如果 crm API 不可达：
1. **生成入职检查清单**（Markdown），按行业通用项生成
2. **输出建议 API 调用序列**（伪代码 + curl 示例）
3. **不编造响应**：明确标注"如可调用 API，应得的结果如下"
4. **提示手动操作**：让用户登录 CRM 后台手动创建

## 5. 完整入职检查清单（输出物）

```
☐ 账号开通
  ☐ 管理员账号创建
  ☐ 子账号批量创建（按角色）
  ☐ 双因素认证开启
  ☐ SSO 接入（如有）

☐ 首次会议
  ☐ Kick-off 会议预约（建议 D+3）
  ☐ 议程：目标/范围/时间线/风险/联系人
  ☐ 录制会议（征得同意）

☐ 合同准备
  ☐ 主合同 + 附件清单
  ☐ NDA（如未签）
  ☐ 数据处理协议（DPA，GDPR/PIPL）
  ☐ SLA 协议（如有）

☐ Welcome Pack
  ☐ 产品手册
  ☐ 视频教程链接
  ☐ 客服联系方式
  ☐ FAQ 文档
  ☐ 邀请加入用户社群

☐ 培训
  ☐ 管理员培训（2h）
  ☐ 终端用户培训（按部门）
  ☐ 高级功能培训（按角色）

☐ 后续支持
  ☐ D+7 健康检查
  ☐ D+30 满意度调研
  ☐ Q1 业务复盘
```

## 6. 输出物清单

- `onboarding-checklist.md`：完整检查清单（按行业定制）
- `api-call-sequence.md`：标准三段式 API 调用序列（含示例 payload）
- `duplicate-check-result.md`：重复 email 检查结果（如果做了查重）
- `stage-naming-map.md`：本次发现的 stage 初始值

## 7. 反模式

- ❌ 不查重直接创建 contact（数据脏）
- ❌ 用 fuzzy match 查重（误判率高）
- ❌ 跳过 API schema 发现就硬编码
- ❌ 创建 contact 不关联 companyId（关系断裂）
- ❌ API 不可达时编造 ID
- ❌ 一次性发完所有 welcome pack（应该分阶段：签约时/D+1/D+7/D+30）

## 8. 修订日志

### v1.2（2026-09-17，去产品绑定）
- 去除 Trycompai/crm 特定路径引用（apps/api/src/contacts/contacts.contracts.ts 等）
- 改为「标准 CRM 三段式 API 模式」，附 Salesforce/HubSpot/Pipedrive/Trycompai 的查重方式表

### v1.1（2026-09-17）
- 新增「重复 Email 处理流程」4 步（exact match → 复用 → 报错降级）
- 加入 v1.1 警告（exact email match + 降级模式）

**审计来源**：
- P2-4/5 case（task id `01a0ab31-881a-7015-8b25-1723a9d3d35d`）
- 完整审计报告：`D:\研究\multica\P2_SKILL_REPLACEMENT_AUDIT.md`
