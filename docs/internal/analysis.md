# Task analysis

Sources: [task-spec.md](../task-spec.md) (ТЗ), [dataset.md](../dataset.md), the sponsor's video message and the organizers' announcements in Telegram (neither is published here). Section numbers like §2.5 refer to the ТЗ.

## TL;DR

Build an internal system where employees of ГК «Модус Трейд» submit problems and suggestions, each one gets an owner and a deadline, the author can always see its status, and management sees everything on one screen.

The video shows what the sponsor (the company owner) actually cares about. Collecting input is not the hard part. **Issues get forgotten without anyone noticing, and then people stop speaking up.** The solution should prove that no request can get lost and that every author gets an answer. A working MVP is preferred over a prototype (§4.3).

## Key dates

| When | What |
|---|---|
| 13 Nov 2026, 14:00 | **Submission deadline.** The Google Form closes at 14:00. One submission per team. All links must open for everyone. |
| 16 Nov 2026 | Final in Pavlodar. The owner attends in person, reviews the finalists and plans to work with the winner. |

The evaluation criteria are not in our files. §5 says the organizers define them separately, so ask in the participants' chat.

## What the sponsor actually wants (from the video)

The owner described one chain of problems. Each link maps to a feature and to something we can show in the demo:

| Pain, in his words | Spec | Feature | How to show it |
|---|---|---|---|
| Issues arrive "chaotically": by email, as a remark at a meeting, in a phone call or a chat | §1.3 | One intake point that takes under a minute and works on a phone. A manager can **register a request on someone's behalf** (e.g. a remark from a meeting), with the source channel recorded. | A manager logs a meeting remark in 30 seconds. |
| "I have to dig through diaries and recall meetings" to know what needs fixing | §2.4, §2.7 | **Management dashboard**: open issues by department and category, recurring themes, the pipeline of ideas | The dashboard built on the seed data |
| An employee thinks the issue is being handled, but it was forgotten | §2.5 ("how loss is prevented") | Every request gets an owner on creation (auto-routing by category, with a fallback). Time limits for first response and for a decision. **Automatic escalation** to the next level when overdue. It can't be closed without a written outcome. | An overdue request turns red and lands on the manager's or owner's screen. |
| The author must see the stage: under consideration, decision being made, or being implemented | §2.3 step 5 | "My requests" with a timeline. Status names in plain language matching his three stages. A notification on every change. | The author's view of one request |
| The assignee must be able to ask questions and report status | §2.3 step 4, §2.4 | Clarification requests (the timer pauses while waiting for the author), a comment thread, status reports | Demo scenario 3 (below) |
| Over time the team "will stop proposing anything" | §2.7 | **Closing the loop**: a reasoned answer even on rejection (A-017), a public "done based on your suggestions" feed (A-020 asks for exactly this), and thanks for positive feedback (A-018) | A feed showing implemented A-004 and A-008 |

Pitch angle: many requests in the demo dataset describe the same pain inside everyday work. People don't know who is responsible, what stage something is at, or when it will be done (A-005, A-009, A-011, A-013, A-015), and context gets lost across channels (A-012, A-019). The system gives that transparency for improvement requests first.

## What the spec requires

### Mandatory deliverables (§4.1)

- [ ] Product concept: the problem, and the value for users
- [ ] Target users and key scenarios
- [ ] Interface prototype: main screens and how they connect
- [ ] Technical concept: architecture, technologies and why, data, security and access, integrations
- [ ] Roadmap: MVP first, then later stages
- [ ] Demo, plus an honest list of limitations

### Extra deliverables if we ship a working MVP (§4.2)

- [ ] Source code in a repository (public, or link opens for everyone)
- [ ] Run and demo instructions
- [ ] Implemented features and known limitations
- [ ] Test data, or instructions to prepare it
- [ ] Demo of one or more end-to-end scenarios
- [ ] In the demo, keep **implemented**, **mocked** (external systems) and **planned** clearly apart

### The three questions every solution must answer (§6)

1. What business problem does it solve, and what value does it create?
2. How does it work in practice?
3. How can it grow and integrate with the company's IT (Bitrix24, 1C)?

### Things the concept must describe explicitly

- **§2.5 process:** how a request reaches its owner, how status and outcome are recorded, how the author finds out, how loss is prevented, how recurring problems are detected.
- **§2.6 access:** who can create, view, edit and process requests, and what the author, assignee and manager each see. Anonymity is optional. If we offer it, describe its purpose, limits and effect on processing.
- **§2.7 metrics:** share of requests reviewed, time to first response, share with a recorded outcome, number of improvements implemented. Put exactly these four on the dashboard.
- **§3.6 phasing:** split into MVP, later extensions, and items that need separate technical work.
- **§5 assumptions:** list the significant assumptions we made and their impact.

### Users (§2.2)

Employees (submit and track), department and area heads (review, decide, assign), admins (categories, routing rules), and clients (a later phase: NPS and surveys, explicitly out of MVP scope unless justified). The video adds one more user: **the owner/leadership**, who needs the company-wide overview.

## The demo dataset

[data/seed_requests.json](../../data/seed_requests.json) holds 20 synthetic requests (A-001 to A-020), generated from the .docx.

| Field | Values |
|---|---|
| Type | Предложение 10, Проблема 9, Положительный отзыв 1 |
| Status | Новое 5, На рассмотрении 6, Ожидает уточнения 2, В работе 3, Реализовано 2, Отклонено 1, Закрыто 1 |
| Priority | Высокий 4, Средний 9, Низкий 7 |
| Author roles | 7 (purchasing, accounting, sales, project coordinator, project manager, office, design) |
| Assignee roles | 15 |
| Categories | **18 for 20 requests** |

The dataset also ships **6 demo scenarios** (dataset §4). Treat them as acceptance tests: the jury will expect to see each one.

1. Create a request: type, category, description, optional test attachment.
2. Assign an owner by category, **and show the fallback when no owner is set.**
3. Change status, request clarification, keep the comment history.
4. Show the author the current state and the outcome, **including a reasoned rejection.**
5. Filter by department, category, status and deadline, **and find overdue requests.**
6. Summary: counts by type, share closed, **average time to first response.**

Gaps in the data we need to fill:

- **No dates.** Scenarios 5 and 6 can't work without them. Generate `created_at`, `first_response_at`, `due_at` and the status history for the seed data.
- **No department field.** Scenario 5 filters by department, but the dataset only has the author's role. Derive the department from it (Сотрудник закупок → Закупки, etc.).
- **Categories are too granular.** With 18 categories almost nothing repeats, so the "recurring problems" analytics would be empty. Use about 6 top-level areas for routing (e.g. Процессы и взаимодействие, Документы и данные, IT и системы, Обучение и знания, Офис и среда, Продажи и проекты), with the original categories kept as subcategories or tags. Add 20 to 40 more synthetic requests, including some deliberate near-duplicates, so repeat detection has something to find.
- **Statuses** are listed as examples, not a mandated process (dataset §2). Proposed lifecycle:
  `Новое → На рассмотрении ⇄ Ожидает уточнения → Решение принято → В работе → Реализовано | Отклонено (с обоснованием) → Закрыто`.
  The owner's three stages map onto it: рассмотрение → принятие решения → реализация.

## Where to win

Most teams will build "a form, a list and statuses". These are the differentiators that hit the owner's pains directly:

1. **Nothing gets lost.** Response and decision deadlines, automatic escalation, and an overdue list. This is pain #1 in the video.
2. **The owner's one-screen overview.** The four §2.7 metrics, overdue items, top recurring themes, and implemented improvements.
3. **Closing the loop.** Every request ends with a written answer, there is a public "what we changed" feed, and authors can see the impact.
4. **Recurring problems.** While someone types a request, show similar existing ones and let them say "me too" instead of filing a duplicate. Count those votes as a signal. Text similarity is enough. An LLM for auto-categorization or a summary of themes is optional and needs a working fallback.
5. **Capture where the chaos is today.** Registering a request on someone's behalf (from a meeting or call) and, later, intake from Bitrix24 or Telegram. This way the system absorbs the channels he listed rather than adding one more.

## Suggested MVP scope (11–13 Nov)

> Updated 11 Nov after the [research](reports/Employee%20idea%20management%20solutions.md). The current scope, with details per role, is in [solution-design.en.md §11](../solution-design.en.md#11-mvp-scope).

**Must**, which covers all 6 demo scenarios:
- Create a request: type, category, description, optional proposed solution, optional attachment.
- A receipt on submit: number, owner, answer-by date.
- Rule-based routing, as spec §2.3 requires: rules on type, category and the author's department point to a role; a backup chain (deputy → department head) covers absences; a default rule catches the rest. A coordinator handles only those exceptions. Demo rules are in [solution-design.en.md §3.1](../solution-design.en.md#31-rule-based-routing).
- Statuses with history, comments, a clarification flow, and a mandatory written outcome on close or reject.
- Two deadlines per category (first response, decision), paused while waiting for the author, one extension with a reason.
- **Automatic escalation of overdue requests**: department head, then leadership. Moved up from Should: no product reviewed does this, and it is the owner's main pain.
- "My requests" for the author, with a timeline.
- Assignee and manager inbox with filters (department, category, status, deadline) and overdue highlighting.
- Dashboard with the four §2.7 metrics, counts by type and status, an overdue list, and top categories.
- Roles: employee, assignee, department head, coordinator, leadership, admin. A role switcher for the demo.
- Confidential mode: the author's name hidden from the assignee.
- Registering a request on someone's behalf, with the source channel. Moved up from Should.
- Kazakhstan's working-day calendar and UTC+5 as settings, used for all deadlines.
- Seed data: the 20 requests plus generated dates, departments, extra near-duplicates, and items at every escalation level.

**Should**, if time allows:
- In-app notifications, plus **real Telegram notifications with account linking** (the first Should item to build). Bitrix24 and email notifications shown as clearly labelled mocks.
- "Similar requests" hint and "me too" votes.
- Public feed of implemented improvements.
- The author confirms the fix or reopens the request.

**Later** (roadmap only):
- Bitrix24: single sign-on and the employee and department directory, notifications in Bitrix24 chat, and turning an accepted idea into a Bitrix24 task.
- 1C: the spec names 1С УТ, a trade-accounting system, so it's unlikely to matter for this product. For org structure, Bitrix24 is the better source.
- Client feedback, NPS and surveys (§2.2).
- AI categorization and summaries of themes.

## Open decisions for the team

1. **Format:** working MVP (recommended, §4.3) or prototype plus concept.
2. **Tech stack:** not chosen yet. Pick what the team can ship and deploy by 13 Nov 14:00. The demo link must open for everyone.
3. **Anonymity (§2.6):** recommend a "confidential" option instead of full anonymity. The author's name is hidden from the assignee but visible to an admin, so clarification (scenario 3) still works. Explain this trade-off in the concept.
4. **Primary channel:** decided on 11 Nov. A mobile-friendly web app, plus Telegram for notifications (MVP) and submission through a Mini App (next) ([solution-design.en.md §7.1](../solution-design.en.md#71-telegram)).
5. **Country:** decided on 11 Nov. One country, Kazakhstan: one instance hosted in Kazakhstan, Law No. 94-V, the Kazakh working-day calendar and UTC+5, all as settings rather than code ([solution-design.en.md §8](../solution-design.en.md#8-data-security-legal)). The other open questions (headcount, Bitrix24 plan, judging criteria) are covered by assumptions in [§12](../solution-design.en.md#12-assumptions-and-open-questions).
6. **Selling points and positioning:** see [value-proposition.en.md](../value-proposition.en.md).
