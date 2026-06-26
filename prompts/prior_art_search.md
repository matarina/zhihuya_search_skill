# 联网检索查新（Step 5，Zhihuiya 优先）

## 必做时机

生成交底书全文**之前或生成过程中**必须执行；检索结论写入第一章 **1.1 现有技术** 及与本案的**区别论述**。

## 检索渠道（**优先 Zhihuiya/Patsnap，再用国知局或 WebSearch 补充**）

### A. Zhihuiya / Patsnap（**优先**）

1. **站点**：`https://analytics.zhihuiya.com/search/input/simple` 与结果页 `analytics.zhihuiya.com/search/result/tablelist/...`。
2. **会话**：始终使用同一个登录会话：`npx -y agent-browser --session zhihuiya-patent-search ...`。若重定向到 `account.zhihuiya.com`，按 `SKILL.md` 的 `credential_handling` 登录；不得保存账号、密码、cookie 或 auth state。
3. **检索词（生成阶段必做，须在拼 URL 之前完成）**
   - 先搜精确公开号 / 申请号锚定同族。
   - 再从本案技术方案、专利点或用户主题中归纳 **2～8 个相关度高的语义块**，分别检索；每个语义块宜为 **2～5 个词**。
   - 优先组合：核心技术对象 + 目标/用途、关键结构/模块 + 方法动作、靶点/材料/载体/支架/制备步骤、关键效果或应用场景。
   - 不要把无空格的一整句长中文当作唯一查询，也不要拆成单字或泛词。
4. **执行方式**：

   ```bash
   python scripts/build_search_url.py "词块"
   npx -y agent-browser --session zhihuiya-patent-search open 'PRINTED_URL'
   npx -y agent-browser --session zhihuiya-patent-search wait --load networkidle
   npx -y agent-browser --session zhihuiya-patent-search get text body
   ```

   若 `scripts/build_search_url.py` 不在当前目录，用 `urllib.parse.quote` 机械编码；不要手写中文百分号编码。

5. **抽取与重试**：
   - 每轮记录查询词、可见结果数、Patsnap families/total、是否打开详情页。
   - 全流程交底书任务中，将每轮记录同步写入用户输出目录下的 **`search_log.md`**；若用户未给输出目录，写入 `outputs/{case}/search_log.md`。该文件只记录检索证据和限制，不记录账号、密码、cookie、auth state 或原始浏览器状态。
   - 若 `get text body` 为空、仅为 `T`、或已显示结果数但无公开号，等待 2 秒、在同一会话重新打开同一 URL 并重试一次。
   - 多查询查新时，每个查询抽取可见计数和第一页结果后继续下一查询；除非用户要求深挖，不要在单一结果页循环。
6. **合并责任在 Agent**：按公开号和 Patsnap family 去重，分为 **种子同族/直接等同**、**近似技术方案**、**宽泛背景技术**。不要声称穷尽检索，除非实际完成多页和详情页审阅。
7. **写入要求**：查新笔记和 1.1 应写明 Zhihuiya/Patsnap、检索日期、关键词组合、可见结果限制、最接近现有技术、公开号、申请人、方案概括、与本案差异。

8. **检索日志模板**（`search_log.md`，全流程交底书任务必填）：

   ```markdown
   # Prior-Art Search Log

   Source: Zhihuiya/Patsnap first; CNIPA/Google Patents only as noted
   Searched: YYYY-MM-DD
   Seed: ...

   | Query | Result URL | Visible count | Families/total | First-page publication numbers | Detail/fallback limit |
   |---|---|---:|---|---|---|
   | CN... | ... | ... | ... | ... | exact family |

   ## Grouped Findings
   - Seed family/direct equivalents: ...
   - Close analogs: ...
   - Broad background: ...

   ## Limits
   - ...
   ```

### B. 中国专利公布公告（官方补充 / fallback）

当需要官方公布公告佐证、Zhihuiya 不可用、Zhihuiya 结果不足、或用户明确要求官方源时，使用本节。

1. **站点**：[国家知识产权局 中国专利公布公告](http://epub.cnipa.gov.cn/)（**仅** `epub.cnipa.gov.cn`）。
2. **工具**（本仓库 `tools/`）：**`cnipa_epub_search.py`** —— **一步**完成公布站检索与结果解析（Playwright 过站点 WAF）；结果页 HTML **仅在内存中处理，不落盘**。成功时终端含 **`EPUB_NOTE:`**（ASCII，如 `html_bytes=… disk=0`）与 **`EPUB_HITS_JSON:`** 一行（JSON 数组：标题、公开号、链接、**`abstract`** 等）。
3. **国知局检索词（生成阶段必做，须在拼 Bash 之前完成）**

   - **拆分责任在 Agent**：在**生成/构造命令阶段**，从本案技术方案、专利点或用户主题中归纳 **2～8 个与方案相关度高的检索单位**，**仅用 ASCII 空格分隔**，再写入 `cnipa_epub_search.py` 的参数。每一单位宜为 **有检索意义的语义块**，例如：**专业术语**、**名词短语**、**名动组合（如「批量调度」「异构调度」）**、**业内固定搭配**；**不要**拆成过碎的单字、泛义双字（如单独 `检索`、`增强`、`系统`、`方法` 等泛词），也**不要**把无关联词硬凑成一串。
   - **禁止**把**无空格的一整句长中文**当作**唯一**参数（例如不要：`".../cnipa_epub_search.py" "知识库检索增强大语言模型"`）。长串在公布站单框内易被当作整句 AND，**极易 0 条**。
   - **Agent 执行时**：**每一轮 `Bash` 只传一个**检索单位（一个词块一句参数）；**2～8 个单位须对应 2～8 次**独立调用，**禁止**在一次工具调用里把多个词块同时作为多个 argv 传给 `cnipa_epub_search.py`（脚本虽支持多词单次进程内合并，**仅供本地/人工**；Agent 为控时、降单次 Playwright 链路与 IDE/终端超时风险，**必须**拆进程）。
   - 示意（须按本案替换；**三次调用、每次一词**）：

     ```bash
     python3 …/cnipa_epub_search.py 知识库
     python3 …/cnipa_epub_search.py 检索增强
     python3 …/cnipa_epub_search.py 大语言模型
     ```

   - **脚本不做**自动分词或自动拆长中文；若确需**整句一次** AND 检索，改用 **`cnipa_epub_crawler.py`** 单传一句。

4. **执行方式**（Step 5 在读完本文件后**先尝试**）：

   ```bash
   pip install -r tools/requirements-cnipa.txt
   python -m playwright install chromium
   # Agent：对上一节每个检索单位各执行一次（示例仅展示首轮）
   python3 ${CLAUDE_SKILL_DIR}/tools/cnipa_epub_search.py 词甲
   ```

   - **合并责任在 Agent**：每次调用解析 **stdout** 上**唯一一行** **`EPUB_HITS_JSON:`** 后的 JSON 数组；在推理中按 **`pub_number`** 为主键去重合并（无则 **`link`**，再否则可用标题前缀），得到**一份**总表后再写入查新笔记与 1.1。
   - **`cnipa_epub_search.py`** 若人工单次传入多词，会按空白拆段、进程内**一段一查**并去重（**stderr** 可出现 **`EPUB_MERGE:`**）；与 Agent **分多次调用**策略无关。
   - 成功时 **stdout 仅一行** **`EPUB_HITS_JSON:`** + JSON 数组（UTF-8，含中文 `abstract`）；**`EPUB_MERGE:`** / **`EPUB_NOTE:`** / **`EPUB_HINT:`** 等在 **stderr** 且为 **ASCII**（减轻 PowerShell 把中文 stderr 当成错误流）。解析命中时请以 **stdout 该行 JSON 为准**，勿因 stderr 或终端编码误判「未命中」而不必要地降级 WebSearch。Windows 乱码与 PowerShell 注意见 **`INSTALL.md`**（`chcp 65001` / `PYTHONUTF8=1`、勿滥用 `2>&1`）。
   - 将 JSON 中**可核验**的公开号、标题、**国知局站点内详情链接**写入查新笔记与 1.1（见下 **`abstract` 必用**）。
   - **继续补充条件**（满足任一则进入 **C**）：命令非 0 退出、超时、无 Playwright、**`EPUB_HITS_JSON` 为空数组**、或条目经人工核对明显与主题无关。

5. **`abstract` 字段（国知局条目，规定必用）**

   若 **`EPUB_HITS_JSON`** 中某项含非空的 **`abstract`**（解析自公布站结果页摘要），对**该条专利**须同时遵守：

   - **必用**：查新笔记、交底书 **1.1** 中对该专利的**技术方案概括、应用场景与局限性分析**，**必须先基于对该 `abstract` 的完整阅读与理解**后再撰写；**禁止**仅凭标题、公开号或 URL **臆造**方案要点或与摘要矛盾的表述。
   - **充分理解**：在写入 1.1 或查新笔记前，Agent 须在**推理过程内**明确：摘要所涉**技术领域、解决什么问题、核心手段/模块、主要效果或流程**；若摘要与标题存在差异，**以摘要为准**概括该技术。
   - **正文呈现**：交底书 1.1 中**不得**大段逐字粘贴官方摘要（避免抄袭与超字数）；应**消化后**用**自己的话**压缩为「方案概括 + 应用 + 缺点/局限」；查新笔记可保留稍长的摘录供自用核对，但须标注来源于公布站摘要。
   - **缺失时**：若某条 JSON **无** `abstract` 或为空（旧版页面 / 表格布局未解析到等），须在查新笔记中注明「该条无摘要字段」，并改用**详情页**或 **Google Patents** 等可核验来源补全理解后再写 1.1，**不得**留空理由含糊带过。

6. **链接与著录**：国知局详情 URL 以脚本输出为准；**禁止编造**；若仅能从公布站得到公开号，可再配 **Google Patents** 稳定页 `https://patents.google.com/patent/CN…/en` 作为**补充**公开源（仍须打开校验）。

### C. Google 学术与 Google Patents（降级 / 补充）

在 Zhihuiya 与国知局结果不足、不可用，或需要非中国公开资料时启用：

1. **中文文献与学术**：[Google 学术搜索](https://scholar.google.com)（`scholar.google.com`）。
   - 用**中文关键词**、技术方案核心术语、应用场景；可组合 2–3 组查询。
   - 强化「中国」语境时可加：`中国`、`site:.cn`、`专利`、`CN`（与专利号区分使用）等，以实际命中为准。
   - 通过 **WebSearch** 或浏览器可用能力检索 Scholar；结果中优先选用**可打开、与标题/作者匹配**的条目链接。
2. **中国专利公开文献（补充）**：[Google Patents](https://patents.google.com/) 检索中文标题、申请人或公开号（`CN…A` / `CN…B` 等），每条使用**稳定著录页 URL**。
3. **其它来源**：英文文献、非中国专利等可继续用 Google Patents、出版社页面、DOI、arXiv 等 + WebSearch。
4. **关键词构造**：技术方案核心术语、应用场景与方法名称，可组合 2–3 组查询。

## 分析要求

对检索到的、与方案**高度相关**的现有专利或公开文献逐项概括：

- 专利号 / 文献标识
- 技术方案要点（**若为国知局 JSON 且含 `abstract`，要点须与摘要理解一致**，见上文「`abstract` 必用」）
- 应用场景
- **局限性**
- **公开源 URL（必填）**：每一条必须附带**至少一个可公开访问、与著录项一致**的链接，写入查新笔记与交底书 1.1，便于代理人复核。**禁止编造或猜测 URL**；写入前应在浏览器中打开确认页面可访问且对应同一文献/专利。

### 链接来源与格式（须准确）

| 类型 | 推荐 URL 形式 | 说明 |
|------|----------------|------|
| 美国等专利（公开出版物号） | `https://patents.google.com/patent/US20240118920A1/en` | 将 `US20240118920A1` 替换为实际公开号；以 Google Patents 页面能打开且标题/摘要匹配为准。 |
| 中国专利 | **`https://patents.google.com/patent/CNXXXXXXXXXA/en`**（或对应 B 型等） | 可用 Zhihuiya/Patsnap 著录、国知局公布站或 Google Patents 稳定著录页复核；勿依赖易过期的检索会话 URL。 |
| 学术论文（含 Scholar） | Scholar 条目页、出版社官方页或 **`https://doi.org/10.xxxx/...`** | Scholar 链接若重定向或镜像，以最终可长期解析的 DOI/出版社页为准。 |
| arXiv 预印本 | `https://arxiv.org/abs/2008.09213` | `abs` 页为规范条目页；勿用未经验证的镜像域名冒充官方。 |
| 期刊 / 会议 | 出版社 DOI：`https://doi.org/10.xxxx/...` 或官方摘要页 | 以 DOI 解析后页面与文献一致为准。 |

文末给出：**检索总结**与**本发明与现有技术的本质区别**，与 1.1 结尾及 1.2 缺点呼应。

## 记录习惯

便于写进交底书：保留专利号、标题、**消化摘要后的**一两句方案概括（有 **`abstract`** 时概括须可追溯至该摘要）；**每条另起一行或表格列给出「来源 URL」**。避免大段抄袭权利要求或整段粘贴官方摘要。

### 1.1「检索说明」写法（交付正文，必遵）

写入交底书 **1.1** 开头的「检索说明」时，面向**代理人/审查员**表述，**不要**暴露 Agent 查新流程或本仓库工具实现。

- **须写**：实际使用的**数据库或公开渠道名称**（如「智慧芽/Patsnap 专利数据库」「国家知识产权局专利公布公告系统」「Google Patents」）、本案**主要检索词**（与 Step 5 用词一致或概括）；若部分条目经 **Google Patents** 等公开页复核著录项，可一句带过。
- **禁止写入 1.1 正文**：脚本/文件名（如 **`cnipa_epub_search.py`**、**`cnipa_epub_crawler.py`**）、「查新优先使用…检索工具」「是否触发 Google 学术降级」、Playwright、WebSearch、Agent、技能仓库名等**内部或流程元信息**。
- **示例（须按本案替换检索词与渠道）**：

  > 检索说明：在**智慧芽/Patsnap 专利数据库**、**国家知识产权局专利公布公告系统**及 **Google Patents** 中，以「批任务调度」「异构集群调度」「任务队列重排」「负载感知调度」等为检索词进行检索；部分条目的公开文本与著录项以 Google Patents 页面复核。

查新笔记（Agent 内部或对话留档）仍可记录是否调用脚本、是否降级 WebSearch；**上述内容不得原样抄进交底书 1.1**。
