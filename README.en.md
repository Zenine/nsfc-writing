# nsfc-writing: an agent skill for NSFC grant proposals

*[中文](README.md) | English*

An agent skill (for Claude Code, Codex and any agent that reads `SKILL.md`) for drafting, revising and auditing proposals to the National Natural Science Foundation of China (NSFC): Young Scientists Fund (Category C), General Program, Regional Fund, Joint Funds, and provincial research programs.

The skill targets the most common failure of Chinese grant proposals: a list of technical tasks with no scientific question. It first builds a "scientific question worksheet" (object, underlying mechanism, limits of current knowledge, new approach, testable hypothesis, key scientific questions), then expands it into the title, abstract, rationale, research content, technical route, innovation and research foundation, keeping every section aligned.

All instructions and templates are written in Simplified Chinese, because the proposals themselves are written in Chinese.

## Layout

- `skills/nsfc-writing/SKILL.md` — router: detects task, section and program type, then loads only what is needed.
- `manifest.yaml` — load list. `core/` is always loaded; `sections/` per section; `references/` on demand.
- The routing design follows [nature-skills](https://github.com/Yuan1z0825/nature-skills).

## Install

```bash
npx skills add Zenine/nsfc-writing -g -y
# or
curl -fsSL https://raw.githubusercontent.com/Zenine/nsfc-writing/main/scripts/install.sh | bash
# or, as a Claude Code plugin
claude plugin marketplace add Zenine/nsfc-writing && claude plugin install nsfc-writing@nsfc-writing
```

## Notes

- Policy items follow the 2026 NSFC call and the 2026 proposal outline; check each year's official call and template.
- NSFC requires human verification of AI-generated content and disclosure of its use, and forbids submitting AI-generated proposals. The skill produces drafts and audits for the applicant to rewrite; it never invents references, and data figures must come from real results.

## Sources

Independently written. Methods were learned from the 2026 NSFC call and outline, the book *From Technical Problems to Scientific Questions* (Gong Xuzhong, Science Press), notes from a grant-writing training course, the open-source projects njzjz/nsfc-agent-skills and jiankang1991/nsfc-benzi-audit, and the maintainer's own proposal-writing experience. No source text, slides or screenshots are included.

## License

Code and configuration: MIT. Skill text and documentation: CC BY 4.0. See [LICENSE](LICENSE).
