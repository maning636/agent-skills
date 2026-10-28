# 参考：本机端到端实测记录（2026-10-07）

一次真实的「需求 → CAD → GLB → Blender → 渲染」全过程记录。所有数字来自实测，不是估算。

## 需求

> 做一个 L 形安装支架，带四个安装孔

## 环境

| 项 | 值 |
|---|---|
| 系统 | Windows 11 IoT 企业版 LTSC Build 26100 |
| GPU | Quadro P1000，4096 MiB，**compute_cap 6.1**，基线占用 1823 MiB |
| CPU | Intel 2.60GHz |
| Blender | 4.5.14 LTS（headless）|
| cadgen | 0.7.15 |
| dcc-mcp-blender / core / server | 0.2.14 / 0.20.41 / 0.20.42 |

## 阶段 1：CAD 生成

```
$ python src/bracket.py
built STEP/bracket.step                     → 59,480 字节
```

耗时 < 1 秒。**LLM token = 0**（纯本地几何计算）。

模型参数：LEG_X=60, LEG_Z=40, BASE_Y=45, THK=6, HOLE_D=5。
产物几何：**1,384 顶点 / 1,372 面**。

## 阶段 2：GLB 转换

```
$ cadgen glb build STEP/bracket.step GLB/bracket.glb
wrote GLB: GLB\bracket.glb                 → 42,680 字节
```

耗时 < 1 秒。

## 阶段 3：快速预览（不经 Blender）

```
$ cadgen glb snapshot GLB/bracket.glb out/preview_iso.png --camera iso --width 1200 --height 900
saved snapshot: E:\tools\cad-demo\out\preview_iso.png  → 42,350 字节
```

**几何正确**：L 形支架 + 4 孔清晰可见。

## 阶段 4：Blender 导入

```
headless 启动 → MCP_URL=http://127.0.0.1:7127/mcp
dcc-mcp-cli list → total:1, dcc_type=blender, version=4.5.14 LTS, direct_control.ready=true
load-skill blender-interchange → 9 tools registered
POST /v1/call blender.97cae000.blender_interchange__import_file
  → success:true, imported_object_names:["bracket"], imported_count:1
```

## 阶段 5：Cycles 渲染（三次迭代）

### 第一次 —— 失败，画面全黑

```
bbox = [-0.03,-0.02,-0.02] ~ [0.03,0.02,0.02]     size = 0.06m
cam 在 (95,-135,75)，灯光 900/250/600W，rotation_euler=(0,0,0)
结果：1,184,568 字节，但画面只有暗蓝灰背景色，零件完全不可见
```

**根因（三个叠加）**：
1. **GLB 单位是米**——60mm 支架变成 0.06 单位，相机在几公里外
2. 灯的 `rotation_euler=(0,0,0)` 让灯垂直向下，不是瞄准零件
3. 灯功率 900W 在 0.1m 距离 → 即使拍到也全过曝

### 第二次 —— 几何可见，但过曝纯白

修正：包围盒取景 + `to_track_quat` 瞄准 + 灯光降到 12/4/10W + 渐变世界。
结果：**12.1 秒**，1,094,905 字节，几何和三点布光正确，金属材质生效但整体偏白。

### 第三次 —— 达标

修正：在第二次基础上补渐变世界（给金属提供可反射环境）。
结果：**13.1 秒**，1,229,526 字节，金属反射、轮廓光、背景渐变都正确。

## 产能数据（本机基准）

| 项目 | 实测 |
|---|---|
| CAD 生成（STEP）| < 1 秒 |
| STEP → GLB | < 1 秒 |
| snapshot 预览 | 数秒 |
| **Cycles 1280×960 / 128采样 / 1384顶点** | **12-13 秒** |
| 显存增量 | 1823 → 1881 MiB（**+58 MiB**）|
| LLM token | **0** |

**换算产能**：

| 成品 | 帧数 | 预计耗时 |
|---|---|---|
| 10 秒 24fps | 240 | **约 52 分钟** |
| 30 秒 24fps | 720 | **约 2.6 小时** |
| 单张产品图 | 1 | 13 秒 |

**结论：P1000 做这个量级的 CAD 广告图产能充足，云渲染不是必需品。**

## 本次修正的三个错误估算

1. 渲染耗时：预估「3-15 分钟/帧」，实测 **13 秒/帧**——错两个数量级
2. 显存压力：预估 4GB 会紧张，实测渲染只多占 **58 MiB**
3. 相机定位：以为导入后物体原点不在几何中心（错），真因是 **mm→m 缩放 1000 倍**

## 关键教训

**先跑 snapshot 再进 Blender。** 本次如果先渲染，会浪费 3 次往返（每次 12 秒启动 + 渲染）才看出问题；而 snapshot 是秒级反馈，能提前发现几何错误。

**所有 3D 位置都用包围盒算。** mm→m 缩放是这条流水线最隐蔽的坑，写死坐标必炸。