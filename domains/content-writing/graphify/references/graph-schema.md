# graph.json 数据结构

## 顶层结构

```json
{
  "nodes": [...],
  "edges": [...],
  "metadata": { ... }
}
```

## Node 对象

```json
{
  "id": "file:backend/app.py:APIRouter",
  "label": "APIRouter",
  "type": "function",
  "source_file": "backend/app.py",
  "source_location": "L42",
  "properties": {
    "language": "python",
    "line_count": 25,
    "complexity": 3.2
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | ✅ | 唯一标识（格式：`file:path:symbol`）|
| `label` | string | ✅ | 人类可读名称 |
| `type` | string | ✅ | function / class / module / variable / 等 |
| `source_file` | string | ✅ | 源文件路径 |
| `source_location` | string | ❌ | 行号（如 L42、L10-L42）|
| `properties` | object | ❌ | 附加属性（语言、复杂度、行数等）|

## Edge 对象

```json
{
  "source": "file:backend/app.py:APIRouter",
  "target": "file:backend/routes/images.py:images_router",
  "relation": "calls",
  "confidence": "EXTRACTED",
  "weight": 1.0,
  "properties": {
    "line_number": 45
  }
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `source` | string | ✅ | 源节点 id |
| `target` | string | ✅ | 目标节点 id |
| `relation` | string | ✅ | 关系类型 |
| `confidence` | string | ✅ | EXTRACTED / INFERRED / AMBIGUOUS |
| `weight` | float | ❌ | 边权重 |
| `properties` | object | ❌ | 附加属性 |

### 关系类型（relation）

| 关系 | 说明 |
|---|---|
| `calls` | 函数调用 |
| `imports` | 导入依赖 |
| `uses` | 使用（泛化）|
| `inherits` | 继承 |
| `implements` | 实现 |
| `defines` | 定义 |
| `references` | 引用 |
| `reads` | 读取 |
| `writes` | 写入 |
| `connects_to` | 连接 |

### 置信度标签（confidence）

| 标签 | 含义 | 来源 |
|---|---|---|
| `EXTRACTED` | 源码中明确写出 | tree-sitter AST 直接解析 |
| `INFERRED` | 合理推断 | 调用图二遍、上下文共现 |
| `AMBIGUOUS` | 不确定 | 需要人工审查 |

## 查询示例

### 查找某函数被谁调用

```python
import json

with open("graphify-out/graph.json") as f:
    graph = json.load(f)

target_id = "file:backend/app.py:APIRouter"
callers = [
    e["source"] for e in graph["edges"]
    if e["target"] == target_id and e["relation"] == "calls"
]
```

### 查找 god nodes（最连接节点）

```python
from collections import Counter

edge_count = Counter()
for e in graph["edges"]:
    edge_count[e["source"]] += 1
    edge_count[e["target"]] += 1

top_10 = edge_count.most_common(10)
```

### 查找所有 EXTRACTED 边

```python
extracted = [
    e for e in graph["edges"]
    if e["confidence"] == "EXTRACTED"
]
```

### 查找某文件的完整依赖

```python
file_deps = [
    e for e in graph["edges"]
    if e["source"].startswith("file:backend/app.py")
    and e["relation"] in ("imports", "calls")
]
```

### 最短路径

```python
from collections import defaultdict, deque

adj = defaultdict(list)
for e in graph["edges"]:
    adj[e["source"]].append(e["target"])

def shortest_path(start, end):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    while queue:
        node = queue.popleft()
        if node == end:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return list(reversed(path))
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    return None
```
