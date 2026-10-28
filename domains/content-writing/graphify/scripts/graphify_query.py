#!/usr/bin/env python3
"""
graphify_query.py - graphify 图谱查询辅助脚本

用法:
    python graphify_query.py <project_dir> [--question "问题"] [--top N] [--path A B] [--explain X] [--affected X]

示例:
    python graphify_query.py .                              # 自动分析项目
    python graphify_query.py . --top 5                     # 前 5 个 god nodes
    python graphify_query.py . --path "FastAPI" "ModelField"
    python graphify_query.py . --explain "APIRouter"
    python graphify_query.py . --affected "AuthMiddleware"
    python graphify_query.py . --question "数据库连接如何管理？"
"""

import json
import os
import subprocess
import sys
from collections import Counter, defaultdict, deque


def build_graph(project_dir):
    """构建图谱（如果不存在）"""
    out_dir = os.path.join(project_dir, "graphify-out")
    graph_path = os.path.join(out_dir, "graph.json")
    if not os.path.exists(graph_path):
        print("[构建图谱] graphify extract . --code-only ...", flush=True)
        result = subprocess.run(
            ["graphify", "extract", project_dir, "--code-only"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode != 0:
            print(f"[错误] graphify extract 失败: {result.stderr}", flush=True)
            sys.exit(1)
        print("[完成] 图谱已构建", flush=True)
    else:
        print(f"[加载] 已存在图谱: {graph_path}", flush=True)
    return graph_path


def load_graph(graph_path):
    """加载图谱（兼容 NetworkX 格式）"""
    with open(graph_path, "r", encoding="utf-8") as f:
        graph = json.load(f)
    # NetworkX 格式用 links，不是 edges
    if "links" in graph and "edges" not in graph:
        graph["edges"] = graph["links"]
    elif "edges" not in graph:
        graph["edges"] = []
    return graph


def find_god_nodes(graph, top_n=10):
    """找到最连接的节点"""
    edge_count = Counter()
    for e in graph["edges"]:
        edge_count[e["source"]] += 1
        edge_count[e["target"]] += 1

    nodes = {n["id"]: n for n in graph["nodes"]}
    results = []
    for node_id, count in edge_count.most_common(top_n):
        node = nodes.get(node_id, {})
        results.append({
            "label": node.get("label", node_id),
            "source_file": node.get("source_file", "?"),
            "edges": count
        })
    return results


def find_path(graph, start_label, end_label):
    """查找两个节点之间的最短路径"""
    nodes = {n["label"]: n["id"] for n in graph["nodes"]}
    start_id = nodes.get(start_label)
    end_id = nodes.get(end_label)
    if not start_id or not end_id:
        return None

    adj = defaultdict(list)
    edge_map = {}
    for e in graph["edges"]:
        adj[e["source"]].append(e["target"])
        adj[e["target"]].append(e["source"])
        edge_map[(e["source"], e["target"])] = e

    queue = deque([start_id])
    visited = {start_id}
    parent = {start_id: None}
    while queue:
        node = queue.popleft()
        if node == end_id:
            path = []
            while node:
                path.append(node)
                node = parent[node]
            path.reverse()
            edges = []
            for i in range(len(path) - 1):
                e = edge_map.get((path[i], path[i+1])) or edge_map.get((path[i+1], path[i]))
                if e:
                    edges.append({"relation": e["relation"], "confidence": e["confidence"]})
            return {"nodes": path, "edges": edges, "length": len(path) - 1}
        for neighbor in adj[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    return None


def explain_node(graph, label):
    """解释一个节点"""
    nodes = {n["label"]: n for n in graph["nodes"]}
    node = nodes.get(label)
    if not node:
        return None

    incoming = [e for e in graph["edges"] if e["target"] == node["id"]]
    outgoing = [e for e in graph["edges"] if e["source"] == node["id"]]
    return {
        "label": node["label"],
        "type": node.get("type", "?"),
        "source_file": node.get("source_file", "?"),
        "source_location": node.get("source_location", "?"),
        "incoming_count": len(incoming),
        "outgoing_count": len(outgoing),
        "callers": [graph_node_label(graph, e["source"]) for e in incoming if e["relation"] == "calls"],
        "callees": [graph_node_label(graph, e["target"]) for e in outgoing if e["relation"] == "calls"],
        "imports": [graph_node_label(graph, e["target"]) for e in outgoing if e["relation"] == "imports"],
        "imported_by": [graph_node_label(graph, e["source"]) for e in incoming if e["relation"] == "imports"],
    }


def find_affected(graph, label, depth=2):
    """找到受某节点变更影响的节点"""
    nodes = {n["label"]: n["id"] for n in graph["nodes"]}
    start_id = nodes.get(label)
    if not start_id:
        return None

    incoming = defaultdict(list)
    for e in graph["edges"]:
        incoming[e["target"]].append(e["source"])

    affected = set()
    queue = deque([(start_id, 0)])
    while queue:
        node, d = queue.popleft()
        if d >= depth:
            continue
        for caller in incoming[node]:
            if caller not in affected:
                affected.add(caller)
                queue.append((caller, d + 1))

    return sorted([graph_node_label(graph, a) for a in affected])


def graph_node_label(graph, node_id):
    """从 node_id 获取 label"""
    for n in graph["nodes"]:
        if n["id"] == node_id:
            return n.get("label", node_id)
    return node_id


def confidence_summary(graph):
    """置信度统计"""
    counts = Counter()
    for e in graph["edges"]:
        counts[e.get("confidence", "unknown")] += 1
    return dict(counts)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="graphify 图谱查询辅助")
    parser.add_argument("project_dir", nargs="?", default=".", help="项目目录")
    parser.add_argument("--question", help="自然语言查询")
    parser.add_argument("--top", type=int, default=10, help="god-nodes 数量")
    parser.add_argument("--path", nargs=2, metavar=("A", "B"), help="最短路径查询")
    parser.add_argument("--explain", help="解释节点")
    parser.add_argument("--affected", help="影响分析")
    parser.add_argument("--summary", action="store_true", help="图谱摘要")
    args = parser.parse_args()

    project_dir = os.path.abspath(args.project_dir)
    graph_path = build_graph(project_dir)
    graph = load_graph(graph_path)

    print(f"\n{'='*60}", flush=True)
    print(f"图谱摘要", flush=True)
    print(f"{'='*60}", flush=True)
    print(f"节点数: {len(graph['nodes'])}", flush=True)
    print(f"边数: {len(graph['edges'])}", flush=True)
    conf = confidence_summary(graph)
    print(f"置信度分布: {json.dumps(conf, ensure_ascii=False)}", flush=True)
    print(f"{'='*60}\n", flush=True)

    if args.summary or not (args.question or args.path or args.explain or args.affected):
        # 默认输出 god-nodes
        print(f"Top {args.top} God Nodes（最连接节点）:", flush=True)
        for i, node in enumerate(find_god_nodes(graph, args.top), 1):
            print(f"  {i}. {node['label']} ({node['edges']} 条边) - {node['source_file']}", flush=True)

    if args.question:
        print(f"\n查询: {args.question}", flush=True)
        result = subprocess.run(
            ["graphify", "query", args.question, "--graph", graph_path],
            capture_output=True, text=True, timeout=60
        )
        print(result.stdout if result.stdout else result.stderr, flush=True)

    if args.path:
        print(f"\n最短路径: {args.path[0]} → {args.path[1]}", flush=True)
        result = find_path(graph, args.path[0], args.path[1])
        if result:
            print(f"  长度: {result['length']} 步", flush=True)
            for i, node in enumerate(result["nodes"]):
                node_info = graph_node_label(graph, node)
                print(f"  {i+1}. {node_info}", flush=True)
            for i, edge in enumerate(result["edges"]):
                print(f"     → [{edge['relation']}] ({edge['confidence']})", flush=True)
        else:
            print("  未找到路径", flush=True)

    if args.explain:
        print(f"\n解释: {args.explain}", flush=True)
        result = explain_node(graph, args.explain)
        if result:
            print(f"  类型: {result['type']}", flush=True)
            print(f"  文件: {result['source_file']}", flush=True)
            print(f"  位置: {result['source_location']}", flush=True)
            print(f"  入边: {result['incoming_count']}  出边: {result['outgoing_count']}", flush=True)
            if result["callers"]:
                print(f"  被调用: {', '.join(result['callers'])}", flush=True)
            if result["callees"]:
                print(f"  调用: {', '.join(result['callees'])}", flush=True)
            if result["imports"]:
                print(f"  导入: {', '.join(result['imports'])}", flush=True)
            if result["imported_by"]:
                print(f"  被导入: {', '.join(result['imported_by'])}", flush=True)
        else:
            print("  未找到该节点", flush=True)

    if args.affected:
        print(f"\n影响分析: {args.affected}", flush=True)
        result = find_affected(graph, args.affected)
        if result:
            print(f"  受影响节点 ({len(result)} 个):", flush=True)
            for i, node in enumerate(result[:20], 1):
                print(f"  {i}. {node}", flush=True)
        else:
            print("  未找到该节点", flush=True)


if __name__ == "__main__":
    main()
