# cad-3d — CAD / 3D 工程

> **触发场景**：CAD建模、DXF、工程图、STEP、URDF、G-code、DFM、3D打印、3D产品图
> **技能数**：14　|　**来源**：earthtojake/text-to-cad + 本机自研

| 技能 | 中文标签 | 关键词（中文 / 英文） | 路径 | 大小 |
|---|---|---|---|---|
| `3d-product` | 3D 产品模型生成 | 3D产品,三维模型,产品建模,blender,stl,3D打印,渲染图 / a one-shot pipeline for hardware product films in blender, from a prom… | `domains/cad-3d/3d-product/SKILL.md` | 48.1K |
| `bambu-labs` | Bambu Lab 3D 打印 | 3D打印,拓竹,bambu,切片,打印参数,gcode打印 / send prints to bambu lab printers through bambu connect, bambu lab's o… | `domains/cad-3d/bambu-labs/SKILL.md` | 3.4K |
| `cad` | 参数化 CAD 建模 | cad,参数化,机械设计,零件图,三维建模 / create/edit parametric cad models, organize cad projects, export step/… | `domains/cad-3d/cad/SKILL.md` | 10.9K |
| `cad-ad-pipeline` | CAD 广告图流水线 | 广告图,CAD图,广告素材,流水线,产品广告图 / cad 建模到广告级渲染出片的全流程。当任务涉及「用 agent 做 cad」「把 cad 变成产品图/宣传图/爆炸图」「blender 渲… | `domains/cad-3d/cad-ad-pipeline/SKILL.md` | 17.8K |
| `dfam-check` | 可制造性检查 DFM | dfm,可制造性,工艺检查,能不能造 / measure mesh files against design for additive manufacturing (dfam) ru… | `domains/cad-3d/dfam-check/SKILL.md` | 5.9K |
| `dfm` | 面向制造的设计 DFM | dfm,制造设计,公差,工艺,装配 / design-for-manufacturing review of a part for sheet metal, cnc machini… | `domains/cad-3d/dfm/SKILL.md` | 5.7K |
| `dxf` | DXF 二维图纸 | dxf,二维图,cad图,交换格式,平面图 / generate, regenerate, and validate 2d dxf drawings from python build12… | `domains/cad-3d/dxf/SKILL.md` | 16.9K |
| `engineering-drawing` | 工程图绘制 | 工程图,技术制图,三视图,尺寸标注 / make an engineering drawing of a part as a pdf - orthographic views wi… | `domains/cad-3d/engineering-drawing/SKILL.md` | 7.7K |
| `gcode` | G-code 生成 | gcode,数控,机床指令,刀路 / slice 3d models into printer-ready g-code with orcaslicer, the open-so… | `domains/cad-3d/gcode/SKILL.md` | 3.9K |
| `sdf` | SDF 机器人描述 | sdf,机器人描述,碰撞模型 / sdformat/sdf model and world authoring, validation, and simulator hand… | `domains/cad-3d/sdf/SKILL.md` | 10.1K |
| `sendcutsend` | SendCutSend 下单 | sendcutsend,在线切割,激光切割下单,板材 / review dxf and step/stp uploads for sendcutsend.com orders using its o… | `domains/cad-3d/sendcutsend/SKILL.md` | 12.6K |
| `srdf` | SRDF 机器人描述 | srdf,机器人中间表示 / moveit2 srdf authoring, validation, and planning-semantics workflow. | `domains/cad-3d/srdf/SKILL.md` | 11.2K |
| `step-parts` | STEP 零件交换 | step,三维交换,零件格式,step文件 / find, evaluate, and download common purchasable cad parts from step.pa… | `domains/cad-3d/step-parts/SKILL.md` | 6.0K |
| `urdf` | URDF 机器人描述 | urdf,机器人,关节,ros,机械臂 / urdf robot description authoring and validation. | `domains/cad-3d/urdf/SKILL.md` | 9.2K |

> 读法：拿用户需求里的关键词去对「关键词」列，命中哪一行就拉哪个路径的 SKILL.md。

> **前置条件**：多数技能需要本机 Python 侧 CAD 内核（`cadquery` / `build123d` / `trimesh` 等），以及 `f3d` / `solid` 工具链。缺依赖时按 SKILL.md 里的安装段执行。
