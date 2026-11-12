# Value proposition and how we differ from competitors

[Русская версия](value-proposition.md)

Material for the pitch and the Q&A. Based on the team's market research (data as of 11 November 2026; sources at the end of this document) and the [solution design](solution-design.en.md).

## The core message in one sentence

> No request gets lost: each one has an owner, a deadline and a reasoned answer, and anything overdue moves up to the department head and the owner on its own.

For a slide: **"A guaranteed answer, not a suggestion box."**

## Positioning

Today the owner and managers hear about problems by email, at meetings and on calls, and can't see what happens to them afterwards. For them, our system is a feedback module with a guaranteed answer. Every employee request gets a number, an owner and a deadline, and if nobody answers, the request moves up on its own.

Unlike the idea banks in Bitrix24 and the international platforms, the system:

- handles problems as well as ideas;
- escalates overdue requests;
- shows the owner who is holding what.

## Who we compete with

The main competitor isn't another product but the way things work now: emails, remarks at meetings, phone calls and the owner's diary.

| Alternative | Examples | Strength | What's missing |
|---|---|---|---|
| The current way | Email, meetings, calls, a diary | Nothing to roll out | Requests get lost; no owner, no deadline, no overview |
| Configure Bitrix24 | A smart process with stages and robots | Staff already work in Bitrix24 | Needs the Professional plan (76,000 ₸ a month) and setup by an integrator. Escalation upwards, "authors see only their own" permissions and an owner's screen all have to be built by hand |
| A Bitrix24 Marketplace app | Aventra «Идеи от сотрудников», Brusnika «Управление идеями» | Cheap, installs in a day, has statuses and reminders | These are idea banks. No routing of problems, no escalation to the head and owner, no "who's holding what" screen, no logging on someone's behalf |
| International idea platforms | Ideanote, IdeaScale, Qmarkets, KaiNexus | Mature interface, analytics | From about $10,800 a year for 100 seats (Ideanote), or price on request. Data is stored abroad, though the law requires keeping it in Kazakhstan. No Bitrix24 integration, no Kazakh language |
| Russian "idea factories" | ТЕКОРА «4И», Atwinta, Brainforce | Powerful, built for industry | Designed for holdings with tens of thousands of staff; no published prices; long rollout |
| Helpdesk | Jira Service Management, Frappe Helpdesk | Deadlines (SLAs) and assignment | Feels like IT support; no ideas, no "me too", no feed of results |
| Engagement surveys | Happy Job, Culture Amp | Measure the team's mood | Don't follow an individual request through to a result |

## What sets us apart

### 1. A guaranteed answer

- Each category has two deadlines: the first response and the decision.
- When a deadline passes, the request moves up on its own: assignee → department head → owner.
- A request can't be closed or rejected without written reasons.
- The author confirms that the problem was actually solved.

**Why this is different.** None of the idea platforms and none of the Marketplace apps we studied escalate overdue items upwards. The best of them only remind the assignee: Aventra does so after 3 working days. The published regulations of large companies don't have automatic escalation either.

### 2. Problems and ideas in one flow

A problem ("purchase requests are missing parameters") goes to the responsible person in the department with a short deadline. An idea goes to review with a longer one. Idea banks can't do the first, and helpdesks can't do the second.

The owner is assigned by rules based on type, category and the author's department, and by a backup chain if that person is on holiday. Nobody distributes requests by hand. The demo rules reproduce the assignment for all 20 requests in the organizers' dataset.

### 3. The owner's "who's holding what" screen

On one screen:

- the four metrics from the spec (§2.7);
- overdue requests by department and by person;
- recurring themes;
- "escalated to me";
- the feed of what was implemented.

This answers what the owner said in the video directly: "I have to dig through diaries and frantically recall meetings."

### 4. Capture where the chaos is today

- A manager or the coordinator logs a remark from a meeting, a call or an email on the employee's behalf and records the source. From there the request follows the same rules.
- Field engineers submit from their phones and get notifications in Telegram.

Competitors assume employees will log into a portal on their own.

### 5. A closed loop that brings people back

- A reasoned answer even for a rejection, with a "what we'll do instead" field.
- A "Done based on your suggestions" feed.
- A confidential mode in which the author can still be asked a follow-up question.

**What the research says:**
- A reasoned rejection makes people more likely to submit again; silence puts them off.
- Publishing results regularly raises the number of suggestions about fourfold: from 0.14 to 0.59 per employee per year (182 organizations).

### 6. Built for Kazakhstan and for Bitrix24

- Data is stored in Kazakhstan, as Law No. 94-V requires.
- The interface is in Russian, with Kazakh as the next stage. Notifications go to Telegram, which staff already use.
- It runs standalone or as a module inside Bitrix24. Integrations — login, employees, notifications, tasks — are switched on one by one and don't affect the core. Marketplace apps only live inside Bitrix24, and a configured smart process is tied to a Bitrix24 plan.
- It complements Bitrix24 rather than replacing it. With the integration on, login, employees and notifications come from Bitrix24, and accepted decisions become Bitrix24 tasks.
- No per-seat fees for a foreign service, and no upgrade to the Professional plan.

### 7. A familiar logic

The principle is the same as in eOtinish and Kazakhstan's АППК: a number on registration, a deadline, a reasoned answer, and silence as grounds for escalation. The jury already knows this logic. The difference is that internal deadlines are measured in days, not weeks.

### 8. An easy launch for a mid-size company

No committees, points, quotas or savings calculators. To launch, the company needs:

- a one-page regulation;
- a table of routing rules approved by leadership;
- a coordinator who handles exceptions only;
- a pilot in 1–2 departments.

## Feature comparison

Out-of-the-box capabilities, without custom work, based on the research as of 11.11.2026.

Legend: ✔ — yes; ◐ — partly, or needs configuration; — — no; ? — couldn't verify.

| Capability | Current way | Bitrix24 smart process | Aventra (Marketplace) | Ideanote | Jira Service Management | Our solution |
|---|---|---|---|---|---|---|
| Problems and ideas in one flow | — | ◐ | — | ◐ | ◐ | ✔ |
| An owner and deadline on every request | — | ✔ | ◐ | ◐ | ✔ | ✔ |
| Automatic assignment by rules | — | ◐ | ? | ✔ | ✔ | ✔ |
| Escalation of overdue items to the head and owner | — | ◐ | — | — | ◐ | ✔ |
| Required reasons for every decision | — | ◐ | ✔ | ◐ | ◐ | ✔ |
| Author confirms the result | — | ◐ | — | — | ◐ | ◐ next stage |
| Owner's "who's holding what" screen | — | ◐ | — | ◐ | ◐ | ✔ |
| Logging on someone's behalf | — | ◐ | — | ? | ✔ | ✔ |
| Telegram notifications | — | — | — | — | — | ✔ |
| Data stored in Kazakhstan | ◐ | ✔ | ? | — | — | ✔ |
| Works with Bitrix24 | — | ✔ | ✔ | — | — | ◐ simulator in the MVP, connection in the next stage |
| Works without Bitrix24 | — | — | — | ✔ | ✔ | ✔ |
| "Done based on your suggestions" feed | — | — | — | ◐ | — | ◐ if time allows |

## Weak spots and answers to objections

| Objection | Answer |
|---|---|
| "Why not just configure Bitrix24?" | Bitrix24 is good for tasks and communication, and we integrate with it. But the guaranteed-answer rules — deadlines per category, escalation up to the owner, required reasons, confirmation by the author, the "who's holding what" screen — would have to be built from smart processes on the Professional plan with an integrator's help. We have them ready, and Bitrix24 stays where people work |
| "Aventra is cheaper" | If all you need is a suggestion box, that's true, and we say so. But the owner's complaint isn't a shortage of ideas; it's that problems get lost. Aventra sends reminders, but it doesn't move overdue items up to the head and doesn't handle problems |
| "It's a new product — who will maintain it?" | The codebase is small, the stack is common, and the data stays with the company in Kazakhstan. Development is staged (section 11 of the solution design). We name this risk openly |
| "International platforms have more features" | Most of them are built for corporate innovation campaigns. What's needed here is a guaranteed answer on everyday problems, data stored in Kazakhstan and a link to Bitrix24 — and they have none of these |
| "People still won't write in" | That's why the launch starts with a message from the owner and his personal answers to the first requests, and results are published. Software removes the sense that speaking up is pointless, but the culture comes from leadership |

## Numbers for slides

- **85%** of employees had stayed silent about an important problem at least once; a quarter of them because they thought it was pointless (Milliken et al., 2003).
- **A reasoned rejection** brings people back better than silence does (Piezunka & Dahlander, 1.3 million contributors on crowdsourcing platforms).
- **0.13 ideas per employee per year and 2% implemented** in a typical suggestion scheme. Publishing results regularly raises participation about fourfold (Leach et al., 182 organizations).
- **84% vs 43%**: HR leaders who think they use feedback well, versus employees who see any change from it (Qualtrics, 2023).
- **Over 5 million requests** went through eOtinish in 2025 under the "number — deadline — reasoned answer" rule.
- **About 38.45M ₸ a year** saved by one idea from the chief power engineer of KazTransOil's Pavlodar division.

## Sources

Checked on 11 November 2026.

- Milliken, Morrison, Hewlin, 2003 — [Psych Safety Field Guide](https://explore.psychsafety.com/n/milliken-morrison-hewlin-2003/)
- Piezunka, Dahlander, 2019 — [INSEAD](https://www.insead.edu/faculty-research/publications/journal-articles/idea-rejected-tie-formed-organizations-feedback)
- Leach, Stride, Wood, 2006 — [White Rose eprints](https://eprints.whiterose.ac.uk/86742/)
- Qualtrics, 2023 — [qualtrics.com](https://www.qualtrics.com/articles/employee-experience/hr-execs-overestimate-feedback/)
- eOtinish, requests in 2025 — [gov.kz](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru)
- KazTransOil — [Bizmedia.kz](https://bizmedia.kz/2024-07-17-kaztransojl-sekonomili-okolo-40-mln-tenge-na-elektronagrevatelyah/)
- Severstal, dropping volume targets — [CFO Russia](https://www.cfo-russia.ru/stati/?article=50203)
- Prices: [Ideanote](https://ideanote.io/pricing), [Bitrix24 plans in Kazakhstan](https://www.bitrix24.kz/prices/)
- The Aventra «Идеи от сотрудников» app — [Bitrix24 Market](https://www.bitrix24.ru/apps/app/aventra.idei_ot_sotrudnikov/)
- Personal-data storage in Kazakhstan — [UPPERSETUP](https://uppersetup.com/en/blog/personal-data-and-localisation-in-kazakhstan-in-2026-law-no). This is a consultancy's summary; have a lawyer check it before it goes on a slide.
