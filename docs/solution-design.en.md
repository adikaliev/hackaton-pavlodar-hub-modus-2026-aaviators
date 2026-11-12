# Solution design: processes, roles, access, integrations

[Русская версия](solution-design.md)

This document describes how the solution works for each participant, and it is the basis for the concept the spec requires (§4.1). The part tagged **[MVP]** is implemented in the working MVP. How to run it is in the [README](../README.en.md); the architecture, data model and stack are in the [technical concept](technical-concept.en.md). The document builds on the team's task analysis and research on existing solutions; the research's key findings are in the [value proposition](value-proposition.en.md).

Stage tags: **[MVP]** means implemented in the working MVP; **[next]** means the first stage after the hackathon; **[later]** means a direction for future development. The full list by stage is in section 11.

**Assumptions we've made** (details in section 12): we design for one country, Kazakhstan, and the messenger is Telegram. The other open questions are covered by assumptions that still need checking.

## 1. Principles

Six rules follow from the owner's video, the spec and the research on how other companies do this:

1. **No request gets lost.** From the moment it's submitted it has a number, an owner and a response deadline. The owner is assigned by rules, not by a person (spec §2.3). When the deadline passes, the request moves up to a manager automatically.
2. **Every author gets a reasoned answer, including a rejection.** Research shows silence discourages people from speaking up more than a reasoned "no".
3. **Submitting takes under a minute, from wherever people already work:** Bitrix24, a phone, Telegram.
4. **Decisions are made as close to the problem as possible:** by the department head at a regular review, not by a central committee.
5. **Results are visible to everyone.** A "Done based on your suggestions" feed is the best proof that speaking up is worth it.
6. **The core works on its own.** Requests, rules, deadlines and the dashboard don't depend on external systems. The solution runs standalone or as a module inside Bitrix24, and each integration can be switched on and off separately (section 7.2).

## 2. Participants

| Role | Who | What they do | What matters to them | Where they work |
|---|---|---|---|---|
| Author | Any employee, including field staff (installation, commissioning, service) | Submits a problem, idea or positive feedback; answers questions; confirms the result | Submit quickly; no fear of consequences; know what's happening with the request | Phone, Telegram, Bitrix24 |
| Assignee | The person the routing rules assigned | Reviews, asks questions, decides, reports progress | A clear queue with deadlines; a way to ask questions; not getting other people's requests | Bitrix24, web app |
| Department head | Head of a department or business area | Sees the department queue, assigns and reassigns owners, receives escalations, runs reviews, logs requests on employees' behalf | See the department's queue and overdue items; not drown in notifications | Web app, team meetings |
| Coordinator | Whoever owns the feedback system: HR or the office manager | Handles exceptions only: requests no rule matched; merges duplicates; moderates tone | Get only the exceptions, and see why a rule didn't match | Web app |
| Leadership | Owner, CEO | Sees the big picture, receives top-level escalations, answers important requests personally | One overview instead of diaries; know who is holding what; see results | Dashboard, weekly digest |
| Colleagues | Other employees | Back open requests ("me too"), read the "Done" feed | See that a problem has already been raised and that things are changing | Feed, request page |
| Administrator | IT or whoever owns the system | Configures categories, routing rules, deadlines, roles, integrations | Change rules and deadlines without a developer | Admin panel |
| Affected person | Employee or manager whose actions a request is about | Must not handle a request about themselves | Fairness: someone else handles a request about them | — |
| External parties | Clients, partners | Feedback and surveys (NPS) | **[later]** A simple form with no login | **[later]** separate form |

## 3. Request lifecycle

### 3.1. Rule-based routing

The spec requires the system to send each request to its owner "according to defined rules" (§2.3), with the administrator managing those rules (§2.2). One of the spec's goals is to cut repetitive manual work (§1.3). So the system assigns the owner by rules, and a person steps in only for exceptions.

**How the owner is chosen.** Rules are checked in order, and the first match wins **[MVP]**:

1. **Sensitive request.** If the author marks the request as being about a specific person's actions, it goes to HR or leadership, bypassing that person (section 4.8).
2. **Special rules** with conditions on request type, category, the author's department or priority. For example, positive feedback in the "Workplace" category goes to HR, while an idea in the same category goes to the head of administration.
3. **Category rule.** A category's rule names the responsible role.
4. **Area rule.** If a category has no rule of its own, the owner of its area (the group of categories it belongs to) is responsible. In the demo table below this is rule 15.
5. **Default rule.** Fires only when nothing else matched, and sends the request to the coordinator. The share of such requests shows how complete the rules are. In the demo table this is rule 16.

**A role, not a name.** A rule names a role, such as "Head of purchasing" or "the author's department head". The system finds the actual person from the org structure: from the directory in the MVP, **[next]** from Bitrix24. When staff change, the rules don't need rewriting.

**Backup when the person is unavailable** (scenario 2 in the demo dataset) is also a rule, not manual reassignment:

assignee → their deputy → the heads above them → coordinator → leadership.

The same chain applies when the person must not handle the request: nobody is assigned their own request or a request about themselves. The request history records it, for example: "Assigned to: Ivanova (covering for Petrov, on holiday)".

**"Not mine".** An assignee doesn't reject a request that isn't theirs. They click "Not mine" with a comment, and the system re-runs the rules without them. If a rule points to them again, the request moves on along the backup chain: to their deputy, then to the heads above them. **[next]** The assignee can also correct the category, and the rules then run for the new category; frequent returns on one rule are shown to the administrator as a sign the rule needs fixing.

**Manual assignment by a manager.** Under the spec (§2.2), managers assign owners. A department head can reassign a request to a specific person in their department, overriding the rule; the coordinator and leadership can reassign it to any employee. A reason is required, and who reassigned the request and why goes into the history. Rules stay the main mechanism, and manual assignment is the exception.

**The author picks the category**, as in the spec's main scenario (§2.3, step 1):
- The categories are in one list, grouped by area.
- The system suggests a category from the text **[MVP]** by keywords; **[later]** with AI. The author confirms or changes it.
- There's a "Don't know" option. Such a request goes by the default rule to the coordinator.

**Managing the rules.** The administrator changes rules without a developer:
- conditions, responsible role and order of checking; the backup (deputy and absence flag) is set in the employee directory, and deadlines are set per category;
- **[MVP]** rules are stored as reference data and edited in the admin panel; the "Rules" page shows them in the order they are checked, with the person who holds each role now;
- **[MVP]** a "who will get it" check on the same page: enter the type, category and author of a sample request and see whom the system assigns and why;
- changes made in the admin panel are logged by the admin panel.

**Rules for the demo.** Rules 1–14 are derived from the dataset's "conditional owners" and reproduce the assignment for all 20 of its requests; an automated test checks this. Rules 15 and 16 catch everything else. Requests from A-021 onwards were added to the demo data by the team; they are synthetic too:

| # | Condition | Goes to | Demo requests |
|---|---|---|---|
| 1 | Marked "about a specific person's actions" | HR, bypassing the affected person | A-027 |
| 2 | Type "Positive feedback" | HR / internal communications | A-018 |
| 3 | Categories «Интеграции и IT», «Коммуникации» | IT specialist | A-007, A-012 |
| 4 | «Каталог и данные» | Product catalog owner | A-003 |
| 5 | «Договорная работа» | Contracts owner | A-009 |
| 6 | «Хранение документов» | Document administrator | A-019 |
| 7 | «Обучение» | Training owner | A-004, A-016 |
| 8 | «Регламенты» | Process owner | A-006 |
| 9 | «Документооборот» | Head of accounting | A-005 |
| 10 | «Проектная деятельность» | Head of projects | A-013 |
| 11 | «Планирование ресурсов» | Head of design | A-014 |
| 12 | «Корпоративная среда» | Head of administration | A-017 |
| 13 | «Межотдельное взаимодействие», «Задачи и коммуникации», «Знания и наставничество», «Прозрачность результатов» | The author's department head | A-001, A-008, A-010, A-020 |
| 14 | «Информационная прозрачность», «Оперативность», «Постановка задач» | The author's business-area head | A-002, A-011, A-015 |
| 15 | A category without a rule of its own | The owner of the category's area | A-025 |
| 16 | Nothing matched | Coordinator | A-024, which the coordinator then reassigned by hand |

The dataset names the owner of A-008 and A-020 generically, as "Руководитель подразделения" (department head), but for A-001 and A-010 specifically, as "Руководитель закупок" and "Руководитель продаж". Rule 13 treats both the same way: the author's department head. For A-020, whose author is in purchasing, that's the head of purchasing. Rule 14 reads "Руководитель направления" the same way, as the author's business-area head.

Rule 2 comes before rule 12. So the positive feedback in A-018 goes to HR, while the idea in A-017, from the same category, goes to the head of administration. This shows the rule order in action. In the company, leadership approves the rules; the table is a demo version.

### 3.2. Statuses

The author sees plain-language wording, not internal status names. The wording follows the three stages from the owner's video: consideration, decision, implementation.

| Internal status | What the author sees | Who sets it | Timer |
|---|---|---|---|
| Новое (New) | "Received. Owner: …, answer by …" | System, on submit, by the rules | First-response deadline starts |
| На рассмотрении (Under review) | "Being reviewed" | Assignee | Decision deadline starts |
| Ожидает уточнения (Awaiting clarification) | "We need your answer" | Assignee | Paused |
| Решение принято (Decision made) | "Accepted, implementation being prepared" | Assignee or head | Planned date |
| В работе (In progress) | "Being implemented", with progress updates | Assignee | Planned date; **[next]** an update at least every 10 working days |
| Реализовано (Implemented) | "Done — please confirm the problem is solved" | Assignee | 7 days for the author to confirm |
| Отклонено (Rejected) | "Rejected", with the reasons and "what we'll do instead" | Assignee or head | — |
| Дубликат (Duplicate) | "Merged with request #…" | Assignee or coordinator | Updates come from the main request |
| Закрыто (Closed) | "Closed" | Author confirmed, or confirmation time ran out | — |

**What the assignee records with a decision** (spec §2.3, step 4):
- the decision: accept, reject, or "already done";
- the reasons;
- next actions: what will be done and by whom;
- the planned date — required when the decision is "accept".

The "next actions" field matches the "example next action" in the demo dataset. A rejection also has a "what we'll do instead" field.

Positive feedback takes a short path: from New straight to Closed, with a note on who it was passed to. There is no separate status for this.

### 3.3. Deadlines

Each category has its own deadlines, and the admin can change them. The defaults come from company and government practice; no study has tested whether they are optimal.

| Deadline | Default | Source |
|---|---|---|
| First human response | 2 working days | Химремонт and ГХК regulations |
| Decision on a problem | 5 working days | Химремонт, ГХК |
| Decision on an idea | 10 working days | Fast track of Russia's ПОС «Решаем вместе», Moscow's «Наш город» |
| Implementation | By the planned date, which the assignee sets with the decision. **[next]** A progress update at least every 10 working days | Team proposal |
| Author's reply to a question | **[next]** 5 working days, then a reminder; after 10, closed with the option to reopen. In the MVP the request waits for the author with the clock paused | Team proposal |

How deadlines work:

- **Pause.** The clock stops while the request waits for the author.
- **Extension.** The decision deadline can be extended once, with a required reason, and the author is notified (as in Kazakhstan's АППК art. 76 and Russia's 59-ФЗ art. 12).
- **Recalculation.** When the owner changes before the first response, the first-response deadline starts again for the new owner. The decision deadline doesn't move, so a handover doesn't make the author wait longer. **[next]** When the category changes, the deadlines are recalculated for the new category (as in ПОС).
- **Priority.** Requests in the demo dataset have a priority: high, medium or low. The author flags the urgency when submitting. High priority halves both deadlines; the factor is a setting. **[next]** The assignee or head can change the priority of a request that is already being handled.
- **Planned date.** An accepted decision must have a planned date. If that date is missed, the request is escalated like any other missed deadline (section 3.4).
- **Working days** follow a calendar kept in settings, not in code: weekend days, working hours and public holidays. Kazakhstan's holidays for 2026–2027 are loaded as data; before rollout they must be checked against the official working-day calendar and then updated every year.
- **Time zone** is UTC+5, the same across Kazakhstan. It's also a setting.

### 3.4. Escalation

The escalation ladder is **[MVP]**; the thresholds are settings:

1. **On the last day of the deadline** — a reminder to the assignee.
2. **1 working day overdue** — the request moves up to the assignee's manager and appears in their queue, marked "overdue with …".
3. **3 working days overdue** — the request moves up to leadership and lands on the leadership dashboard.

The system always shows **who** is holding the request. The dashboard breaks overdue items down by department and person, not just a total count.

**How it works in the MVP.** A background check does the escalation, not a page load. In the demo it runs as a thread inside the web process; in production it is a separate process (`python manage.py worker`). The check can run any number of times: each step is taken once, written to the request history with the moment it happened, and sent as notifications to the assignee, their manager or leadership. Every new stage of a request — a status change, a new owner, an extension or a new planned date — starts the ladder again.

**In the demo.** The demo data is generated relative to the day it is loaded and includes requests at every escalation level. There is also a demo clock: the "+1 working day" and "+3 working days" buttons move the system time, so a juror can watch a fresh request go up the ladder without waiting.

### 3.5. Reopening and rating

- After "Implemented", the author clicks "Confirm" or "Not solved". "Not solved" needs a comment and sends the request back to the assignee with a new planned date. If the author does neither within 7 days, the request closes automatically; the number of days is a setting. **[MVP]**
- After closing, the author rates whether the answer was useful. The rating separates real fixes from box-ticking replies. **[next]**

### 3.6. How recurring problems are detected

The spec asks for this twice (§1.3, §2.5). The mechanisms:

- **[MVP]** Counts by area and category on the dashboard, with each area compared with the previous period (the last 14 days against the 14 days before). You can see where requests pile up and where their number is growing.
- **[MVP]** Merging duplicates. The assignee or coordinator merges similar requests into a main one, which shows a "repeated N times" counter.
- **[MVP]** Suggesting similar requests during submission, and a "me too" button. The number of backers shows how many people face the problem. "Me too" votes and merged duplicates feed the "recurring problems" block on the dashboard.
- **[next]** Reopen rates by category: where fixes often don't work.
- **[later]** Grouping similar themes with AI.

In the organizers' dataset almost every category appears only once, so no repeats show. The demo data has a few similar requests added to show these mechanisms.

## 4. Journeys by role

### 4.1. Author

1. **Opens the form** — from wherever is easiest:
   - **[MVP]** a phone-friendly web app;
   - **[next]** the form inside Telegram (Mini App), a Bitrix24 left-menu item, the Bitrix24 mobile app, or a QR code on a poster in the office or warehouse;
   - **[later]** forwarding an email to a shared address.
2. **Fills in the form.** The type (problem, idea or positive feedback), the category and a description are required. The system suggests the category from the text (section 3.1). Everything else is optional:
   - proposed solution — reporting a problem without a solution is fine;
   - photo or file (on a phone, straight from the camera);
   - urgency, and whether colleagues may see the request;
   - mode: "open" or "confidential" (section 5);
   - a "this is about a specific person's actions" flag — the request then bypasses that person (section 4.8).
3. **Sees similar requests** while typing, and can click "me too" instead of filing a new one. **[MVP]**
4. **Gets a receipt:** number, the owner the rules assigned, and the dates the first response and the decision are due. **[MVP]**
5. **Gets a notification on every status change** — in Telegram **[MVP]**, in Bitrix24 **[next]** (the MVP has a simulator), and always in the app. A button in the notification opens the request, where the author can answer a clarifying question straight away (section 7.1).
6. **Answers clarifying questions** in the request's thread.
7. **Sees the outcome:** the decision and the reasons. Confirms the result or sends the request back to work (section 3.5). **[MVP]**
8. **Sees the request in the "Done based on your suggestions" feed**, if it was implemented and the author allowed colleagues to see it. **[MVP]**

The "My requests" page lists all of the author's requests with each one's history.

### 4.2. Assignee

1. **Gets notified** of a new request. The inbox is sorted by deadline: overdue first, then due soon.
2. **Takes the request.** If it isn't theirs, they click "Not mine" with a comment, and the system re-runs the rules without them (section 3.1). This is not a rejection: nothing is closed on the author. **[next]** Changing the category of a request that has already been submitted.
3. **Asks clarifying questions** while the clock is paused. Internal comments are visible only to the people handling the request.
4. **Decides and writes the reasons.** A request can't be closed or rejected without a written reason. There are templates for common answers **[next]**.
5. **For a large decision, creates a Bitrix24 task** **[later]**. The task's status then updates the request's progress. Until then, the assignee reports progress by hand.
6. **If the deadline can't be met**, extends it once with a reason.

### 4.3. Department head

- Sees the department queue: new, awaiting decision, overdue, escalated.
- **"Review" mode** **[next]**: a list of requests to decide at the weekly team meeting, with one-click decisions. This is how the companies with the highest implementation rates work.
- **Logs a request on an employee's behalf** — from a meeting, a call or an email — and records the source **[MVP]**. From there the request follows the same rules. This answers the owner's complaint about "chaotic" channels directly, and the employee doesn't have to go over their boss's head.
- Assigns or reassigns an owner from their department, overriding the rule, with a reason (section 3.1).
- Has a deputy for holidays; the backup chain in the rules picks this up automatically. In the MVP the administrator records the deputy and the absence flag in the employee directory. **[next]** The head sets their deputy themselves.
- Decides on requests beyond the assignee's authority.

### 4.4. Coordinator

The coordinator doesn't distribute requests by hand: the rules do that. They handle exceptions only:

- Requests that reach the default rule: no rule matched, or the backup chain ran out. The coordinator reassigns such a request by hand, with a reason. Each such case is a reason to add or fix a rule.
- Merges duplicates. **[next]** Splits a request that involves several departments.
- **[next]** Moderates tone. Requests about a specific person's actions go down a separate route already in the MVP (section 4.8).
- Can log a request on an employee's behalf, just as a manager can.

The more complete the rules, the lighter the coordinator's load. The share of requests that reach the coordinator is shown on the dashboard.

### 4.5. Leadership

- **[MVP]** Dashboard:
  - the four metrics from spec §2.7: share of requests reviewed, time to first response, share with a recorded outcome, number of improvements implemented;
  - request counts by type and status, and the share closed (scenario 6 in the demo dataset);
  - overdue items by department and person ("who is holding what"), and the share of first responses given on time;
  - "escalated to me";
  - recurring problems, themes by area compared with the previous period, and new requests per week;
  - the share of requests assigned by rules with no manual step, and how many reached the coordinator;
  - the feed of what was implemented.
- **[MVP]** Text search and filters across all requests and past decisions: the owner's department, the author's department, category, status, type and deadline — overdue, escalated, due today or tomorrow, paused (scenario 5 in the demo dataset). Department heads and the coordinator get the same filters, within their permissions.
- **[next]** A weekly digest in Bitrix24 or by email.
- Can open any request and answer personally. Such answers are marked "answer from leadership".
- **At launch:** personally answers the first batch of requests. In high power-distance companies, a formal channel only works if people see the top person respond.

### 4.6. Colleagues

- See other people's open requests, if the author allowed publication, and the "Done" feed **[MVP]**.
- Can back a request with "me too". The count of backers signals a recurring problem in the analytics.
- Don't see confidential requests, the thread with the author, internal comments, or the names of authors of confidential requests.

### 4.7. Administrator

In the MVP the administrator does all of this without a developer: reference data and settings are edited in the admin panel, and integrations have a page of their own.

- Reference data: areas and categories, departments, employees and roles.
- Routing rules: conditions, responsible role, order of checking, the default rule (section 3.1); deputies and absences for the backup chain are in the employee directory.
- Keywords for category suggestions.
- Deadlines per category, the escalation thresholds, the working-day calendar.
- **[MVP]** The "Integrations" page: a switch for each integration, its status, the last error and the delivery log (section 7.2).

### 4.8. Affected person and sensitive requests

- If a request is about a specific manager's or colleague's actions, it **can never reach that person**. Rule 1 sends it to HR or leadership; if a specific person is named, the system also excludes them from the backup chain.
- Such requests are confidential automatically. Views are written to the request's history: once per session for each person who opens it.
- In the demo data this is request A-027.

### 4.9. External parties **[later]**

Client feedback, surveys and NPS. The spec puts these in later stages. They need a separate form that works without logging in, their own categories and their own routing rules. The architecture should allow for this: an "external" source type and separate permissions.

## 5. Visibility and access

Submission modes:

- **Open**: everyone handling the request sees the author's name. If the author allows it, colleagues can see the request too.
- **Confidential** **[MVP]**: the author's name is hidden from the assignee and department head, but visible to the coordinator and leadership. Messaging the author still works. We recommend this mode over full anonymity, because with full anonymity no one can ask the author a follow-up question.
- **Anonymous** **[later]**. The spec (§2.6) asks for its purpose, limitations and effect on processing:
  - **Purpose:** topics an employee isn't ready to raise even confidentially.
  - **How it works:** the author gets a code to track the request, as in the Aventra app for Bitrix24. We push updates to the author rather than waiting for them to check.
  - **Limitations:** follow-up questions are possible only through the thread tied to the code; the author gets no credit in the "Done" feed; there's a higher risk of harsh, unverifiable requests.
  - **Effect on processing:** the coordinator moderates these requests; if the author doesn't answer a question within 10 working days, the request is closed with the note "no answer from the author".

| What is visible | Author | Assignee | Dept head | Coordinator | Leadership | Colleagues |
|---|---|---|---|---|---|---|
| Text and status | ✔ | ✔ | ✔ own dept | ✔ | ✔ | open and published only |
| Author's name, open | ✔ | ✔ | ✔ | ✔ | ✔ | only if published |
| Author's name, confidential | ✔ | — | — | ✔ | ✔ | — |
| Thread with the author | ✔ | ✔ | ✔ | ✔ | ✔ | — |
| Internal comments | — | ✔ | ✔ | ✔ | ✔ | — |
| Decision and reasons | ✔ | ✔ | ✔ | ✔ | ✔ | in the "Done" feed |
| Analytics | own requests | own queue | department | everything | everything | public feed |

**Who can do what** (spec §2.6: create, view, edit, process):

| Action | Author | Assignee | Dept head | Coordinator | Leadership | Administrator |
|---|---|---|---|---|---|---|
| Create a request | ✔ | ✔ | ✔, including on an employee's behalf | ✔, including on an employee's behalf | ✔ | — |
| Add a message or file to a request | ✔ own | ✔ | ✔ | internal comment only | ✔ | — |
| Change category or priority ¹ | — | ✔ | ✔ | ✔ | — | — |
| Change status, record a decision | — | ✔ | ✔ | "Duplicate" only | ✔ | — |
| Reassign the owner | — | "Not mine" | ✔ within own department | ✔ | ✔ | — |
| Extend a deadline (once) | — | ✔ | ✔ | — | ✔ | — |
| Merge duplicates, split a request ¹ | — | ✔ | ✔ | ✔ | ✔ | — |
| Confirm the result or reopen | ✔ own | — | — | — | — | — |
| Configure categories, rules, deadlines, roles | — | — | — | — | — | ✔ |

¹ Next stage **[next]**: changing the category or priority of a submitted request, and splitting a request. In the MVP the author sets the category and urgency when submitting, and duplicates can be merged.

Rules:

- Requests are never deleted, only archived.
- After submitting, the author can't edit the text, only add a message. This keeps the history honest.
- Every action is logged: who, when, what changed, including which rule assigned the owner.
- The administrator has technical access. In the MVP views of a request about a specific person's actions are written to its history (once per session); **[next]** the same for every confidential request.

## 6. Ease of access and use

**Login**
- **[MVP]** A role switcher for the demo.
- **[next]** In standalone mode, our own login via an email link. With integrations switched on, login through Bitrix24 (OAuth) or through Telegram once the account is linked, with no separate password (section 7.2).

**Intake channels** — the system has to go where requests come from today (email, meetings, calls) rather than become one more place to check:
- logging on someone's behalf **[MVP]**;
- the form inside Telegram **[next]** (section 7.1);
- forwarding an email **[later]**.

**Field staff.** Engineers on site don't have a computer. They need a mobile form, photos straight from the camera and, **[later]**, voice messages with automatic transcription.

**Form**
- Three required fields: type, category (suggested from the text) and description.
- **[next]** Drafts are saved.
- Above the form, a "What happens to your request" block with the promised deadlines.

**Notifications**
- In the MVP every notification is sent at once: the author hears about status changes, the assignee about new requests and the author's replies, and the assignee and managers about escalations.
- **[next]** Less urgent notifications go in a daily digest, so managers don't get worn down.
- Notifications go where people read them. The employee chooses the channel in their profile: automatic (Telegram, then Bitrix24), Telegram, Bitrix24, or in-app only. If delivery fails, the system tries the next channel (section 7.1). In the MVP the Bitrix24 channel is a simulator; email as a fallback is **[later]**.

**Language**
- The interface is in Russian.
- Kazakh **[later]**. In the MVP the interface text sits in the page templates. Moving it into translation files is the first step towards a Kazakh interface **[next]**.

**Interface**
- Statuses in plain language, no jargon.
- Empty screens with hints.
- **[next]** Answer templates for assignees.

**Technical accessibility**
- Works on a small screen and a slow mobile connection.
- Enough contrast.
- Labels on every field.

## 7. Integrations

Principles:

- The Bitrix24 portal is in the cloud. So integration goes only through the REST API, webhooks and apps; on-premise modules and core changes are out. Our system is hosted separately, in Kazakhstan, and talks to the portal through the API.
- **We don't connect to Bitrix24 during the hackathon:** we have no access to the client's portal. We show the integration as a concept and as a working mechanism on our side, with a simulator standing in for Bitrix24 (section 7.2).
- The request system is the source of truth for requests, and Bitrix24 is the source of truth for people, org structure and tasks.
- Each kind of data flows in one direction only, so statuses never disagree.
- Notification channels plug in through one small interface. In the MVP the Telegram channel is a real adapter, and the Bitrix24 channel is a clearly labelled simulator (spec §4.2 requires keeping implemented and mocked parts apart). The "Integrations" page marks each integration as implemented, simulated or planned.

| System | Why | Direction and data | Stage | What to clarify before building it (spec §3.4) |
|---|---|---|---|---|
| Bitrix24: employees and org structure | Rules find the person by role and department; login without a password | Bitrix24 → system: employees, departments, managers (REST `user.get`, `department.get`, OAuth 2.0) | MVP: import from a file in Bitrix24's response format (section 7.2); **[next]** sync through the API and login through Bitrix24 | The plan and REST API access; how up to date the org structure is; where managers and deputies are recorded |
| Bitrix24: notifications | Author and assignee hear about events where they work | System → Bitrix24: a notification with a link to the request | MVP: the simulator records the exact `im.notify.system.add` call in the integration log (section 7.2); **[next]** real sending | Who creates the webhook or app; request rate limits |
| Bitrix24: tasks | An accepted decision becomes a task, and the task's progress becomes the request's progress | System → task; task events → system | **[later]** | Which project or group the tasks go in; who is the task creator |
| Bitrix24: embedding | The system opens from the Bitrix24 left menu and mobile app | Bitrix24 app (placement) | **[later]** | Portal admin permission to install the app |
| Bitrix24: absences | The backup chain accounts for holidays on its own | Bitrix24 → system | **[later]**; in the MVP, an "on holiday" flag in the directory | Whether there's an API for the absence chart, and whether the chart is kept up to date |
| 1С:УТ | Context for purchasing and sales problems: a link to an order, receipt or counterparty | 1C → system, read-only, document number only (OData or HTTP service) | **[later]**; no personal data taken from 1C | Version and access method; which documents are needed; who maintains 1C |
| 1С:ЗУП, if they have it | Backup source of org structure | 1C → system | **[later]** | Whether they have ЗУП, and whether its org structure is more current than Bitrix24's |
| Email | Requests from emails | Email to a shared address → new request with source "email" | **[later]** | Mail server and shared address; how to tell employees' emails from external ones |
| Telegram | Notifications and quick submission for people who don't use Bitrix24 | Bot and Mini App (section 7.1) | MVP: account linking and notifications — a real adapter, covered by automated tests and checked with a real bot (section 7.1); **[next]** action buttons and submission through the Mini App | Who owns the bot; whether Telegram is allowed for work notifications |
| AI (optional) | Category suggestions, duplicate detection, theme summaries | Inside the system | **[later]** | Where to host the model in Kazakhstan; what data it may receive |

**AI rule.** AI suggests, a person confirms, and every correction is logged. This is how eOtinish works. The model must process data in Kazakhstan: on the company's own server or at a local provider. Foreign cloud models must not receive personal data.

### 7.1. Telegram

How it works:

- **Account linking** **[MVP]**. The employee opens a link like `t.me/<bot>?start=<one-time code>` from their profile in the system (**[next]** also from Bitrix24). The bot ties their Telegram ID to their employee record. An unlinked account can't send or see anything, so outsiders can't get in.
- **Notifications** **[MVP]**: the request number, the new status and an "Open" button. The button appears when the system has a public address; on a local address the link goes in the message text. We don't send request text or names to Telegram, because Telegram's servers are outside Kazakhstan.
- **Submission through a Mini App** **[next]**. A button in the bot opens our own web form inside Telegram. The form data goes from the phone straight to our server, not through the bot chat. The user is identified by `initData`, whose signature the server checks against the bot token.
- **Action buttons** **[next]**: "Confirm" and "Not solved" after implementation, and "Reply" to a clarifying question (opens the request in the Mini App). In the MVP a notification has only the "Open" button.
- **What the bot doesn't do** **[MVP]**: take request text as a chat message, so the content doesn't sit in chat history on Telegram's servers. If someone writes to the bot, it replies that requests are submitted in the system. Voice messages could come later, if the lawyers agree.

Telegram works without restrictions in Kazakhstan and is widely used, so it's the main notification channel. If a Telegram notification fails to deliver after several attempts, it goes to the next channel, Bitrix24 (a simulator in the MVP; email is **[later]**), and the in-app notification is always there.

Telegram is the only external integration we build for real: the bot is ours, and it needs nobody else's access, only a bot token in `.env`. Its state: the adapter is covered by automated tests with a fake transport, and on 12 November 2026 it was checked with a real bot: an account was linked with a one-time code and notifications were delivered, both as text with a link and with the "Open" button.

### 7.2. The core and pluggable integrations **[MVP]**

The solution runs both as a standalone system and as a module inside the company's existing tools. Integrations are switched on and off one by one and don't affect the main workflow. We have no access to the client's Bitrix24, so we build everything needed on our side, and the real connection becomes a configuration step for later.

**The core works without a single integration:**
- requests, routing rules, statuses, deadlines and escalation, the thread with the author, decisions;
- the dashboard, search, roles and permissions, the activity log;
- its own employee and department directory, maintained in the admin panel or loaded from a file;
- its own login **[next]** via an email link; in the MVP, a role switcher;
- in-app notifications, which can't be switched off.

**Pluggable integrations.** Each has an on/off switch, settings, a status and its own log:

| Kind | Options | When switched off |
|---|---|---|
| Login | Own (core); Bitrix24 OAuth; Telegram | Own login works |
| Employee directory | Own (core); Bitrix24; 1С:ЗУП; file import | The last loaded directory stays and can be edited by hand |
| Notification channels | In-app (core, always on); Telegram; Bitrix24; email | The notification goes to the next channel that's on, and is always visible in the app |
| Intake channels | Web form (core); Telegram Mini App; Bitrix24 embedding; email | Submission through the web form |
| Tasks | Bitrix24 | The assignee records implementation progress by hand |
| Context | 1С:УТ | The document number is entered by hand |
| AI suggestions | A model hosted in Kazakhstan | Category suggestions by keywords |

Of these options the MVP has in-app notifications, the Telegram channel (real), the Bitrix24 notification channel (a simulator) and the directory import from a file. The others are listed on the "Integrations" page as planned.

**Why switching off an integration doesn't break the core:**
- The core never calls external systems directly. It writes events to the outgoing event log, and the integrations that are on pick events up from there.
- A user action never waits for an external system. A request is registered even if Telegram or Bitrix24 is down.
- The core owns the data. Integrations only sync it, each kind of data in one direction.
- The core is tested with every integration switched off: the core's automated tests run in exactly this mode.

**Two operating modes from one codebase:**
- **Standalone** **[MVP]**: its own web app and its own directory; its own login is **[next]**, and the MVP has a role switcher instead. It suits a company without Bitrix24, or a quick pilot.
- **As a module** **[later]**: opens inside Bitrix24 as an app in the left menu, with employees and login coming from Bitrix24. It can be embedded in another company portal through a frame in the same way. An open REST API of our own, so other systems can create requests and read their status, belongs to the same stage.

In cloud Bitrix24, a "module" is an app opened in a frame inside the portal. The interface stays ours rather than becoming Bitrix24's own interface.

**What the MVP has:**
- **Notification channels with a shared interface.** Each channel answers the same three questions: does it suit this recipient, what request should go out, and how to send it. Telegram is a real adapter; Bitrix24 is a simulator. A new channel is added without changing the rest of the code. **[next]** The same approach for login, the employee directory and tasks. Until then, login through Bitrix24 (OAuth), tasks, embedding, email, 1C and AI are listed on the "Integrations" page as planned.
- **Outgoing event log.** Every event — a new request, a status change, an escalation, a decision — is first written to an events table. A sender picks events up and passes them to the channels that are switched on. On failure it retries, and then falls back to the next channel. So a notification isn't lost even if the external system is down: the "nothing gets lost" principle applies to integrations too.
- **Bitrix24 simulator.** Instead of sending a notification, it records the exact request that would have gone to Bitrix24: the REST method `im.notify.system.add` and its parameters (`USER_ID`, `MESSAGE`, `TAG`). Creating tasks through `tasks.task.add` is planned **[later]**.
- **Directory import.** Employees and departments are loaded from a JSON file in the response format of `user.get` and `department.get`. After the hackathon, the same import can take its data from the real API.
- **An "Integrations" page:** each integration has a badge (implemented, simulated or planned), an on/off switch (for the administrator only), its status and the last error; below them is the delivery log with the recorded REST requests. In the demo we switch Telegram off, and the request still goes through the whole process, with the notification visible in the app.
- **Incoming events** **[later]**: a receiver for Bitrix24 events, such as a task change. The connection point is described but not built in the MVP.

What the client needs to provide to switch on the real integration: a webhook or an installed app with permissions for users, departments, notifications and tasks. The other questions are in the "What to clarify" column of the table above.

## 8. Data, security, legal

**We design for one country, Kazakhstan** (assumption, section 12). There is one instance of the system.

- **Personal data law** — Law No. 94-V: personal data is stored in databases in Kazakhstan (art. 12). So the system is hosted in a Kazakh cloud (e.g. PS.KZ) or on the company's own server in Kazakhstan. Foreign clouds aren't suitable for the database of employee data.
- **Bitrix24.** A portal on bitrix24.kz keeps its data in a Kazakh datacenter, so integrating with it doesn't take data out of the country.
- **Telegram** receives only the request number, status and a link (section 7.1).
- **Country settings** — calendar, time zone, language — live in configuration, not in code. If the company later adds staff in another country, a separate instance with its own settings and in-country data storage can be deployed for them **[later]**.

A lawyer should check the legal conclusions before rollout.

**Data minimization.** Store only name, department, job title and work contacts. No passport details or other unnecessary data.

**Protection**
- Encrypted connections.
- Role-based permissions (section 5).
- Activity log.
- Backups.
- Limits on attachment type and size.

**Retention.** Agree with the client. For example, anonymize requests N years after closing.

**Demo data.** Synthetic only, as spec §3.5 requires.

## 9. Rollout: what's needed besides the software

The research shows software alone doesn't create a feedback culture. The pitch should cover the organizational side too.

1. **A one-page regulation:** deadlines, routing rules (who owns which categories), who the coordinator is, when reviews happen, confidentiality rules.
2. **Launch from the top:** a short message from the owner to staff, like his hackathon video. He handles the first requests personally.
3. **Bring in the backlog.** The questions the owner now keeps in diaries and email go into the system at launch. The system then has content from day one, and the owner gets his overview.
4. **A 4–6 week pilot** in 1–2 departments, then company-wide. In the demo dataset, purchasing, sales and accounting submit the most requests.
5. **Reviews in existing team meetings**, weekly or fortnightly. Less often than that, and staff stop believing in the system.
6. **Recognition instead of money:** the "Done" feed with the author's name, and thanks from leadership. No quotas on the number of ideas and no cash per idea. Severstal's economic effect doubled after it dropped volume targets.

**Pilot metrics**
- Share of answers within the deadline.
- Time to first response.
- Share of requests assigned by rules with no manual step.
- Share of authors who submit a second request.
- Share of reopened requests.
- Number of improvements implemented.

**Risks and responses**

| Risk | Response |
|---|---|
| Managers are overloaded | Digests instead of a stream of notifications, answer templates, reviews in existing meetings |
| Box-ticking replies | Required reasons, reopening by the author, answer rating |
| Fear of speaking up | Confidential mode, logging on someone's behalf, routing around the affected person |
| "Yet another system" | Login and notifications through Bitrix24, then embedding into Bitrix24 |
| Rules assign the wrong person | "Not mine" re-runs the rules, and the administrator fixes the rule; **[next]** the system shows the administrator frequent returns on a rule |
| Off-topic requests | The assignee clicks "Not mine"; the coordinator redirects to the right channel (IT tickets, HR matters) with an explanation |

## 10. Edge cases

| Case | What the system does |
|---|---|
| Assignee on holiday or has left | Backup chain: deputy → the heads above → coordinator → leadership (section 3.1) |
| No owner for the category | Area rule, then the default rule; the request reaches the coordinator only if nothing matched (scenario 2 in the demo dataset) |
| Assignee thinks the request isn't theirs | "Not mine" with a comment: the rules re-run without them; if it's them again, the request moves on along the backup chain |
| Request involves several departments | The rule assigns a main owner; the author sees one request. **[next]** The owner or the coordinator adds co-assignees |
| Complaint about a manager | Rule 1: bypasses that manager, confidential automatically |
| Duplicate | Merged into the main request; the duplicate's author gets updates from the main request; their backing is counted |
| Author has left the company | The request is still handled; the outcome shows in the feed |
| Large idea that needs a budget | "Decision made", a planned date that the system tracks, progress updates from the assignee; **[later]** a Bitrix24 task or project |
| Author doesn't answer a question | In the MVP the request waits with the clock paused. **[next]** A reminder; after 10 working days, closed with a note and the option to reopen |
| Rude or abusive text | **[next]** Moderated by the coordinator without losing the substance |
| Wrong channel (IT ticket, personal HR matter) | Redirected to the right channel, with an explanation to the author |
| Telegram notification not delivered (account not linked, or the employee blocked the bot) | The next channel: Bitrix24 (a simulator in the MVP); email is **[later]**. The in-app notification is always there |

## 11. MVP scope

The research confirmed the original plan, with two changes: automatic escalation moves into the required scope, and a receipt with the answer-by date is added. Routing is rule-based, as the spec requires.

The first column lists what the working MVP implements. Several things first planned for the next stage were built as well: similar requests and "me too", confirmation of the result by the author, the "Done" feed, and the "who will get it" check.

| MVP (implemented) | Next stage | Later |
|---|---|---|
| Phone-friendly submission with attachments (limits on type and size), urgency, "show to colleagues"; receipt with number, owner and deadlines | Connecting to the real Bitrix24, once the client provides a webhook: login, directory sync and real notifications, built as adapters like the notification channels | Embedding in Bitrix24, tasks from decisions |
| Rule-based routing: role by type and category, the author's department head and business-area head, the area rule, the default rule, backup chain, "Not mine", manual reassignment with a reason | Changing the category or priority of a submitted request, with the deadlines recalculated | Load balancing within a group of owners |
| Rules edited in the admin panel; the "who will get it" check | Splitting a request and co-assignees; tone moderation by the coordinator | AI suggestions for category and duplicates, email intake |
| Category suggestion by keywords; similar requests while typing and "me too" | A reminder and automatic closing when the author doesn't answer a question; a reminder to report progress at least every 10 working days | Anonymous mode with a code |
| Statuses, thread with the author, internal comments; a decision with reasons, next actions and a planned date; "what we'll do instead" for a rejection | Answer rating; reopen rates by category in analytics | Client feedback, NPS, surveys |
| The author confirms the result or sends the request back to work; an unconfirmed result closes automatically after 7 days | "Review" mode for meetings, answer templates | Grouping themes with AI |
| Two deadlines per category in working days by the calendar, priority, pause, one extension | Daily digest of notifications; weekly digest for leadership | Context from 1C |
| Escalation by a background check: a reminder, then the assignee's manager, then leadership; every step is in the request history; a demo clock | Saving drafts | Kazakh interface |
| Search and filters across all requests; merging duplicates with a repeat counter | Interface text in translation files, the first step towards the Kazakh interface | Incoming Bitrix24 events; an open REST API for other systems |
| "My requests" with history; the "Done based on your suggestions" feed and colleagues' open requests | Telegram: action buttons in notifications and submission through the Mini App | A separate instance for another country, if needed |
| Inboxes for the assignee, the head and the coordinator: assigned to me, department queue, escalated to me, exceptions | Our own login for standalone mode | |
| Leadership dashboard: the four spec metrics, counts by type and status, share closed, "who is holding what", overdue items, recurring problems, themes compared with the previous period, share of automatic assignment | The head sets their deputy themselves; frequent "Not mine" returns on a rule are shown to the administrator | |
| Confidential mode, requests about a specific person's actions, roles, request history | A view log for every confidential request | |
| Logging on someone's behalf, with the source | | |
| In-app notifications; the employee chooses the notification channel in their profile | | |
| The core and pluggable integrations: outgoing event log, a sender with retries and fallback to the next channel, an "Integrations" page with switches and the delivery log, a Bitrix24 notification simulator, directory import from a file in Bitrix24's format (section 7.2) | | |
| Telegram: account linking and notifications; covered by automated tests and checked with a real bot (section 7.1) | | |
| Admin panel for reference data: categories and their deadlines, rules, roles, the directory, the calendar, escalation thresholds | | |
| Demo data: the dataset's 20 requests with priorities plus the team's own synthetic ones (from A-021), the rules from section 3.1, an employee "on holiday", a few similar requests, dates generated relative to the day of loading, requests at every escalation level | | |
| A role switcher instead of login, for the demo; 80 automated tests, and the core's tests run with every integration switched off | | |

**Needs separate technical work** (spec §3.6):
- embedding in Bitrix24 and syncing the org structure;
- integration with 1C;
- anonymous mode: legal and technical questions;
- AI suggestions, with the model hosted in Kazakhstan;
- deployment for another country.

## 12. Assumptions and open questions

Spec §5 requires us to record significant assumptions and explain how they affect the solution. As of 12 November 2026 we've made these:

| Question | Assumption | Basis | Effect on the solution |
|---|---|---|---|
| Country | One: Kazakhstan | Team decision | One instance, data stored in Kazakhstan, Kazakh calendar and UTC+5 (section 8) |
| Messenger | Telegram | Team decision | Main notification channel; bot and Mini App (section 7.1) |
| Routing rules | Derived from the dataset's "conditional owners"; in the company, leadership approves them | Dataset, spec §2.3 | Demo rules in section 3.1; in the company, the rule table is part of the regulation |
| Headcount | 100–300 employees, some working in the field | Guess from the company's profile | Mobile submission is needed; one coordinator handles exceptions |
| Bitrix24 | Cloud portal; bitrix24.kz domain; plan unknown | Cloud — confirmed by the team on 12.11.2026; domain and plan — assumption | Integration only through the REST API, webhooks and apps (section 7). The system doesn't depend on the plan, since it needs no smart processes. It does need REST API access (webhook or local app) — check on the client's plan |
| Bitrix24 access | We won't get access to the client's portal | Team decision, 12.11.2026 | We don't connect to Bitrix24; the integration is shown through the simulator (section 7.2) |
| Operating modes | Standalone and as a module inside Bitrix24; integrations switched on separately | Team decision, 12.11.2026 | The core doesn't depend on integrations; an "Integrations" page with switches (section 7.2) |
| Technology stack | Django 5.2 LTS; SQLite for the demo and PostgreSQL in production; server-rendered pages | Team decision, 12.11.2026 | One command to run it, and an admin panel for reference data out of the box. Details are in the [technical concept](technical-concept.en.md) |
| HR system | No 1С:ЗУП; org structure is kept in Bitrix24 | Assumption | Employees, departments and managers for the rules come from Bitrix24 |
| Coordinator | HR or the office manager; handles exceptions only | Assumption | A queue of exceptions; the more complete the rules, the lighter the load |
| Evaluation criteria | Unknown; we follow the required deliverables in spec §4 and the three questions in §6 | Spec | The pitch answers the three §6 questions |

We'll update these if the organizers answer. Worth asking in the participants' chat:

1. How many employees, and what share work in the field?
2. What are the hackathon's evaluation criteria?

The Bitrix24 plan and REST API access only matter for the real connection after the hackathon.
