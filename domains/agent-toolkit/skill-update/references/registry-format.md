# Registry format for skill-update skill

## Format

`~/.kimi/skills-registry.json` — simple key-value map:

```json
{
  "skill-dir-name": "owner/repo[:path]"
}
```

The `path` part is optional — only needed when the skill lives in a subdirectory of the repo (e.g., `skills/hyperframes`).

## Field Details

| Field | Required | Description |
|-------|---------|-------------|
| `owner/repo` | Yes | GitHub shorthand (e.g., `heygen-com/hyperframes`) |
| `path` | No | Repo sub-path to the skill (e.g., `skills/hyperframes`) |

**Path defaults:** if no `:` path is specified, the skill path is assumed to be the skill directory name within the repo.

## Examples

```json
{
  "hyperframes": "heygen-com/hyperframes",
  "website-to-hyperframes": "heygen-com/hyperframes",
  "hyperframes-cli": "heygen-com/hyperframes",
  "agent-reach": "Panniantong/Agent-Reach",
  "officecli": "iOfficeAI/OfficeCLI"
}
```

For `hyperframes` — skill lives in `heygen-com/hyperframes/skills/hyperframes/`:
```json
{
  "hyperframes": "heygen-com/hyperframes:skills/hyperframes"
}
```

## Updating the Registry

**Add a new entry:**
```bash
jq ". + {\"new-skill\": \"owner/repo\"}" ~/.kimi/skills-registry.json > /tmp/reg.tmp && mv /tmp/reg.tmp ~/.kimi/skills-registry.json
```

**Remove an entry:**
```bash
jq "del(.\"skill-name\")" ~/.kimi/skills-registry.json > /tmp/reg.tmp && mv /tmp/reg.tmp ~/.kimi/skills-registry.json
```

**List all:**
```bash
cat ~/.kimi/skills-registry.json | jq 'keys[]'
```

## Path Detection Logic

When updating, the skill finds the skill files in the repo by:

1. Default: `{owner}/{repo}/{skill-name}/` (e.g., `heygen-com/hyperframes/hyperframes/`)
2. With explicit path: `{owner}/{repo}/{path}/` (e.g., `heygen-com/hyperframes/skills/hyperframes/`)
3. Fetch all files recursively via `gh api repos/{owner}/{repo}/git/trees/{sha}` with `recursive=1`

## Git Repo Detection

Local skills that have `.git/` in their directory are treated as git clones:
- Update via `git fetch && git reset --hard origin/main`
- SHA comparison uses `git rev-parse HEAD` vs `git rev-parse origin/main`

Currently detected git repos in `~/.kimi/skills/`:
- `hyperframes-src` → full monorepo clone (heygen-com/hyperframes)

All others are flat-file skills (no `.git/`).