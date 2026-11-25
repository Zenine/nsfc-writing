# nsfc-writing：国自然申请书写作 skill

*中文 | [English](README.en.md)*

供 Claude Code、Codex 等能读取 `SKILL.md` 的 agent 使用的国家自然科学基金（国自然、NSFC）申请书写作 skill，覆盖青年科学基金C类（青C）、面上、地区、联合基金和省级科研项目。

它解决的核心问题是：**本子写成了任务清单，没有科学问题，读起来像流水账、没有亮点**。skill 把一份本子看成同一个科学问题的多次表达，先用“科学问题工作表”把对象、科学本质、局限、新切入、假说和关键科学问题理清，再展开成题目、摘要、立项依据、研究内容、技术路线、创新和研究基础，并保证前后一一对应。

## 能做什么

| 任务 | 例子 |
|---|---|
| 起草 | “根据我的笔记写青C摘要”“把这几条任务改写成研究内容、研究目标和关键科学问题” |
| 修改 | “题目太长，改几个版本”“立项依据第二段像流水账，帮我重写” |
| 诊断 | “看看这段立项依据有什么问题，按严重程度列出来” |
| 自查 | “整本要交了，按清单过一遍” |
| 政策问答 | “新版青C正文写哪几部分？研究方案放哪？要不要编预算？” |
| 英文与预算 | “把题目和摘要翻成英文”“面上项目的预算怎么和方案对应” |
| 往年结题报告 | “这几份往年结题报告能借鉴什么”（报告由用户在知识库网页上通过验证后自行保存） |

起草的是供申请人改写的初稿，附“对应关系”和“待核与待补”清单。skill 要求 agent 只用用户提供或可核实的文献、数据和个人贡献信息，查不到的标【待核】，不编造参考文献。

## 结构

```
skills/nsfc-writing/
├── SKILL.md            路由：判断任务、章节、项目类型，按需加载
├── manifest.yaml       加载清单（必读片段、章节片段、条件参考）
├── core/               每次必读：工作立场与语体、科学问题工作表、评审视角
├── sections/           按章节：题目、摘要、英文题目摘要、立项依据、研究内容、方案、配图、创新、计划、研究基础、预算
├── references/         按条件：2026 版提纲与硬要求、项目类型差异、用词、诊断、自查清单、大模型辅助、完整示例、往年结题报告
└── scripts/            字数统计；把本地保存的结题报告页面合并为 PDF（需要 Pillow）
```

路由方式借鉴了 [nature-skills](https://github.com/Yuan1z0825/nature-skills) 的“核心必读 ＋ 按维度加载片段 ＋ 按条件查参考”设计，避免一次把所有规则塞进上下文。

## 安装

skill 本体是 `skills/nsfc-writing/` 目录，任选一种方式。

**npx（推荐，自动装到本机检测到的 agent）**

```bash
npx skills add Zenine/nsfc-writing -g -y
```

**curl（不需要 Node，装到已存在的 `~/.claude` 与 `~/.codex`）**

```bash
curl -fsSL https://raw.githubusercontent.com/Zenine/nsfc-writing/main/scripts/install.sh | bash
```

传参数时这样写：

```bash
curl -fsSL https://raw.githubusercontent.com/Zenine/nsfc-writing/main/scripts/install.sh | bash -s -- --link   # 克隆后软链接；装的是分支时可用 git pull 更新
curl -fsSL https://raw.githubusercontent.com/Zenine/nsfc-writing/main/scripts/install.sh | REF=v0.2.0 bash   # 安装指定版本
```

其他选项：`TARGET=claude` 或 `TARGET=codex` 只装一个；`DEST=<skills 目录>` 指定 skills 目录，实际装到 `<skills 目录>/nsfc-writing`；目标已存在但不是本 skill 时脚本会停止。想先看脚本：下载后 `less install.sh` 再运行。脚本只下载、复制或软链接，不改任何配置文件。

多种方式混装（如 npx 与 curl 各装一份）时，同一个 agent 可能看到两份同名 skill，保留一种即可。

**Claude Code 插件**

```bash
claude plugin marketplace add Zenine/nsfc-writing && claude plugin install nsfc-writing@nsfc-writing
```

**手动**

```bash
git clone https://github.com/Zenine/nsfc-writing.git
cp -r nsfc-writing/skills/nsfc-writing ~/.claude/skills/nsfc-writing   # Claude Code
cp -r nsfc-writing/skills/nsfc-writing ~/.codex/skills/nsfc-writing    # Codex
```

其他 agent：把 `skills/nsfc-writing/SKILL.md` 作为首条指令加载，它的路由表会告诉 agent 读哪些文件。

**验证**：新开会话说“帮我把这段立项依据诊断一下”或“青C正文写哪几部分”，agent 应先给出一行判断（任务、章节、项目类型），再按 skill 的结构作答。

## 使用须知

- 政策条款按 2026 年度通告与青C申请书提纲整理，每年以当年通告、指南和信息系统下载的模板为准。
- 页数、字数、条数等数字是经验默认值；与用户单位规定或本人决定冲突时，以后者为准。
- 国自然要求人工核实生成内容、如实声明并标识生成式人工智能使用情况，不得直接提交生成的申请书。skill 产出的是供申请人改写的初稿和诊断意见；参考文献须由申请人逐篇检索核实；实验图、数据图只用真实结果。

## 内容来源

写作方法参考了以下材料，skill 文本按科学问题工作表重新组织。仓库中没有课程和书籍的原文、课件或截图；官方通告与提纲按原文引用。

- 国家自然科学基金委员会《关于2026年度国家自然科学基金项目申请与结题等有关事项的通告》及 2026 年版申请书提纲。
- 一套基金申请书写作培训课程的学习笔记：各章节写法和常见问题的许多要点来自这套课程。
- 公旭中《从技术问题到科学问题：国家自然科学基金申请书写作指南》（科学出版社）中科学问题与科学假说的凝练方法。
- 开源项目 [njzjz/nsfc-agent-skills](https://github.com/njzjz/nsfc-agent-skills)、[jiankang1991/nsfc-benzi-audit](https://github.com/jiankang1991/nsfc-benzi-audit) 中关于评审视角与科学问题凝练的思路。
- 维护者撰写多份基金申请书的实践经验。

## 开发

- 验证入口：`bash scripts/verify.sh`（skill 结构与版本号、README 链接、与参考资料的重合检查、公开隐私扫描）；脚本回归测试在 `tests/scripts/`。
- 行为测试用例在 `tests/fixtures/`，无 skill 基线与各版本输出在 `tests/regression/`。
- 仓库规则见 [AGENTS.md](AGENTS.md)。

## 许可

代码与配置采用 MIT，skill 文本与文档采用 CC BY 4.0，详见 [LICENSE](LICENSE)。
