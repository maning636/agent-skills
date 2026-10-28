# Update Flow — Git Repo vs Flat-File

## Decision Tree

```
Registry lookup: "hyperframes" → "heygen-com/hyperframes"
                          ↓
         Is ~/.kimi/skills/hyperframes/.git a directory?
                    ↓ yes               ↓ no
            GIT REPO PATH        FLAT-FILE PATH
```

## Git Repo Path

Used when the skill is a full git clone (has `.git/` directory).

```bash
SKILL_NAME="hyperframes"
SKILL_PATH="$HOME/.claude/skills/$SKILL_NAME"

# Check if .git exists
if [ -d "$SKILL_PATH/.git" ]; then
  cd "$SKILL_PATH"
  git fetch origin
  LOCAL_SHA=$(git rev-parse HEAD)
  REMOTE_SHA=$(git rev-parse origin/main)

  if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
    echo "有更新: 本地 $LOCAL_SHA → 远程 $REMOTE_SHA"
    # Confirm with user, then:
    git reset --hard origin/main
    echo "已更新"
  else
    echo "已是最新"
  fi
fi
```

Note: `origin/main` may be `origin/master` depending on the repo. Check both:
```bash
git fetch origin
git branch -r | grep -E "main|master"
```

## Flat-File Path

Used when the skill is a directory of files without a git repo.

```bash
OWNER="heygen-com"
REPO="hyperframes"
SKILL_PATH="$HOME/.claude/skills/hyperframes"

# Get latest commit SHA via gh api
if command -v gh &> /dev/null; then
  REMOTE_SHA=$(gh api repos/$OWNER/$REPO/commits --jq '.[0].sha')
else
  REMOTE_SHA=$(curl -s https://api.github.com/repos/$OWNER/$REPO/commits | python3 -c "import sys,json; print(json.load(sys.stdin)[0]['sha'])")
fi

# Get local file count as proxy for freshness (no SHA stored for flat-file)
LOCAL_FILES=$(find "$SKILL_PATH" -type f | wc -l)
echo "远程最新 SHA: $REMOTE_SHA"
echo "本地文件数: $LOCAL_FILES"
echo "请确认是否更新（直接覆盖）"
```

## Fetching Flat-File Skill from GitHub

Once confirmed, fetch all files:

```bash
OWNER="heygen-com"
REPO="hyperframes"
SKILL_PATH="$HOME/.claude/skills/hyperframes"
BRANCH="main"

# Get file tree
if command -v gh &> /dev/null; then
  FILE_LIST=$(gh api repos/$OWNER/$REPO/contents/skills/hyperframes --jq '.[].path')
else
  FILE_LIST=$(curl -s https://api.github.com/repos/$OWNER/$REPO/contents/skills/hyperframes | python3 -c "import sys,json; [print(item['path']) for item in json.load(sys.stdin)]")
fi

for FILE in $FILE_LIST; do
  mkdir -p "$(dirname $SKILL_PATH/$FILE)"
  curl -s "https://raw.githubusercontent.com/$OWNER/$REPO/$BRANCH/$FILE" -o "$SKILL_PATH/$FILE"
done
```

## Error Handling

| Situation | Action |
|-----------|--------|
| `gh api` rate limited | Fall back to `curl api.github.com` |
| `curl` also rate limited | Tell user "GitHub 限额，请稍后再试" |
| 404 on raw file | Log error, skip that file, continue |
| Network error | Report error, abort update |
| Not in registry | Tell user "xxx 未在注册表中，先添加到注册表" |