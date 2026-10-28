# light-ocr 快速参考（中文 / Windows）

> 上游 SKILL.md 是权威文档（英文）。本文件是**本地补充**：本机实测环境 + Windows/PowerShell 写法 + 踩坑记录。
> 上游文档与本文件冲突时，以 SKILL.md 为准。

## 本机实测环境（2026-10-27 验证）

| 项 | 值 |
|---|---|
| 包 | `@arcships/light-ocr` v0.5.9，全局 npm |
| 安装路径 | `E:\npm-global\node_modules\@arcships\light-ocr` |
| 可执行文件 | `E:\npm-global\light-ocr.cmd`（`E:\npm-global` 已在用户 PATH） |
| 核心/模型 | core 0.5.9 / `ppocrv6-small-native-20260719.1`（small 档，50 种语言，18709 条词典） |
| 推理后端 | ONNX Runtime 1.24.4，`WebGpuExecutionProvider` 选中（D3D12） |
| 备选 | `--provider cpu` 可强制纯 CPU |
| Node | v24.21.0（要求 >= 22） |
| PDF | 支持（`light-ocr document info` → `pdfSupport: true`，PDFium 内置，**不要**另装） |

显存较小的机器（Pascal 架构，如 P1000）若 WebGPU 会话偶发失败，加 `--provider cpu` 兜底。

## Windows / PowerShell 常用命令

```powershell
# 整图转文字
light-ocr "C:\path\img.png" --format text

# 整图转 JSON（带坐标 + 置信度）
light-ocr "C:\path\img.png" --format json --schema-version 1

# 先检测文本区域（不识别，大图更快）
light-ocr detect "C:\path\img.png"

# 只识别某个区域（x,y,w,h，pageSpace 坐标）
light-ocr recognize "C:\path\img.png" --region 30,30,500,90 --format json

# PDF（可指定页码范围 / 渲染 DPI）
light-ocr "C:\path\doc.pdf" --format json
light-ocr "C:\path\doc.pdf" --pages 1-10 --format jsonl
light-ocr "C:\path\doc.pdf" --dpi 300 --format text

# 多图当一份文档
light-ocr document "a.png" "b.png" --format text

# 诊断（硬件 / 后端状态）
light-ocr doctor --json
light-ocr info --model-info
```

### PowerShell 注意

- 路径含空格 → 用**双引号**包裹：`light-ocr "D:\我的 图片\a.png"`
- 管道给 jq / python 时注意 PowerShell 5.1 默认按 GBK 解码，中文可能乱码；优先让 light-ocr 直接写文件再读：
  ```powershell
  light-ocr "a.png" --format json | Out-File -Encoding utf8 "C:\tmp\ocr.json"
  ```
- 批量循环用 PowerShell 语法（上游示例是 bash）：
  ```powershell
  Get-ChildItem *.png | ForEach-Object { light-ocr recognize $_.FullName --format jsonl }
  ```
- 管道中途 `Select-Object -First N` 会提前断流导致 exit code 1，属正常截断，**不是** OCR 失败。

## 坐标系统

- `box` 是 4 个点，`coordinateSpace: "pageSpace"`：原点在左上角，x 向右、y 向下，单位是**已应用 EXIF 方向后的像素**。
- `--region x,y,w,h` 与 `pageSpace` 同一坐标系，可直接把 json 里的 box 换算成 region 再局部重识别。
- `detect` 输出把 `lines` 换成 `detections[]`（`{ id, score, box }`），`structure` 变为 `"detect"`。

## 退出码

| 码 | 含义 | 处理 |
|---|---|---|
| 0 | 成功 | 解析 stdout |
| 64 | 用法错误 | 改命令 |
| 65 | 参数非法（region / format / schema） | 改参数 |
| 66 | 图片损坏 | 换图 |
| 67 | 能力不支持 | 看 `info --model-info` |
| 68 | 模型/包错误 | 重装包 |
| 69 | 资源超限 | 缩小图或用 `--region` |
| 70 | 环境/原生模块失败 | 查 native addon |
| 71 | 推理失败 | 重试或报 bug |
| 72 | 内部错误 | 报 bug |

**先看 exit code 再解析 stdout**——非 0 时 stdout 可能是空，真实原因在 stderr。

## 与多模态模型配合

多模态模型读图可能把小字/密集字读错或编造。流程：

1. 先 `light-ocr <img> --format text` 得到确定性结果；
2. 再与模型说法比对；
3. **不一致时以 OCR 的 `text` 字段为准**，不采信模型描述；
4. 置信度 < 0.5 时明确告知用户该区域不确定。

## 其他

- 完全离线运行，不联网、不上传任何图片。
- 换语言包 / 升级模型：见 `light-ocr info --model-info` 的 `modelBundleId`，模型由 npm 平台包自带，**不要**运行时去下载。
- 换机部署：`npm i -g @arcships/light-ocr`（Node >= 22），然后 `light-ocr doctor --json` 验证。
