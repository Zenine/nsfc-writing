# nsfc-writing: an agent skill for NSFC grant proposals

*[中文](README.md) | English*

An agent skill (for Claude Code, Codex and any agent that reads `SKILL.md`) for drafting, revising and auditing proposals to the National Natural Science Foundation of China (NSFC): Young Scientists Fund (Category C), General Program, Regional Fund, Key Program, Joint Funds, and provincial research programs.

The skill targets the most common failure of Chinese grant proposals: a list of technical tasks with no scientific question. It first builds a "scientific question worksheet" (object, underlying mechanism, limits of current knowledge, new approach, testable hypothesis, key scientific questions), then expands it into the title, abstract, rationale, research content, technical route, innovation and research foundation, keeping every section aligned.

All instructions and templates are written in Simplified Chinese, because the proposals themselves are written in Chinese.

## Layout

- `skills/nsfc-writing/SKILL.md` — router: detects task, section and program type, then loads only what is needed.
- `manifest.yaml` — load list. `core/` is always loaded; `sections/` per section; `references/` on demand.
- `scripts/` — a character counter, and a tool that merges locally saved pages of past NSFC final reports into a PDF (requires Pillow; no network access).
- The routing design follows [nature-skills](https://github.com/Yuan1z0825/nature-skills).

## Install

```bash
npx skills add Zenine/nsfc-writing -g -y
# or
curl -fsSL https://raw.githubusercontent.com/Zenine/nsfc-writing/main/scripts/install.sh | bash
# DEST=<skills dir> installs into <skills dir>/nsfc-writing; pass flags with | bash -s -- --link
# or, as a Claude Code plugin
claude plugin marketplace add Zenine/nsfc-writing && claude plugin install nsfc-writing@nsfc-writing
```

## Past final reports (manual browser steps)

Final reports of completed NSFC projects are public on kd.nsfc.cn, but viewing a full report requires passing a slider verification in the browser, so the skill does not download them automatically. Search the site in your browser, open a report, pass the verification, save each page image into one folder per project (file names numbered by page), merge them with `python3 skills/nsfc-writing/scripts/merge_pages.py <folder> --name "<project name>"` (requires Pillow), and give the PDF to the agent. For personal study only; follow the site's terms of use.

## Notes

- Policy items follow the 2026 NSFC call and the 2026 proposal outline; check each year's official call and template.
- NSFC requires human verification of AI-generated content, disclosure and labelling of its use, and forbids submitting AI-generated proposals. The skill produces drafts and audits for the applicant to rewrite. It instructs the agent not to invent references and to mark unverifiable items as 【待核】; data figures must come from real results.

## Sources

Writing methods draw on the 2026 NSFC call and outline, notes from a grant-writing training course (the source of many section-level points), the book *From Technical Problems to Scientific Questions* (Gong Xuzhong, Science Press), the open-source projects njzjz/nsfc-agent-skills and jiankang1991/nsfc-benzi-audit, and the maintainer's own proposal-writing experience. The skill text is organized around its own scientific-question worksheet. The repository contains no text, slides or screenshots from the course or the book; the official call and outline are quoted verbatim.

## License

Code and configuration: MIT. Skill text and documentation: CC BY 4.0. See [LICENSE](LICENSE).
