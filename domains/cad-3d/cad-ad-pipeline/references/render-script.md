# 参考：Cycles 渲染脚本（完整可跑）

本机实测通过的版本。**所有位置都用包围盒算，不写死坐标**——因为 GLB 导入后单位是米（见主文档坑 1）。

## 完整脚本

保存为 `scripts/render_product.py`：

```python
"""CAD -> Blender -> Cycles 渲染。强制 CUDA 后端，规避 Pascal 上的假 OPTIX 设备。"""
import os
import mathutils
import bpy

OUT_DIR = r"E:\tools\cad-demo\out"
os.makedirs(OUT_DIR, exist_ok=True)
scene = bpy.context.scene

TARGET = "bracket"          # 要渲染的物体名
RES_X, RES_Y = 1280, 960
SAMPLES = 128

ob = bpy.data.objects.get(TARGET)
if ob is None:
    raise SystemExit("object %s not found" % TARGET)

# ---- 1. 包围盒（关键：解决 mm->m 缩放）----
corners = [ob.matrix_world @ mathutils.Vector(c) for c in ob.bound_box]
center = mathutils.Vector(tuple(
    (min(c[i] for c in corners) + max(c[i] for c in corners)) / 2.0 for i in range(3)))
size = tuple(max(c[i] for c in corners) - min(c[i] for c in corners) for i in range(3))
print("center =", [round(v, 4) for v in center], " size =", [round(v, 4) for v in size])

# ---- 2. 清理上一轮残留 ----
for n in ("KeyLight", "FillLight", "RimLight", "AdCam", "Cube", "Light", "Camera"):
    o = bpy.data.objects.get(n)
    if o:
        bpy.data.objects.remove(o, do_unlink=True)

# ---- 3. Cycles + 强制 CUDA ----
scene.render.engine = "CYCLES"
scene.cycles.device = "GPU"
cprefs = bpy.context.preferences.addons["cycles"].preferences
cprefs.compute_device_type = "CUDA"       # P1000 无 RT core，OPTIX 是假条目
cprefs.refresh_devices()
for d in cprefs.devices:
    d.use = (d.type == "CUDA")            # 关掉 CPU，强制纯 GPU
print("enabled =", [d.name for d in cprefs.devices if d.use])

scene.cycles.samples = SAMPLES
scene.cycles.use_denoising = True
try:
    scene.cycles.denoiser = "OPENIMAGEDENOISE"   # OptiX 降噪器在 CC6.1 上不可用
except Exception as e:
    print("denoiser fallback:", e)
scene.cycles.max_bounces = 8
scene.render.resolution_x = RES_X
scene.render.resolution_y = RES_Y
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"

# ---- 4. 世界：竖向渐变（给金属提供可反射环境）----
world = bpy.data.worlds.get("World") or bpy.data.worlds.new("World")
scene.world = world
world.use_nodes = True
nt = world.node_tree
nt.nodes.clear()
out_n  = nt.nodes.new("ShaderNodeOutputWorld")
bg_n   = nt.nodes.new("ShaderNodeBackground")
ramp  = nt.nodes.new("ShaderNodeValToRGB")
sep   = nt.nodes.new("ShaderNodeSeparateXYZ")
tex   = nt.nodes.new("ShaderNodeTexCoord")
mapr  = nt.nodes.new("ShaderNodeMapRange")
nt.links.new(tex.outputs["Generated"], sep.inputs[0])
nt.links.new(sep.outputs["Z"], mapr.inputs["Value"])
nt.links.new(mapr.outputs[0], ramp.inputs["Fac"])
nt.links.new(ramp.outputs["Color"], bg_n.inputs[0])
ramp.color_ramp.elements[0].position = 0.25
ramp.color_ramp.elements[0].color = (0.012, 0.014, 0.020, 1)
ramp.color_ramp.elements[1].position = 0.85
ramp.color_ramp.elements[1].color = (0.32, 0.36, 0.44, 1)
bg_n.inputs[1].default_value = 1.0
nt.links.new(bg_n.outputs[0], out_n.inputs[0])

# ---- 5. 灯组（功率必须匹配米级尺度，见主文档坑 2）----
def add_light(name, energy, offset, size_l):
    ld = bpy.data.lights.new(name, type="AREA")
    ld.energy = energy
    ld.size = size_l
    o = bpy.data.objects.new(name, ld)
    o.location = center + mathutils.Vector(offset)
    o.rotation_euler = (center - o.location).to_track_quat("-Z", "Y").to_euler()  # 必须瞄准
    scene.collection.objects.link(o)
    return o

add_light("KeyLight",  12.0, ( 0.16, -0.22,  0.26), 0.10)   # 主光
add_light("FillLight",  4.0, (-0.24, -0.10,  0.10), 0.18)   # 补光，压暗部
add_light("RimLight",  10.0, ( 0.06,  0.26,  0.16), 0.08)   # 轮廓光

# ---- 6. 材质 ----
mat = bpy.data.materials.get("adMat") or bpy.data.materials.new("adMat")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.68, 0.70, 0.74, 1.0)
    bsdf.inputs["Metallic"].default_value = 0.9
    bsdf.inputs["Roughness"].default_value = 0.22
ob.data.materials.clear()
ob.data.materials.append(mat)

# ---- 7. 相机（按包围盒对角线定距离）----
cd = bpy.data.cameras.new("AdCam")
cd.lens = 55
cam = bpy.data.objects.new("AdCam", cd)
scene.collection.objects.link(cam)
scene.camera = cam

dist = mathutils.Vector(size).length * 2.1
cam.location = center + mathutils.Vector((dist * 0.62, -dist * 0.78, dist * 0.48))
cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()

# ---- 8. 渲染 ----
out_path = os.path.join(OUT_DIR, "render.png")
scene.render.filepath = out_path
bpy.ops.render.render(write_still=True)
print("RESULT_BEGIN\nrendered =", out_path, os.path.getsize(out_path), "\nRESULT_END")
```

## 调用

```powershell
$gw = 'http://127.0.0.1:9765'
$inst = (dcc-mcp-cli list | ConvertFrom-Json).instances[0].instance_id
$short = (dcc-mcp-cli list | ConvertFrom-Json).instances[0].instance_short

# 先确认技能已加载
dcc-mcp-cli load-skill blender-scripting --dcc-type blender --instance-id $inst

Invoke-RestMethod -Uri "$gw/v1/call" -Method Post -ContentType 'application/json' -Body (@{
  tool_slug = "blender.$short.blender_scripting__execute_script_file"
  arguments = @{ filepath = 'E:\tools\cad-demo\scripts\render_product.py' }
} | ConvertTo-Json -Depth 8) -TimeoutSec 900
```

## 参数调节速查

| 要什么 | 调什么 |
|---|---|
| 更亮/更暗 | 灯的 `energy`，或世界渐变两端颜色 |
| 更快出图 | 降 `SAMPLES` 到 48-64（OIDN 降噪保质量）|
| 更高分辨率 | 改 `RES_X/RES_Y`，显存够就行（本例只多用 58 MiB）|
| 磨砂金属 | `Roughness` 调到 0.35-0.45 |
| 换视角 | 改 `cam.location` 的三个系数比例 |
| 多角度批量出图 | 改相机位置循环 `bpy.ops.render.render()`，每次改 `filepath` |

## 动画批量出图

```python
# 在脚本末尾替换单帧渲染为序列
import os
frames_dir = os.path.join(OUT_DIR, "frames")
os.makedirs(frames_dir, exist_ok=True)
scene.render.filepath = os.path.join(frames_dir, "f_")
bpy.ops.render.render(animation=True)   # 按 scene.frame_start/end 逐帧
```

之后用 FFmpeg 合序列：
```bash
ffmpeg -framerate 24 -i frames/f_%04d.png -c:v libx264 -crf 18 -pix_fmt yuv420p out.mp4
```