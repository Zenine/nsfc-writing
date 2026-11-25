---
name: nsfc-writing
description: 用于撰写、修改、诊断国家自然科学基金（国自然、NSFC）及省级科研基金申请书（“本子”）：青年科学基金C类（青C）、面上、地区、联合基金、省自然科学基金等。凡涉及选题与题目、摘要、立项依据、研究内容与研究目标、关键科学问题与科学假说、研究方案与技术路线图、特色与创新、年度计划与预期成果、研究基础与可行性、代表作与个人贡献、新版提纲与篇幅、提交前自查，或用户抱怨本子“流水账、没亮点、太技术、像综述、AI味”时使用，即使用户没有点名本 skill。
---

# 国自然申请书写作

本 skill 把一份本子看成**同一个科学问题的多次表达**：题目、摘要、立项依据、研究内容、关键科学问题、技术路线、创新、研究基础，都从同一张“科学问题工作表”出发，前后一一呼应。评审只有十分钟左右，多数是大同行，所以每一部分都要让人一眼看到“研究什么、为什么值得、凭什么能做成”。

## 路由

先读 [manifest.yaml](manifest.yaml)，再按下面三步加载，不要一次读完所有文件。

1. **每次都读** `core/` 下三个文件：
   - [core/stance.md](core/stance.md)：工作立场、事实底线、语体规则、输出格式。
   - [core/science-question.md](core/science-question.md)：科学问题工作表与主线链条。
   - [core/reviewer-lens.md](core/reviewer-lens.md)：评审怎么读本子。
2. **判断三个维度**，动笔前用一行告诉用户判断结果（如“任务：起草｜章节：摘要｜项目：青C”），用户可随时纠正，这一行不是审批关口：
   - `task` 任务：起草 `draft`／修改 `revise`／诊断审阅 `diagnose`／提交前自查 `check`。
   - `section` 章节：可多选，对应 `sections/` 下的文件。
   - `program` 项目类型：青C／面上／地区／联合基金／省级；默认青C。
3. **按需加载** `references/`：条件见下表和 manifest。

| 章节 | 文件 |
|---|---|
| 选题与题目、关键词、申请代码 | [sections/topic-title.md](sections/topic-title.md) |
| 摘要 | [sections/abstract.md](sections/abstract.md) |
| 立项依据 | [sections/rationale.md](sections/rationale.md) |
| 研究内容、研究目标、关键科学问题 | [sections/content-aims-questions.md](sections/content-aims-questions.md) |
| 研究方案与技术路线 | [sections/plan-roadmap.md](sections/plan-roadmap.md) |
| 框架图、技术路线图等配图 | [sections/figures.md](sections/figures.md) |
| 特色与创新 | [sections/innovation.md](sections/innovation.md) |
| 年度研究计划与预期成果 | [sections/schedule-outcomes.md](sections/schedule-outcomes.md) |
| 研究基础、可行性、风险应对、工作条件、在研项目、代表作 | [sections/foundation.md](sections/foundation.md) |

| 条件 | 文件 |
|---|---|
| 问到提纲结构、篇幅、预算、研究属性、代表作数量等硬要求 | [references/policy-2026.md](references/policy-2026.md) |
| 项目类型不是青C，或涉及联合基金、省级项目 | [references/programs.md](references/programs.md) |
| 起草或修改任何正文 | [references/wording.md](references/wording.md) |
| `task=diagnose`，或用户说本子流水账、没亮点、太技术、AI味 | [references/diagnosis.md](references/diagnosis.md) |
| `task=check`，或整本交稿前 | [references/checklist.md](references/checklist.md) |
| 用户要借助大模型自查、仿写、按往年评审意见修改 | [references/ai-assist.md](references/ai-assist.md) |
| 用户要完整示例，或对“科学问题如何贯穿全本”理解不清 | [references/worked-example.md](references/worked-example.md) |

## 执行顺序

1. **先填工作表**：起草新章节或重写整本前，先按 `core/science-question.md` 把工作表填出来；用户材料里缺的格子列为待补，不替用户编。修改单段、改题目、局部润色时跳过，只核对与工作表是否一致。
2. **再写正文**：按章节文件的结构写，句式和篇幅按章节文件给的默认值。
3. **最后自查**：按 `core/stance.md` 的输出格式附自查和【待核】清单。

## 优先级

当年度官方指南与申请书模板 ＞ 用户所在项目或单位的规定 ＞ 用户本人的明确决定 ＞ 本 skill 的默认值。本 skill 的数字（页数、字数、条数）都是经验默认值；与用户已有做法冲突时，说明一次差别，按用户决定执行。
