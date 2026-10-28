---
id: growth-ops/sales-funnel
domain: growth-ops
name: sales-funnel
description: 销售漏斗统计与瓶颈定位。基于标准 CRM REST API 模式（POST /deals/search + facetCounts 或同类聚合查询），不绑定特定后端。触发场景：用户要看销售数据、问"为什么成单率低"、生成销售周报、漏斗阶段转化率。⚠️ v1.2 修订：Stage 命名以接入的 CRM 后端 DealStage enum 为准（典型如 DEMO_BOOKED / QUALIFIED_TO_BUY / DECISION_MAKER_BOUGHT_IN / CONTRACT_SENT / CLOSED_WON / CLOSED_LOST / UNQUALIFIED_TO_BUY），调用前先 discover 后端 schema。
origin: 本机自研
license: 见来源
---


# 销售漏斗分析 (sales-funnel)

## 1. 适用边界

### 1.1 适用场景
- 销售周报/月报需要漏斗数据
- 转化率突然下降需要诊断
- 战略复盘需要量化输入
- 团队 OKR 制定需要漏斗基线

### 1.2 不适用
- 单点 deal 跟进（属 `deal-management` skill）
- 客户关系管理（属 `customer-onboarding` skill）
- 预测模型（属 `forecast-modeling` skill）

## 2. 标准 CRM 接入模式（不绑定后端）

### 2.1 发现后端能力（首次接入）

执行前**必须**调用 `crm-discover` 工具（如果存在）获取：
```
- API base URL
- 认证方式（API key / OAuth / session）
- Deal stage enum 的实际值
- 字段映射（standard field → backend-specific field）
```

如果无 crm-discover 工具，按以下通用模式推断：
- REST + JSON（80% CRM）
- GraphQL（10%）
- 特定 SDK（10%，需要文档）

### 2.2 标准接口契约（REST 模式）

**聚合查询**（必备）：
```
POST /deals/search
{
  "filter": {
    "createdAt": { "$gte": "2026-09-01" },
    "ownerId": { "$in": ["user-1", "user-2"] }
  },
  "facetCounts": ["stage", "source"],
  "limit": 0,                              // 不需要明细
  "aggregations": {
    "amount": { "sum": true, "avg": true }
  }
}
```

**响应结构**：
```json
{
  "data": {
    "items": [],                          // limit=0 时为空
    "facetCounts": {
      "stage": [
        { "value": "DEMO_BOOKED", "count": 35, "sumAmount": 1200000 },
        { "value": "QUALIFIED_TO_BUY", "count": 28, "sumAmount": 980000 }
      ],
      "source": [...]
    },
    "aggregations": {
      "amount": { "sum": 12500000, "avg": 45000 }
    }
  }
}
```

### 2.3 Stage 命名（v1.2 修订）

**不要硬编码 stage 名称**。首次调用时先做 stage 枚举探测：

```javascript
// Step 1: 获取后端的 stage 列表
const stages = await crm.listDealStages();
// 可能返回: ['DEMO_BOOKED','QUALIFIED_TO_BUY',...] 或 ['lead','qualified',...] 

// Step 2: 按"开放阶段"（未关闭）+ "胜利阶段" + "失败阶段"分类
const openStages = stages.filter(s => !['CLOSED_WON','CLOSED_LOST','UNQUALIFIED_TO_BUY'].includes(s));
```

**典型 CRM 的 stage 命名映射**（仅供参考，以后端为准）：

| 抽象阶段 | Salesforce | HubSpot | Pipedrive | Trycompai/crm |
|---------|-----------|---------|-----------|---------------|
| 初接触 | `Prospecting` | `Appointment Scheduled` | `Lead In` | `DEMO_BOOKED` |
| 资格确认 | `Qualification` | `Qualified to Buy` | `Qualified` | `QUALIFIED_TO_BUY` |
| 决策人确认 | `Value Proposition` | `Presentation Scheduled` | `Proposal Made` | `DECISION_MAKER_BOUGHT_IN` |
| 合同谈判 | `Proposal/Price Quote` | `Contract Sent` | `Contract Sent` | `CONTRACT_SENT` |
| 成交 | `Closed Won` | `Closed Won` | `Won` | `CLOSED_WON` |
| 失败 | `Closed Lost` | `Closed Lost` | `Lost` | `CLOSED_LOST` |

## 3. 漏斗计算逻辑

```javascript
// 输入：facetCounts.stage 数组
// 输出：每阶段 count、amount sum、stage→stage 转化率

const stageData = facetCounts.stage;  // [{value, count, sumAmount}, ...]
const total = stageData.reduce((acc, s) => acc + s.count, 0);

const funnel = stageData.map((s, i) => {
  const next = stageData[i + 1];
  const conversion = next ? (next.count / s.count * 100).toFixed(1) + '%' : '-';
  const percentage = (s.count / total * 100).toFixed(1) + '%';
  return {
    stage: s.value,
    count: s.count,
    amount: s.sumAmount || 0,
    percentage,
    conversionToNext: conversion
  };
});
```

## 4. 瓶颈诊断规则

按经验阈值识别 Top 瓶颈：

| 转化率阈值 | 可能原因 | 建议动作 |
|-----------|----------|----------|
| `初接触 → 资格确认` < 30% | ICP 不准 / lead 质量差 | 调整 ICP 筛选条件 |
| `资格确认 → 决策人确认` < 25% | 决策人接触失败 / 价值主张不清 | 加强 MEDDPICC 培训 |
| `决策人确认 → 合同谈判` < 30% | 定价/竞争问题 | 调整定价或补充 ROI 论证 |
| `合同谈判 → 成交` < 25% | 合同条款 / 决策链不清 | 优化合同 + 决策链确认 |

## 5. 降级模式（API 不可达）

如果 crm API 不可达，按以下顺序降级：
1. **导出 CSV**：让用户从 CRM 后台导出最近 30 天 deal CSV
2. **本地脚本解析**：用 csv-parse 解析，统计各 stage 的 count
3. **文档化输出**：明确标注"基于 CSV 数据"vs"基于 API 实时查询"
4. **不编造**：没有数据就标注"待补"，不要输出假数字

## 6. 输出物清单

- `funnel-report.md`：漏斗全景表（Markdown 表格）
- `bottleneck-analysis.md`：Top 3 瓶颈 + 转化率 + 建议动作
- `stage-naming-map.md`：本次发现的 stage 命名映射（避免下次重新发现）

## 7. 反模式

- ❌ 硬编码 stage 名称（"proposal"/"negotiation"等模糊命名）
- ❌ 不做 schema 发现就假设后端能力
- ❌ API 不可达时编造数据
- ❌ 只看 count 不看 amount（漏斗金额比数量更重要）
- ❌ 不标注数据来源（API / CSV / 估算）

## 8. 修订日志

### v1.2（2026-09-17，去产品绑定）
- 去除 Trycompai/crm 特定路径引用（apps/api/src/deals/deals.router.ts 等）
- 改为「标准 CRM REST 模式」，附 Salesforce/HubSpot/Pipedrive/Trycompai 的 stage 命名映射表
- 强制 Step 1 = schema 发现（防止硬编码）

### v1.1（2026-09-17，P2 审计反馈）
- Stage 命名对齐典型 CRM enum（已包含在 v1.2 的映射表）
- 失败处理表补充：API 不可达时使用降级模式

**审计来源**：
- P2-2/5 case（task id `01a0ab31-80fe-77e3-bde0-4faea4314ce1`）
- 完整审计报告：`D:\研究\multica\P2_SKILL_REPLACEMENT_AUDIT.md`
