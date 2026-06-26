---
name: search-zhihuiya-patents
description: Automates Patsnap/Zhihuiya patent search, similar-patent analysis, patent mining, disclosure drafting, prior-art comparison, Word export, and disclosure iteration. Use when the user asks to search Zhihuiya, Patsnap, 智慧芽, patent analytics, patent keywords, applicants, inventors, publication numbers, 专利挖掘, 技术交底书, 查新, or patent disclosure work.
---

<objective>
Search patents on Patsnap/Zhihuiya Analytics and run a full patent-disclosure workflow when requested. This skill keeps Zhihuiya as the primary prior-art source, then reuses the disclosure drafting, Office conversion, Mermaid/Word export, iteration logging, and self-check workflow borrowed from `patent-disclosure-skill`.
</objective>

<essential_principles>
- **Zhihuiya first for prior art**: For disclosure work, run Zhihuiya/Patsnap searches before CNIPA or WebSearch. Use CNIPA as official-source fallback or corroboration, not the default first step.
- **One browser session**: Use one named `agent-browser --session zhihuiya-patent-search` after login. New sessions often lose auth and redirect to `account.zhihuiya.com`.
- **No credential persistence**: Do not store account names, passwords, tokens, cookies, browser state, or exported auth states in this skill. Use conversation-provided credentials or `ZHIHUIYA_EMAIL` / `ZHIHUIYA_PASSWORD`; never echo passwords.
- **Generated disclosures are artifacts, not repo content**: Save user outputs under `outputs/{case}/` unless the user specifies another path. Do not commit generated disclosures, converted Office markdown, screenshots, downloaded HTML, cookies, or auth state.
- **Borrowed workflow prompts are authoritative**: Before each disclosure step, read the mapped `prompts/*.md` file and follow it, with the Zhihuiya-first override in `prompts/prior_art_search.md`.
</essential_principles>

<quick_start>
For search-only tasks:

```bash
npx -y agent-browser --session zhihuiya-patent-search open https://analytics.zhihuiya.com/search/input/simple
npx -y agent-browser --session zhihuiya-patent-search wait --load networkidle
npx -y agent-browser --session zhihuiya-patent-search snapshot -i
```

For direct result URLs, use:

```bash
python scripts/build_search_url.py "关键词A 关键词B"
npx -y agent-browser --session zhihuiya-patent-search open 'PRINTED_URL'
```
</quick_start>

<credential_handling>
When login is required:

1. Prefer credentials already provided in the current conversation.
2. Otherwise, check `ZHIHUIYA_EMAIL` and `ZHIHUIYA_PASSWORD`.
3. If either value is missing, ask the user for the missing value(s).
4. Fill the account and password fields, check visible agreement boxes, click Login, and wait for return to `analytics.zhihuiya.com`.
5. If CAPTCHA, MFA, device verification, or account security challenge appears, stop and ask the user to complete it manually.
6. Do not persist credentials with `agent-browser auth save` or `state save` unless the user explicitly asks.
</credential_handling>

<routing>
Route directly from user intent:

| User intent | Procedure |
|---|---|
| Simple Zhihuiya search, patent number, keyword, applicant, inventor | Follow `<zhihuiya_search_workflow>` |
| Similar patents from a publication number, PDF, patent text, or seed technology | Follow `<similar_patent_workflow>` |
| 专利挖掘, 技术交底书, 交底书, 查新+成稿, disclosure drafting | Follow `<disclosure_workflow>` |
| Continue, revise, correct, merge, or supplement an existing disclosure draft | Follow `<iteration_workflow>` |
</routing>

<zhihuiya_search_workflow>
1. Open `https://analytics.zhihuiya.com/search/input/simple` in `zhihuiya-patent-search`.
2. Log in according to `<credential_handling>` if redirected.
3. Generate encoded result URLs mechanically. Prefer `python scripts/build_search_url.py "query"`; otherwise use `urllib.parse.quote`.
4. Run searches in the same logged-in session. After every navigation or dynamic page update, run a fresh `snapshot -i`; old refs are invalid.
5. Extract visible results with `get text body`; if it is empty, only says `T`, or has no publication numbers after a result-count page loads, wait 2 seconds, re-open the same URL in the same session, and retry once.
6. Return Markdown with query, source, searched date, visible count, and visible result rows. State limits such as "top 10 visible results" or "detail pages not opened."
</zhihuiya_search_workflow>

<similar_patent_workflow>
1. If the user gives a PDF or filename, locate it from the workspace and extract seed text, e.g. `pdftotext -layout /path/to/patent.pdf - | sed -n '1,220p'`.
2. Extract title, abstract, independent claims, assignee/applicant, inventors, dates, IPC/CPC, publication/application numbers, family clues, and distinctive claim nouns.
3. Search the exact publication number first to anchor the family.
4. Run 2-5 narrow Zhihuiya queries from claim terms, target, molecule/modality, carrier/scaffold, application, mechanism, or manufacturing step. Use one logged-in session for all queries.
5. For each query, capture visible count and first-page rows, then move on. Do not spend more than one retry or one optional detail-row open on a single query unless the user asks for deep analysis.
6. De-duplicate by publication number and family. Separate seed family/direct equivalents, close technical analogs, and broad background patents.
7. State query set, de-duplication rule, and visible-result limits.
</similar_patent_workflow>

<disclosure_workflow>
Run the borrowed disclosure workflow, but make Step 5 Zhihuiya-first:

1. Read `prompts/intake.md` and collect the minimum missing input.
2. Read `prompts/project_scan.md`; if the scan scope contains `.docx` or `.pptx`, convert first with `tools/docx_to_md.py` or `tools/pptx_to_md.py`, then read the Markdown outputs.
3. Read `prompts/patent_points_analyzer.md`; identify candidate patent points, merge related points, and select the disclosure target.
4. Read `prompts/prior_art_search.md`; run Zhihuiya prior-art search first, then optional CNIPA/WebSearch fallback or corroboration.
5. Read `prompts/disclosure_preview.md`; provide the summary preview unless the user explicitly skips it.
6. Read `prompts/disclosure_builder.md` and `prompts/template_reference.md`; draft the disclosure with desensitization, fenced Mermaid for section 3.2 and 3.4, and required formula style.
7. Render final artifacts with `tools/mermaid_render.py`, producing `{case}_{YYYYMMDDHHmmss}.md` and matching `.docx`.
8. Read `prompts/disclosure_self_check.md`; internally fix logic, formula, parameter, citation, and format issues before final delivery. Do not add a self-check section to the disclosure body.
</disclosure_workflow>

<iteration_workflow>
When the user is continuing from an existing disclosure or asks to correct, merge, supplement, or revise:

1. Read `prompts/iteration_context.md`.
2. Read `prompts/merger.md` for new material or expansion, or `prompts/correction_handler.md` for factual/style corrections.
3. Save a new timestamped `.md` and `.docx`; do not overwrite the previous draft unless the user explicitly asks.
4. Append `交底书修订对话记录.md` using `tools/iteration_dialog_log.py` or the same structure manually.
5. Output the required merge or correction summary.
</iteration_workflow>

<tooling>
- Basic Python dependencies: `pip install -r requirements.txt`
- Optional CNIPA fallback: `pip install -r tools/requirements-cnipa.txt && python -m playwright install chromium`
- Mermaid rendering: run `npm install` in `tools/` when repeated rendering matters; otherwise `mermaid_render.py` can fall back to `npx`.
- Word export and Office conversion tools are in `tools/`; detailed usage is in `tools/README.md`.
</tooling>

<output_format>
For search-only work:

```markdown
Query: ...
Source: Patsnap/Zhihuiya Analytics
Searched: YYYY-MM-DD
Visible count: ...

| # | Title | Number | Applicant/Assignee | Date | Notes |
|---|---|---|---|---|---|
```

For disclosure work, deliver the generated `.md` and `.docx` paths, plus a concise summary of search sources, closest prior art, and any remaining user decisions.
</output_format>

<anti_patterns>
- Do not claim a Zhihuiya search is exhaustive when only visible rows were extracted.
- Do not split logged-in searches across new `agent-browser --session ...` sessions.
- Do not conclude "no results" from a truncated snapshot or collapsed terminal output; retry `get text body` or save it to a file.
- Do not manually encode Chinese query URLs.
- Do not store credentials, cookies, auth states, generated disclosures, or downloaded result pages in git.
- Do not run the CNIPA-first path from the borrowed skill before Zhihuiya in this fork.
- Do not put a self-check checklist into the final disclosure body.
</anti_patterns>

<success_criteria>
- Search tasks return visible Zhihuiya results with query, date, count/limits, metadata, and source limits.
- Similar-patent tasks anchor the exact family, run focused query sets, de-duplicate, and separate close analogs from broad background.
- Disclosure tasks produce timestamped `.md` and `.docx` artifacts, include Zhihuiya-first prior-art analysis, and pass internal self-check.
- Iteration tasks preserve prior drafts, create new timestamped artifacts, and append revision logs.
</success_criteria>
