---
id: agent-toolkit/sandcastle-verify
domain: agent-toolkit
name: sandcastle-verify
description: 通过 Sandcastle 在隔离环境中验证代码变更。当你的 Claude Code 在某个环境写了代码，想让另一个 Claude 实例验证时使用。触发词："验证代码"/"sandcastle 验证"/"调用沙箱"/"verify with sandbox"
argument-hint: [项目路径] [验证范围: build|test|all]
origin: 本机自研
license: 见来源
---


# Sandcastle Verify — 跨环境代码验证

## 概念

你在环境 A 写了代码，调用 Sandcastle 在环境 B（隔离沙箱）验证。Sandcastle 会启动另一个 Claude Code 实例去执行验证任务。

## 前提条件

- Sandcastle 项目已部署在 `F:/sandcastle-main/`
- 目标项目有 `package.json` 和验证脚本（`build`, `test`, `typecheck`）

## 输入

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `PROJECT_PATH` | 要验证的项目路径 | 当前目录 |
| `SCOPE` | 验证范围 | `all` |

## 工作流程

### Phase 1: 准备验证

1. 确认 Sandcastle 已构建：`ls F:/sandcastle-main/dist/`
2. 确认目标项目存在且有 `package.json`
3. 创建验证 prompt

### Phase 2: 生成验证 Prompt

根据项目类型生成合适的验证 prompt：

```
# 验证任务

Project: {PROJECT_PATH}
Scope: {SCOPE}

## 验证步骤

1. 切换到项目目录
2. 安装依赖: npm install
3. 执行验证:
   - build: npm run build
   - test: npm run test
   - all: npm run typecheck && npm run build && npm run test

4. 报告结果

如果全部通过，输出:
<promise>VERIFIED</promise>

如果失败，输出具体错误信息。
```

### Phase 3: 执行沙箱验证

使用 noSandbox 模式直接在本地执行验证（无需 Docker）：

```typescript
// verify-project.ts
import * as sandcastle from "@ai-hero/sandcastle";
import { noSandbox } from "@ai-hero/sandcastle/sandboxes/no-sandbox";
import { readFileSync } from "fs";
import { resolve } from "path";

const projectPath = process.argv[2];
const scope = process.argv[3] || "all";

// 生成验证 prompt
const verifyPrompt = `# 验证任务

项目路径: ${projectPath}
验证范围: ${scope}

## 验证步骤

1. cd 到项目目录
2. 运行 npm install（如果 node_modules 不存在）
3. 根据验证范围执行:
   - build: npm run build
   - test: npm run test
   - typecheck: npm run typecheck
   - all: npm run typecheck && npm run build && npm run test

## 输出格式

成功时:
```
✅ Build: PASSED
✅ Tests: PASSED
<promise>VERIFIED</promise>
```

失败时:
```
❌ [检查项]: FAILED
错误详情:
...
```

## 注意

- 只读验证，不要修改任何文件
- 报告所有检查结果，即使部分通过
`;

async function main() {
  console.log(`\n🔍 Sandcastle Verify`);
  console.log(`   项目: ${projectPath}`);
  console.log(`   范围: ${scope}`);
  console.log();

  const result = await sandcastle.run({
    sandbox: noSandbox(),
    name: "Code Verifier",
    agent: sandcastle.claudeCode("claude-sonnet-4-6"),
    prompt: verifyPrompt,
    cwd: projectPath,
    maxIterations: 1,
  });

  console.log("\n=== 验证输出 ===\n");
  console.log(result.stdout);

  if (result.stderr) {
    console.log("\n=== 错误输出 ===\n");
    console.error(result.stderr);
  }

  const verified = result.stdout.includes("<promise>VERIFIED</promise>");
  console.log(`\n${verified ? "✅ 验证通过" : "⚠️ 验证未完成，请检查输出"}`);

  process.exit(verified ? 0 : 1);
}

main().catch((err) => {
  console.error("验证失败:", err);
  process.exit(1);
});
```

### Phase 4: 执行并报告

运行验证脚本，解析输出，给用户最终报告。

## 快捷命令

```bash
# 验证当前目录
npx tsx F:/sandcastle-main/.sandcastle/verify/run.ts $(pwd)

# 验证指定目录
npx tsx F:/sandcastle-main/.sandcastle/verify/run.ts /path/to/project all

# 快速验证 build
npx tsx F:/sandcastle-main/.sandcastle/verify/run.ts /path/to/project build
```

## 高级用法

### 使用 Docker 沙箱（完全隔离）

如果需要完全隔离的验证环境，使用 Docker 模式：

```typescript
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";

// 在 Docker 沙箱中验证
const result = await sandcastle.run({
  sandbox: docker({
    imageName: "sandcastle:local", // 需要预先构建的镜像
  }),
  agent: sandcastle.claudeCode("claude-sonnet-4-6"),
  prompt: verifyPrompt,
});
```

### 批量验证多个项目

```typescript
const projects = ["/path/to/proj1", "/path/to/proj2"];
const results = await Promise.all(
  projects.map((path) =>
    sandcastle.run({
      sandbox: noSandbox(),
      agent: sandcastle.claudeCode("claude-sonnet-4-6"),
      prompt: generatePrompt(path, "all"),
      cwd: path,
    })
  )
);
```

## 输出示例

```
🔍 Sandcastle Verify
   项目: /Users/me/my-project
   范围: all

=== 验证输出 ===

## 验证步骤

1. 切换到项目目录
2. npm install
   ✅ 依赖安装完成

3. npm run typecheck
   ✅ TypeScript 检查通过

4. npm run build
   ✅ 构建成功

5. npm run test
   ✅ 所有测试通过 (42/42)

<promise>VERIFIED</promise>

✅ 验证通过
```