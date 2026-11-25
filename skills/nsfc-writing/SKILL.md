---
name: nsfc-writing
description: 用于撰写、修改、诊断国家自然科学基金（国自然、NSFC）及省级科研基金申请书（“本子”）：青年科学基金C类（青C）、面上、地区、重点、联合基金、省自然科学基金等。凡涉及选题与题目、摘要与英文摘要、立项依据、研究内容与研究目标、关键科学问题与科学假说、研究方案与技术路线图、特色与创新、年度计划与预期成果、研究基础与可行性、代表作与个人贡献、预算、新版提纲与篇幅、提交前自查，或用户抱怨本子“流水账、没亮点、太技术、像综述、AI味”时使用，即使用户没有点名本 skill。不用于结题或进展报告、期刊论文、专利与企业可研报告。
---

# 国自然申请书写作

本 skill 把一份本子看成**同一个科学问题的多次表达**：题目、摘要、立项依据、研究内容、关键科学问题、技术路线、创新、研究基础，都从同一张“科学问题工作表”出发，前后一一呼应。评审阅读时间有限，多数是大同行，所以每一部分都要让人一眼看到“研究什么、为什么值得、凭什么能做成”。

## 路由

1. **每次都读** `core/` 下三个文件：
   - [core/stance.md](core/stance.md)：工作立场、事实底线、语体规则、各类任务的输出格式。
   - [core/science-question.md](core/science-question.md)：科学问题工作表与主线链条。
   - [core/reviewer-lens.md](core/reviewer-lens.md)：评审怎么读本子。
2. **判断三个维度**，回复第一行写出判断结果（如“任务：起草｜章节：摘要｜项目：青C”），用户可随时纠正，这一行不是审批关口：
   - `task` 任务：起草 `draft`／修改 `revise`／诊断审阅 `diagnose`／提交前自查 `check`／政策问答 `qa`。
   - `section` 章节：可多选，对应下表；政策问答不选章节。
   - `program` 项目类型：青C／面上／地区／重点／联合基金／省级；默认青C。
3. **按 [manifest.yaml](manifest.yaml) 加载**：读用户涉及的章节文件；参考文件的加载条件只写在 manifest 中，按条件读取，不要一次读完。

| 章节 | 文件 |
|---|---|
| 选题与题目、关键词、申请代码 | [sections/topic-title.md](sections/topic-title.md) |
| 摘要 | [sections/abstract.md](sections/abstract.md) |
| 英文题目与英文摘要 | [sections/english.md](sections/english.md) |
| 立项依据 | [sections/rationale.md](sections/rationale.md) |
| 研究内容、研究目标、关键科学问题 | [sections/content-aims-questions.md](sections/content-aims-questions.md) |
| 研究方案与技术路线 | [sections/plan-roadmap.md](sections/plan-roadmap.md) |
| 框架图、技术路线图等配图 | [sections/figures.md](sections/figures.md) |
| 特色与创新 | [sections/innovation.md](sections/innovation.md) |
| 年度研究计划与预期成果 | [sections/schedule-outcomes.md](sections/schedule-outcomes.md) |
| 研究基础、可行性、风险应对、工作条件、项目情况、其他说明、代表作 | [sections/foundation.md](sections/foundation.md) |
| 预算（预算制项目） | [sections/budget.md](sections/budget.md) |

| 参考文件 | 内容 |
|---|---|
| [references/policy-2026.md](references/policy-2026.md) | 2026 年度提纲原文、篇幅、研究期限、研究属性、经费方式、生成式人工智能等条款 |
| [references/programs.md](references/programs.md) | 各项目类型的差异 |
| [references/wording.md](references/wording.md) | 用词、易混词、句式、去除 AI 味 |
| [references/diagnosis.md](references/diagnosis.md) | 常见症状、严重程度分级、诊断模板 |
| [references/checklist.md](references/checklist.md) | 提交前自查清单 |
| [references/ai-assist.md](references/ai-assist.md) | 借助大模型自查与修改的方法和边界 |
| [references/worked-example.md](references/worked-example.md) | 一个虚构课题从工作表到题目、摘要、内容、目标、问题、创新的完整示例 |

## 执行顺序

1. **工作表**：起草新章节或重写整本时，先按 `core/science-question.md` 填工作表，放在正文之前；对象、科学本质或新切入缺失到拟不出假说时，先就这几格提问。修改单段、改题目、局部润色时跳过，只核对与工作表是否一致。政策问答不填工作表。
2. **正文初稿**：按章节文件的结构写，句式和篇幅按章节文件给的默认值。
3. **收尾**：按 `core/stance.md` 对应任务的输出格式，附对应关系和【待核】清单。

## 优先级

当年度官方通告、指南与申请书模板 ＞ 用户所在项目或单位的规定 ＞ 用户本人的明确决定 ＞ 本 skill 的默认值。本 skill 的数字（页数、字数、条数）都是经验默认值；与用户已有做法冲突时，说明一次差别，按用户决定执行。
