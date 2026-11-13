# Coverage of the spec

[Русская версия](requirements-coverage.md)

A check as of 12 November 2026, after the MVP was built: how our documents and the working app cover the requirements of the [spec (ТЗ)](../task-spec.md), the demo scenarios in the [dataset](../dataset.md), the owner's video message and the submission rules.

Legend: ✔ — covered; ◐ — partly, or will be covered during development; ✗ — not done yet.

References like "§3.1" without a document name point to the [solution design](../solution-design.en.md).

## Required deliverables (spec §4.1)

| Requirement | Where | Status |
|---|---|---|
| Product concept, the problem it solves, value for users | [analysis.md](analysis.md), [value-proposition.en.md](../value-proposition.en.md) | ✔ in working documents; the final presentation isn't done yet |
| Target users and key scenarios | §2, §4 | ✔ |
| Interface prototype: main screens and interaction logic | the working app; screen map in [technical-concept.en.md](../technical-concept.en.md), section 4; screenshots in `docs/screenshots/` | ✔ |
| Technical concept: architecture, technologies, data, security, integrations | [technical-concept.en.md](../technical-concept.en.md) | ✔ |
| Roadmap with the MVP and later stages | §11 | ✔ |
| Demo and an explanation of limitations | the app's home page with the scenarios; README: "How to view the demo", "Known limitations" | ✔ no recorded video of the demo |

## Extra deliverables for a working MVP (spec §4.2)

| Requirement | Where | Status |
|---|---|---|
| Source code and repository | [public repository](https://github.com/adikaliev/hackaton-pavlodar-hub-modus-2026-aaviators), [live demo](https://hackaton-pavlodar-hub-modus-2026.onrender.com/) | ✔ published on 13 November |
| Run and demo instructions | [README](../../README.en.md) | ✔ |
| Implemented features and known limitations | [README](../../README.en.md): "What is implemented, what is simulated, what is planned", "Known limitations" | ✔ |
| Test data, or instructions to prepare it | `data/`: 34 requests, directory, rules, calendar, histories in relative time; README: "Test data" | ✔ |
| Demo of end-to-end scenarios | the app's home page; `feedback/tests/test_demo.py` | ✔ |
| Keep implemented features, mocked external systems and plans apart | the "Integrations" page with mode badges; the home page; README | ✔ |

## Main scenario (spec §2.3)

| Step | Where | Status |
|---|---|---|
| 1. The user picks a category | §3.1, §4.1: category is required, suggested from the text | ✔ |
| 2. Describes the problem or idea, proposes a solution, attaches materials | §4.1 | ✔ |
| 3. The system registers it and routes it to the owner by defined rules | §3.1 | ✔ |
| 4. The owner records the decision and next actions | §3.2, §4.2 | ✔ |
| 5. The author follows the status and result | §3.2, §4.1, §7.1 | ✔ |
| 6. Information is kept for analysis and spotting repeats | §3.6, §4.5 | ✔ |

## Review process (spec §2.5)

| What to describe | Where | Status |
|---|---|---|
| How a request reaches its owner | §3.1 | ✔ |
| How status and outcome are recorded | §3.2 | ✔ |
| How the author learns about progress | §4.1, §6, §7.1 | ✔ |
| How loss is prevented | §3.1 (default rule, backup chain), §3.3, §3.4 | ✔ |
| How recurring problems are detected | §3.6 | ✔ |
| Simplified routing rules and test data | §3.1: 15 rules derived from the dataset | ✔ |

## Users (spec §2.2)

| User | Where | Status |
|---|---|---|
| Employees: report, propose, follow up | §2, §4.1 | ✔ |
| Managers: review, decide, assign owners | §3.1 (manual assignment), §4.3 | ✔ |
| Administrators: categories, settings, routing rules | §4.7 | ✔ |
| Clients — later stages | §4.9 | ✔ as a future direction |
| MVP priority — the internal process | §11 | ✔ |

## Functional areas (spec §2.4)

| Area | Where | Status |
|---|---|---|
| Creating and registering requests | §4.1 | ✔ MVP |
| Categorizing by department, business area and type | §3.1 | ✔ MVP |
| Passing requests to owners | §3.1 | ✔ MVP |
| Statuses and deadlines | §3.2, §3.3 | ✔ MVP |
| Comments and requests for clarification | §3.2, §4.2 | ✔ MVP |
| Notifications to authors and owners | §6, §7.1 | ✔ MVP (Telegram and in-app) |
| Recording decisions and actions | §3.2 | ✔ MVP |
| Search, filtering, history | §4.5 | ✔ MVP |
| Analytics by category, repeats, outcomes | §3.6, §4.5 | ✔ MVP |
| Extension to surveys and client feedback | §4.9 | ✔ as a future direction |

## Confidentiality and access (spec §2.6)

| Requirement | Where | Status |
|---|---|---|
| Who creates, views, edits and processes requests | §5: the "What is visible" and "Who can do what" tables | ✔ |
| What the author, owner and manager can see | §5 | ✔ |
| Anonymity: purpose, limitations, effect on processing | §5 | ✔ (confidential mode in the MVP, anonymous mode later) |

## Business value and metrics (spec §2.7)

| Requirement | Where | Status |
|---|---|---|
| Share reviewed, time to first response, share with an outcome, number of improvements implemented | §4.5 | ✔ on the dashboard |
| Target values | — | The spec says these are set separately; we propose setting them after the pilot (§9) |

## General requirements (spec §3)

| Requirement | Where | Status |
|---|---|---|
| §3.1 Problem, users and needs, scenarios, MVP scope, limitations and assumptions, a way to test usefulness | analysis.md; §2, §4, §11, §12; pilot metrics in §9; limitations in the README and technical-concept.en.md, section 9 | ✔ |
| §3.2 Interface: main screens and transition logic | the app; technical-concept.en.md, section 4 | ✔ |
| §3.3 Components, data storage, technologies and reasons, integrations, access, limitations, growth | technical-concept.en.md, sections 1–9 | ✔ |
| §3.4 Integrations: purpose, data and direction, method, what to clarify | §7 | ✔ |
| §3.5 Test data, data protection, access rights | §5, §8 | ✔ |
| §3.6 MVP, extensions, items needing separate technical work | §11 | ✔ |

## The company's development goals (spec §1.3)

| Goal | Where |
|---|---|
| An accessible channel for ideas and problems | §4.1, §6, §7.1 |
| Fewer lost requests and less manual work | §3.1, §3.3, §3.4 |
| Keeping and organizing decisions | §3.2, §4.5 |
| Transparency and accountability for results | §3.2, §3.4, §4.5 |
| Role-based access | §5 |
| Staged development | §11 |
| Spotting recurring problems | §3.6 |

## Dataset demo scenarios (dataset section 4)

| Scenario | How we cover it | Status |
|---|---|---|
| 1. Create a request: type, category, description, test file | the submission form, the receipt | ✔ implemented, checked by a test |
| 2. Assign an owner by category; an alternative when they're absent | A-016 (deputy), A-024 (default rule), the Rules page with the "who will get it" check | ✔ implemented, checked by a test |
| 3. Change status, ask for clarification, keep the comment history | A-005: question, paused deadline, answer, history | ✔ implemented, checked by a test |
| 4. Show the author the state and outcome, including a reasoned rejection | A-017 (rejection), A-004 (confirming the result), "My requests" | ✔ implemented, checked by a test |
| 5. Filter by department, category, status and deadline; find overdue items | the "All requests" page | ✔ implemented, checked by a test |
| 6. Summary: counts by type, share closed, average time to first response | the dashboard | ✔ implemented, checked by a test |

## Key questions (spec §6)

| Question | Where we answer it | Status |
|---|---|---|
| What business problem does it solve, and what value does it create? | value-proposition.en.md | ✔ material ready |
| How does it work in practice? | §3–§4; the working app | ✔ |
| How can it grow and integrate with the company's systems? | §7, §11 | ✔ |

## The owner's video

| What he asks for | Where | Status |
|---|---|---|
| One module for collecting feedback and suggestions | the whole document | ✔ |
| See which issues need solving and which ideas exist | §4.5 | ✔ |
| The author understands the stage: development, decision, implementation | §3.2 | ✔ |
| The owner can ask clarifying questions and report status | §3.2, §4.2 | ✔ |
| Proposals for "which modules, and how to build them" | technical-concept.en.md, sections 1–2: the core and pluggable integrations, the module list | ✔ |

## Submission rules (organizers' Telegram channel)

| Rule | Status |
|---|---|
| Deadline 13 November, 14:00; the form closes after that | ✔ taken into account |
| One submission per team | ✔ noted |
| Project links must open for everyone | ✔ the repository is public and the demo is online; both links open without logging in (checked on 13 November) |

## What's left to do

A check as of 12 November 2026, after the MVP was built.

1. ~~Publish the repository~~ — done on 13 November: the repository is public, the demo is hosted on Render, and both links open without logging in.
2. **Submit the form** before 13 November, 14:00: team name, email, repository link.
3. ~~Check Telegram live~~ — done on 12 November: an account was linked with a one-time code, and notifications were delivered by a real bot.
4. ~~Build the Docker image~~ — done on 12 November: the image builds, and all 80 tests pass inside the container.
5. **A presentation for the final on 16 November** that answers the three questions in spec §6, and a 2–3 minute screen recording in case something fails.
6. **Ask the organizers:** the evaluation criteria; whether the repository may change between 13 and 16 November.
