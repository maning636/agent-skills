# 参考：参数化 CAD 模型范例

模型契约：**带装饰器的无参函数**，返回 build123d 形状。`out=` 路径相对模型脚本自身。

## 最小骨架

```python
# src/bracket.py
from cadgen import build123d as bd
from cadgen import step

WIDTH = 40.0

@step(out="../STEP/bracket.step")
def bracket():
    body = bd.Box(WIDTH, 20, 6)
    body.label = "bracket"
    return body

if __name__ == "__main__":
    bracket()
```

## 实用骨架：L 形支架（含 4 孔）

```python
# src/bracket.py  —— 本机实测通过的版本
from cadgen import build123d as bd
from cadgen import step

# ---- 参数（全部显式，改这里就能重新生成）----
LEG_X = 60.0          # 立板长度（X）
LEG_Z = 40.0          # 立板高度（Z）
BASE_Y = 45.0         # 底板深度（Y）
THK = 6.0             # 板厚
HOLE_D = 5.0          # 安装孔直径
HOLE_INSET_X = 10.0   # 孔位距 X 两端
HOLE_INSET_Y = 9.0    # 孔位距 Y 两端


@step(out="../STEP/bracket.step")
def bracket():
    upright = bd.Box(LEG_X, THK, LEG_Z)     # 立板：长X 薄Y 高Z
    base = bd.Box(LEG_X, BASE_Y, THK)       # 底板：长X 深Y 薄Z
    body = upright + base

    hole_r = HOLE_D / 2.0
    depth = THK * 4.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            x = sx * (LEG_X / 2.0 - HOLE_INSET_X)
            y = sy * (BASE_Y / 2.0 - HOLE_INSET_Y)
            body -= bd.Pos(x, y, 0.0) * bd.Cylinder(hole_r, depth)

    body.label = "bracket"
    return body


if __name__ == "__main__":
    bracket()
```

`bd.Cylinder(radius, depth)` 默认轴向为 Z，正好穿透底板。

## 常用 build123d 操作

| 操作 | 写法 |
|---|---|
| 长方体 | `bd.Box(l, w, h)` |
| 圆柱 | `bd.Cylinder(radius, depth)` |
| 平移 | `bd.Pos(x, y, z) * shape` 或 `shape.moved(...)` |
| 布尔 | `a + b` / `a - b` / `a & b` |
| 圆角 | `bd.fillet(edges, radius)` — 边选择容易失败，先用简单形体 |
| 打标签 | `shape.label = "name"` |

**建模原则（来自 cad skill）**
- 优先封闭、正体积的实体
- 参数集中在模块顶部，几何写在工厂函数里
- 几何不能依赖时间、随机数、环境变量、当前工作目录
- 装配体调用子模型，用 `.moved()` 或 `Location * shape` 放置

## 输出格式

| 格式 | 命令 | 去向 |
|---|---|---|
| STEP | `@step(out=...)` 装饰器 | 工程存档、CAD 交换 |
| GLB | `@glb(out=...)` 或 `cadgen glb build` | **Blender / 3D 引擎** |
| STL | `@stl(out=...)` 或 `cadgen stl build` | 3D 打印、网格 |
| 3MF | `@threemf(out=...)` | 3D 打印 |
| DXF | `$dxf` skill | 2D 图纸、激光切割 |
| URDF/SRDF/SDF | `$urdf` / `$srdf` / `$sdf` skill | 机器人仿真 |

## ⚠️ 单位

**模型一律用毫米。** GLB 导出时会按 glTF 标准转成米（缩放 1/1000）。
Blender 里所有相机/灯光位置必须用**包围盒**算，不要写死毫米数值。见主 SKILL.md 坑 1。