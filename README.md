# Zhihuiya Patent Search Skill

Small GSD/Codex skill for searching Patsnap/Zhihuiya Analytics with `agent-browser`.

## Install

Copy this repository into your skills directory:

```bash
mkdir -p ~/.agents/skills
cp -R SKILL.md README.md scripts ~/.agents/skills/search-zhihuiya-patents/
```

The active skill file is `SKILL.md`. The optional helper script only builds encoded search URLs.

## Runtime Tools

- `npx` for `agent-browser`
- Python 3 for `scripts/build_search_url.py`
- `pdftotext` only when extracting seed metadata from a patent PDF

## Credentials

Provide credentials in the conversation when login is needed, or set:

```bash
export ZHIHUIYA_EMAIL='your-account'
export ZHIHUIYA_PASSWORD='your-password'
```

No account name, password, API token, browser cookie, or auth state is stored by this repo. The skill also tells agents not to save login state unless you explicitly ask.

## Examples

Build a patent-number search URL:

```bash
python scripts/build_search_url.py "CN117964767B"
```

Build a keyword search URL:

```bash
python scripts/build_search_url.py "关键词A 关键词B"
```

Build several narrow similar-patent searches:

```bash
python scripts/build_search_url.py \
  "抗体 药物偶联物 连接子" \
  "靶点 纳米颗粒 递送" \
  "融合蛋白 半衰期 延长"
```

Open any printed URL in the logged-in browser session:

```bash
npx -y agent-browser --session zhihuiya-patent-search open 'PRINTED_URL'
```

For similar-patent work, start from seed metadata, run 2-5 narrow queries, then de-duplicate by publication number or family. Report exact family/direct equivalents, close analogs, and broad background separately.
