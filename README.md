# Zhihuiya Patent Search and Disclosure Skill

Full GSD/Codex skill for Patsnap/Zhihuiya patent search, similar-patent analysis, patent mining, technical disclosure drafting, Word export, and disclosure iteration.

The skill keeps `search-zhihuiya-patents` as its public name for compatibility. Disclosure-generation workflow and tools are borrowed from `patent-disclosure-skill`, with prior-art search adapted to use Zhihuiya/Patsnap first.

## Install

Copy this repository into your skills directory:

```bash
mkdir -p ~/.agents/skills/search-zhihuiya-patents
cp -R SKILL.md README.md INSTALL.md LICENSE requirements.txt prompts scripts tests tools ~/.agents/skills/search-zhihuiya-patents/
```

## Runtime Tools

- `npx` for `agent-browser`
- Python 3 for URL building, Office conversion, Word export, and helper tools
- `pdftotext` when extracting seed metadata from patent PDFs
- Optional: `pip install -r requirements.txt` for Office conversion, math rendering, and `.docx` export
- Optional: `cd tools && npm install` for repeated Mermaid rendering
- Optional: `pip install -r tools/requirements-cnipa.txt && python -m playwright install chromium` for CNIPA fallback

## Credentials

Provide Zhihuiya credentials in the conversation when login is needed, or set:

```bash
export ZHIHUIYA_EMAIL='your-account'
export ZHIHUIYA_PASSWORD='your-password'
```

No account name, password, API token, browser cookie, or auth state is stored by this repo. The skill tells agents not to save login state unless you explicitly ask.

## Search Examples

Build a patent-number search URL:

```bash
python scripts/build_search_url.py "CN117964767B"
```

Build a keyword search URL:

```bash
python scripts/build_search_url.py "关键词A 关键词B"
```

Open a printed URL in the logged-in browser session:

```bash
npx -y agent-browser --session zhihuiya-patent-search open 'PRINTED_URL'
```

For similar-patent work, start from seed metadata, run 2-5 narrow Zhihuiya queries, then de-duplicate by publication number or family. Report exact family/direct equivalents, close analogs, and broad background separately.

## Disclosure Workflow

For 专利挖掘 / 技术交底书 / 查新 / disclosure drafting tasks, the skill runs:

1. intake
2. project scan, including `.docx` / `.pptx` conversion when needed
3. patent-point mining and fusion
4. Zhihuiya-first prior-art search, with CNIPA/WebSearch as fallback or corroboration
5. disclosure preview
6. disclosure drafting from templates
7. Mermaid + Word export
8. internal self-check

Generated disclosures should go under `outputs/{case}/` unless the user specifies another path. Final artifacts use `{案件名}_{YYYYMMDDHHmmss}.md` and matching `.docx`.

## Attribution

Disclosure prompts and tooling are borrowed from `patent-disclosure-skill` by handsomestWei under the MIT License. See `LICENSE`.
