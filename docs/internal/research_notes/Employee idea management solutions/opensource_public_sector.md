# Open-source feedback/idea platforms and public-sector appeal systems as analogs for an internal employee feedback module (ГК «Модус Трейд»)

Research date: 2026-11-11. All GitHub figures (stars, licence as detected by GitHub, latest release, last push, presence of Russian locale files) were pulled live from the GitHub REST API on 2026-11-11. Legal texts were read from article-level mirrors of the official codes; edition dates are noted for each.

---

## 1. Open-source options: licence, stack, activity, Russian support, relevant features, effort to adapt

### Takeaway
No single open-source product covers the whole brief: idea voting, routing problems to an owner, clarifying Q&A, an SLA clock and management analytics. **Fider** is the best fit for the ideas side. It is small, actively released, has a Russian UI, a status set and duplicate merging, but it has no assignee or SLA. **Frappe Helpdesk**, **Zammad**, **osTicket** and **GLPI** fit the problems side (assignment, SLAs, requester portal) but have no idea voting. **Decidim** and **CONSUL Democracy** are civic-scale Ruby platforms, too heavy to adapt in 2 days. They are still worth copying for their answer and accountability workflows.

### Cited Findings

**Comparison table (GitHub API, 2026-11-11)**

| Tool | Licence (GitHub) | Main stack | Stars | Latest release / activity | Russian locale in repo | Source |
|---|---|---|---|---|---|---|
| Fider | AGPL-3.0 | Go (+ React/TS frontend) | 4,621 | v0.39.0, 2026-11-03 | yes (`locale/ru/client.json`, `server.json`) | [GitHub](https://github.com/getfider/fider) |
| Decidim | AGPL-3.0 | Ruby on Rails | 1,850 | v0.32.2, 2026-10-27 | yes (`decidim-core/config/locales/ru.yml`) | [GitHub](https://github.com/decidim/decidim) |
| CONSUL Democracy | AGPL-3.0 | Ruby on Rails, PostgreSQL | 1,560 | 2.6.1, 2026-10-08 | yes (`config/locales/ru`) | [GitHub](https://github.com/consuldemocracy/consuldemocracy) |
| FixMyStreet (mySociety) | GitHub: NOASSERTION (custom mySociety licensing file) | Perl | 625 | last tagged release v6.0, 2024-11-15 (**older than 18 months**); master pushed 2026-11-10 | yes (`locale/ru.UTF-8`) | [GitHub](https://github.com/mysociety/fixmystreet) |
| Ushahidi Platform | GitHub: NOASSERTION | PHP API; new "Mzima" TS client | 734 (API), 17 (client) | API v2025.04.0, 2025-02-14; client v2026.41.0, 2026-10-08 | not checked | [GitHub API](https://github.com/ushahidi/platform), [client](https://github.com/ushahidi/platform-client-mzima) |
| Frappe Helpdesk | AGPL-3.0 | Frappe (Python) + Vue (frappe-ui) | 3,493 | v16.1.0, 2026-11-04 | yes (`helpdesk/locale/ru.po`) | [GitHub](https://github.com/frappe/helpdesk) |
| ERPNext | GPL-3.0 | Python (Frappe) | 41,174 | v16.54.0, 2026-11-06 | not checked | [GitHub](https://github.com/frappe/erpnext) |
| OpenProject | GPL-3.0 | Ruby on Rails | 17,249 | v17.9.7, 2026-11-09 | yes (`config/locales/crowdin/ru.yml`) | [GitHub](https://github.com/opf/openproject) |
| Redmine | GitHub: NOASSERTION (mirror repo) | Ruby on Rails | 6,078 | latest tag 7.0.3; 7.0-stable commit 2026-11-10 | yes (`config/locales/ru.yml`) | [GitHub mirror](https://github.com/redmine/redmine) |
| GLPI | GPL-3.0 | PHP | 6,579 | 12.0.1, 2026-10-28 | yes (`locales/ru_RU.po`) | [GitHub](https://github.com/glpi-project/glpi) |
| Zammad | AGPL-3.0 | Ruby on Rails | 6,101 | tags 7.2.3 (stable), 7.4.0-alpha | yes (`i18n/zammad.ru.po`) | [GitHub](https://github.com/zammad/zammad) |
| osTicket | GPL-2.0 | PHP 8.2–8.4, MySQL | 4,005 | v1.18.4, 2026-06-17 | not in repo (separate language packs; not verified) | [GitHub](https://github.com/osTicket/osTicket) |
| Taiga (backend) | MPL-2.0 | Python/Django | 858 | pushed 2026-11-03; no GitHub releases | yes (`taiga/locale/ru`) | [GitHub](https://github.com/taigaio/taiga-back) |
| OCA/project (Odoo community) | AGPL-3.0 | Python (Odoo) | 429 | pushed 2026-11-11 | n/a | [GitHub](https://github.com/OCA/project) |

**Fider (ideas/feedback portal)**
- Describes itself as "a feedback portal for feature requests and suggestions". Self-hosting is free; a managed cloud is also offered — [Fider README](https://github.com/getfider/fider).
- The post status API accepts `open`, `planned`, `started`, `completed`, `declined`, `duplicate`. Setting `duplicate` requires `originalNumber`, the post it is merged into. Status changes can carry a text note, e.g. a reason for declining — [Fider API docs: posts](https://docs.fider.io/api/posts).
- Ships 20+ UI locales including `ru` (client and server strings) — [GitHub locale dir](https://github.com/getfider/fider/tree/main/locale).

**Decidim (participatory democracy framework)**
- By default, proposal answers use the states *Not answered / Evaluating / Accepted / Rejected*. Admins can edit and add custom statuses, and statuses show on lists, cards and proposal pages. Answer templates exist — [Decidim docs: proposal answers](https://docs.decidim.org/en/admin/components/proposals/answers).
- The **Accountability** component lets participants "know the status of a project's implementation and follow its evolution". Results can be linked to proposals and have a status, dates and a 0–100% progress bar — [Decidim docs: accountability](https://docs.decidim.org/en/develop/admin/components/accountability).

**CONSUL Democracy**
- Originally built for Madrid City (decide.madrid.es). Development started 15 July 2015 and production launched 7 Sep 2015. Code is AGPLv3 — [README](https://github.com/consuldemocracy/consuldemocracy).
- Prerequisites: Ruby 3.4.11, Node.js 22.23.3, PostgreSQL ≥13, ImageMagick. The README warns the full test suite takes "more than an hour" — [README](https://github.com/consuldemocracy/consuldemocracy).

**FixMyStreet (mySociety)**
- By default the platform sends a questionnaire four weeks after a report. A report can be marked fixed by the reporter (in an update or in that questionnaire) or by council staff. Staff/admins can also *close* a report without declaring it fixed — [FixMyStreet Administrator's Manual](https://fixmystreet.org/running/admin_manual/).
- Supports Open311 for sending reports to council back-office systems — [FixMyStreet Open311 page](https://www.fixmystreet.com/open311).
- A 2022 SocietyWorks article (the commercial arm working with councils) advises not marking reports "fixed" until they actually are. Citizens read "closed" as "fixed" and then reopen or duplicate the report — [SocietyWorks, 2022 (older source)](https://www.societyworks.org/2022/07/20/how-to-increase-transparency-with-fixmystreets-report-statuses/).

**Frappe Helpdesk**
- Key features: agent and customer portals, customizable SLAs, assignment rules ("custom auto-assignment of tickets based on priority, issue type, or workload"), knowledge base, saved replies, and analytics on response times — [Helpdesk README](https://github.com/frappe/helpdesk).
- Built on Frappe Framework (Python/JS) with a Vue UI; self-host via an install script or Frappe Cloud — [Helpdesk README](https://github.com/frappe/helpdesk).

**Zammad / osTicket**
- Zammad is a web-based open-source helpdesk for email, chat, telephone and social media. It is licensed AGPLv3, and the code is owned by the independent Zammad Foundation — [Zammad README](https://github.com/zammad/zammad).
- osTicket: users create tickets via website, email or phone; incoming tickets are saved and assigned to agents. Requirements are PHP 8.2–8.4 and MySQL ≥5.5 — [osTicket README](https://github.com/osTicket/osTicket).

**Odoo modules for ideas / suggestion box** (from Odoo Apps listings; licences and prices not verified)
- *Continuous Improvement Process (`cip`)* is a digital suggestion box with a configurable workflow, where employees can track the outcome of their ideas. Listings stop at Odoo 16.0 — [apps.odoo.com 16.0/cip](https://apps.odoo.com/apps/modules/16.0/cip).
- *Employee Idea Management (`sh_emp_idea`, Softhealer)* lists versions up to 17/18. Ideas are submitted under categories, and approvers accept, decline or cancel them with comments and ratings — [apps 17.0/sh_emp_idea](https://apps.openerp.com/apps/modules/17.0/sh_emp_idea).
- *Employee Idea (`dev_employee_idea`, DevIntelle)* has a draft → post → approve → rating → close workflow with department-manager approval — [apps 16.0/dev_employee_idea](https://apps.odoo.com/apps/modules/16.0/dev_employee_idea).
- *Employee Ideas (`hr_employee_ideas`, Probuse)* is paid. HR defines idea types and approves or rejects — [apps 10.0/hr_employee_ideas](https://apps.odoo.com/apps/modules/10.0/hr_employee_ideas).

### Inferences
- **Effort to adapt for a 2-day MVP (rough ranking):**
  - **Fider** is the lowest effort to *deploy*: one Go binary or Docker image plus Postgres, already in Russian, with voting, statuses and merge built in. Adding an "assignee + deadline + private clarification thread" would mean Go/React changes, which is non-trivial in 2 days.
  - **Frappe Helpdesk** is medium effort. It needs a Frappe bench with MariaDB and Redis. SLAs and assignment rules are configuration, not code. Idea voting and a public feed would need custom DocTypes.
  - **Zammad / GLPI / osTicket** are medium effort. They are strong at ticket routing and SLAs, but their UIs are agent-centric, with no voting or "ideas" concept.
  - **Decidim / CONSUL** are high effort: a large Rails monolith built for municipal participation (processes, assemblies, budgets, verification). Borrow their *concepts* (answer states, accountability progress bar), not the code.
  - **OpenProject / Redmine / Taiga** are generic trackers. They are workable as a back office through custom trackers and workflows, but poor as an employee-facing "submit an idea" UX.
- **AGPL note (Fider, Decidim, CONSUL, Zammad, Frappe Helpdesk):** running a modified AGPL app for employees over a network obliges offering those users the modified source. For an internal tool this is a low practical burden, but the customer should be told. GPL-licensed apps used only internally have no distribution trigger.
- The Odoo modules are irrelevant to Модус Трейд unless they adopt Odoo, since they use Bitrix24 + 1С. They do confirm the typical "employee idea" workflow: category → manager approval → rating → close.

### Gaps
- I found no widely adopted, actively maintained open-source *employee suggestion box* project beyond Fider-class feedback boards and the Odoo apps. Searches did not surface one with meaningful GitHub adoption. This is a negative result from a limited search, not proof of absence.
- Fider merge behaviour (whether votes and comments transfer to the original post) is not documented in the page I read.
- Not verified: the licence texts for Redmine (commonly GPL-2.0), Ushahidi and FixMyStreet (GitHub reports NOASSERTION); Odoo module licences and prices; osTicket Russian language-pack availability; Taiga feature specifics (voting, issue statuses).

---

## 2. Kazakhstan public sector: eOtinish, АППК deadlines, escalation, duplicates, statistics, «Слышащее государство», open-government portals

### Takeaway
Kazakhstan's appeal regime is a ready-made spec for "nothing gets silently lost":
- intake cannot be refused, and every appeal gets a unique number (АППК ст. 64);
- misrouted appeals are forwarded within 3 working days (ст. 65);
- answers are due in 15 working days, with one reasoned extension of up to 2 months and notice within 3 working days (ст. 76);
- answers must be reasoned, address the applicant's arguments and explain how to complain (ст. 89);
- if the deadline passes in silence, this is treated as a refusal and can be appealed (ст. 91);
- complaints are reviewed in 20 working days with no extension (ст. 99);
- identical repeat appeals without new arguments are returned and then simply attached to the old case (ст. 64).

eOtinish puts this into practice with 4 visible statuses, a "complain about the answer" button and, since 2025, AI summaries, tags and draft replies on 2.8 million appeals.

### Cited Findings

**Legal deadlines and rules: Административный процедурно-процессуальный кодекс РК (АППК), № 350-VI of 29.06.2020, as amended (incl. Law № 241-VIII of 17.12.2025)**
- **Ст. 64(1):** "Обращение … подлежит обязательному приему, регистрации, учету и рассмотрению. Отказ в приеме обращения запрещается." — [АППК ст. 64 (checked 31.10.2026)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm)
- **Ст. 64(2)–(3):** the applicant receives a ticket (талон) with a unique number, date/time and the name and position of the registering official. The appeal is registered the same day, or on the next working day if it arrives after hours — [АППК ст. 64](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm)
- **Ст. 64(7)–(8), duplicates and repeat appeals:** an appeal is returned with reasons within 3 working days if its substance is identical to an earlier appeal whose procedure was terminated, it was handled by the same body/official, and it contains no new arguments or newly discovered facts. Appeals with obscene or insulting language are also returned. If such an identical appeal is filed again after return, "приобщается к материалам ранее рассмотренного административного дела без предоставления ответа на него". Exception (64(7-2)): reports of crimes or security threats must be forwarded immediately — [АППК ст. 64](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm)
- **Ст. 64(9):** the applicant may withdraw the appeal before a decision, and withdrawal does not bar re-filing — [АППК ст. 64](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm)
- **Ст. 65, redirection:** an appeal sent to a body without competence is forwarded to the competent body "в срок не позднее трех рабочих дней со дня его поступления", and the applicant is notified — [АППК via prg.kz, edition as of 25.08.2026](https://prg.kz/m/amp/document/35132264/5/660000)
- **Ст. 70(5):** a repeat appeal on an already-decided matter is allowed only "если имеются новые доводы или вновь открывшиеся обстоятельства" — [prg.kz, edition 25.08.2026](https://prg.kz/m/amp/document/35132264/5/660000)
- **Ст. 76, core deadline (new edition by Law 241-VIII of 17.12.2025):**
  - (1) the procedure on an appeal lasts **15 working days from registration** unless laws provide otherwise;
  - (2) the clock starts the next day, or on receipt by the competent body after redirection;
  - (3) it can be extended by a **reasoned decision of the head, deputy or chief of staff, for a reasonable period of no more than two months**, to establish facts;
  - (4) an unjustified extension brings disciplinary liability for the decision-maker;
  - (5) a deadline falling on a non-working day moves to the next working day.
  
  — [АППК ст. 76 (checked 31.10.2026)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/76.htm). An earlier edition, also shown on prg.kz, requires the participant to be notified **within 3 working days** of the extension — [prg.kz](https://prg.kz/m/amp/document/35132264/5/660000).
- **Ст. 89, simplified procedure for сообщение / предложение / отклик / запрос:**
  - the possible outcomes are (1) an answer on the merits, (2) "принятие к сведению" (taken into account), or (3) termination;
  - answers must be "обоснованными и мотивированными … содержать конкретные факты, опровергающие или подтверждающие доводы заявителя, с разъяснением его права на подачу жалобы";
  - the applicant must be informed of the results and of the measures taken.
  
  — [АППК ст. 89](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/89.htm)
- **Ст. 91, escalation:**
  - (2) if the body does not act within the Code's deadlines, "с даты истечения сроков считается, что административный орган … отказали", i.e. silence counts as a refusal and can be appealed;
  - (3) complaints are reviewed by the **higher** body/official;
  - (4) the complaint is filed with the body being complained about, which must pass it to the higher body within 3 working days, *unless within those 3 working days it fully satisfies the complaint itself*;
  - (5) court action generally follows the pre-trial complaint.
  
  — [АППК ст. 91](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/91.htm)
- **Ст. 99:** "Срок рассмотрения жалобы составляет **двадцать рабочих дней** со дня регистрации жалобы … Продление срока рассмотрения жалобы не допускается", except where laws provide (edition of Law 241-VIII, 17.12.2025) — [АППК ст. 99](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/99.htm)
- **Ст. 90-2, e-petitions:**
  - a petition must gather **at least 50 citizens joining within 20 working days** before it is published;
  - it is not published if a petition on the same subject is already public and a decision on it is less than one year old;
  - the authorized body checks it within 20 working days and rejects it with reasons if it does not qualify.
  
  — [АППК ст. 90-2](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/90-2.htm)

**eOtinish: how it works for the applicant** (Bizmedia guide, 24.10.2026)
- Appeal types and the deadlines the guide uses: заявление, сообщение and запрос take 15 working days; жалоба takes 20 working days; for предложение and отклик the guide states no deadline. Counting starts the next day, and after-hours or weekend filings register on the next working day — [Bizmedia, 2026-10-24](https://bizmedia.kz/2026-10-24-kak-podat-obrashhenie-cherez-eotinish-i-chto-delat-esli-otvet-ne-ustroit/)
- **Visible statuses:** «Зарегистрировано» → «Назначен исполнитель» → «В работе» → «Исполнено». The answer arrives in «Мои обращения» — [Bizmedia](https://bizmedia.kz/2026-10-24-kak-podat-obrashhenie-cherez-eotinish-i-chto-delat-esli-otvet-ne-ustroit/)
- **Escalation UX:** from a completed appeal the applicant can press «Подать жалобу на ответ». If the deadline passed without a decision, they can file a complaint about inaction citing the first appeal's number. «Подать иск в суд» is also offered — [Bizmedia](https://bizmedia.kz/2026-10-24-kak-podat-obrashhenie-cherez-eotinish-i-chto-delat-esli-otvet-ne-ustroit/)
- **Other rules:**
  - a sent appeal cannot be edited; additions go in a new appeal referencing the first one's number;
  - withdrawal («Отозвать обращение») is possible until «Исполнено»;
  - anonymous filing is not possible; login is via ЭЦП or eGov Mobile;
  - attachments are capped at 80 MB, and audio/video is not accepted.
  
  — [Bizmedia](https://bizmedia.kz/2026-10-24-kak-podat-obrashhenie-cherez-eotinish-i-chto-delat-esli-otvet-ne-ustroit/)

**eOtinish: scale, features and «Слышащее государство»** (Ministry of AI and Digital Development, 30.04.2026)
- Launched **1 July 2021**, merging separate appeal channels. The ministry calls e-Otinish "ключевым инструментом концепции «Слышащего государства»" — [gov.kz / МЦРИАП, 2026-04-30](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru). *Conflict:* an egov.kz news item summarized in search results gives 1 July **2022** — [egov.kz](https://egov.kz/cms/ru/news/eOtinish_platform); I could not open that page to check.
- **2025:** more than 5 million appeals (over 4 million from citizens, about 1 million from businesses). Since launch: 16.2 million appeals. Complaints are about 5–7% of appeals. Average annual user growth is 42.6% — [gov.kz, 2026-04-30](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru)
- **Participants:** more than 26,000 connected organisations, more than 380,000 employees handling appeals, and 3.2 million applicants. *Conflict:* other search-result snippets cite "50 тысяч организаций" as connected; I could not tie that number to a specific page — [gov.kz](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru)
- **Features:** online status tracking, interaction history and **rating the quality of responses** by the applicant — [gov.kz](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru)
- **Channels:** eOtinish.kz, eGov.kz, eGov Mobile (2022), ЦОН and «Нәтиже» centres, Qazpost (2022), Citizen Reception Centres (2023). E-petitions added in 2024; pilot AI and a Unified Knowledge Base in 2025 — [gov.kz](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru)
- **AI in eOtinish (as of 16.10.2026):**
  - three functions are in use: a **summary** of the appeal, **topic detection and tags**, and a **draft reply**. They have been applied to **2.8 million appeals**;
  - AI cannot send replies; an official reviews, edits and sends them;
  - an "intelligent router" that suggests the responsible agency is in **pilot**, planned to become citizen-facing to cut redirections;
  - there are **no published accuracy or error statistics**. Staff gave only about 7,000 "useful / not useful" ratings across 2.8 million appeals (~0.25%);
  - it runs on the closed infrastructure of АО «НИТ», and appeals are not sent to third-party AI.
  
  — [BES.media, 2026-10-16](https://bes.media/news/ii-obrabotal-2-8-mln-zhalob-kazahstantsev-cherez-eotinish-no-nikto-ne-znaet-skolko-raz-on-oshibsya/)

**Open-government portals and participatory budgeting**
- «Открытое правительство» components: open data, **open NPA** (draft regulations published for public comment before adoption), **open dialogue** (blog platform of agency heads, internet conferences, polls), **open budgets** (budget.egov.kz; any citizen can comment on draft budget programmes) and evaluation of agency performance. Open data and open NPA launched in 2014, open budgets and open dialogue in 2015 — [egov.kz: e-government projects](https://egov.kz/cms/ru/information/about/projects); [egov.kz: open budgets](https://egov.kz/cms/ru/articles/communications/open-budgets)
- **«Бюджет народного участия» (БНУ), 2025:**
  - city akimats cite Order of the Minister of Finance No. 208 of 29.04.2025 (budget planning rules). Projects are limited to local improvements (greening, sidewalks, playgrounds etc.) funded from the local budget;
  - **Astana, Сарыарка district:** 73 proposals were received 20 Jan – 1 Mar 2025, and an expert council admitted 43 to online voting, which ran until 24 April — [Astana akimat](https://www.gov.kz/memleket/entities/astana/press/news/details/1137653?lang=ru); [Kazpravda](https://kazpravda.kz/n/byudzhet-narodnogo-uchastiya-onlayn-golosovanie-za-luchshie-proekty-prohodit-v-astane);
  - **Almaty:** 4,632 applications were filed 1–30 Sep 2025, with voting 27 Oct – 9 Nov 2025 on budget.open-almaty.kz and a cap of 324.3 mln tenge per initiative — [Kapital.kz](https://kapital.kz/gosudarstvo/141803/byudzhet-narodnogo-uchastiya-v-almaty-startuet-golosovanie-po-proektam.html).
  
  The figures come from search summaries of these pages and should be spot-checked.

### Inferences
- The legal chain gives a ready-made **state machine with deadlines**:
  - registration (same day, unique number);
  - routing check (≤3 working days to forward);
  - answer (15 working days);
  - one reasoned extension (with notice);
  - reasoned answer that explains the right to complain;
  - complaint, first to the original handler, who has 3 working days to fix it themselves;
  - higher authority (20 working days, no extension).
  
  An internal system can copy the *shape* with shorter, company-appropriate timers.
- "Silence = refusal" (ст. 91(2)) maps directly to **auto-escalation on SLA breach**: the author shouldn't have to chase.
- The ст. 64 duplicate rule (same question, same handler, no new arguments → link to the existing case, no new answer) is a clean, defensible **dedup policy** for recurring problems.
- The ст. 90-2 petition mechanics (50 co-signers in 20 working days; no re-opening of a topic decided less than a year ago) translate to "an idea needs N co-signers to reach management review" and "a declined idea can't be re-submitted for X months without new arguments".
- eOtinish's AI experience shows "AI drafts, human sends" is the accepted pattern. It also shows that **measuring AI quality** (feedback rate, accuracy) is the weak point, so an MVP using LLM categorisation should log overrides from day 1.

### Gaps
- I could not confirm the exact current article for the "no deadline for предложение/отклик" claim. Secondary guides apply 15 working days to сообщения, предложения and запросы, citing АППК ст. 76/87; I did not open ст. 87.
- Origin and official text of the «Слышащее государство» concept (commonly attributed to President Tokayev's 2019 address) were not verified in this session.
- Not found: public eOtinish dashboards (on-time %, satisfaction scores), the user-rating scale, and whether repeat appeals are auto-detected by the system.
- "Открытый диалог" (dialog.egov.kz) current activity level in 2025–2026 was not verified.

---

## 3. Russian public sector: ПОС «Госуслуги. Решаем вместе», ЦУР, «Наш город», «Активный гражданин», 59-ФЗ

### Takeaway
Russia separates **formal appeals** under 59-ФЗ (30 days, +30 extension) from **fast-track "messages"** on ПОС (≤10 calendar days for categories flagged as fast-track). Its SLA is driven by a **three-level classifier** (категория → подкатегория → факт), and every re-classification or redirection **recalculates the deadline**. Moscow's «Наш город» shows a stricter operating model: moderation within 24 h, an answer within 8 working days, and residents confirming or rejecting the fix. Public evidence that ПОС itself uses ML auto-categorisation was not found. It does run an "автомодерация" stage.

### Cited Findings

**59-ФЗ "О порядке рассмотрения обращений граждан РФ" (02.05.2006; latest amendment listed 28.12.2024 № 547-ФЗ — [Consultant](https://www.consultant.ru/document/cons_doc_LAW_59999/))**
- **Ст. 8 ч. 2:** a written appeal must be registered **within 3 days** of receipt. **Ч. 3:** if it is outside the body's competence, it is forwarded **within 7 days of registration** to the competent body, with the citizen notified. **Ч. 4:** if several bodies are competent, copies go to each within 7 days. **Ч. 6:** a complaint may not be sent to the body or official whose decision is being complained about — [59-ФЗ ст. 8](https://www.zakonrf.info/doc-15934004/st8/)
- **Ст. 11 ч. 1:** if there is no name or return address, no answer is given, unless the appeal reports a crime. **Ч. 5:** if the same question has been answered on the merits **several times**, there are no new arguments, and the appeals went to the same body, the head may declare the new appeal unfounded and **stop the correspondence**, notifying the citizen. **Ч. 5.1:** if the answer to the question is already published on the body's website (under ст. 10 ч. 4), the citizen is sent **the link within 7 days** — [59-ФЗ ст. 11](https://www.zakonrf.info/doc-15934004/st11/)
- **Ст. 12 ч. 1:** a written appeal is considered **within 30 days of registration** (20 days for migration-violation reports to regional governors, ч. 1.1). **Ч. 2:** in exceptional cases, or when information has been requested from other bodies, the deadline can be **extended by no more than 30 days, with the citizen notified** — [59-ФЗ ст. 12](https://www.zakonrf.info/doc-15934004/st12/)

**ПОС: deadline logic from the operator's own documents** (pos.gosuslugi.ru; undated PDFs, current on site)
- At submission the appeal gets a "59-ФЗ" flag:
  - if the citizen picked no category, it is a 59-ФЗ appeal by default;
  - if the category or subcategory has a **30-calendar-day** deadline in the organisation's settings, it gets the flag;
  - if the deadline is **≤10 calendar days**, it is **"фаст-трек"** and not a 59-ФЗ appeal.
  
  Once set, the flag is never removed — [ПОС: Логика расчета сроков](https://pos.gosuslugi.ru/docs/main/docs/Логика_расчета_сроков_обработки_обращений.pdf)
- **Automatic moderation** stage: the deadline is computed from the **"факт" (third level of the ПОС classifier)**, falling back to the subcategory — [ПОС: Логика расчета сроков](https://pos.gosuslugi.ru/docs/main/docs/Логика_расчета_сроков_обработки_обращений.pdf)
- **Redirection recalculates the deadline.** In a worked example, a coordinator re-classifies "Мусор/Контейнерные площадки" to "Благоустройство/Зеленые насаждения". The appeal moves to a city administration where this fact is fast-track and gains a 10-day deadline. It is passed to another municipality with a 30-day standard and loses fast-track. It is then returned to the regional government as "not our competence" and regains fast-track — [ПОС: Логика расчета сроков](https://pos.gosuslugi.ru/docs/main/docs/Логика_расчета_сроков_обработки_обращений.pdf)
- **Roles and workstations:**
  - АРМ «Координатор» (triage, re-classify, redirect);
  - АРМ «Исполнитель»;
  - АРМ «Оператор приема обращений»;
  - АРМ «Администратор», with the "Классификатор тем", where per-category deadlines are set.
  
  Other mechanics: appeals can be **split** into several (the 59-ФЗ flag is inherited); every appeal gets an automatic **unique 9-digit number**, also used by ССТУ.РФ; special deadlines can be set (migration 20 calendar days, appeals of court decisions 7 days); answers to 59-ФЗ appeals are signed with УКЭП; answer text must be typed into ПОС rather than attached as scans (Минцифры protocol № 679пр, 04.09.2023) — [ПОС: Обработка обращений](https://pos.gosuslugi.ru/docs/main/docs/Обработка%20обращений.pdf)
- **ПОС for business (launched April 2025):** up to **5 calendar days** for a simple question and up to **10 calendar days** where documents must be studied. In pilot regions single processing centres sit in economic ministries, development agencies or ЦУР — [Regberry](https://www.regberry.ru/news/na-gosuslugah-zapushchen-servis-obratnoy-svyazi-dlya-msp)
- **Scale:** Минцифры's 16-year Госуслуги summary says citizens used the feedback platform **26 million times**, most likely cumulative since launch — [Hi-Tech Mail, 2025](https://hi-tech.mail.ru/news/139301-na-gosuslugah-podveli-itogi-16-let-raboty-pochti-120-mln-polzovatelej/)
- **Citizen rating:** after an answer the app asks the citizen to rate how the problem was solved, and a low rating prompts a review by the agency. This comes from the app-store description, a weaker source — [App Store: Госуслуги Решаем вместе](https://apps.apple.com/ru/app/%D0%B3%D0%BE%D1%81%D1%83%D1%81%D0%BB%D1%83%D0%B3%D0%B8-%D1%80%D0%B5%D1%88%D0%B0%D0%B5%D0%BC-%D0%B2%D0%BC%D0%B5%D1%81%D1%82%D0%B5/id1516448015)

**ЦУР (Центры управления регионом) and «Инцидент Менеджмент»** (mostly 2018–2021 sources, **older; flag**)
- ЦУРы have operated in 83 regions since December 2020 as single points for monitoring and handling residents' complaints. «Инцидент Менеджмент» picks up social-media posts, routes them to the responsible agency and controls deadlines and answer quality — [Gazeta.ru, 2021](https://www.gazeta.ru/social/news/2021/12/03/n_16958593.shtml); [MSK1, 2021](https://msk1.ru/text/world/2021/05/19/69918221/)
- Search-result snippets attributed to АНО «Диалог Регионы» (2020–2021) report:
  - an average response time to online posts of **8 h 01 min** in Jan–May 2020;
  - a **10-calendar-day** maximum resolution time for problems not needing major spending, down from 28 days a year earlier;
  - answer quality graded "вплоть до наличия приветствия".
  
  I did not open the original article, so treat the attribution as unverified — [FedPress](https://fedpress.ru/interview/2791520); [360.ru](https://360.ru/news/vlast/podmoskove-stalo-primerom-raboty-s-zhiteljami-pri-pomoschi-tsur/)
- «Инцидент Менеджмент» was reported in 2018 as developed by ООО «Медиалогия» and in test in 10 regions — [Anti-Malware.ru, 2018 (old)](https://www.anti-malware.ru/news/2018-07-23-1447/26910). Academic papers from 2024 discuss using ML and NLP to classify incident-management messages, e.g. at Moscow's КГХ. These are proposals and research, not documented production ML in ЦУР — [Lomonosov-2024](https://lomonosov.msu.ru/archive/Lomonosov_2024/data/32743/171340_uid713428_report.pdf); [MLSD-2024](https://mlsd2024.ipu.ru/proceedings/0892.pdf)
- AI in Russian government correspondence: the Government Staff (Аппарат Правительства) began using AI for text recognition, spell-checking, quick briefs and **drafting replies** to incoming documents (Nov 2025) — [Нацпроекты.рф](https://xn--90aivcdt6dxbc.xn--p1ai/articles/news/iskusstvennyy-intellekt-nachali-vnedryat-v-rabotu-s-dokumentami-v-apparate-pravitelstva/)

**Moscow «Наш город» and «Активный гражданин»**
- «Наш город»:
  - **moderation within 24 hours**, and the standard deadline for an answer is **8 working days**;
  - the resident can **confirm or reject that the problem was fixed**;
  - users earn points, and the portal ranks the most active users;
  - a regulation governs processing and publication.
  
  — [Cyclowiki: Наш город](https://cyclowiki.org/wiki/%D0%9D%D0%B0%D1%88_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4_(%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB)); the official app also promises an answer "в течение 8 рабочих дней" — [App Store: Наш город](https://apps.apple.com/ru/app/%D0%BD%D0%B0%D1%88-%D0%B3%D0%BE%D1%80%D0%BE%D0%B4/id6444522487). Moscow cut electronic-complaint deadlines from 30 to 8 working days in 2012 — [ComNews, 2012 (old)](https://www.comnews.ru/content/67794/2012-09-07/elektronnye-zhaloby-moskvichey-rassmotryat-bystree)
- «Активный гражданин» (city referendum and voting app, since 2014):
  - 7.2 million participants over 11 years (about every second Muscovite), per the mayor — [Vedomosti](https://www.vedomosti.ru/gorod/ourcity/articles/kazhdii-vtoroi);
  - more than 6,600 votes held by its 10th anniversary, and typically 30–40 citizen-backed decisions a month;
  - over 2,000 yards, streets and parks redesigned since 2014.
  
  The last two figures are from search summaries of mos.ru pages — [mos.ru](https://www.mos.ru/news/item/138876073/)

### Inferences
- The **ПОС classifier-driven SLA** (deadline set per leaf category, recomputed when the category or owner changes) is the single most transferable design. It lets one system run both "fast-track" operational problems and slower "formal" requests.
- The **coordinator role** (triage, re-classify, split, redirect) is how both ПОС and ЦУР avoid misrouted items piling up. An internal MVP needs at least one "dispatcher" role, even if auto-routing exists.
- «Наш город»'s "author confirms or rejects the fix" step is the cheapest effective guard against fake closures.
- 59-ФЗ ст. 11 ч. 5.1 (point repeat askers to a published answer) is in effect a FAQ / knowledge-base dedup mechanism. eOtinish's 2025 "Unified Knowledge Base" is the KZ analogue.

### Gaps
- No public, current (2024–2026) regulation for ЦУР / Инцидент Менеджмент reaction deadlines was found; figures above are from 2020–2021.
- No confirmed public documentation that ПОС uses ML for auto-categorisation. Only "автоматическая модерация" is documented, and its internals are not described.
- No national data found for ПОС share of "solved" appeals or average satisfaction ratings.
- «Наш город» rules for re-opening (how many times, and what timer applies after rejection) were not found.

---

## 4. International: UK/US 311, FixMyStreet, Open311 standard

### Takeaway
**Open311 GeoReport v2** is a minimal, proven data model for "service requests": typed request categories with per-category dynamic attributes, a request with `status` (open/closed only), `status_notes`, `agency_responsible`, `expected_datetime`, timestamps and media. Real 311 systems add richer statuses and a **post-resolution satisfaction survey**. Their main known failure is closing tickets without real resolution, with vague resolution text.

### Cited Findings
- **Request fields (Open311 GeoReport v2):**
  - `service_request_id` (or a `token` for async systems);
  - `status`, which is **only `open` or `closed`**;
  - `status_notes`, an optional explanation of the current status;
  - `service_code` / `service_name`;
  - `description` (up to 4,000 chars);
  - `agency_responsible`;
  - `service_notice`, the expected action;
  - `requested_datetime`, `updated_datetime` (which equals the close date for closed requests) and an optional `expected_datetime`;
  - location (`lat`/`long` or `address`) and `media_url`.
  
  — [Open311 GeoReport v2 spec](https://wiki.open311.org/GeoReport_v2/)
- **Service list and definitions (Open311 GeoReport v2):**
  - each service has `service_code`, `service_name`, `description`, `metadata`, `type` (`realtime` / `batch` / `blackbox`), `keywords` and `group` (category grouping);
  - each service definition has attributes with `code`, `datatype` (`string`, `number`, `datetime`, `text`, `singlevaluelist`, `multivaluelist`), `required`, `order`, `description` and `values` (key/name pairs).
  
  — [Open311 GeoReport v2 spec](https://wiki.open311.org/GeoReport_v2/)
- The Open311 bulk-data spec notes that GeoReport v2 allows only open/closed, while back-office systems typically use richer states such as "Open, Processing, Hold, Closed". It also adds a `closed_date` field that is not in v2 — [Open311 GeoReport bulk spec](https://wiki.open311.org/GeoReport/bulk)
- **NYC 311 open data:**
  - statuses include **Assigned, Canceled, Closed, Pending**, and a *resolution description* records the agency's last action and next steps;
  - requesters who leave contact details are offered the **311 Resolution Satisfaction Survey**, published as its own dataset;
  - a City Council analysis found that about **46% (134,000) of DOT-handled complaints in 2018** had ambiguous resolution descriptions;
  - a 2024 Council hearing raised agencies closing complaints without proper resolution.
  
  — [NYC Council data team: 311](https://council.nyc.gov/data/311-agency/); [CityMeetings.nyc, 2024 hearing](https://citymeetings.nyc/city-council/2024-03-01-0100-pm-committee-on-governmental-operations-state-federal-legislation/chapter/what-is-being-done-to-improve-311-service-responses-and-resolve-complaints). NYC also publishes a "311 Service Level Agreements" dataset (expected days per complaint type) — [data.amerigeoss.org mirror](https://data.amerigeoss.org/en/dataset/311-service-level-agreements)
- **FixMyStreet:** a 4-week reporter questionnaire; "fixed" can be set by the reporter or by staff, and "closed" (not fixed) is a separate state — [FixMyStreet Admin Manual](https://fixmystreet.org/running/admin_manual/). Reports are pushed to council systems via Open311 — [FixMyStreet Open311](https://www.fixmystreet.com/open311). Public council report pages show reporters reopening items marked fixed when the problem persisted — e.g. [Oxfordshire report](https://fixmystreet.oxfordshire.gov.uk/report/2333018) (individual cases, not documentation).

### Inferences
- Open311's split between **Service (category definition with dynamic attributes and an SLA)** and **Request (instance)** is exactly what is needed to make category forms configurable without code. Examples: "Склад/логистика → which warehouse?", "IT/1С → which document number?".
- Open311's two-value status is too coarse internally. Use the eOtinish / Fider / NYC union instead: new → assigned → in progress → waiting for author → resolved → closed, plus declined, duplicate and reopened.
- The NYC experience argues for two controls: (a) a **mandatory resolution note** at closure, and (b) closure that is only "provisional" until the author confirms or a timeout passes.

### Gaps
- UK 311-style systems beyond FixMyStreet (e.g., council CRM SLAs) were not researched in depth. No 2024–2026 FixMyStreet usage statistics were collected.

---

## 5. Which mechanisms transfer to an internal company system, and which don't

### Takeaway
Most of the process mechanics transfer well: mandatory registration with an ID, category-driven routing and deadlines, a dispatcher role, extension-with-reason, auto-escalation on silence, reasoned answers, author confirmation, reopen and rating, and dedup and linking. The legal formalities don't: e-signatures, identity verification, court appeal, very long deadlines, and fully public disclosure.

### Cited Findings (mechanism → source it comes from)
- **Mandatory intake + unique number + no refusal** → [АППК ст. 64](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm); automatic 9-digit number in [ПОС](https://pos.gosuslugi.ru/docs/main/docs/Обработка%20обращений.pdf).
- **Misrouting fix within a short window (3 WD KZ / 7 days RU)** → [АППК ст. 65](https://prg.kz/m/amp/document/35132264/5/660000); [59-ФЗ ст. 8](https://www.zakonrf.info/doc-15934004/st8/).
- **Per-category SLA, recalculated on re-classification or redirect; fast-track vs standard** → [ПОС deadline logic](https://pos.gosuslugi.ru/docs/main/docs/Логика_расчета_сроков_обработки_обращений.pdf).
- **Single reasoned extension with notice; accountability for unjustified extension** → [АППК ст. 76](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/76.htm); [59-ФЗ ст. 12](https://www.zakonrf.info/doc-15934004/st12/).
- **Silence after deadline = escalation trigger** → [АППК ст. 91(2)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/91.htm).
- **Complaint goes first to the original handler with a short self-fix window (3 WD), then to the superior** → [АППК ст. 91(4)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/91.htm); "Подать жалобу на ответ" button in [eOtinish](https://bizmedia.kz/2026-10-24-kak-podat-obrashhenie-cherez-eotinish-i-chto-delat-esli-otvet-ne-ustroit/).
- **Reasoned answer that addresses the author's arguments and states the next step** → [АППК ст. 89(2)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/89.htm).
- **Idea outcomes "answer / taken into account / terminated"** → [АППК ст. 89(1)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/89.htm); Decidim's *Evaluating / Accepted / Rejected* → [Decidim docs](https://docs.decidim.org/en/admin/components/proposals/answers); Fider's *planned / started / completed / declined / duplicate* → [Fider API](https://docs.fider.io/api/posts).
- **Duplicate handling: link to the earlier case, no new answer; repeat only with new arguments** → [АППК ст. 64(7)–(8), 70(5)](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/64.htm); [59-ФЗ ст. 11 ч. 5](https://www.zakonrf.info/doc-15934004/st11/); Fider merge via `originalNumber` → [Fider API](https://docs.fider.io/api/posts).
- **Point to a published answer / knowledge base** → [59-ФЗ ст. 11 ч. 5.1](https://www.zakonrf.info/doc-15934004/st11/); eOtinish Unified Knowledge Base → [gov.kz](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru).
- **Author confirms or rejects the fix; reopen; rating of the answer** → [«Наш город»](https://cyclowiki.org/wiki/%D0%9D%D0%B0%D1%88_%D0%B3%D0%BE%D1%80%D0%BE%D0%B4_(%D0%9F%D0%BE%D1%80%D1%82%D0%B0%D0%BB)); [FixMyStreet 4-week questionnaire](https://fixmystreet.org/running/admin_manual/); [eOtinish rating](https://www.gov.kz/memleket/entities/maidd/press/news/details/1212365?lang=ru); [NYC 311 satisfaction survey](https://council.nyc.gov/data/311-agency/).
- **Co-signing threshold for ideas; cooldown on re-submitting decided topics** → [АППК ст. 90-2](https://kodeksy-kz.com/ka/administrativnyj_protsedurno-protsessualnyj_kodeks/90-2.htm).
- **Public "implementation progress" for accepted ideas** → [Decidim Accountability](https://docs.decidim.org/en/develop/admin/components/accountability).
- **AI: summary, tags and draft reply, with a human sending; router as a suggestion only** → [eOtinish via BES.media](https://bes.media/news/ii-obrabotal-2-8-mln-zhalob-kazahstantsev-cherez-eotinish-no-nikto-ne-znaet-skolko-raz-on-oshibsya/).

### Inferences: what does **not** transfer (or needs changing)
- **Deadline lengths.** 15 WD / 30 days / 20 WD are statutory maximums for state bodies. Internally, a "first response" SLA in hours or 1–2 working days plus a "resolution / decision" SLA per category (e.g., 3–10 WD) is more credible. «Наш город» (8 WD) and ПОС fast-track (≤10 calendar days) are closer benchmarks.
- **Anonymity.** eOtinish forbids anonymous filing, and 59-ФЗ ст. 11 ч. 1 gives no answer to anonymous appeals. In a company, fear of retaliation makes **optional anonymity** (or "confidential: visible only to the dispatcher") valuable. The trade-off is that clarifying questions must go through a pseudonymous thread.
- **Fully public disclosure** (open maps, public feeds) should become an **internal feed** with per-item visibility. HR or personal complaints stay private, while process problems and ideas can be company-visible.
- **Legal formalities.** ЭЦП/УКЭП signing, court appeal, mandatory state-language answers and the "ст. 91 ч. 5 court after pre-trial" chain have no internal analogue beyond "escalate to director".
- **Geolocation** (Open311/FixMyStreet) becomes **organisational location**: branch/office/warehouse/project or customer site. That fits a security-systems integrator with field installations.
- **Gamification** (points and ratings of active users in «Наш город» / «Активный гражданин») is optional and risky internally: it can incentivise noise. Recognition for *implemented* ideas is safer.

### Gaps
- No published evaluation was found showing which of these mechanisms most improved citizen satisfaction or on-time rates. The choice above is design judgement, not evidence-based ranking.

---

## What to borrow for our MVP

Concrete, buildable in ~2 days:

1. **Data model (Open311-inspired)**
   - `Category` (≈Open311 *service*): name, group, *default owner / role*, *SLA for first response*, *SLA for resolution*, a fast-track flag, and an optional JSON list of extra fields (Open311 *attributes*).
   - `Item` (≈*service request*): id/number, type (problem | idea), category, title, description, location (office/warehouse/object), attachments, author (or anonymous token), assignee, status, `status_note`, `expected_at` (deadline), `created_at`, `updated_at`, `closed_at`, `duplicate_of`, `rating`, `reopen_count`.
   - `Event` timeline: every status change, comment, clarifying question/answer, extension, reassignment and escalation.
2. **Statuses visible to the author** (eOtinish-style wording in Russian): «Зарегистрировано» → «Назначен ответственный» → «В работе» / «Нужны уточнения» (waiting for author) → «Решено (ожидает подтверждения)» → «Закрыто». Side states: «Отклонено (с обоснованием)», «Дубликат → №…», «Переоткрыто». For ideas, add Fider/Decidim-style outcomes: «На рассмотрении», «Принято в план», «Внедряется (% прогресса)», «Внедрено», «Принято к сведению».
3. **"Nothing gets lost" rules**
   - Every submission gets a number immediately.
   - A dispatcher role (ПОС «Координатор») can re-classify, split, merge or redirect. Redirect **recalculates the deadline** from the new category's SLA, as in ПОС.
   - SLA timers on first response and on resolution.
   - **Auto-escalation to the assignee's manager on breach** ("silence = escalation", after АППК ст. 91(2)).
   - **One extension with a mandatory reason**, notifying the author (АППК ст. 76 / 59-ФЗ ст. 12).
4. **Closure quality**
   - A mandatory resolution note that addresses the author's point (АППК ст. 89(2)).
   - The author **confirms or rejects** the result (Наш город / FixMyStreet). Rejection reopens the item to the same assignee with a short self-fix window, then escalates (АППК ст. 91(4) pattern).
   - Auto-close after N days without author response.
   - A 1–5 rating of the answer.
5. **Duplicates and recurring problems**
   - At submission, show similar open items (title similarity or LLM) so the author can "join" an existing one. Joining adds a +1 / co-signer, which feeds frequency analytics.
   - Merged items keep a `duplicate_of` link and the author follows the original (Fider merge; АППК ст. 64 "attach to the existing case").
   - Optional: an idea needs N co-signers to reach management review, and a declined topic has a cooldown (АППК ст. 90-2 analogue).
6. **Management view**
   - Counts by category/location/period, top recurring problems (by merged-duplicate count and co-signers), SLA compliance %, overdue list, average rating, and reopen rate.
   - An internal "решено" feed for transparency (FixMyStreet / Decidim accountability).
7. **AI (optional, low-risk)**
   - The LLM *suggests* category, owner and summary, and *drafts* a reply. A human confirms and sends (the eOtinish pattern).
   - Log whether the suggestion was accepted or overridden, so accuracy can be measured. eOtinish's lack of this was criticised.

## Reuse an open-source tool vs. build: recommendation for a 2-day hackathon

- **Recommendation: build a thin custom app and borrow the patterns above. Don't fork a platform.**
  - The brief's differentiators are routing, clarifying Q&A, SLA and escalation, author confirmation, and recurring-problem analytics. No single OSS tool has all of them.
  - Adapting Rails/Frappe/Go codebases in 2 days carries more risk than writing a focused CRUD app with a state machine, a timer job and a dashboard.
  - A custom app also makes Bitrix24 integration (notifications or task creation via REST/webhooks) and a Russian/Kazakh UI straightforward.
- **If a ready tool must be shown:**
  - **Fider** (AGPL, one Docker container + Postgres, Russian UI) can stand up the *ideas* board, with voting, statuses and merge, within hours. It has no assignee, SLA or private clarification, so it would cover only half the brief.
  - **Frappe Helpdesk** (AGPL, Russian, SLAs, assignment rules, customer portal) is the most complete for the *problems* half. Expect to spend much of the first day on setup (Frappe bench / Docker, MariaDB, Redis) and on learning DocTypes.
- **Avoid for the hackathon:** Decidim and CONSUL (heavy civic platforms; borrow their answer and accountability concepts only), FixMyStreet (Perl, geo-centric, last tagged release Nov 2024), and Ushahidi (crisis-mapping focus).
- **Pitch framing:** "Process designed on the same principles as eOtinish / Госуслуги «Решаем вместе» / FixMyStreet, scaled to a company: mandatory registration, category-based SLA, escalation on silence, reasoned answers, author confirmation, dedup of recurring problems." This lends credibility, and the legal articles above can be cited on a slide.
