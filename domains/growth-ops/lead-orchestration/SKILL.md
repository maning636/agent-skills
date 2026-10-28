---
id: growth-ops/lead-orchestration
domain: growth-ops
name: lead-orchestration
description: 线索协同与自动化分发。基于标准 CRM 任务/工作流引擎，不绑定特定后端。触发场景：批量分发线索、自动化 follow-up、SDR 任务调度。⚠️ v1.2 修订：实际能力因 CRM 后端而异，必须先做 crm-discover 再调度；批量分配用 POST /deals/bulk-assign-owner（标准 REST 模式）；F:\平替skill\0090-lead-orchestration\alt1 和 alt2 资源缺失。
origin: 本机自研
license: 见来源
---


# 线索协同 (lead-orchestration)

## 1. 适用边界

### 1.1 适用场景
- 批量分发线索到 SDR/AE
- 自动化 follow-up（按 dueAt + reason）
- 工作流编排（lead → qualify → deal）
- 多渠道归因（inbound / outbound / referral）

### 1.2 不适用
- 单个 lead 跟进（属 `lead-management` skill）
- 线索评分（属 `lead-scoring` skill）
- 营销自动化（属 `marketing-automation` skill）

## 2. 标准 CRM 接入模式（不绑定后端）

### 2.1 必须先做 crm-discover

每个 CRM 后端的任务/工作流引擎差异极大：
- Salesforce: Process Builder + Flow
- HubSpot: Workflows + Sequences
- Pipedrive: Activities + Workflow Automation
- Trycompai/crm: tasks + eve agent 框架

**首次执行前必须**确认后端是否支持：
- 批量 deal 更新（POST /deals/bulk-assign-owner 或同类）
- 任务自动创建（POST /tasks 或 trigger-based）
- 工作流 trigger（webhook / schedule / event-based）
- 调度引擎（cron / queue / eve agent）

### 2.2 标准批量分配模式

```
Step 1: 拉取待分配 lead
  POST /deals/search { filter: { stage: "DEMO_BOOKED", ownerId: null }, limit: 100 }

Step 2: 按规则分配（轮询/权重/技能）
  // 轮询算法示例
  const sdrs = ['sdr-1', 'sdr-2', 'sdr-3'];
  leads.forEach((lead, i) => {
    lead.ownerId = sdrs[i % sdrs.length];
  });

Step 3: 批量更新（一次请求）
  POST /deals/bulk-assign-owner { 
    dealIds: leads.map(l => l.id), 
    ownerIds: leads.map(l => l.ownerId) 
  }
  // 关键：批量请求而非循环单条更新（性能差异 100x）

Step 4: 验证分配结果
  GET /deals?ids=[...]  或  POST /deals/search { filter: { ids: [...] } }
```

### 2.3 自动 follow-up 模式

```
// 创建任务（不是创建 cron）
POST /tasks { 
  type: 'follow_up_call', 
  dueAt: '2026-09-20T10:00:00Z', 
  ownerId: sdrId, 
  dealId: lead.id,
  reason: 'lead inbound from landing page, no contact in 24h',  // 必填：reason 显示给 SDR
  priority: 'high' 
}
```

**关键约束**：
- 必须传 `reason`（CRM 会在 UI 上展示给 SDR）
- 必须传 `dueAt`（ISO 8601）
- 不要自己写 cron 任务（CRM 内部调度更可靠）

## 3. F:\平替skill\0090 资源缺失说明

```
F:\平替skill\0090-lead-orchestration\
├── alt1/  (空，只有 .git)
├── alt2/  (空，只有 .git)
└── ...

降级方案：
- 使用 crm-discover 探测后端能力
- 按 §2 标准模式实现
- 记录实际使用的接口到 stage-naming-map.md
```

## 4. 降级模式（API 不可达）

如果 CRM API 不可达：
1. **生成轮询算法脚本**（独立于 CRM，可作为 Python/JS 脚本）
2. **输出建议 API 调用序列**（伪代码 + curl）
3. **不编造任务 ID**
4. **建议手动操作**：让用户登录 CRM 手动分配

## 5. 常用算法

### 5.1 轮询（Round Robin）
```javascript
const sdrs = ['sdr-1', 'sdr-2', 'sdr-3'];
leads.forEach((lead, i) => {
  lead.ownerId = sdrs[i % sdrs.length];
});
```
适用：SDR 容量相近，新线索均匀分配

### 5.2 权重分配（Weighted）
```javascript
const weights = { 'sdr-1': 0.5, 'sdr-2': 0.3, 'sdr-3': 0.2 };
// 按累计权重选
```
适用：SDR 容量不同，按权重分配

### 5.3 技能匹配（Skill Match）
```javascript
// lead.industry === 'fintech' → 分配给有 fintech 经验的 SDR
```
适用：行业差异大，专业 SDR 转化率高

### 5.4 地理分配（Geo-based）
```javascript
// lead.region === 'north' → 分配给负责北区的 SDR
```
适用：本地化业务

## 6. 输出物清单

- `assignment-result.md`：分配结果（lead × sdr 矩阵）
- `algorithm-rationale.md`：算法选择理由
- `stage-naming-map.md`：本次发现的 CRM 任务/工作流 API
- `followup-tasks.md`：自动 follow-up 任务清单

## 7. 反模式

- ❌ 循环单条更新（性能差，应批量）
- ❌ 创建 cron 任务而非 CRM 内部 task
- ❌ 不传 reason（SDR 看不到为什么）
- ❌ 不做 crm-discover 就假设后端能力
- ❌ 忽略 SDR 容量（轮询压垮 1 个人）
- ❌ 不验证分配结果（失败任务无人发现）

## 8. 修订日志

### v1.2（2026-09-17，去产品绑定）
- 去除 Trycompai/crm 特定路径引用（lib/tasks.ts::claimDue 等）
- 改为「标准 CRM 任务/工作流引擎」通用模式
- 强制 Step 1 = crm-discover（防止硬编码）

### v1.1（2026-09-17）
- 明确「降级模式」是正常路径（0090 资源缺失）
- 标注 `list_outstanding_work` 返回 contacts 而非 lead 队列的发现

**审计来源**：
- P2-5/5 case（task id `01a0ab31-85b0-7efe-ba87-ce15b45d49cb`）
- 完整审计报告：`D:\研究\multica\P2_SKILL_REPLACEMENT_AUDIT.md`
