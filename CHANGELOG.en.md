# Changelog

[Русская версия](CHANGELOG.md)

All notable changes to this project are documented here, in [Keep a Changelog](https://keepachangelog.com) style.

## [Unreleased]

### Added
- 2026-11-12: Git preparation: `.gitignore` (secrets, the video, Telegram posts, the demo database, attachments, caches, Word lock files) and `.gitattributes` (LF line endings, binary files).
- 2026-11-11: Spec coverage check (`docs/requirements-coverage.en.md`). Following it, the solution design gains: manual assignment by managers, decision fields (next actions, planned date), priority, a section on detecting recurring problems, search, a "who can do what" table, a fuller description of anonymity, a "what to clarify" column for integrations, a list of items needing separate technical work, and the needs of each role.
- 2026-11-11: Value proposition: how we differ from competitors, a comparison table, answers to objections, numbers for slides (`docs/value-proposition.en.md`).
- 2026-11-11: Assumptions and Telegram as the messenger: the solution design gains a Telegram section and an assumptions table (`docs/solution-design.en.md`, sections 7.1, 12).
- 2026-11-11: Solution design document: journeys for each role, lifecycle and deadlines, escalation, visibility and access, integrations, legal, rollout (`docs/solution-design.en.md`).
- 2026-11-11: Research report on existing solutions and practices (`reports/`), with sourced notes (`research_notes/`).
- 2026-11-11: Task analysis with suggested MVP scope (`docs/analysis.md`).
- 2026-11-11: Transcript and summary of the sponsor's video message.
- 2026-11-11: Markdown versions of the spec and dataset, and a JSON seed file with the 20 demo requests (`tools/convert_source_docs.py`).
- 2026-11-11: Project scaffold. The organizers' files are moved from `init/` to `docs/source/` with ASCII names.

### Changed
- 2026-11-12: The organizers' originals (`docs/source/`) are excluded from git; their Markdown versions stay in the repository.
- 2026-11-12: Team working material (analysis, spec coverage check, video transcript, research) moved to `docs/internal/` and, together with the coding-agent instructions, excluded from git. The sources for the slide numbers now sit directly in `docs/value-proposition.en.md`. The README points to the jury-facing documents.
- 2026-11-12: Architecture principle "core and pluggable integrations": the core works without integrations, each integration is switched on and off separately, and the solution runs standalone or as a module inside Bitrix24 (`docs/solution-design.en.md`, section 7.2; `docs/value-proposition.en.md`).
- 2026-11-12: No connection to Bitrix24: we have no access to the client's portal. Added the integration mechanism on our side — adapters, an outgoing event log, a Bitrix24 simulator with an "Integration log" page, and a directory import from a file in Bitrix24's format (`docs/solution-design.en.md`, section 7.2).
- 2026-11-12: Confirmed that the Bitrix24 portal is in the cloud: integration only through the REST API, webhooks and apps (`docs/solution-design.en.md`, sections 7 and 12).
- 2026-11-11: Rule-based routing, as spec §2.3 requires: rules on type, category and the author's department assign a role; a backup chain covers absences; a default rule catches the rest; "Not mine" re-runs the rules. Category is now required, with a suggestion from the text. The "Dispatcher" role is replaced by a "Coordinator" who handles exceptions only. Demo rules are derived from the dataset (`docs/solution-design.en.md`, section 3.1).
- 2026-11-11: The solution is designed for one country, Kazakhstan: one instance, data in Kazakhstan, the Kazakh working-day calendar and UTC+5 as settings. The two-country option (Russia and Kazakhstan) is dropped.
- 2026-11-11: README and changelog are now in Russian; English versions are in files with the `.en.md` suffix.
