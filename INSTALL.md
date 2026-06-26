# 安装说明

本技能根目录即包含 `SKILL.md` 的目录，技能名保持为 `search-zhihuiya-patents`。

## GSD / Codex

```bash
mkdir -p ~/.agents/skills/search-zhihuiya-patents
cp -R SKILL.md README.md INSTALL.md LICENSE requirements.txt prompts scripts tests tools ~/.agents/skills/search-zhihuiya-patents/
```

## Claude Code / Cursor 类 skills 目录

若宿主要求 `.claude/skills` 或 `.cursor/skills`，目录名也应使用 `search-zhihuiya-patents`，并保证 `SKILL.md` 位于该目录根级。

```bash
mkdir -p .claude/skills/search-zhihuiya-patents
cp -R SKILL.md README.md INSTALL.md LICENSE requirements.txt prompts scripts tests tools .claude/skills/search-zhihuiya-patents/
```

Cursor 全局路径示例：

- Windows: `%USERPROFILE%\.cursor\skills\search-zhihuiya-patents\`
- macOS / Linux: `~/.cursor/skills/search-zhihuiya-patents/`

## 可选依赖

基础转换和 Word 导出：

```bash
pip install -r requirements.txt
```

Mermaid 图示渲染：

```bash
cd tools
npm install
```

若 `mmdc` 报找不到 Chrome：

```bash
npx puppeteer browsers install chrome-headless-shell
```

CNIPA 官方公布公告 fallback：

```bash
pip install -r tools/requirements-cnipa.txt
python -m playwright install chromium
```

Zhihuiya 登录凭据仅通过对话或环境变量提供：

```bash
export ZHIHUIYA_EMAIL='your-account'
export ZHIHUIYA_PASSWORD='your-password'
```

不要保存账号、密码、cookie 或 browser state，除非用户明确要求。
