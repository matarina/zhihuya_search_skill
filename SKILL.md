---
name: search-zhihuiya-patents
description: Automates Patsnap/Zhihuiya patent search with agent-browser, including login, simple patent queries, and visible result extraction. Use when the user asks to search Zhihuiya, Patsnap, 智慧芽, patent analytics, patent keywords, applicants, inventors, or publication numbers on analytics.zhihuiya.com.
---

<objective>
Search patents on Patsnap/Zhihuiya Analytics at `https://analytics.zhihuiya.com/search/input/simple` using `agent-browser`. Handle login, run simple searches, and return visible patent results in a concise structured summary.
</objective>

<credential_handling>
Do not store account names, passwords, tokens, cookies, or exported auth states in this skill.

When login is required:

1. Prefer credentials already provided in the current conversation.
2. Otherwise, check environment variables `ZHIHUIYA_EMAIL` and `ZHIHUIYA_PASSWORD`.
3. If either value is missing, ask the user for the missing value(s) before logging in.
4. Never echo the password in final output, logs, summaries, or generated files.
5. Do not persist credentials with `agent-browser auth save` unless the user explicitly asks for saved login.
</credential_handling>

<quick_start>
Use one named session for the whole task. Do not open parallel sessions unless each one is logged in.

```bash
npx -y agent-browser --session zhihuiya-patent-search open https://analytics.zhihuiya.com/search/input/simple
npx -y agent-browser --session zhihuiya-patent-search wait --load networkidle
npx -y agent-browser --session zhihuiya-patent-search snapshot -i
```
</quick_start>

<seed_document_handling>
If the user gives a patent PDF or only a filename:

1. Do not assume the PDF is inside this skill directory. Locate it from the workspace first, e.g. `rg --files /mnt/data3/mxw | rg '/[^/]+\\.pdf$'`.
2. Extract seed text before searching:
   `pdftotext -layout /path/to/patent.pdf - | sed -n '1,220p'`
3. Pull out title, abstract, independent claims, assignee/applicant, inventors, priority/application/publication dates, IPC/CPC, publication/application numbers, family clues, and distinctive claim terms.
4. Use the extracted metadata to seed the query set: exact number first, then 2-5 narrow technical phrases from claim nouns, target, composition, mechanism, carrier/scaffold, use case, or manufacturing step.
5. Watch for ambiguous abbreviations, English common words used as technical terms, and machine-translated titles. Check the original title/abstract and technical context before accepting or rejecting a hit.
</seed_document_handling>

<workflow>
1. Open `https://analytics.zhihuiya.com/search/input/simple` with a named session, usually `zhihuiya-patent-search`.

2. If redirected to `account.zhihuiya.com` or a Patsnap login page:
   - Use the Account tab if it is not already selected.
   - Get credentials according to `<credential_handling>`.
   - Fill the email field with the provided email/account.
   - Fill the password field with the provided password.
   - Check "Keep me logged in" if visible.
   - Check the "User Agreement" / "Privacy Policy" agreement checkbox if visible and unchecked.
   - Click Login.
   - If a second modal with "Agree" appears, click "Agree".
   - Wait for network idle or for the URL to return to `analytics.zhihuiya.com`.
   - If CAPTCHA, MFA, device verification, or account security challenge appears, stop and ask the user to complete it manually.

3. After every navigation, click, form submission, filter change, or dynamic page update, run a fresh `snapshot -i`; old refs are invalid after page changes.

4. Run the user's requested simple search:
   - Fast path for repeatable keyword/publication searches: open the result URL directly in the logged-in session:
     `https://analytics.zhihuiya.com/search/result/tablelist/1?sort=sdesc&limit=100&q={urlencoded query}&_type=query&search_mode=publication`
   - Generate `{urlencoded query}` mechanically, especially for Chinese. Do not hand-type percent encoding:
     - If available in the skill directory, use `python scripts/build_search_url.py "关键词A 关键词B"` and open the printed URL with `agent-browser open`.
     - Otherwise use the stdlib one-liner: `python -c 'from urllib.parse import quote; print(quote("关键词A 关键词B"))'`
   - UI path from `/search/input/simple`: click the contenteditable search box, use `keyboard inserttext`, then click Search. `fill` may not work because the input is not a normal textbox.
   - For keyword queries, enter the user's exact search phrase unless they ask for query expansion.
   - For similar-patent work, run 2-5 narrow queries rather than one broad query. Prefer narrow combinations such as target + molecule/modality + carrier/scaffold/application/manufacturing step.
   - For applicants, inventors, publication numbers, or application numbers, use the matching field/filter when the UI exposes one; otherwise use the main simple-search box.
   - Submit with the visible Search button or Enter, then wait for results.

5. Extract visible results from the results page:
   - Patent title
   - Publication or application number
   - Applicant/assignee when visible
   - Inventor when visible
   - Publication/application date when visible
   - Abstract, snippet, or highlighted match text when visible
   - Detail-page URL when available
   - Use `get text body` after the result page loads; it exposes table rows more reliably than `snapshot -i`.
   - If `snapshot -i` omits titles or numbers, do not assume no results. Use `get text body`, a screenshot, or open the detail row.
   - If the terminal/UI truncates output, redirect the full page text to a file and inspect that file:
     `npx -y agent-browser --session zhihuiya-patent-search get text body > /tmp/zhihuiya-results.txt`

6. Return results as Markdown. Include the search query, date searched, result count if visible, and up to the user's requested number of results. If the user does not specify a count, return the top 10 visible results.
</workflow>

<command_patterns>
- Correct: `npx -y agent-browser --session zhihuiya-patent-search get text body`
- Wrong: `npx -y agent-browser --session zhihuiya-patent-search 'get text body'`
- Correct JavaScript extraction for complex pages:

```bash
npx -y agent-browser --session zhihuiya-patent-search eval --stdin <<'JS'
JSON.stringify(
  Array.from(document.querySelectorAll('body *'))
    .map(e => e.textContent && e.textContent.trim())
    .filter(Boolean)
    .slice(0, 200)
)
JS
```

Use `eval --stdin` for multiline or quote-heavy JavaScript. Avoid inline JS with reused `let` names or nested shell quotes.
</command_patterns>

<similar_patent_workflow>
When searching similar patents from a seed patent or PDF:

1. Extract the seed title, abstract, independent claims, assignee/applicant, inventors, dates, IPC/CPC classes, publication/application numbers, family clues, and distinctive claim nouns first.
2. Search the exact publication number to anchor the family and confirm Patsnap metadata.
3. Run narrow concept queries from the claims, for example target + molecule/modality + carrier/scaffold/application. Prefer several focused 2-4 term queries over one broad query.
4. De-duplicate by publication number and family. Treat continuations, equivalents, translations, and same-priority publications as one family unless the user asks for every publication.
5. Separate:
   - seed family or direct equivalents,
   - close technical analogs,
   - broader background patents.
6. State the query set used, de-duplication rule, and visible-result limits in the final answer.
</similar_patent_workflow>

<output_format>
Use this compact format:

```markdown
Query: ...
Source: Patsnap/Zhihuiya Analytics
Searched: YYYY-MM-DD
Visible count: ...

| # | Title | Number | Applicant/Assignee | Date | Notes |
|---|---|---|---|---|---|
| 1 | ... | ... | ... | ... | ... |
```

Add links below the table only when the URLs are too long for the table.
</output_format>

<anti_patterns>
- Do not claim the search is exhaustive if only visible page results were extracted.
- Do not use stale element refs after a page update.
- Do not split one task across new `agent-browser --session ...` sessions after login; new sessions usually lose auth and redirect to the login page.
- Do not conclude "no results" from a truncated snapshot or collapsed terminal artifact. Confirm with `get text body` saved to a file.
- Do not manually encode Chinese query URLs; a single wrong character changes the search.
- Do not switch to a headful browser/Puppeteer flow unless it is already available. The headless `agent-browser` path is enough.
- Do not download exports or PDFs unless the user explicitly asks; this v1 skill is search and visible extraction only.
- Do not include account names or passwords in final user-facing output unless the user explicitly asks for account confirmation; never include passwords.
</anti_patterns>

<success_criteria>
- The browser reaches the simple search page or stops on a user-action-required security challenge.
- The requested search is submitted with the user's query unchanged unless they ask otherwise.
- Visible results are summarized with titles, numbers, key metadata, snippets, and links when available.
- The final answer states any limits, such as "top 10 visible results" or "detail pages not opened."
</success_criteria>
