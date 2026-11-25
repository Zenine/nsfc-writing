# 仓库规则（给 agent）

本仓库是公开库，内容是国自然申请书写作 agent skill。所有 agent 会话进入本仓库先读本文件。

## 硬边界

1. **参考资料永不入库。** 书籍、课程课件、录像、转写文本放 `sources/`（已忽略），任何 `*.pdf`、`*.pptx`、`*.docx`、`*.mp4` 和 `sources/` 下文件不得提交。`scripts/verify.sh` 会检查。
2. **重新整理，不复述。** `skills/` 用自己的逻辑和话整理方法、结构和清单；不连续抄录参考资料原文，不搬用课程自创的口诀、配比、模板句和案例，不收课件页、截图和讲稿。`scripts/check_overlap.py` 按整份文件以连续 20 个汉字做机检；与 `sources/official/` 中官方通告、提纲相同的片段属于有意引用，不计入。官方条文的常见转述可加入 `scripts/overlap_allowlist.txt`，只收官方条文，不收课程内容。
3. **来源写法。** 参考资料的署名以 README“内容来源”一节为准，修改时不另行增减。
4. **隐私。** 示例一律用虚构课题，不使用维护者或任何真实申请人的项目、单位、地点、数据。维护者可在本地放私有词表 `.private/privacy-blacklist.txt`（已忽略），`verify.sh` 存在该文件时自动使用。
5. **语言。** 说明文字用简体中文；README.en.md 为英文简版。
6. **不自动提交。** 除用户当轮明确要求外不执行 `git commit`；提交信息不加 AI 署名。

## 目录

- `skills/nsfc-writing/`：最终产品，含 `scripts/`（字数统计、本地页面合并，不联网）。`SKILL.md` 路由与文件索引 ＋ `manifest.yaml`（参考文件加载条件的唯一出处）＋ `core/`、`sections/`、`references/`。
  - 章节文件统一结构：这一部分要让评审相信什么 → 从工作表取什么 → 写法 → 自检。新增或改写章节沿用此结构，以科学问题工作表为线索组织，不按任何参考资料的分节顺序。
- `tests/fixtures/`：行为测试用例（输入 ＋ 期望表现）。
- `tests/regression/`：无 skill 基线与带 skill 输出。
- `tests/scripts/`：脚本回归测试。
- `scripts/`：验证、重合检查、隐私扫描、安装。
- `docs/decisions/`：默认值取舍记录。

## 修改 skill 的流程

1. 新增或修改规则前，先在 `tests/fixtures/` 写出能体现该规则的用例，跑无 skill 或旧版 skill 看到失败。
2. 修改 `skills/`，新增片段时同步更新 `SKILL.md` 文件索引与 `manifest.yaml`；加载条件只写在 manifest。
3. 带 skill 重跑用例，输出存 `tests/regression/<日期目录>/`。
4. `bash scripts/verify.sh` 通过后再提交；发布新版本时同步 `manifest.yaml`、`.claude-plugin/plugin.json` 的版本号与 CHANGELOG。

## 验证入口

`bash scripts/verify.sh`（skill 结构与版本号、README 链接、重合检查、隐私扫描）；`tests/scripts/*.sh` 为脚本回归测试，CI 在 Python 3.9 与 3.12 下都跑。

## 文档写法

- md 只记事实和规则，不写过程自证和防御性声明。
- CHANGELOG 每条一行，30–60 字，写「动作 + 对象 + 文件」。
- TODO 每条只写做什么、一句为什么、下一步、验证方式；完成即删，CHANGELOG 记一行。
