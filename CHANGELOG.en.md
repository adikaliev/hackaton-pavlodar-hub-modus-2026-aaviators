# Changelog

[Русская версия](CHANGELOG.md)

All notable changes to this project are documented here, in [Keep a Changelog](https://keepachangelog.com) style.

## [Unreleased]

### Added
- 2026-11-13: The demo is online on Render's free hosting: <https://hackaton-pavlodar-hub-modus-2026.onrender.com/>. The link is at the top of the README and in "How to view the demo", which also explains how the online version differs from a local one. The Telegram bot is connected and works in the online demo.
- 2026-11-12: Linking Telegram by QR code: the profile shows a QR code with the same one-time link next to the button, so an account can be linked from a page open on a computer. Our server draws the QR code (new dependency `segno`), so the code never goes to an outside service. The profile page notices the link and updates by itself. 3 new tests, 83 in total.
- 2026-11-12: User stories (`docs/user-stories.en.md`): 42 stories by role with stage tags; how employees stay motivated (the author's journey, recognition instead of money and quotas, motivating the people who answer) and what keeps the process from fading (what the system enforces, the review rhythm, process health metrics, the first 90 days). The share of authors who submit a second time is added to the next-stage plan (`docs/solution-design.en.md`, section 11).
- 2026-11-12: Phone screenshots (`docs/screenshots/11–13`) and a section about them in the README. Every page has been checked at 390 px wide.
- 2026-11-12: Live checks: the Telegram bot (account linking with a one-time code, delivery of notifications) and the Docker image (it builds, and all 80 tests pass inside the container). The notes saying these were not verified are removed from the README and the design documents.
- 2026-11-12: A working MVP on Django 5.2 and SQLite (`feedback/`, `config/`, `manage.py`): request submission with a receipt, routing by 16 rules with a backup chain, statuses and a thread with the author, deadlines in working days, automatic escalation, confirmation of the result by the author, search and filters, a leadership dashboard, the "Done" feed, confidential mode, registration on an employee's behalf, "me too" and merging of duplicates.
- 2026-11-12: The core and pluggable integrations in code: an outgoing event log, a dispatcher with retries and a fallback channel, a Telegram bot (notifications and account linking), a Bitrix24 simulator (records the REST call `im.notify.system.add`, imports the directory from a file), an "Integrations" page with switches and a log.
- 2026-11-12: A demo for the jury: a home page with the organizers' six scenarios, a role switcher, a demo clock ("+1 working day"), a data reset. Demo data (`data/`): a directory in Bitrix24's format, rules, 14 extra requests and each request's history in relative time.
- 2026-11-12: 80 automated tests (`feedback/tests/`); the core's tests run with every integration switched off.
- 2026-11-12: Technical concept: modules, data model, screen map, technology choices, security, the path to production (`docs/technical-concept.en.md`). Screenshots (`docs/screenshots/`).
- 2026-11-12: Run and demo instructions, the list of what is implemented, simulated and planned, known limitations (`README.en.md`). Files for running: `requirements.txt`, `.env.example`, `Dockerfile`, `docker-compose.yml`.
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
- 2026-11-12: A "For the jury" section at the top of the README: the solution in brief, the list of documents (moved from the end of the README) and a "what the spec requires — where to look" table linking to the relevant document sections, including the three questions of spec §6.
- 2026-11-12: Tables on a phone: each field in a card now has a label. Before, the author and the owner looked the same in the request list: a name and a department with no heading.
- 2026-11-12: The solution design and the value proposition now match what is implemented: the "MVP" tag means "implemented in the working MVP"; confirmation of the result by the author, the "Done" feed, similar requests and "me too" moved into the MVP; what is not implemented (changing the category after submission, digests, drafts, translation files) moved to the next stage; escalation is described as a background check written to the history (`docs/solution-design.en.md`, `docs/value-proposition.en.md`).
- 2026-11-12: The stack is chosen: Django 5.2 LTS, SQLite in the demo and PostgreSQL in production, pages rendered on the server (`docs/technical-concept.en.md`, section 5).
- 2026-11-12: The organizers' originals (`docs/source/`) are excluded from git; their Markdown versions stay in the repository.
- 2026-11-12: Team working material (analysis, spec coverage check, video transcript, research) moved to `docs/internal/` and, together with the coding-agent instructions, excluded from git. The sources for the slide numbers now sit directly in `docs/value-proposition.en.md`. The README points to the jury-facing documents.
- 2026-11-12: Architecture principle "core and pluggable integrations": the core works without integrations, each integration is switched on and off separately, and the solution runs standalone or as a module inside Bitrix24 (`docs/solution-design.en.md`, section 7.2; `docs/value-proposition.en.md`).
- 2026-11-12: No connection to Bitrix24: we have no access to the client's portal. Added the integration mechanism on our side — adapters, an outgoing event log, a Bitrix24 simulator with an "Integration log" page, and a directory import from a file in Bitrix24's format (`docs/solution-design.en.md`, section 7.2).
- 2026-11-12: Confirmed that the Bitrix24 portal is in the cloud: integration only through the REST API, webhooks and apps (`docs/solution-design.en.md`, sections 7 and 12).
- 2026-11-11: Rule-based routing, as spec §2.3 requires: rules on type, category and the author's department assign a role; a backup chain covers absences; a default rule catches the rest; "Not mine" re-runs the rules. Category is now required, with a suggestion from the text. The "Dispatcher" role is replaced by a "Coordinator" who handles exceptions only. Demo rules are derived from the dataset (`docs/solution-design.en.md`, section 3.1).
- 2026-11-11: The solution is designed for one country, Kazakhstan: one instance, data in Kazakhstan, the Kazakh working-day calendar and UTC+5 as settings. The two-country option (Russia and Kazakhstan) is dropped.
- 2026-11-11: README and changelog are now in Russian; English versions are in files with the `.en.md` suffix.
