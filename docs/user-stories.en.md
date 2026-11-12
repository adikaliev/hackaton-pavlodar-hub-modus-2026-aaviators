# User stories: keeping employees motivated and the process alive

[Русская версия](user-stories.md)

This document answers the two questions that decide the fate of any suggestion system:

1. **Why would an employee write a second time?** People submit the first request out of curiosity. They submit the second only if the first one led somewhere.
2. **Why would the process still work six months from now, once the novelty wears off?** Suggestion boxes are rarely shut down by an order. Usually they just go quiet.

Section 2 lists user stories for each role. Section 3 shows how they add up to motivation, for authors and for the people who answer. Section 4 describes what keeps the process from fading away. The full process is in the [solution design](solution-design.en.md); how we differ from competitors, and the numbers for slides, are in the [value proposition](value-proposition.en.md).

Stage tags are the same as in the solution design: **[MVP]** means implemented in the working MVP; **[next]** means the next stage; **[later]** means a direction for future development. The **[rollout]** tag marks an agreement within the company, not a software feature: the regulation, the meeting rhythm, how managers behave. Numbers such as A-017 are requests in the demo data; you can open them in the MVP.

## 1. The main idea

In his video, the owner isn't worried that there are too few ideas. He is worried that "the team will simply stop talking about anything" because issues never get resolved. Research describes exactly this:

- 85% of employees had at least once kept quiet about an important problem; a quarter of them because they thought speaking up was pointless.
- Whether people speak up depends more on whether they see their words have an effect than on whether they feel safe.
- A reasoned rejection brings people back better than silence does.
- Feedback to the author doubles the number of suggestions, and regular publicity of outcomes roughly quadruples it. Cash rewards are linked neither to the number of suggestions nor to implementation; recognition is linked to both.

Two principles follow, and this document is built on them:

- **Motivation is proof that speaking up makes sense**, not prizes or points. At every step the author sees the request moving, and at the end sees what changed and that it was noticed.
- **The process doesn't depend on anyone's memory or willpower.** If the assignee forgot, the department head is busy and the coordinator is on holiday, the request still isn't lost: deadlines and escalation push it up. People set the rhythm; the system makes sure it can't slip unnoticed.

## 2. User stories by role

Each story reads as "As a <role>, I want …, so that …". The "How it works" column shows how the system meets that need.

### 2.1. Employee: the author of a request

The author is any employee: an office specialist who works in Bitrix24 all day; an engineer on site with nothing but a phone; a newcomer who doesn't yet know whom to ask.

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-01 | report a problem from my phone in a minute, with a photo, even if I don't know the fix | I don't put it off and forget | Three required fields: type, category (the system suggests it from the text) and description. A proposed solution is optional. Photos straight from the camera; pages work on a 390 px wide screen | [MVP]; form inside Telegram — [next]; voice message — [later] |
| US-02 | know right away who will answer and by when | I'm sure the request didn't vanish | A receipt: number, assignee, and the dates for the first answer and the decision | [MVP] |
| US-03 | see that someone has already raised my problem, and back it | I don't write the same thing again and still learn the outcome | Similar requests appear while I type; a "Me too" button. Backers are notified when a decision is made and when it is implemented | [MVP] |
| US-04 | hear about progress where I already work | I don't have to log in to check | A notification on every status change, in Telegram and inside the app; the channel is chosen in the profile | [MVP]; Bitrix24 — [next], a simulator in the MVP |
| US-05 | answer a clarifying question right in the request | the conversation doesn't spill over into email and calls | A thread inside the request; the button in the notification opens it. While the assignee waits for the author, their deadline is paused (A-005) | [MVP]; a reminder to an author who doesn't answer — [next] |
| US-06 | get an honest answer, even if it's "no" | I understand why and don't feel brushed off | A request can't be rejected without reasons. A rejection has a "what we'll do instead" field (A-017) | [MVP] |
| US-07 | confirm myself that the problem is solved, or send it back | "done" means done, not just closed | After "Implemented", the "Confirm" and "Not solved" buttons, the latter with a comment. If the author stays silent for 7 days, the request closes (A-004) | [MVP] |
| US-08 | have colleagues see that I proposed this change | my contribution is noticed | The "Done based on your suggestions" feed, with the author's name and the number of backers, if the author allowed showing the request to colleagues | [MVP] |
| US-09 | report a problem with a manager or colleague without fear of consequences | I can raise what people usually keep quiet about | The "this is about a specific person's actions" flag: the request goes to HR, bypassing that person, becomes confidential, and views are logged in its history (A-027). Confidential mode hides the author's name from the assignee (A-028) | [MVP]; anonymous mode with a tracking code — [later] |
| US-10 | mention a problem at a team meeting or in conversation instead of filling in a form | I don't have to go over my boss's head | A department head or the coordinator registers the request on my behalf and records the source. I remain the author: the receipt and notifications come to me (A-023 — from a meeting, A-034 — from a call) | [MVP] |
| US-11 | thank a colleague or another department | good work is visible too, and the system doesn't become a complaints book | The "Positive feedback" type: it goes to HR, the assignee passes it on to the person, and the author gets a confirmation (A-018) | [MVP] |
| US-12 | rate whether the answer helped | a formal brush-off doesn't count as a resolution | A "helpful / not helpful" rating after closing | [next] |
| US-13 | see all my requests and their history | I don't have to remember what I wrote, when and to whom | "My requests" with the history of each | [MVP] |

### 2.2. Colleagues

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-14 | see what changes in the company thanks to employees' suggestions | I believe writing makes sense, even before my first request | The "Done based on your suggestions" feed | [MVP] |
| US-15 | see colleagues' open requests and back the ones that matter | it's clear the problem affects many people | A "Now in progress" panel next to the feed, and the "Me too" button. The assignee sees the number of backers, and on the dashboard such requests show up under "Recurring problems" | [MVP] |

### 2.3. Assignee

The assignee isn't a feedback specialist but an ordinary employee or manager with a day job. If the system gets in their way, they will start answering formally, and authors will notice.

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-16 | receive only requests that are mine to handle | I don't waste time on other people's issues | Assignment by rules. "Not mine" with a comment reapplies the rules without me; nothing is closed for the author | [MVP] |
| US-17 | see my queue sorted by deadline | I know what's urgent | The inbox: overdue first, then due soon | [MVP] |
| US-18 | get a reminder before the deadline passes | I can answer in time, rather than hear about it from my boss | A reminder on the last day of the deadline | [MVP] |
| US-19 | ask the author a question without breaking the deadline | I understand the issue instead of guessing | A thread with the author; while they answer, the deadline is paused. Internal comments are visible only to the people handling the request | [MVP] |
| US-20 | move the deadline honestly if the issue is hard | I don't mislead the author or get escalated for a hard question | One extension with a required reason; the author is told about it | [MVP] |
| US-21 | set a planned date for a big decision and report progress | the author sees movement even if implementation takes a month | An accepted decision requires a planned date. Each progress update reaches the author as a notification; changes to the planned date stay in the history | [MVP]; a reminder to report progress every 10 working days — [next]; a Bitrix24 task — [later] |
| US-22 | answer common questions from a template | an answer takes minutes, not half an hour | Answer templates | [next] |

### 2.4. Department head

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-23 | see my department's queue: new, awaiting a decision, overdue | I manage it, rather than hear about problems from the owner | The department queue in the inbox, with filters | [MVP] |
| US-24 | learn about a subordinate's overdue request before the owner does | I can resolve it at my level | 1 working day after the deadline, the request appears for the assignee's manager, marked "overdue with …" | [MVP] |
| US-25 | review the queue at the weekly team meeting in 10–15 minutes | decisions are made close to the problem, without a separate committee | In the MVP, the department queue with filters; a "Review" mode with one-click decisions is the next stage | [MVP] / [next] |
| US-26 | record a remark from a meeting on an employee's behalf | a good point isn't forgotten and the author gets the credit | Registration on an employee's behalf, with the source recorded (A-023) | [MVP] |
| US-27 | reassign a request within my department | I can account for what the rules don't know | Reassignment with a required reason, recorded in the history | [MVP] |
| US-28 | hand requests to a deputy while I'm on holiday | holidays don't stop the work | The backup chain: deputy → higher manager → coordinator → leadership (A-016) | [MVP], the administrator enters the deputy; the department head does it — [next] |
| US-29 | get non-urgent notifications as one daily digest | I'm not buried in notifications | A daily digest | [next] |

### 2.5. Coordinator

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-30 | receive only exceptions | I don't become a manual dispatcher for every request | A request reaches the coordinator only if no rule matched or the backup chain ran out (A-024). The share of such requests is on the dashboard | [MVP] |
| US-31 | merge duplicates | one problem is one request, and repeats are counted | Merging into the main request, with a "repeated N times" counter; the duplicate's author follows the main request | [MVP] |
| US-32 | see where the rules go wrong | I fix the cause, not each case | Every exception is a reason to fix a rule. Frequent "Not mine" on the same rule will be visible in the system | [MVP] / [next] |

### 2.6. Owner and leadership

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-33 | see the whole company's issues on one screen | I don't dig through diaries or try to recall meetings | The dashboard: the four spec metrics, requests by type and status, the share closed, the feed of implemented items | [MVP] |
| US-34 | see who is holding what | I can ask a specific person, not "everyone in general" | "Who is holding what": overdue items by department and person | [MVP] |
| US-35 | receive only what wasn't resolved further down | I don't become the bottleneck | 3 working days after the deadline, the request moves up to leadership and lands in "Escalated to me" | [MVP] |
| US-36 | answer a request personally, visibly | staff see that I read them | An answer from leadership is marked in the request's history | [MVP] |
| US-37 | see recurring problems and growing themes | I fix causes, not individual cases | "Recurring problems" (backers and duplicates), themes by area compared with the previous 14 days, new requests by week | [MVP] |
| US-38 | get a weekly digest without opening the system | I keep my finger on the pulse even when travelling | A digest in Bitrix24 or by email | [next] |
| US-39 | know whether the process is alive | I can step in before people go quiet | Process health metrics (section 4.4) | [MVP] partly, the rest — [next] |

### 2.7. Administrator

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-40 | change categories, rules, deadlines and the calendar without a programmer | the regulation and the system don't drift apart | The admin panel; the "Rules" page with the "who will get it" check | [MVP] |
| US-41 | switch an integration off without stopping the system | a Telegram or Bitrix24 outage doesn't lose requests | Switches on the "Integrations" page. Notifications wait in the outgoing event log and go to the next channel; inside the app they are always available | [MVP] |

### 2.8. The person a request is about

| # | I want to… | so that… | How it works | Stage |
|---|---|---|---|---|
| US-42 | have someone else handle a request about my actions | the review is fair | Rule 1 excludes me from both the assignment and the backup chain; views of such a request are logged (A-027) | [MVP] |

## 3. How employees stay motivated

### 3.1. The author's journey: where the will to write disappears

At every step there is a moment when a person may decide "never again". For each of those moments the system or management has an answer.

| Step | What kills the will to write | What we do | Stories |
|---|---|---|---|
| Before the first request | "Nothing will change anyway" | The "Done" feed shows real changes. At launch the owner personally answers the first requests [rollout] | US-14, US-36 |
| Submitting | "No time", "I don't know where to write", "I don't have a ready solution" | A one-minute form on the phone; the system suggests the category and the rules pick the assignee; a solution is optional | US-01 |
| | "I'm afraid", "I don't want to go over my boss's head" | Confidential mode, bypassing the affected person, registration on an employee's behalf | US-09, US-10 |
| Right after submitting | "It vanished" | A receipt with the assignee's name and the dates | US-02 |
| Waiting | Silence | A notification on every status change. If the assignee stays silent, the request moves up by itself: the author doesn't have to chase or complain | US-04, US-24, US-35 |
| The answer | A brush-off, a "no" without reasons | Required reasons and "what we'll do instead"; answer rating [next] | US-06, US-12 |
| Implementation | "They said it's done, but nothing changed" | The author confirms or sends it back to work | US-07 |
| Afterwards | "Nobody knows it was my idea" | The name in the "Done" feed; the "answer from leadership" mark; thanks from the manager at the team meeting [rollout] | US-08, US-36 |
| Next time | "I got lucky once" | Regular queue reviews every week or two [rollout]: employees see that this always happens, not by chance | US-25 |

### 3.2. Example: how one request leads to the next

This is how request A-001 from the demo dataset could play out.

1. A purchasing specialist notices that equipment requests often lack the item's purpose and parameters, and submits a request from their phone.
2. The receipt: the assignee is the head of purchasing; first answer within 2 working days.
3. The head of purchasing asks for an example of a correctly filled-in request. The author opens the request from the Telegram notification and attaches a file. While they answer, the deadline is paused.
4. The decision: required fields will be added to the request template; the planned date is two weeks away.
5. The template is updated. The author clicks "Confirm", and the change appears in the "Done" feed with their name. Two colleagues who had clicked "Me too" get a notification.
6. At the team meeting, the department head says requests now come back for rework less often, and names the author.

This is the cycle employees see in the feed and at meetings, and it is what the whole system is for: people submit the next request because the previous one led somewhere.

### 3.3. Recognition instead of money and quotas

**What we do:**

- **We celebrate implementation, not submission.** The feed shows what was done, with the author's name and the number of backers.
- **Thanks come from the top** [rollout]. The owner or a manager names the author at a company meeting or a team meeting. In a company where a lot depends on the person at the top, this weighs more than any prize.
- **We make thanking a colleague as easy as complaining.** Positive feedback is a full request type.
- **We count backing as a contribution.** "Me too" shows how big a problem is, and backers get updates on it.

**What we deliberately don't do:**

| We don't | Why |
|---|---|
| Pay for each idea | In a study of 182 organizations, cash rewards were linked neither to the number of suggestions nor to implementation, while non-monetary recognition was linked to both |
| Set quotas on the number of suggestions | Severstal dropped its volume targets: the number of ideas fell and the economic effect doubled. Quotas produce a stream of trivia, assignees drown in it, and the process dies |
| Introduce points, leaderboards by submissions, prize shops | That's machinery for holdings with tens of thousands of employees. For a company of 100–300 people it is extra work that rewards quantity, not results |
| Run one-off "idea campaigns" | A spike followed by silence. The process needs a steady rhythm, not a campaign |

If the company wants to reward big improvements materially, that is a management decision about a specific implemented improvement [rollout], not a payment for submitting.

### 3.4. Motivating the people who answer

Processes die more often because of the people who answer than because of the authors. If answering is a burden, answers become formal and late, and authors stop writing. So:

- **The assignee gets only what's theirs.** Rules by category, and "Not mine" (US-16).
- **A warning first, escalation second.** A reminder on the last day of the deadline (US-18).
- **A hard question is not a failure.** One honest extension with a reason (US-20); changes to the planned date are visible in the history, not hidden.
- **Answering is quick.** A review in a team meeting that already exists instead of a separate committee [rollout]; answer templates [next].
- **Escalation is a signal, not a reprimand** [rollout; write it into the regulation]. The history shows at which step and with whom the request got stuck. Often the assignee is waiting for another department, and the manager's job is to remove that obstacle, not to punish.
- **Good work is visible.** Managers acknowledge those who close requests on time and with substance [rollout]. Deadlines met, not the number of requests closed, measure a department's work (section 4.6).

## 4. Keeping the process from fading away

### 4.1. How such systems usually die

| How it fades | Example | What we do about it |
|---|---|---|
| Requests pile up unanswered, and people stop writing | A hospital: ideas worth ≈ $20M, ≈ $1M approved, ≈ $70K implemented, after which submissions dried up | A deadline on every request, escalation on silence (section 4.2) |
| Collecting more than can be decided | Gazprom Neft: 96% of employees signed up to the portal, about 6% of ideas implemented | Decisions are made in the department, close to the problem; a big decision requires a planned date, and the system tracks it |
| Closing without a fix | New York, 311: about 46% of 2018 complaints to the transport department were closed with an ambiguous resolution | Required reasons and confirmation by the author |
| Reviewing too rarely | A vendor of an idea-bank module warns that if ideas are reviewed less than once or twice a month, staff may lose faith | A review every week or two in a team meeting that already exists (section 4.3) |
| It rests on one enthusiast, who goes on holiday or leaves | — | Rules name a role, not a person; the backup chain; the coordinator handles only exceptions |
| Leadership stops looking | In high power-distance countries, a formal channel increases speaking up only where employees perceive a participative climate (421 units, 24 countries) | Escalation to leadership, the dashboard, a weekly look by the owner (section 4.3) |

### 4.2. What the system enforces

These mechanisms work even if nobody remembers the request:

- **It can't be lost.** From the moment it's submitted, the request has a number, an assignee and a deadline. There are no "nobody's" requests: if no rule finds a person, the request goes to the coordinator. [MVP]
- **It can't go silent.** Escalation is run by a background check, not by opening a page. Even if nobody logs in for a week, overdue requests still move up. [MVP]
- **The deadline can't be moved quietly.** One extension, with a reason, and the author is told. An accepted decision requires a planned date; if it's missed, the request is escalated. [MVP]
- **It can't be closed as a formality.** No closing or rejecting without reasons; the author confirms the result. [MVP]
- **It can't get stuck in a long implementation.** The planned date is under escalation control [MVP]; a reminder to report progress at least every 10 working days [next].
- **It can't be lost to a holiday or a resignation.** A rule names a role, and the system finds the person in the directory; the backup chain covers absences. [MVP]
- **It can't be lost to an integration failure.** An event is first written to the outgoing event log; the sender retries and moves to the next channel; inside the app the notification is always there. [MVP]
- **It can't hang forever waiting for the author.** A reminder to the author, then after 10 working days closing with the right to reopen. [next]

**If the assignee forgot.** The first-answer deadline is 2 working days. On the last day the assignee gets a reminder. One working day after the deadline, the request appears for their manager, marked "overdue with …". Two working days later it is on the leadership dashboard, under "Who is holding what". The author doesn't have to do anything. In the MVP you can see this with the "+1 working day" and "+3 working days" buttons.

### 4.3. The rhythm people set [rollout]

The system doesn't create a culture, but it supports every step of one.

| How often | Who | What | How the system helps |
|---|---|---|---|
| Daily | Assignees | Check the inbox: only their own requests, sorted by deadline | Notifications and reminders [MVP]; daily digest [next] |
| Every week or two | Department head, at a team meeting that already exists | Reviews the queue: decisions, reassignments, thanks | The department queue and filters [MVP]; "Review" mode [next] |
| Weekly | Owner | 10 minutes on the dashboard: "Who is holding what", "Escalated to me"; one or two personal answers | The dashboard [MVP]; weekly digest [next] |
| Monthly | Owner or coordinator | Shows staff 3–5 changes from the "Done" feed with the authors' names, at a company meeting or in a newsletter | The "Done" feed [MVP] |
| Quarterly | Coordinator and administrator, with leadership | Revise categories, rules and deadlines: where the exceptions, "Not mine" and overdue items are | The dashboard and the "who will get it" check [MVP] |

### 4.4. Process health metrics

The spec (§2.7) leaves target values to be defined separately. We propose setting them after the pilot. The direction matters more than the value: each metric is an early warning of a specific problem.

| Metric | Warning sign | What it means | What to do | Where to see it |
|---|---|---|---|---|
| Share of first answers on time | Falling | Assignees are overloaded or don't see answering as part of their job | Open "Who is holding what" and talk to the specific manager; check whether people are getting requests that aren't theirs | Dashboard [MVP] |
| Overdue items by department and person | The same names for weeks | A bottleneck | Redistribute categories, appoint a deputy | Dashboard [MVP] |
| New requests by week | Falling several weeks in a row | People are going quiet — the very risk from the owner's video | Check whether the "Done" roundup went out, whether reviews happened, whether leadership is answering | Dashboard [MVP] |
| Number of implemented improvements | None in a month | The feed runs dry, and there's nothing left to prove the point | Leadership picks a few quick improvements and sees them through | Dashboard [MVP] |
| Rejections versus accepted decisions | Noticeably more rejections | People hear "no" more often than they see change | Check the reasons and the "what we'll do instead" field | Dashboard, statuses [MVP] |
| Share of requests reaching the coordinator | Rising | The rules have fallen behind the org structure | Fix the rules | Dashboard [MVP] |
| Share of authors who submit a second time | Low | The first experience disappointed them — the main measure of trust | Look at how their first requests ended: rejections, deadlines, brush-offs | [next]; during the pilot, from the request list |
| Share of reopened requests | Rising | Brush-offs instead of fixes | Go through the categories with frequent reopens with the assignees | [next] |

### 4.5. The first 90 days [rollout]

The first weeks decide whether the system becomes a working tool. So the launch is planned as carefully as the software.

1. **Before launch, 1–2 weeks.** A one-page regulation: deadlines, who owns which categories, who the coordinator is, when reviews happen. Leadership approves the rules table. The questions the owner now keeps in diaries and email go into the system, so it has content from day one. A short message from the owner to staff.
2. **Weeks 1–6: a pilot in 1–2 departments.** In the demo dataset, purchasing, sales and accounting submit the most requests. The owner personally answers the first batch of requests. Reviews every week.
3. **End of week two: the first "Done based on your suggestions" roundup.** Even if it's two or three small changes, they must be real.
4. **Week 6: pilot results**, measured by the metrics in section 4.4 and the pilot metrics in the [solution design](solution-design.en.md#9-rollout-whats-needed-besides-the-software) (section 9). Rules and deadlines adjusted, and a decision on the company-wide launch.
5. **Months 2–3: the whole company.** The rhythm from section 4.3 becomes routine. The first quarterly review of the rules.

### 4.6. Who is responsible for keeping the process alive [rollout]

- **The owner** sponsors the process. His visible answers build trust; once a week he looks at the dashboard. Software removes the sense that speaking up is pointless, but the culture comes from the leader.
- **Department heads** hold regular reviews and make decisions close to the problem.
- **The coordinator** handles exceptions, duplicates, signals that rules are out of date, and the monthly "Done" roundup.
- **The administrator** keeps rules and deadlines in line with the current org structure.
- **A department's performance is measured by answers on time and confirmed results**, not by the number of requests or ideas. PGK does this: meeting deadlines on initiatives is a team KPI, and the system shows which department caused a delay.

## Sources

Data checked on 11 November 2026.

- Milliken, Morrison, Hewlin, 2003: 85% kept quiet, a quarter out of futility — [Psych Safety Field Guide](https://explore.psychsafety.com/n/milliken-morrison-hewlin-2003/)
- Sherf, Parke, Isaakyan: perceived impact and psychological safety — [London Business School](https://www.london.edu/faculty-and-research/academic-research/d/distinguishing-voice-and-silence-at-work-unique-relationships-with-psychological-safety-impact-and-burnout)
- Piezunka, Dahlander, 2019: a reasoned rejection beats silence — [INSEAD](https://www.insead.edu/faculty-research/publications/journal-articles/idea-rejected-tie-formed-organizations-feedback)
- Leach, Stride, Wood, 2006: feedback to the author, publicity of outcomes, money and recognition — [White Rose eprints](https://eprints.whiterose.ac.uk/86742/)
- Huang, Van de Vliert, Van der Vegt, 2005: power distance and formal channels — [RePEc](https://ideas.repec.org/a/cup/maorev/v1y2005i03p459-482_00.html)
- Severstal, dropping volume targets — [CFO Russia](https://www.cfo-russia.ru/stati/?article=50203)
- Gazprom Neft, initiatives portal — [IT HR Awards](https://ithrawards.ru/gazprom-neft-portal-iniciativ)
- A hospital whose ideas never reached implementation — [KaiNexus](https://www.kainexus.com/mark-graban-and-greg-jacobson-on-why-most-idea-programs-stall-and-how-to-close-the-gap-between-ideas-submitted-and-improvements-actually-implemented)
- New York City 311 — [NYC Council](https://council.nyc.gov/data/311-agency/)
- MCART, how often to review ideas — [mcart.ru](https://www.mcart.ru/blogs/bank-idey/)
- PGK, initiative deadlines as a team KPI — [Habr](https://habr.com/ru/post/722254)
