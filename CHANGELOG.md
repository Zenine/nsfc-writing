# CHANGELOG

## 2026-11-25（v0.1.2）

- 按青C实测补规则：研究内容开头不放前期数据、编号与数据流向一致。
- 诊断先核对图片路径与交叉引用，新增四类症状，`references/diagnosis.md`。
- 遇“尚无、首次”提示检索并给出检索词，`innovation.md`、`rationale.md`。
- 新增用例 H、I 与 v0.1.1 基线、v0.1.2 复测输出。

## 2026-11-25（v0.1.1）

- 按五路审阅修复 skill 正文冲突与政策过度推断，提纲改按原文摘录，`policy-2026.md`。
- 新增英文题目摘要与预算两节，`sections/english.md`、`sections/budget.md`。
- 重写配图、大模型辅助、自查清单与示例，去除课程独有的口诀与配比。
- 任务新增政策问答，加载条件只留 `manifest.yaml`，新增 `check_skill_structure.py`。
- 修复 `install.sh` 以父目录为 DEST 时误删其他 skill，补回归测试。
- 重合检查改为整份文件比对并扩大范围，新增 `tests/scripts/test-overlap.sh`。
- 修复 Python 3.9 与 bash 3.2 兼容问题，CI 增加 3.9 矩阵与只读权限。
- 许可证补全 CC BY 4.0 全文、版权人与目录边界，`LICENSE`。

## 2026-11-25

- 新建 `skills/nsfc-writing/`：路由、加载清单、core 三件、9 个章节片段与 7 个参考文件。
- 新增 `scripts/verify.sh`、中文重合检查、带私有黑名单的隐私扫描与安装脚本。
- 新增 `tests/fixtures/` 5 个行为用例及无 skill 基线、带 skill 输出。
