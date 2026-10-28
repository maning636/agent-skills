---
id: cad-3d/cad-ad-pipeline
domain: cad-3d
name: cad-ad-pipeline
description: CAD 建模到广告级渲染出片的全流程。当任务涉及「用 agent 做 CAD」「把 CAD 变成产品图/宣传图/爆炸图」「Blender 渲染产品动画」「text-to-cad 出图」「机械零件建模出片」「STEP 转 GLB 导入 Blender」时使用。也覆盖机器人 URDF/仿真模型、SDF 场景导出。触发词：CAD、出图、产品渲染、爆炸图、装配动画、Blender、text-to-cad、STEP、GLB、URDF、参数化建模。
origin: local
license: MIT
---


# CAD → 广告级渲染 全流程

三层架构。**每一层换工具都不影响其他层**，接口是文件格式。

```
层1  CAD 生成      text-to-cad / cadgen        → STEP / GLB / STL / URDF
层2  3D 出片       Blender 4.5+ / Cycles        → PNG 序列
层3  2D 合成       HyperFrames / Remotion / FFmpeg → 成片
```

---

## 环境前提（本机实测通过的组合）

| 组件 | 版本 | 位置 |
|---|---|---|
| cadgen | 0.7.15 | `uvx --from cadgen==0.7.15` |
| Blender | 4.5.14 LTS | `E:\tools\blender-4.5.14-windows-x64\blender.exe` |
| dcc-mcp-cli | 0.20.42 | `~\.local\bin\dcc-mcp-cli.exe` |
| dcc-mcp-blender | 0.2.14 | Blender 内置 Python（`4.5\python\bin\python.exe`）|
| HyperFrames | 0.8.55 | npm 全局 |
| FFmpeg | 8.1 | PATH |

**命令别名（写进 shell profile 可省事）**
```powershell
$cadgen = 'uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.15 cadgen'
$cpy    = 'uvx --no-config --managed-python --python 3.13 --from cadgen==0.7.15 python'
```

---

## 阶段 0：环境自检（每次新会话先跑）

```powershell
# 1. CAD 内核能否加载（验 OCP 有没有被 Smart App Control 拦）
uvx cadgen doctor

# 2. Blender headless 是否能被网关发现
& 'E:\tools\blender-4.5.14-windows-x64\blender.exe' --background `
  --python 'E:\tools\blender-4.5.14-windows-x64\4.5\python\lib\site-packages\dcc_mcp_blender\blender_bootstrap.py'
# 后台跑，另开窗口：
dcc-mcp-cli list     # 期望 total:1，且 dcc_type=blender
```

`dcc-mcp-cli list` 返回 `total:0` = Blender 没启动。`total:1` 即可开工。

---

## 阶段 1：CAD 生成

模型是**带装饰器的无参函数**，返回 build123d 形状。完整范例见 `references/model-example.md`。

```python
# src/bracket.py
from cadgen import build123d as bd
from cadgen import step

@step(out="../STEP/bracket.step")
def bracket():
    body = bd.Box(60.0, 6.0, 40.0)
    body.label = "bracket"
    return body

if __name__ == "__main__":
    bracket()
```

```powershell
Invoke-Expression "$cpy src/bracket.py"        # → STEP/bracket.step
Invoke-Expression "$cadgen glb build STEP/bracket.step GLB/bracket.glb"
```

---

## 阶段 2：快速预览（不过 Blender，秒级反馈）

**改参数后的第一道验证，不要跳过。**

```powershell
Invoke-Expression "$cadgen glb snapshot GLB/bracket.glb out/preview.png --camera iso --width 1200 --height 900"
```

`--camera` 可选：`front/back/left/right/top/bottom/iso`。
**注意：`snapshot` 的详细日志 flag 是 `--debug`，不是 `--verbose`（用了会 exit 2）。**

---

## 阶段 3：导入 Blender

### 3.1 先启动（见阶段 0），取 instance_short

```powershell
$inst = (dcc-mcp-cli list | ConvertFrom-Json).instances[0].instance_id
```

### 3.2 加载技能再调用（必须，否则 unknown-slug）

```powershell
dcc-mcp-cli load-skill blender-interchange --dcc-type blender --instance-id $inst
```

工具 slug 格式：`blender.<instance_short>.<skill>__<tool>`，
例如 `blender.97cae000.blender_interchange__import_file`。

### 3.3 走网关 REST，不要用 CLI 传 JSON

**PowerShell 5.1 把 JSON 传给原生 exe 会吃掉引号。** 用 `Invoke-RestMethod`：

```powershell
$gw = 'http://127.0.0.1:9765'
function Call-Api($path, $bodyObj){
  Invoke-RestMethod -Uri "$gw$path" -Method Post -ContentType 'application/json' `
    -Body ($bodyObj | ConvertTo-Json -Depth 8) -TimeoutSec 900
}

Call-Api '/v1/call' @{
  tool_slug = "blender.$inst.blender_interchange__import_file"
  arguments = @{ path = 'E:\tools\cad-demo\GLB\bracket.glb' }
}
```

---

## 阶段 4：渲染

**推荐用 `execute_script_file` 跑脚本文件，而不是 `execute_python` 传字符串**——避开转义问题，且脚本可复用可 review。

完整可跑脚本见 `references/render-script.md`。要点：

```python
scene.render.engine = "CYCLES"
cprefs.compute_device_type = "CUDA"     # 见坑 3
for d in cprefs.devices: d.use = (d.type == "CUDA")
scene.cycles.samples = 128
scene.cycles.use_denoising = True
scene.cycles.denoiser = "OPENIMAGEDENOISE"   # 见坑 3
```

```powershell
Call-Api '/v1/call' @{
  tool_slug = "blender.$inst.blender_scripting__execute_script_file"
  arguments = @{ filepath = 'E:\tools\cad-demo\scripts\render_product.py' }
}
```

**实测基准（P1000 4GB / 1384 顶点零件）**

| 分辨率 | 采样 | 单帧耗时 |
|---|---|---|
| 1280×960 | 128 | **12-13 秒** |

据此：10 秒 24fps 动画 ≈ 52 分钟；30 秒 ≈ 2.6 小时。**本地产能够，云渲染只在超大场景/4K 时才需要。**

### Cycles vs EEVEE 怎么选

| | Cycles | EEVEE Next |
|---|---|---|
| 用途 | 静帧主视觉、爆炸图、产品图 | 动画帧、转场、批量 |
| 质量 | 真实光追、反射折射 | 依赖布光与材质质量 |
| 速度（本机） | 13 秒/帧 | 数秒/帧 |
| 显存 | 低（本例 +58 MiB） | 中 |

**混用**：同一工程里两个 view layer 分别出静帧和动画帧，最后 FFmpeg 拼。

---

## 阶段 5：动效与合成

| 环节 | 工具 |
|---|---|
| 字幕、动态文字、转场、图形包装 | HyperFrames（`hyperframes` / `hyperframes-animation` / `hyperframes-keyframes`）|
| PNG 序列 → 视频 | `ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -crf 18 out.mp4` |
| 音轨、混音、时长对齐 | FFmpeg |

---

## 九个必须知道的坑（全部实测踩出）

### 坑 1：GLB 导入后单位从毫米变成米（缩放 1/1000）

CAD 建模用毫米，GLB 按 glTF 米制导出。**60mm 的支架在 Blender 里是 `0.06` 个单位。**

后果：用绝对坐标放相机（比如 `(95,-135,75)`）会拍到几公里外，**画面全黑只有背景色**。

解决：**永远用包围盒算位置，不要写死坐标。**
```python
corners = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
center = Vector(tuple((min(c[i] for c in corners)+max(c[i] for c in corners))/2 for i in range(3)))
size   = tuple(max(c[i] for c in corners)-min(c[i] for c in corners) for i in range(3))
dist = Vector(size).length * 2.1
```

### 坑 2：灯光功率必须按米级尺度重算

6cm 的物体用 1200W 面光放在 10cm 距离 → **完全过曝成纯白**，金属质感全丢。

实测可用值（0.06m 物体）：
- Key 12W / Fill 4W / Rim 10W，距离 0.1-0.3m

灯必须瞄准目标，默认朝向是 **-Z（垂直向下）**：
```python
ob.rotation_euler = (center - ob.location).to_track_quat("-Z","Y").to_euler()
```

### 坑 3：P1000 有一个**假的 OPTIX 设备条目**

Blender 在 Pascal（CC 6.1，无 RT core）上**仍然列出** `type: 'OPTIX'` 的 Quadro P1000。但 **OptiX 需要 CC ≥ 7.0，实际不可用**。

同理，切 `compute_device_type` 到 HIP/ONEAPI 时 Blender 会**静默返回同一份缓存设备列表**，看起来"支持"其实没换。

必须显式：
```python
cprefs.compute_device_type = "CUDA"     # 不要信自动选出来的 OPTIX
scene.cycles.denoiser = "OPENIMAGEDENOISE"   # OptiX 降噪器同样不可用
```

### 坑 4：dcc-mcp 参数名不统一

| 工具 | 路径参数名 |
|---|---|
| `blender_interchange__import_file` | `path` |
| `blender_scripting__execute_script_file` | **`filepath`** |
| `blender_interchange__import_usd` | **`filepath`** |

传错直接 `400 invalid-params: missing required field`。**报错信息会写清楚要哪个字段，照抄即可。**

### 坑 5：工具 slug 必须先 load_skill

44 个 skill 是**渐进加载**的。未加载就调用 → `unknown-slug`。

另外 skill 名和工具名对不上，容易踩空：
- `get_blender_info` 在 **`blender-scripting`**，不在 `blender-dev`
- `execute_python` / `execute_script_file` 也在 `blender-scripting`

`load_skill` 的返回值里有 `registered_tools` 全表，直接从里面抄准确工具名。

### 坑 6：新建相机的 location 恒为 (0,0,0) —— 渲染全空的**头号杀手**

```python
cd = bpy.data.cameras.new("Cam")
cam = bpy.data.objects.new("Cam", cd)   # ← cam.location == (0,0,0)，且朝 -Z 垂直向下
```

新建相机的位置是**世界原点、朝 −Z 向下**。如果模型中心在 `(0.04, -0.01, 0)`，
相机就**卡在齿轮箱内部往外看**，渲染结果是 100% 空帧（只有世界背景）。

**这个坑最阴险的地方**：先调好相机再 `keyframe_insert` 的脚本是对的，
所以"看起来能跑通"；但**在插关键帧之前先渲一张自检图**时，相机还没被赋值 → 全空。
同一次调试里"先渲的图是空的、后渲的动画是对的"，极易误判成进程状态问题。

**修法：创建相机后立刻写死一个静态位，再谈动画。**
```python
cam.location = center + Vector((cos(a)*dist, sin(a)*dist, dist*0.26))
cam.rotation_euler = (center - cam.location).to_track_quat("-Z","Y").to_euler()
scene.camera = cam
```

### 坑 7：GLB 导入后，顶点局部坐标**已经含装配位置**

逐件导入装配体时：
```
p10_gear_A  obj.loc=[0,0,0]  localBB=[[-0.10,-0.07,0.01] .. [-0.03,0.0,0.04]]
p11_gear_B  obj.loc=[0,0,0]  localBB=[[-0.01,-0.06,0.01] .. [0.04,-0.01,0.03]]
```
9 个零件的 `localBB` **各自落在不同区域**——说明导出时就按装配坐标烘进顶点里了，
物体变换是单位矩阵。

此时如果再写 `ob.location = 顶点几何中心`，就是**二次平移**，整机被推歪。

**正确做法：导入后不动 `location`，它就是装配基准位。**

```python
home = Vector((0, 0, 0))     # 装配基准位，就这个值
```

⚠️ **这个坑专挑动画段下手**。做爆炸动画时很自然会想"爆炸要从零件中心往外推"，
于是去算几何中心当基准——**这一步就毁了整段动画**：

```python
# ❌ 错：每个零件被整体平移了各自 ctr 的距离，"分离度归零"时依然错位散架
ctr = sum((v.co for v in ob.data.vertices), Vector()) / len(ob.data.vertices)
ob.location = ctr + d * RAD * k

# ✅ 对：以单位变换为基准，k=0 就是严丝合缝的装配位
ob.location = Vector((0,0,0)) + d * RAD * k
```

**判据**：`k=0` 时零件必须回到导入后的原始相对位置。只要爆炸动画"合不拢"，
第一个要怀疑的就是这里。

### 坑 8：长任务不要走 MCP 同步调用，用原生 CLI + 像素自检

在**长驻** headless Blender 进程里，经 MCP `execute_script_file` 跑完整动画渲染，
即使场景完全正确（视锥诊断显示 112 个包围盒角点在视野内），输出**依然是空帧**。
渲染耗时 5 秒就"完成"——说明 GPU/Cycles 上下文在该进程里已失效。

**长任务一律走原生 CLI，在全新进程里跑：**
```powershell
blender.exe -b --factory-startup --python render.py -- --anim
```
参考实现：`E:\tools\cad-demo\scripts\cli_render.py`

**并且在渲动画前，先渲一张自检图做像素级验证**——把零件临时换成 emission=40 的纯白材质，
渲 1 帧，读回像素统计"亮度 > 0.5"的占比：

```python
_em = mk("DIAG_EM", (1,1,1), 0, 1, (1,1,1), 40.0)   # 所有零件换成它
bpy.ops.render.render(write_still=True)
# → VIS_PCT=60.98%  PASS     几何占据画面六成，可放心渲动画
# → VIS_PCT=0.000%  FAIL     直接 exit(3)，别浪费几小时渲 96 帧空气
```

这一步把"渲完 96 帧才发现是空帧"的 10 分钟级浪费压缩成 12 秒。

### 坑 9：相机 `location` 插了帧、`rotation_euler` 忘了插 → 相机背对模型

绕圈运镜的写法：
```python
def pc(fr, ang, dmul, h):
    cam.location = center + Vector((cos(a)*dist, sin(a)*dist, dist*h))
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z","Y").to_euler()
    cam.keyframe_insert("location", frame=fr)          # ← 只插了位置
```

三帧插完后，`cam.rotation_euler` 的**属性值停留在最后一帧（292°）的朝向**，
而 `frame_set(1)` 求值时相机位置又回到 238° 方位 → **相机背对模型，96 帧全黑**。

坑在"它看起来是对的"：脚本里 `rotation_euler` 每次都赋了值，
静态预览（不插帧）完全正常，只有**动画求值后**才暴露。

```python
    cam.keyframe_insert("rotation_euler", frame=fr)   # ★ 必须一起插
```

**由此推出一条通用规则：自检必须放在"和最终渲染完全相同的状态"下做。**

在插帧**之前**做自检 → 测的是静态相机，测不出关键帧驱动出来的任何错误。
正确顺序是：建场景 → 插完所有关键帧 → `scene.frame_set(f)` → 渲自检图 → 通过才渲动画。

```python
# 参考实现里这一段是独立的两轮自检，静态一轮、动画态一轮
for fr in (F0, F1):
    scene.frame_set(fr)
    px = _shot(...)
    if diff_stats(px_bg, px) <= 1.0:
        sys.exit(4)   # 关键帧驱动后相机/变换有问题
```

### 坑 10：爆炸图动画必须首尾闭合——拆完要装回去

只做「拆开」不做「装回」，叙事是不完整的：观众看不到成品，也就感受不到
"这是一台能运转的机器"。

标准时间线（96 帧 @24fps = 4 秒）：

| 帧 | 状态 | 相机 |
|---|---|---|
| F0 = 1 | **完全合装**，分离度 0 | 近景，看装配细节 |
| FA = 42 | **完全展开**，分离度 1 | 拉远，零件铺满画面 |
| FB = 82 | **装回**，分离度 0 | 近景 |
| F2 = 96 | 合装保持，环绕收尾 | 中景 |

```python
F0, FA, FB, F2 = 1, 42, 82, 96
for fr, t in ((F0, 0.0), (FA, 1.0), (FB, 0.0), (F2, 0.0)):
    ob.location = home + expl * t        # t 是归一化分离度
    ob.keyframe_insert("location", frame=fr)
```

**这样也不需要再做"正放+倒放"的循环版了**——正片首尾都是装配态，直接接得上。
强行 concat 反向会造成接缝处两帧静止的顿挫。

关键帧数量不重要，**关键是 FA 和 FB 对称**（展开 41 帧 / 合回 40 帧），
节奏才不急促。

配套的自检要覆盖三个状态而不是两个：

```python
for fr in (F0, FA, FB):      # 合装 / 展开 / 装回，三态都要验
    scene.frame_set(fr)
    ...
```

`metallic = 1.0` 的材质**没有漫反射**，成像完全依赖反射环境。
世界背景亮度给不够时，金属齿轮箱会渲染成全黑，只有自发光灯条可见——
看起来像"几何丢了"，其实是环境光为零。

三个必须同时满足的条件：
1. `world` 节点 `Background.Strength` 给到 0.8~2（不是默认的 1.0 随手）
2. 光源**面积要大**（`ld.size = RAD * 2~4`）。点光源打在 roughness 0.3 的
   金属上只留一个针尖高光，形状完全读不出来
3. 金属 `Base Color` 要**暗**（0.05 上下）。给亮灰会渲成白塑料，不是金属

一次加太狠就整片过曝成纯白。别靠反复全量渲染试错——加个低采样多档曝光扫描，
30 秒定位：

```python
scene.cycles.samples = 24
for ev in (-2.5, -1.5, -0.5, 0.5):
    scene.view_settings.exposure = ev
    scene.render.filepath = os.path.join(CAL, "ev_p%03d" % int(ev*10))
    bpy.ops.render.render(write_still=True)
# 目视挑定 → scene.view_settings.exposure = -1.5  写死进正式渲染
```

---

## 快速排错表

| 现象 | 原因 | 处理 |
|---|---|---|
| `ImportError: DLL load failed while importing OCP` | Smart App Control 或第三方安全软件拦未签名 DLL | `uvx cadgen doctor`；Win11 IoT/LTSC 默认关闭，若是 Pro/Ent 检查注册表或改用 WSL |
| `dcc-mcp-cli list` 返回 `total:0` | Blender 没启动 | 跑阶段 0 的 bootstrap 命令 |
| 渲染全黑/只有背景色 | 相机用了绝对坐标，物体被缩放成 0.06 | 见坑 1，改用包围盒 |
| 渲染纯白无细节 | 灯光功率过高 | 见坑 2 |
| `unknown-slug` | skill 没加载 | 先 `load-skill` |
| `missing required field 'x'` | 参数名错 | 看报错，照抄字段名 |
| `--json must be valid JSON` | PS 5.1 吃掉引号 | 改走网关 REST |
| snapshot `exit 2` | 用了不存在的 flag | snapshot 用 `--debug` 不是 `--verbose` |
| 渲染空帧、只有世界背景，**且视锥诊断显示物体明明在视野内** | 相机 `location` 停在 (0,0,0)，卡在模型内部 | 见坑 6，创建相机后立刻写死静态位 |
| 导入装配体后整机歪掉/散架 | 把顶点几何中心赋给了 `ob.location`，二次平移 | 见坑 7，GLB 顶点已含装配坐标，别动 `location` |
| 视锥正常但渲出来全黑，且"渲染只花 5 秒" | 长驻 MCP 进程 GPU 上下文已失效 | 见坑 8，改 `blender -b --python` + 先跑像素自检 |
| 静态预览正常，渲动画全黑 | 相机只插了 `location` 帧，`rotation_euler` 没插 | 见坑 9，两个都要插；自检放到插帧之后 |
| 几何"消失"只剩发光灯条 | 金属 metallic=1 无漫反射，环境光为零 | 见附：world 强度 + 大面积光源 + 暗 Base Color |
| 整片过曝纯白 | 环境光/光源能量一次加太狠 | 跑多档 EV 扫描标定，别全量重渲试错 |
| 爆炸动画看完"合不拢"，零件错位 | 把顶点几何中心当装配基准，零件被二次平移 | 见坑 7，`home` 只能是 `(0,0,0)` |
| 爆炸动画只拆不装，叙事不完整 | 缺反向关键帧 | 见坑 10，补 `t=0` 的装回帧，首尾都要是装配态 |

---

## 参考文件

| 文件 | 内容 |
|---|---|
| `references/model-example.md` | 完整参数化 CAD 模型范例（含孔、圆角、装配）|
| `references/render-script.md` | 完整可跑的 Cycles 渲染脚本（含包围盒取景、灯组、渐变世界）|
| `references/pipeline-demo.md` | 本次端到端验证的完整实测记录 |

---

## 下一步做什么

改任何一层后，先跑阶段 2 的 snapshot 秒级验证，再进 Blender。
**不要跳过预览直接渲染**——Blender 一次往返 30 秒起，而改参数往往要迭代十几次。