---
id: agent-toolkit/skill-update
domain: agent-toolkit
name: skill-update
description: |
  Update locally installed skills and plugins from GitHub. Use when: (1) user says "更新技能" / "更新插件" / "更新所有技能", (2) user asks "检查更新", (3) user wants to list registered skills or plugins, (4) user wants to know if a skill has a newer version on GitHub. Do NOT use for installing new skills — only for updating skills already in the registry.
origin: 本机自研
license: 见来源
---


# Skill Update

Manage and update skills and plugins registered in the local system.

## Commands

### 列出已注册技能
Read `~/.kimi/skills-registry.json` and display all registered skills with their GitHub sources.

```bash
cat ~/.kimi/skills-registry.json
```

### 列出已注册插件
Read `~/.kimi/plugins-registry.json` and display all registered plugins.

```bash
cat ~/.kimi/plugins-registry.json
```

### 检查更新
Check if any registered skill or plugin has a newer version on GitHub. Use `gh api` if available (authenticated = higher rate limit), fall back to `curl api.github.com`.

**Git repo check (has `.git/`):**
```bash
cd ~/.kimi/skills/{skill-name}
git fetch origin
git rev-parse HEAD              # local
git rev-parse origin/main       # remote
```

**Flat-file check:**
```bash
gh api repos/{owner}/{repo}/commits --jq '.[0].sha'
```

Compare with locally stored SHA. Report each entry with a status.

### 更新技能 {name}
Update a specific skill by name.

**Step 1 — Read registry:**
```bash
SKILL_NAME="hyperframes"
jq -r ".$SKILL_NAME" ~/.kimi/skills-registry.json
```

**Step 2 — Check if it's a git repo:**
```bash
if [ -d "~/.kimi/skills/$SKILL_NAME/.git" ]; then
  # git pull
  cd ~/.kimi/skills/$SKILL_NAME
  git fetch origin && git reset --hard origin/main
else
  # flat-file: fetch from GitHub
  # use gh api to get file tree, then curl each file
fi
```

**Step 3 — Confirm local files changed:**
```bash
ls ~/.kimi/skills/$SKILL_NAME/SKILL.md
echo "更新完成: $SKILL_NAME"
```

### 更新插件 {name}
Same as above but for `~/.kimi/plugins/` and `~/.kimi/plugins-registry.json`.

### 更新所有技能
Loop through all entries in `~/.kimi/skills-registry.json`. For each:
1. Check for updates (git fetch or gh api)
2. If update available, ask user: `"${name} 有新版本，是否更新？(y/n)"`
3. If yes, pull/fetch and overwrite
4. Report final status

### 更新所有插件
Same for plugins.

## Registry Format

Both registries use the same JSON format:

```json
{
  "skill-name-or-plugin": "author/repo"
}
```

Example:
```json
{
  "hyperframes": "heygen-com/hyperframes",
  "website-to-hyperframes": "heygen-com/hyperframes",
  "superpowers": "obra/superpowers"
}
```

**Always confirm with the user before overwriting files.** The update is destructive — no backup is made.

## GitHub API Notes

- Use `gh api` if `gh` CLI is installed (authenticated, 5000 req/hr)
- Fall back to `curl https://api.github.com/repos/{owner}/{repo}/commits` (unauthenticated, 60 req/hr)
- For flat-file skills, fetch individual files via `raw.githubusercontent.com`
- Store the last known SHA in the registry file for comparison:

```json
{
  "hyperframes": {
    "repo": "heygen-com/hyperframes",
    "path": "skills/hyperframes",
    "lastSha": "abc123"
  }
}
```

Wait — actually keep it simple. The registry is just `"name": "author/repo"` (simple format). SHA comparison is done at runtime via GitHub API.

## Anti-patterns

- Do NOT install a skill that isn't in the registry
- Do NOT overwrite without asking for confirmation first
- Do NOT make backups — per user instruction, direct overwrite is intentional
- Do NOT skip the "check update" step when user just says "更新 xxx" — always confirm first

## References

- [update-flow.md](references/update-flow.md) — detailed git vs flat-file branching logic
- [registry-format.md](references/registry-format.md) — full registry JSON schema