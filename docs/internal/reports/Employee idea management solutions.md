# Guaranteed answers keep employees speaking up

> **Note (added 11 Nov 2026):** this report assumes the company is based in Kazakhstan, as the owner's video suggests. The team has since fixed this as an assumption: **one country, Kazakhstan**. See [solution-design.en.md §8](../../solution-design.en.md#8-data-security-legal).

Organizations that keep employee problems and ideas flowing don't win by collecting more of them. They win by guaranteeing that every item is registered, owned, answered with reasons within days, and visibly acted on. Research, corporate programs and government systems agree on this. People speak up when they see their input has an effect, not merely when they feel safe. A reasoned "no" brings contributors back, while silence drives them away. The median UK suggestion scheme produced **0.13 ideas per employee per year and implemented 2%**, while systems built on fast local decisions reach tens of ideas per person and implement 70–90%+. The closest blueprint for ГК «Модус Трейд» is Kazakhstan's own appeal regime. The АППК and eOtinish require mandatory registration with a number, a fixed answer deadline, at most one reasoned extension and a reasoned answer, and they treat silence after the deadline as a refusal the applicant can escalate. Ready-made tools each cover only part of this:

- **Global suites** are quote-priced, have no Bitrix24 or 1C connectors and no Kazakh UI, and host data abroad, which conflicts with Kazakhstan's data-localization rule.
- **Bitrix24** gets roughly 70–80% of the way, through the Aventra «Идеи от сотрудников» app or a smart process on the Профессиональный plan.
- **1C** has nothing current.
- **Russian «фабрика идей» platforms** are built for holdings with tens of thousands of workers.
- **Open-source tools** handle either ideas (Fider) or tickets (Frappe Helpdesk), not both.

None of them handles what the owner actually complained about:

- problems and ideas in one flow;
- per-category deadlines with automatic escalation up the chain;
- closure that the author confirms;
- one screen showing who is holding what.

That gap should be the core of the MVP. Concretely, move auto-escalation from "Should" to "Must". Pitch the product as the "nothing gets lost" rule set that runs next to Bitrix24 now and inside it later, not as another idea box and not as a Bitrix24 replacement.

## Futility, not a shortage of ideas, is what silences employees

The owner worries that staff "will stop proposing anything". Research has documented exactly this pattern. In interviews by Milliken, Morrison and Hewlin, **34 of 40 employees (85%)** had at least once felt unable to raise an important issue, and **25% cited a sense of futility**. Suggestions for improving processes were among the topics most often withheld (35%) ([Psych Safety Field Guide](https://explore.psychsafety.com/n/milliken-morrison-hewlin-2003/)). McClean, Burris and Detert studied 136 restaurants. Where managers lacked the orientation, participation or resources to act, employee voice went with **higher** later turnover. Where managers had them, voice went with lower turnover. When voice goes unanswered, people leave ([University of Arizona](https://experts.arizona.edu/en/publications/when-does-voice-lead-to-exit-it-depends-on-leadership/)). Sherf, Parke and Isaakyan separated the two drivers. **Perceived impact** is more strongly linked to speaking up, and psychological safety is more strongly linked to staying silent. Making people feel safe does not by itself produce ideas; they also have to see something happen ([London Business School](https://www.london.edu/faculty-and-research/academic-research/d/distinguishing-voice-and-silence-at-work-unique-relationships-with-psychological-safety-impact-and-burnout)). The cost is uneven. In Detert and Burris's study of 3,149 employees, manager openness affected the **best performers** most ([Field Guide](https://explore.psychsafety.com/n/detert-burris-2007/)). A system that swallows input loses its most valuable contributors first.

The flip side is that answering works, even when the answer is no. Piezunka and Dahlander analysed **1.3 million contributors across 70,159 organizations** on crowdsourcing platforms. A rejection *increased* newcomers' willingness to submit again compared with hearing nothing, and the effect was stronger when the rejection came with an explanation ([INSEAD](https://www.insead.edu/faculty-research/publications/journal-articles/idea-rejected-tie-formed-organizations-feedback)). These were external contributors, not employees, but the mechanism transfers: silence does more damage than "no".

Leach, Stride and Wood surveyed 182 UK organizations and provide both the baseline and the levers ([White Rose eprint](https://eprints.whiterose.ac.uk/86742/)). The median scheme drew **0.13 ideas per covered employee per year and implemented 2%**. Compared with schemes weak on each feature:

| Feature | Suggestion rate when weak | Suggestion rate when strong |
|---|---|---|
| Feedback to the author | 0.14 | 0.28 (double) |
| Frequently updated publicity of outcomes | 0.14 | **0.59** (four times) |

Decentralized schemes beat central committees. Monetary rewards were unrelated to suggestion or implementation rates, while non-monetary recognition predicted both. Only management support uniquely raised the implementation rate, from 0.17 to 0.30. Vendor survey data point the same way: **84% of HR leaders** rate their use of employee feedback as effective, but only **43% of employees** have seen positive change from it ([Qualtrics](https://www.qualtrics.com/articles/employee-experience/hr-execs-overestimate-feedback/)).

The local context makes the problem sharper, not softer. Only **11% of employed Russians** voiced any idea at work in the previous three years, according to an HSE ISSEK survey from 2023/24 ([HSE ISSEK](https://issek.hse.ru/mirror/pubs/share/1026160741.pdf)). No Kazakhstan equivalent was found; Gallup puts engagement in Kazakhstan at **23%** in 2025 data ([Gallup](https://www.gallup.com/workplace/705842/state-global-workplace-kazakhstan-country-level-data.aspx)). Huang, Van de Vliert and Van der Vegt studied 421 units in 24 countries. In high power-distance countries, formal involvement channels went with more voice **only where employees also perceived a participative climate** ([RePEc](https://ideas.repec.org/a/cup/maorev/v1y2005i03p459-482_00.html)). Morrison's 2023 review notes that power distance breeds resigned or harmony-preserving silence rather than fearful silence ([Field Guide](https://explore.psychsafety.com/n/morrison-2023.md)). Kazakh management culture is described as high power distance, with position-based authority and little delegation ([Universum](https://7universum.com/ru/economy/archive/item/13584)).

Two consequences follow for an owner-led company:

- **Software can attack futility; climate comes from the owner.** Visible status, guaranteed answers and visible outcomes are things a system can enforce. Only the owner's own visible responses create the climate that makes people use the channel.
- **The system needs two side doors.** "Don't go over the boss's head" is a common unwritten rule, so managers need a way to log a remark on an employee's behalf. Issues *about* a colleague's or supervisor's competence were the most often withheld category in the Milliken study (37.5%), so those need a confidential route.

The evidence does not say how fast is fast enough. No study found measures how much a 1-day versus a 2-week response time changes future participation, so any deadline the MVP sets is a design choice, not a research result.

## Programs that work decide every item within days, close to the problem

The high-performing systems in the literature look nothing like a suggestion box. Robinson and Schroeder call the box the place "where ideas go to die" and warn that putting it online doesn't fix it ([Berrett-Koehler](https://bkconnection.com/books/title/the-idea-driven-organization)). In one practitioner account, a Toyota production worker submitted roughly **50 small suggestions a year, and about 98% were implemented**. The ideas concerned the worker's own job, the team leader agreed on the spot, and rewards were 500–2,000 yen ([Lean Enterprise Institute](https://www.lean.org/the-lean-post/articles/recruiting-creative-ideas/)). Toyota's own list of failure modes includes "failing to respond to every proposal" ([Art of Lean](https://artoflean.com/reference/suggestion-system/)).

The documented cases closest to Modus Trade's size share that structure:

- **Boardroom Inc.**, a publisher of about 100 people, averaged **104 ideas per employee per year with over 90% implemented**. Ideas were built into every team's weekly meeting ([Schroeder](https://dmschroeder.com/the-surprising-consequences-of-a-high-performance-idea-system/)).
- **Clarion Hotel Stockholm** got more than 50 ideas per employee. Staff could enter a raw problem when they had no solution, and each department reviewed every idea and problem in a weekly meeting ([Idea-Driven Organization sample chapter](https://ekkozvbwnx8.exactdn.com/wp-content/uploads/2022/04/IdeaDrivenOrganization_sampleChapter.pdf)).

High implementation rates come from scope and rhythm, not from generous reviewers: small ideas, decided by the nearest manager, in a meeting that already exists.

Russian industrial groups digitized the same logic at scale and published unusually specific deadlines:

- **Severstal** moved from paper boxes to a common platform in 2014. Unit technical councils meet twice a month and assign a responsible expert to every idea. Over seven years, **414,000 ideas were submitted and 248,000 implemented** ([CFO Russia](https://www.cfo-russia.ru/stati/?article=50203)). Severstal also shows what quotas do: after it dropped volume targets in 2018, the number of ideas fell but the economic effect doubled.
- **EVRAZ** replaced Excel tables that had "become hard to manage at scale" with a platform. It added a chatbot and mobile app for workers without a PC, and a «Доска решения проблем» (problem board) that tracks owners, deadlines and overdue problems ([Neftegaz.RU](https://magazine.neftegaz.ru/articles/tsifrovizatsiya/733371-fabrika-idey-v-evraze-kak-predlozheniya-sotrudnikov-pomogayut-kompanii-zarabatyvat/)).
- **Химремонт** (ТАУ НефтеХим) publishes its regulation, which shows what "fast" means in practice. The author gets an SMS on registration. Preliminary comments are due within **2 working days**, the decision protocol within **5 working days**, and the executor gets the task within 2 more ([up-pro.ru](https://up-pro.ru/library/production_management/organization_files/upravlenie-uluchsheniyami/)).
- **Rosatom's ГХК** reviews within 5 days and must explain every rejection to the author ([up-pro.ru](https://up-pro.ru/library/production_management/systems/poshagovaya-instruktsiya-dlya-sotrudnikov/)).
- **PGK**, a freight company of about 3,000 people, ran more than 6,000 initiatives through a ticket system. Each stage has its own deadline, the system **shows which department caused a delay**, and meeting deadlines is a team KPI ([Habr](https://habr.com/ru/post/722254)).

Gazprom Neft is the cautionary tale. Its portal signed up 96% of employees (13,609 people) and collected 4,781 ideas, but implemented only **290 (about 6%)**. It invited resource-heavy proposals without matching decision capacity ([IT HR Awards](https://ithrawards.ru/gazprom-neft-portal-iniciativ)). By contrast, TVEL implemented about 87% of its 40,000+ small improvement proposals in 2025 ([TVEL](https://www.tvel.ru/activity/rosatom-production-system/)).

In Kazakhstan, structured programs exist mainly in heavy industry and quasi-state companies:

- **ERG**'s «Фабрика идей» received **32,084 proposals in 2021** and paid 565M KZT for the best ones. It also returns 10% of the effect of large initiatives to the originating enterprise, to be spent on working conditions ([Inbusiness.kz](https://inbusiness.kz/ru/news/svyshe-32-tysyach-proektov-po-uluchsheniyu-rabochih-processov-predlozhili-sotrudniki-eurasian-recourses-group-v-2021-godu)).
- **KazMunayGas** ran a «Банк идей» platform at its refineries in **Pavlodar**, Atyrau and Shymkent from 2015 to 2022, with about 6,000 registered users and 190 ideas implemented ([KMG](https://www.kmg.kz/ru/company/projects/all/vnedrenie-sistemnoy-platformy-bank-idey/)). The Pavlodar jury may recognize it.
- **KazTransOil** reports that one idea, from the chief power engineer of its Pavlodar pipeline division, saves about **38.45M KZT a year** ([Bizmedia.kz](https://bizmedia.kz/2024-07-17-kaztransojl-sekonomili-okolo-40-mln-tenge-na-elektronagrevatelyah/)).

No program with published metrics was found for any Kazakh private SME or distributor, or for a security integrator of 50–300 people anywhere. The case for Modus Trade therefore rests on analogy with small foreign firms and local industrial programs.

Taken together, these programs prevent silent loss with five mechanics:

1. Every submission is registered with a named owner.
2. Each step has a deadline of a few working days, and the author is notified at intake and at decision.
3. A recurring meeting clears the queue.
4. Overdue items are visible to the boss, with the delay attributed to a person or department.
5. Every outcome, rejections included, goes back to the author with reasons.

One mechanic is conspicuously absent: **none of the published corporate regulations defines automatic escalation when a deadline is missed**. PGK's delay attribution comes closest. A vendor has documented what happens without these mechanics. One hospital's submitted ideas carried about $20M of estimated value; about $1M was approved and about $70K implemented, after which submissions dried up ([KaiNexus](https://www.kainexus.com/mark-graban-and-greg-jacobson-on-why-most-idea-programs-stall-and-how-to-close-the-gap-between-ideas-submitted-and-improvements-actually-implemented)).

## Kazakhstan's appeal law already specifies a process that cannot lose a request

Government appeal systems solve the same problem for millions of requests. Kazakhstan's version is effectively a state machine with timers, set out in the Administrative Procedural Code (АППК):

| Article | Rule |
|---|---|
| Ст. 64 | An appeal "подлежит обязательному приему, регистрации, учету и рассмотрению", and refusing to accept one is prohibited. The applicant gets a ticket with a **unique number, timestamp and the registering official's name** ([АППК ст. 64](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm)). |
| Ст. 64(7)–(8) | An identical appeal with no new arguments is returned. If it is filed again, it is attached to the existing case without a new answer. |
| Ст. 65 | A misrouted appeal must be forwarded within **3 working days**, and the applicant is notified ([prg.kz](https://prg.kz/m/amp/document/35132264/5/660000)). |
| Ст. 76 | The answer is due in **15 working days**. The head can extend this once, by a reasoned decision, for up to two months. Unjustified extensions carry disciplinary liability ([АППК ст. 76](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/76.htm)). |
| Ст. 89 | Answers must be "обоснованными и мотивированными", address the applicant's arguments with concrete facts, and explain the right to complain ([АППК ст. 89](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/89.htm)). |
| Ст. 91(2) | If the body misses the deadline, **its silence counts as a refusal**, which the applicant can appeal ([АППК ст. 91](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/91.htm)). |
| Ст. 91(4) | A complaint goes first to the original body, which has 3 working days to satisfy it before passing it to the higher body. |
| Ст. 99 | The higher body must review the complaint within 20 working days, with no extension ([АППК ст. 99](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/99.htm)). |

eOtinish turns this into software ([Bizmedia](https://bizmedia.kz/2026-10-24-kak-podat-obrashhenie-cherez-eotinish-i-chto-delat-esli-otvet-ne-ustroit/)). The applicant sees four statuses: «Зарегистрировано» → «Назначен исполнитель» → «В работе» → «Исполнено». The answer arrives in «Мои обращения». From there the applicant can press «Подать жалобу на ответ», or file a complaint about inaction that cites the original number. A sent appeal cannot be edited, only supplemented by a new appeal that links to it, and anonymous filing is impossible. The platform handled **more than 5 million appeals in 2025** and 16.2 million since its 2021 launch. It connects more than 26,000 organizations and 380,000 staff who handle appeals, and applicants can rate the quality of answers ([gov.kz](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru)).

eOtinish's AI is a useful lesson for any team tempted to lead with AI ([BES.media](https://bes.media/news/ii-obrabotal-2-8-mln-zhalob-kazahstantsev-cherez-eotinish-no-nikto-ne-znaet-skolko-raz-on-oshibsya/)):

- It has produced summaries, topic tags and draft replies for **2.8 million appeals**, but it cannot send anything; an official reviews and sends every reply.
- The router that suggests the responsible agency is still in pilot.
- Staff have left only about 7,000 usefulness ratings, so nobody knows the error rate.

Russia's systems add two refinements:

- **Госуслуги «Решаем вместе» (ПОС)** sets each deadline from a three-level category classifier. A category flagged fast-track gets **≤10 calendar days**, while a formal appeal under 59-ФЗ gets 30. When a coordinator re-classifies or redirects an item, **the deadline is recalculated** from the new category ([ПОС: deadline logic](https://pos.gosuslugi.ru/docs/main/docs/Логика_расчета_сроков_обработки_обращений.pdf)). A dedicated «Координатор» workstation triages, splits and redirects appeals ([ПОС: processing](https://pos.gosuslugi.ru/docs/main/docs/Обработка%20обращений.pdf)). The underlying law allows 30 days plus one extension of up to 30 more, with notice to the citizen ([59-ФЗ ст. 12](https://www.zakonrf.info/doc-15934004/st12/)).
- **Moscow's «Наш город»** moderates within 24 hours, answers within **8 working days**, and lets the resident **confirm or reject that the problem was actually fixed** ([Cyclowiki](https://cyclowiki.org/wiki/%D0%9D%D0%B0%D1%88_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4_%28%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB%29)).

Open311 is the request standard behind many US and UK city 311 services and behind FixMyStreet. It contributes a minimal data model: each service (category) carries its own extra fields, and each request carries a responsible agency, status notes and an expected date ([Open311 GeoReport v2](https://wiki.open311.org/GeoReport_v2/)). Its status field has only two values, open and closed, which proved too coarse. The field's main failure is closing tickets without fixing anything: a New York City Council analysis found that about **46% (134,000) of 2018 transport-department complaints were closed with ambiguous resolution descriptions** ([NYC Council](https://council.nyc.gov/data/311-agency/)). FixMyStreet's countermeasures are a separate "closed, not fixed" state and a questionnaire sent to the reporter four weeks later ([FixMyStreet manual](https://fixmystreet.org/running/admin_manual/)).

Most of these mechanics transfer almost one-for-one to a company:

- mandatory registration with a number;
- a dispatcher for misrouted items;
- per-category deadlines, recalculated on reassignment;
- one reasoned extension, with notice to the author;
- escalation triggered by silence;
- reasoned answers;
- confirmation by the author;
- linking duplicates to an existing case.

What does not transfer is the timing and the formality. Fifteen working days is a legal maximum for state bodies and far too slow for an internal channel. Internal practice (Химремонт, ГХК, «Наш город») points to 2 working days for a first human response and 5–10 for a decision. eOtinish bans anonymity, which works for citizens who sign with an e-signature (ЭЦП) but not for employees who fear their manager. A public map becomes an internal feed. E-signatures and court appeals have no internal equivalent beyond "escalate to the director".

## Every ready-made tool covers only part of the brief

The ready-made options fall into five families, and each fails Modus Trade for a different reason: price and scale, language and integration, data localization, or scope.

| Option | Examples and prices (seen 11 Nov 2026) | Worth copying | Fit for Modus Trade |
|---|---|---|---|
| Enterprise innovation suites | IdeaScale, Brightidea, Qmarkets, HYPE (which now owns Viima and Planbox). All quote-only; one third-party figure puts HYPE from about US$16,000/yr ([GetApp](https://www.getapp.co.uk/software/91239/hype-innovation)) | Campaigns, voting, staged review, anonymity set per idea | No. Built for corporate innovation programs. No Bitrix24 or 1C connector, no Kazakh UI, hosted outside Kazakhstan |
| Self-serve idea SaaS | Ideanote US$899/month per 100 seats, Russian UI ([Ideanote](https://ideanote.io/pricing)). Viima Basic €89/month for 10 users plus €7 per extra user, no Russian ([Viima](https://www.viima.com/pricing)) | Ideanote's phases, statuses that explain outcomes, routing by department, author notifications | UX reference only. Foreign hosting, no SLA escalation, no Bitrix24 |
| Frontline continuous-improvement apps | Rever, KaiNexus; quote-only | An owner and due date on every item, photo capture by phone, impact tracking ([Rever](https://reverscore.com/)) | No. Industrial, English-first |
| Adjacent tools | Culture Amp (surveys), Jira Service Management (free up to 3 agents), Canny (Pro from US$79/month, [Canny](https://canny.io/pricing)) | JSM's SLA timers; Canny notifies everyone who voted when the status changes | No. Surveys can't track a case, JSM feels like an IT helpdesk, Canny is built for external customers |
| Bitrix24 smart process | Профессиональный, 76,000 ₸/month list price for 100 users, or Энтерпрайз ([bitrix24.kz](https://www.bitrix24.kz/prices/)) | Stages, robots, access rights by role and stage; data stays in Kazakhstan | Partial. Needs an upgrade if the company is on a plan below Профессиональный; letting authors see only their own items is tricky; no owner overview |
| Bitrix24 Marketplace apps | Aventra «Идеи от сотрудников», Brusnika «Управление идеями», BARIO «Банк идей», ХайХаб «Есть идея», MCART box module (261,450 ₽, [1С-Битрикс](https://marketplace.1c-bitrix.ru/solutions/mcart.idea/)) | Aventra's anonymity with a tracking code and its reminders; Brusnika's idea → task link | Strongest "buy" option, but these are idea banks. No routing of problems, no escalation, no owner dashboard |
| 1C | No current module. An old АИС for rationalization proposals on 1С:Предприятие ([up-pro.ru](https://up-pro.ru/library/production_management/kaizen/povysheniye-effektivnosti-raboty-prosto/)) | — | No. 1С:УТ is trade accounting |
| Russian «фабрика идей» platforms | ТЕКОРА «4И», Atwinta, Brainforce; unpriced, custom or on-premise | Atwinta's problem board; Brainforce's duplicate hints and personal answer to every idea | No. Built for holdings with tens of thousands of staff |
| Open source | Fider, Frappe Helpdesk, Zammad, osTicket, GLPI, Decidim, CONSUL | Fider's merging of duplicates; Helpdesk's SLAs; Decidim's progress tracking for accepted ideas | Each covers half the brief |

### Global SaaS

The category leaders are enterprise innovation suites sold by quote, and the market has consolidated: HYPE bought Viima in 2021 and merged with Planbox in 2024 ([Pulse 2.0](https://pulse2.com/why-hype-innovation-is-buying-planbox/)). The only published prices within reach of a mid-size firm are Ideanote (about US$10,800 a year for 100 seats) and Viima Basic, which is capped at two boards. Russian UI is confirmed only for IdeaScale and Ideanote, and Kazakh for none ([Ideanote languages](https://ideanote.io/faq/what-language-is-ideanote-available-in)). **No vendor reviewed lists a Bitrix24 or 1C integration**; their connectors centre on Microsoft Teams, Jira, SAP and Salesforce. Ideanote documents the clearest loop for the author: statuses can explain why an idea was archived ([Ideanote](https://ideanote.io/feature/custom-statuses)), and ideas are routed by department or category ([Ideanote](https://ideanote.io/feature/automatic-progression)). Rever puts an owner and a due date on every item. But no idea-management vendor advertises ticket-style SLA timers with escalation.

The harder blocker is legal. Article 12(2) of Kazakhstan's Personal Data Law requires personal data, employee data included, to be stored in databases located in Kazakhstan. Consent to cross-border transfer does not cure a localization breach. Fines under CoAO Art. 79 Part 3 reach **KZT 1.95M for a medium business and KZT 2.6M for a large one** ([UPPERSETUP](https://uppersetup.com/en/blog/personal-data-and-localisation-in-kazakhstan-in-2026-law-no)). No global vendor reviewed offers a Kazakhstan region. Two caveats apply: this rests on a consultancy summary, and practitioners note ambiguity about the law's reach ([Chambers](https://chambers.com/articles/problem-issues-of-personal-data-localization-in-kazakhstan)). Have a lawyer check it before it goes on a slide. Even so, it is a strong argument for keeping employee data either on bitrix24.kz, whose .kz portals are hosted in a Kazakh datacenter ([status.bitrix24.kz](https://status.bitrix24.kz/)), or on servers in Kazakhstan. Payments to foreign cloud suppliers can also be reclassified as royalties for tax purposes ([Chambers](https://chambers.com/articles/taxation-practice-of-cloud-services)).

### Russian and CIS products, and 1C

Russia's standalone platforms are ТЕКОРА «4И» (the platform behind EVRAZ's «Фабрика идей 2.0», [ТЕКОРА](https://www.tekora.ru/proekty/fabrika-idey-2-0/)), Atwinta «Цифровая фабрика идей» ([Atwinta](https://digital-factory.atwinta.ru/)) and Brainforce ([CNews](https://www.cnews.ru/articles/2026-02-02_kak_tsifrovizatsiya_idej_sotrudnikov)). They are custom or on-premise, publish no prices, and are built for holdings with tens of thousands of workers, economic-effect calculators and bonus accounting. They are design references, not purchases. Atwinta keeps a separate «доска проблем» (problem board) beside its idea registry. Brainforce shows similar ideas while the author types and answers every idea, rejections included, with a personal notification.

HR suites cover fragments. WebTutor has had a «Банк идей» app for its LMS customers (information from 2020, [WebSoft](https://blog.websoft.ru/2020/04/webtutor.html)). Happy Job collects suggestions inside engagement surveys but cannot track an individual case ([Happy Job](https://happy-job.ru/)).

1C has nothing current. Its only live link to this area is Brainforce pulling employee data from 1С:ЗУП. 1С:УТ is a trade, warehouse and sales system with no employee-workflow layer. For this product it is at most a source of context, such as a 1C order or supplier number attached to a purchasing problem. No Kazakhstan-made idea or feedback product for SMEs was found.

### Open source

Open-source tools split cleanly into problem tools and idea tools:

- **Fider** (AGPL, Go, Russian UI, released 3 Nov 2026) can stand up an ideas board in hours. It has statuses such as planned, started, completed and declined, and can mark a post as a duplicate of another ([Fider](https://github.com/getfider/fider); [Fider API](https://docs.fider.io/api/posts)). It has no assignee, no SLA and no private clarification thread.
- **Frappe Helpdesk** (AGPL, Russian locale) has customizable SLAs and auto-assignment by issue type, but no idea voting ([Frappe Helpdesk](https://github.com/frappe/helpdesk)). Setting up a Frappe bench with MariaDB and Redis would eat much of a hackathon day.
- **Zammad, osTicket and GLPI** are helpdesks built around the agent's view.
- **Decidim and CONSUL** are heavy Rails platforms built for city-level participation. Their ideas are worth more than their code, for example Decidim's accountability component with a 0–100% implementation progress bar ([Decidim](https://docs.decidim.org/en/develop/admin/components/accountability)).

For a two-day build, a thin custom app with a status workflow, a deadline check and a dashboard carries less risk than adapting any of them.

## Bitrix24 can host the form, but not yet the promise

The strongest objection the jury can raise is "why not just configure Bitrix24?" It deserves an honest answer, because Bitrix24 does a lot.

A smart process gives stages, custom fields, robots, triggers, and access rights set per role and per stage. Integrators routinely build internal request desks this way. IPG built a «банк идей» on smart processes for VEKA Rus's 250-user portal, and it has been live for more than a year ([IPG](https://ipg.digital/portfolio/avtomatizatsiya/kak-my-avtomatizirovali-dokumentooborot-komandirovki-i-bank-idey-na-baze-korporativnogo-portala-bitr/)). Smart processes require the **Профессиональный** plan (76,000 ₸/month list price for 100 users, excluding VAT) or Энтерпрайз ([netit24](https://netit24.com/smart-processy-v-bitrix24/)).

Installing an app from the Marketplace is faster still. Aventra's «Идеи от сотрудников» (5/5 from 20 reviews, 568 installs) already provides ([Aventra](https://www.bitrix24.ru/apps/app/aventra.idei_ot_sotrudnikov/)):

- the stages Новая → На рассмотрении → Принята → В работе → Реализована / Отклонена, with a reason for rejection;
- a dialog between author and reviewer, and a notification to the author on each decision;
- genuinely anonymous submission with a tracking code;
- a reminder to reviewers after **3 working days**, plus a Monday digest.

Brusnika's «Управление идеями» (980 installs) turns approved ideas into Bitrix24 tasks whose status flows back to the idea ([Brusnika](https://www.bitrix24.ru/apps/app/novus.ideamanagement/)). Data on a .kz portal stays in Kazakhstan. Whatever the team builds, the pitch must acknowledge that the owner could pilot Aventra within days.

What configuration does not deliver is exactly what the owner described:

1. **Problems, not just ideas.** Every Marketplace app is an idea bank. None routes an operational problem, such as a purchasing blocker or a fault in an accounting process, to the responsible department with a deadline specific to its type.
2. **Escalation, not just reminders.** Aventra nudges the reviewer, but nothing moves an overdue item up to the department head and then to the owner. No app shows the owner which departments are holding what.
3. **Authors seeing only their own items.** In smart processes this is a rights puzzle: "без права чтения сотрудник не увидит даже созданный им элемент" ([netit24](https://netit24.com/smart-processy-v-bitrix24/)). Whether the "own items" scope covers the creator has not been tested.
4. **Intake from meetings and calls.** Nothing captures a remark made at a meeting or on a call and credits it to the person who raised it.
5. **The owner's one screen.** No app puts the four §2.7 metrics on one screen. Bitrix24's BI constructor can approximate it on the Профессиональный plan.

Aventra also lacks attachments and tasks. Costs and friction add up as well:

- Moving from Стандартный to Профессиональный adds 38,000 ₸/month at list price.
- Cloud apps require the "BitrixGPT + Маркетплейс" subscription. Its tenge price was not found; in Russia it is 6,000 ₽/month for Профессиональный ([Bitrix24](https://www.bitrix24.ru/apps/subscribe_base.php)).
- Cloud portals reportedly allow at most two business processes running at once on one element ([Bitrix24 helpdesk](https://helpdesk.bitrix24.ru/open/5671433/)).
- Integrators warn that large Bitrix24 projects can overrun budget and timeline by a factor of two ([Workspace](https://workspace.ru/blog/top-10-riskov-i-problem-pri-vnedrenii-i-dorabotke-bitriks24/)).

That defines the positioning. Against "just configure Bitrix24": the MVP does not compete with Bitrix24. It is the rule set Bitrix24 lacks out of the box:

- one intake for problems and ideas;
- deadlines per category;
- escalation on silence;
- reasoned closure that the author confirms;
- the owner's one-screen view.

Bitrix24 stays where people work and where accepted work gets done, so the roadmap integrates with it rather than replacing it:

- single sign-on and the department directory from Bitrix24;
- notifications in Bitrix24 chat;
- an accepted idea becomes a Bitrix24 task (the Brusnika pattern);
- eventually, the module runs as a Bitrix24 app, with data on Kazakh servers.

Against "buy a tool": global suites fail on price, language, integration and localization, Russian platforms on scale, and open-source tools on scope.

A one-line answer for the jury: «Aventra — хороший ящик для идей. Но владелец жалуется не на нехватку идей, а на то, что проблемы теряются. У нас у каждого обращения есть ответственный, срок и мотивированный ответ, а просрочка сама поднимается к руководителю и владельцу».

Two caveats keep the pitch honest. First, if the owner wanted only an idea box with reminders, Aventra would be cheaper than any custom build, which also has to be maintained. The case for building rests on problems, escalation and the owner's dashboard. Second, the cost comparison depends on facts the team does not have: Modus Trade's headcount, whether its Bitrix24 is cloud or self-hosted and on which plan, and whether it already pays for the Marketplace subscription. Put these in the §5 assumptions list and ask about them in the participants' chat.

## Borrow the state machine, skip the gamification

The plan in `docs/internal/analysis.md` already matches most of the evidence. The research suggests three shifts in emphasis: move escalation to Must, add a registration receipt and two deadline timers per category, and add author confirmation of the fix. It also suggests a few cheap additions.

| Pattern to borrow | Source | In current plan | Recommendation |
|---|---|---|---|
| Receipt on submit: number, owner, answer-by date | АППК ст. 64 ticket; Химремонт SMS on registration | Implicit | **Must.** One line on the confirmation screen and in «Мои обращения» |
| Two timers per category (first response, decision): problems on a fast track; recalculated on reassignment | ПОС classifier; Open311 service definitions | "Time limits" (Must) | **Must.** Two fields in the category table |
| Escalation on silence: overdue → head → owner, showing who is holding the item | АППК ст. 91(2); PGK delay attribution; EVRAZ problem board | Should | **Promote to Must.** No product reviewed does this |
| One extension with a required reason and notice to the author | АППК ст. 76; 59-ФЗ ст. 12 | Absent | Should. Stops deadlines being moved quietly |
| Reasoned outcome on every close or rejection, plus a "what we'll do instead" field | АППК ст. 89; Piezunka & Dahlander; KaiNexus's ranking of responses | Must | Keep. The new field turns a "no" into partial action |
| Author confirms the fix or reopens the item after «Реализовано»; auto-close after N days | «Наш город»; FixMyStreet; NYC 311 | Absent | Should. Two buttons |
| Dispatcher who handles the fallback queue | ПОС «Координатор» | Must (fallback) | Keep. Name the role in the concept |
| Similar items, "me too", merge as «Дубликат → №…» | Fider; АППК ст. 64; Brainforce | Should | Keep. Feeds the recurring-themes chart |
| «Сделано по вашим предложениям» feed with author credit | Leach 2006; Decidim accountability | Should | Keep. Cheapest proof that speaking up has an effect |
| Register on someone's behalf with the source channel; raw problems allowed without a solution | Clarion; Huang 2005 | Should | Keep. Fits the "don't go over the boss's head" norm |
| Confidential mode now; anonymous tracking code later | Aventra; NAVEX | Open decision | Confidential in the MVP |
| Category-specific fields, e.g. 1C document number or site | Open311 service attributes | Absent | Later. Gives a concrete 1C answer for §6 |
| AI suggests, a human confirms, overrides are logged | eOtinish | Later | Keep optional |

The default timers below are taken from practice, not tested as optimal:

- **First human response within 2 working days** for every item. Source: Химремонт's preliminary review.
- **Decision within 5 working days** for problems. Sources: Химремонт, ГХК.
- **Decision within 10 working days** for ideas. This matches ПОС's fast-track ceiling, «Наш город»'s 8 working days, and one cycle of a twice-monthly department review.

Store them as category fields an admin can change. Pause them while waiting for the author, and recompute them when an item is reassigned. For a two-day build, the cheapest robust approach is to work out "overdue" and the escalation level whenever a page loads, from the due date, the status and any paused time, instead of running a scheduler. Seed a few items at each escalation level, so the demo shows red items landing on the head's and the owner's screens without waiting.

Keep the four §2.7 metrics on the main dashboard as the spec requires. Add the share of overdue items per department and the reopen rate, which catches tickets closed without a fix, NYC-style. In the roadmap, add the share of authors who submit a second time, the outcome Piezunka and Dahlander measured.

Several things should stay out:

- **Big-company machinery.** Points shops, leaderboards of submission counts, effect calculators, expert committees and campaign tooling are built for groups of 15,000–70,000 employees.
- **Volume quotas.** Severstal dropped its volume targets, and its economic effect doubled.
- **Cash per idea.** Leach found monetary rewards unrelated to suggestion or implementation rates. Recognition tied to implementation (credit in the "сделано" feed, a thank-you from the owner) is what the evidence supports.

On anonymity, keep the plan's "confidential" default and add an Aventra-style anonymous tracking code later. NAVEX reports that the median share of anonymous whistleblowing reports globally is 54% ([NAVEX](https://www.navex.com/en-us/company/press-room/regional-whistleblowing-benchmark-report-highlights-rise-in-anonymous-reports/)). Anonymous reporters are hard to follow up with, though, so updates must be pushed to them rather than waiting for them to check.

If AI is added, follow eOtinish: suggest the category, owner and a draft answer, require a human to confirm, and log every override from day one so accuracy can be measured.

The roadmap also needs a launch plan alongside the software. In a high power-distance culture, a formal channel only works where people see a participative climate:

- **The owner answers the first batch personally.**
- **Each department reviews its queue in a meeting it already holds**, weekly or fortnightly. This is the Boardroom and Clarion pattern. MCART, which sells an idea-bank module, warns that if reviews happen less than once or twice a month, "сотрудники могут потерять веру" ([MCART](https://www.mcart.ru/blogs/bank-idey/)).
- **The first «сделано по вашим предложениям» digest goes out within two weeks.**

The best-sourced numbers for slides:

- **85%** of employees had withheld an issue at least once (peer-reviewed, small sample).
- Silence does more damage than a reasoned "no" (peer-reviewed, 1.3 million contributors).
- The median scheme gets **0.13 ideas per employee and implements 2%**, and frequent publicity of outcomes quadruples the suggestion rate (peer-reviewed, 182 organizations).
- **84% vs 43%**: HR leaders who think they act on feedback vs employees who see change (vendor data).
- **5 million** eOtinish appeals a year run on exactly these rules.
- **6%**: Gazprom Neft's implementation rate, despite signing up nearly every employee.

## Conclusion

The research changes what the product is. The owner does not need more input: the seed requests themselves describe staff not knowing who is responsible for something, what stage it is at, or when it will be done. What he needs is a service-level guarantee. The closest working blueprint is not a SaaS product but Kazakhstan's own appeal law, which turns a missed deadline into an escalation and requires every answer to give reasons. No competitor on the Bitrix24 Marketplace or in the global market offers that. The jury already knows the process from eOtinish; the team's job is to cut it from weeks to days and enforce it in software that sits beside Bitrix24, with data in Kazakhstan. The success metric for a pilot follows from this. It is not ideas per employee but the share of items answered within the deadline and the share of authors who come back with a second one.

The evidence also sets a limit that the pitch should state openly. Software can remove the sense that speaking up is pointless, but it cannot create a participative climate by itself. In an owner-led company with high power distance, the owner's first month of visible responses will decide whether people use the channel at all. Positioning the MVP as the guarantee Bitrix24 lacks, with a roadmap that deepens Bitrix24 integration and a launch plan that puts the owner's answers first, is more credible than claiming to replace either Bitrix24 or the idea-box apps already on its Marketplace.
