# Russian/CIS market: collecting employee problems, ideas and suggestions (focus: Bitrix24 and 1C)

Research date: 2026-11-11. All prices are "as seen on 2026-11-11" unless stated otherwise. Searches were mostly in Russian. ₸ = tenge, ₽ = rubles.

## 1. Bitrix24 built-in capabilities, plans and Kazakhstan prices, guides and integrator cases

### Takeaway
Bitrix24 can model the whole flow without new software: a smart process (смарт-процесс) with stages, custom fields, robots and triggers, plus a CRM form for submission. Smart processes are only on the cloud **Профессиональный** plan (76 000 ₸/month list, 100 users) and **Энтерпрайз**. They are not on Базовый or Стандартный. There is at least one documented integrator case of a "банк идей" built on smart processes (VEKA Rus, 250-user portal). We found no official Bitrix24 step-by-step guide.

### Cited Findings
**Plans and prices in Kazakhstan (bitrix24.kz, seen 2026-11-11):**
- Official bitrix24.kz prices are per company, not per user, and exclude VAT ("Цены указаны без НДС… Цены указаны за всю компанию, а не за отдельных пользователей"). Бесплатный: free, unlimited users, 25 GB. Базовый: 13 000 ₸/month, 5 users. Стандартный: 38 000 ₸/month, 50 users. Профессиональный: 76 000 ₸/month, 100 users. Энтерпрайз: from 190 000 ₸/month for 250 users. The page has a month/year toggle marked "-20%". The discounted figures are 10 400 / 30 400 / 60 800 / 152 000 ₸ per month, presumably for annual payment, though the page excerpt did not label this explicitly — [bitrix24.kz/prices](https://www.bitrix24.kz/prices/)
- Third-party Kazakh resellers report a **30%** annual discount, not 20%: [blog.biz24.kz](https://blog.biz24.kz/tarify-bitrix24-kazahstan/) (says it cites the official site as of June 2026) and [astrix.kz](https://astrix.kz/blog/bitrix24-license-kazakhstan). [itba.kz](https://itba.kz/bitrix24/licenses/) lists different numbers (12 900 / 31 900 / 63 900 / 127 900 ₸). These conflict with the official page; treat the official page as authoritative.
- The bitrix24.kz price page lists "BI Конструктор" among the Профессиональный tools, and "Автоматизация" and "Сквозная аналитика" among the Энтерпрайз tools. The full per-plan feature matrix could not be extracted (page truncated) — [bitrix24.kz/prices](https://www.bitrix24.kz/prices/)

**Smart processes: availability and mechanics:**
- Cloud plan availability: "Смарт-процессы в облачном Битрикс24 есть лишь на тарифах Профессиональный (до 150 штук)". Энтерпрайз allows up to 1 000. Free, Basic and Standard have none. Professional also includes 20 "цифровых рабочих мест" (digital workplaces). Article dated 16 Sep 2026 — [netit24.com](https://netit24.com/smart-processy-v-bitrix24/)
- This is corroborated by a 2026 comparison (Стандарт "нет", Профессиональный "да") — [profreforma.ru](https://profreforma.ru/blog/sravnenie-tarifov-bitrix24/). An older official comparison table shows "Число смарт-процессов 150 / 1 000" — [bitrix24.ru compare](https://www.bitrix24.ru/prices/compare_cloud_plans.php)
- Robots and triggers on a smart process work only when the smart process has its own stages and kanban ("Роботы и триггеры работают, если включены свои стадии и канбан"). Business processes can also start on item creation or change — [netit24.com](https://netit24.com/smart-processy-v-bitrix24/)
- Smart-process access rights are set per role (read, add, change, delete, export, import). They can be restricted per stage and by scope: own, department or all. "Без права чтения сотрудник не увидит даже созданный им элемент" (without read permission, an employee cannot see even the item they created). Field type and multiplicity cannot be changed after creation, and deleting a field deletes its data — [netit24.com](https://netit24.com/smart-processy-v-bitrix24/)
- Automation by plan, as reported by a 2026 third-party comparison:

  | Feature | Базовый | Стандарт | Профессиональный | Энтерпрайз |
  |---|---|---|---|---|
  | CRM robots | "простые" | "расширенные" | "неограниченно" | "неограниченно" |
  | Business processes | "—" | "до 500" | "неограниченно" | "неограниченно" |
  | Reports | "до 20" | "до 30" | "до 50 + конструктор" | "до 100 + конструктор" |

  Russian prices on the same page are 2 490 / 6 990 / 13 990 / from 33 990 ₽ per month. The page says it is not a public offer — [profreforma.ru](https://profreforma.ru/blog/sravnenie-tarifov-bitrix24/). netit24 instead says business processes are listed "from Professional" — [netit24.com](https://netit24.com/smart-processy-v-bitrix24/). **Conflict: verify on the live portal.**

**Other built-in pieces relevant to the use case:**
- The messenger supports open and anonymous polls in chats, collabs and channels ("Вы можете создавать как открытые, так и анонимные опросы") — [bitrix24.ru chat features](https://www.bitrix24.ru/features/company/chat/)
- The bitrix24.kz feature list includes "Лента" (Live Feed) and "Благодарности" (appreciation posts), but per-plan availability was not extracted — [bitrix24.kz/prices](https://www.bitrix24.kz/prices/)
- Integrators commonly use smart processes for internal employee requests ("внутренние заявки сотрудников, сервисные обращения, … HR-заявки"). Typical setup: stages such as «Запрос получен», «На согласовании», «Уточнение», «Одобрено», «Отклонено»; role-based rights; robots and triggers for notifications — [autobit24.ru](https://autobit24.ru/blog/smart-processy-bitrix24-nastrojka-instrukciya/), [dikobraz.tech](https://dikobraz.tech/bitrix24/smart-protsessy/), [fact.digital](https://fact.digital/blog/bitrix24/smart-protsessy-bitriks24-nastroyka-i-avtomatizatsiya-biznes-protsessov/)
- WeJET case (Лео Телеком): all requests are created via a **CRM form**, and the service desk is built as a request route visible to employees at all stages — [wejet.ru](https://wejet.ru/cases/vnedrenie-i-nastroyka-bitriks24-dlya-integratora-leo-telekom.html). Other examples: an internal ticket system on Bitrix24 — [citrus-soft.ru](https://citrus-soft.ru/blog/kak-nastroit-obrabotku-vnutrennikh-tiketov-v-bitriks24/); smart processes for finance requests and approvals — [stekspb.ru](https://stekspb.ru/projects/bitrix24/optimizatsiya-upravleniya-zaprosami-s-pomoshchyu-smart-protsessov-v-bitriks24/); Экомобайл internal requests with deadline and status reports (official partner case) — [bitrix24.ru partner case](https://www.bitrix24.ru/partners/case/28525584/)

**Integrator case: "Банк идей" on smart processes (IPG for VEKA Rus):**
- Ideas run through a smart process ("Смарт-процессы чем-то похожи на Сделки"), with IPG "чуть «допилив» штатный функционал". Stages include «Проверка идеи», «Согласование даты заседания», «Рассмотрение комитетом», then curator assignment, recommend/reject, significance score and author bonus decision. Rejected ideas move to an archive rather than being deleted.
- Submission form fields: title, problem solved, solution, expected effect (technical/economic/social), author and co-authors, department, process, improvement goals, attachments.
- Roles: idea-bank admin, a committee meeting every two months, experts and curators, implementers, author.
- At each stage "запускаются задачи и выстраивается цепочка действий"; participants are notified automatically; meeting protocols are sent out.
- Client: VEKA Rus, a 250-user portal, two plants. Live "больше года" (more than a year), with dozens of ideas reviewed and implemented. Support tender won in 2023, so the case is roughly 2024–2025. The source does not describe the exact robots or customizations.
- Source for all of the above: [ipg.digital case](https://ipg.digital/portfolio/avtomatizatsiya/kak-my-avtomatizirovali-dokumentooborot-komandirovki-i-bank-idey-na-baze-korporativnogo-portala-bitr/)
- An HRM system built on Bitrix24 by MBS Group advertises a "Банк идей" module (page found, not fetched) — [hrm.mbsgroup.ru](https://hrm.mbsgroup.ru/bank-idej/). An info-expert blog post titled "Система сбора и оценки предложений от сотрудников для Битрикс24" exists, but returned HTTP 502 when fetched — [info-expert.ru](https://www.info-expert.ru/blog/sistema-sbora-i-otsenki-predlozheniy-ot-sotrudnikov-dlya-bitrix24/)

### Inferences
- If Modus Trade is on Стандартный or lower, building on smart processes requires upgrading to Профессиональный. That costs +38 000 ₸/month at list price (76 000 vs 38 000), or about +30 400 ₸/month (about 365 000 ₸/year) at the -20% discounted rate, VAT excluded. Professional caps users at 100; above that they need Энтерпрайз from 190 000 ₸/month.
- The VEKA case shows the pattern works, but it relies on an admin manually moving cards and a slow committee cadence. That cadence is exactly the "silently forgotten" risk the owner fears, unless SLA robots and reminders are added.
- On the author-visibility requirement: "свои элементы" scoping plus the warning that authors can't even see their own item without read rights means letting the **author** see status but not other people's issues takes careful rights design. Likely workarounds: the author as observer, a robot notification on each stage change, or the item assigned in a way that "own" covers the author. This is the single most important thing to prototype.

### Gaps
- An exact per-plan matrix from the official bitrix24.kz page for robots, triggers, BPs, CRM forms, BI-конструктор, polls and благодарности. The page was truncated and the official compare page lost its checkmark values.
- Whether "Свои" permission in smart processes covers the creator or observers, or only the responsible person. No authoritative helpdesk page found; must be tested.
- Modus Trade's current Bitrix24 plan and headcount are unknown, but both decide the cost.
- No official Bitrix24 helpdesk or how-to specifically for "банк идей" or "ящик предложений" on smart processes was found.

## 2. Bitrix24 Marketplace (Битрикс24.Маркет) apps for ideas, suggestions and feedback

### Takeaway
At least five dedicated apps exist. The closest fit to "author sees status and dialogs with the reviewer" is **«Идеи от сотрудников» (Aventra)**, a suggestion box with statuses, two-way comments, real anonymity and reminders. **«Управление идеями» (Brusnika Solutions)** is the most complete idea-to-task workflow. Cloud apps require the paid "BitrixGPT + Маркетплейс" subscription. Its tenge price for Kazakhstan was not found.

### Cited Findings
- **«Идеи от сотрудников» — Aventra.** Subtitle: "Сбор идей и предложений сотрудников: ящик предложений".
  - Pricing and traction: "Доступно в подписке" (Marketplace subscription). Rating 5/5 from 20 reviews (18×5★). 568 installs. Published 05.05.2025, with reviews up to 06.11.2026.
  - Statuses: Новая → На рассмотрении → Принята → В работе → Реализована / Отклонена (with reason). Status history on the card, and the author is notified of each decision.
  - Reviewers: admins assign reviewers, who get a «Разобрать» button, a list of the longest-waiting ideas, and bulk status changes.
  - Dialog: reviewer and author exchange messages per idea.
  - Anonymity: anonymous authors get a tracking code (e.g. 7KQM-4MPX-29QW) to follow status and reply. "Анонимность настоящая: у анонимной идеи автор не сохраняется ни в приложении, ни в журналах." Admins choose anonymous-by-default, named-by-default or named-only.
  - Reminders: reviewers are reminded after 3 working days without a decision and get a Monday digest. No notifications at night or weekends.
  - Other: optional "Идеи коллег" voting with hidden voters; topical idea campaigns (up to 12 topics); trend totals; Excel export; submission from profile and mobile.
  - Not included: tasks, feed posts, file attachments. Reviewers asked for photo attachments, and the developer promised them. A box-version broken-link bug was reported and fixed.
  - Source: [bitrix24.ru/apps/app/aventra.idei_ot_sotrudnikov](https://www.bitrix24.ru/apps/app/aventra.idei_ot_sotrudnikov/)
- **«Управление идеями» — Brusnika Solutions (novus).**
  - Pricing and traction: "Бесплатно при наличии подписки на маркет Битрикса". Rating 5/5 from 2 reviews. 980 installs. Published 05.03.2019, latest version 7 on 03.09.2026 ("Переработан интерфейс"). 18 interface languages; Kazakh is not confirmed.
  - Workflow: draft → approval → implementation → implemented or rejected, with history. Flexible sequential or parallel approval matrix, category routes, and final approval by a committee or a responsible person.
  - Tasks: **approved ideas become Bitrix24 tasks** with assignees, observers and deadlines, and the idea status follows its tasks. A "requires my action" queue collects pending work.
  - Engagement: comments and likes; voting by likes, a 10-point scale or custom criteria; top-10 ideas and authors; points and a gift shop.
  - Notifications: via Bitrix24 IM.
  - Reports: exportable, by month, quarter or year.
  - Sources: [bitrix24.ru/apps/app/novus.ideamanagement](https://www.bitrix24.ru/apps/app/novus.ideamanagement/). The task linkage is also described in a [search snippet](https://www.bitrix24.ru/apps/app/novus.ideamanagement/). A search snippet from the .by/.uz listing mentioned a USD 499/year cap outside RU/BY; this was not confirmed on a fetched page — [bitrix24.uz listing](https://www.bitrix24.uz/apps/app/novus.upravlenie_ideyami/)
- **«Банк идей» — БАРИО.**
  - Pricing and traction: "Доступно в подписке". 5/5 from 1 rating. 106 installs. Published 26.08.2025. "Работает на всех облачных и коробочных тарифах Битрикс24".
  - Features: idea submission with tags; weighted point voting for employees and managers; auto-sorting; author rankings; roles detected from the department structure; search; CSV export; data stays inside Bitrix24.
  - Gaps: implementation stages and deadlines are only "planned extensions". This is a voting and ranking tool, not a workflow tool.
  - Source: [bitrix24.ru/apps/app/bario.app3](https://www.bitrix24.ru/apps/app/bario.app3/)
- **«Есть идея» | ХайХаб — Эм Си Арт (mcart.idea4cloud).**
  - Pricing and traction: 4 195 installs, the most installed. Rating 3/5 from 2 reviews, citing sync errors and the free-tier limit. Published 04.10.2017, version 15 on 29.12.2025. Free tier "лимит в 5 активных пользователей". Paid price not published, by request via @HiHub_Bot or hi@hihub.ru. A 2024 developer reply mentioned a 30% discount for Bitrix24 users.
  - Features: statuses Новая / В работе / Внедрена and rejection with reason in comments; comments with @mentions; likes and ratings; anonymous or public submission; attachments; tree categories; admin stats with filters; mobile. Version 15 added a chatbot for comment notifications.
  - Gaps: no assignee field described, and no status-change notification to the author described.
  - Source: [bitrix24.ru/apps/app/mcart.idea4cloud](https://www.bitrix24.ru/apps/app/mcart.idea4cloud/)
- **«Банк Идей» — Эм Си Арт (mcart.idea), on-premise module.**
  - Pricing and compatibility: **261 450 ₽**. Compatible with 1С-Битрикс editions «Корпоративный портал», «Энтерпрайз», «Интернет-магазин + CRM», i.e. self-hosted, not cloud. 100–499 installs, 1 review. Published 28.04.2023, updated 22.10.2026 (v1.0.21).
  - Features: committee statuses «На модернизации», «Отправлено на доработку», «Голосование и оценка экспертом», «Принята», «Отклонена»; official answers such as «будет внедрено», «уже работает», «выполнено»; employee voting and comments.
  - The vendor advises committee meetings 1–2 times a month: "Если делать это реже, сотрудники могут потерять веру".
  - Sources: [marketplace.1c-bitrix.ru/solutions/mcart.idea](https://marketplace.1c-bitrix.ru/solutions/mcart.idea/), [mcart.ru blog](https://www.mcart.ru/blogs/bank-idey/)
- Not an ideas app: «Кайдзен.Структура» is an admin tool for CRM fields and reference lists — [bitrix24.ru/apps/app/kaydzen_bot.struktura](https://www.bitrix24.ru/apps/app/kaydzen_bot.struktura/). Related category: "HR / Мотивация" — [bitrix24.ru/apps/category/hr_motivation](https://www.bitrix24.ru/apps/category/hr_motivation/)
- **Subscription cost (needed for the cloud apps):**
  - Russia: the "единая подписка BitrixGPT + Маркетплейс" costs, per month for the whole company, Базовый 1 000 ₽ (800 ₽ discounted), Стандартный 3 000 ₽ (2 400 ₽), Профессиональный 6 000 ₽ (4 800 ₽), Энтерпрайз-250 13 600 ₽ (10 880 ₽). Prices exclude VAT. The page does not list KZ prices — [bitrix24.ru/apps/subscribe_base.php](https://www.bitrix24.ru/apps/subscribe_base.php)
  - The single subscription replaced "Маркет Плюс" and the free integration package (planned for Q1 2025). Market Plus discounts "не действуют для Битрикс24, зарегистрированных в доменной зоне KZ" — [bitrix24.ru promo page](https://www.bitrix24.ru/promo/blackfriday/)
  - The equivalent bitrix24.kz pages returned 404.

### Inferences
- For a fast, low-risk pilot, Aventra already covers the owner's stated pains out of the box: status visibility for the author, clarifying-question dialog, reminders to stop silent forgetting, and anonymity to keep people speaking up. It needs no Professional plan; the app does not state a plan requirement.
- Brusnika covers the "decision → implementation via tasks" part better. Neither app is designed for operational *problems* (blockers and complaints) as distinct from *ideas*, and neither offers SLA-by-type or routing to a department head by category beyond "category-based routes" (Brusnika).
- Install counts are small (hundreds to a few thousand), which suggests this is a niche category and not a standard practice among Bitrix24 users.

### Gaps
- Price of "BitrixGPT + Маркетплейс" in tenge for bitrix24.kz (pages 404; no KZ price found in search).
- Whether Aventra's or Brusnika's apps support Kazakh-language UI.
- Exact plan requirements for Aventra (not stated on the fetched page).

## 3. 1C solutions; is 1С:УТ relevant?

### Takeaway
No mainstream 1C configuration or extension for "банк идей", кайдзен- or рац-предложения was found for 2024–2026. The only 1C-platform product found is an old АИС "Управление рационализаторскими предложениями" from ООО «Разработчик» (age about 2020; status unknown). 1С:УТ (trade management) has no relevant functionality; for this use case it is at most a reference-data source.

### Cited Findings
- АИС «Управление рационализаторскими предложениями» on "1С:Предприятие 8" by ООО «Разработчик»: authors register a proposal with co-authors; it supports IP registration, implementation planning and implementation schedules. The page is marked roughly 2437 days old (about 2020) and no price was found. Flag as old — [up-pro.ru](https://up-pro.ru/library/production_management/kaizen/povysheniye-effektivnosti-raboty-prosto/)
- Searches across 1С:Документооборот, ТОИР and ERP turned up no built-in idea or proposal module. 1С:ТОИР is equipment-maintenance oriented — [1cbit.ru on 1С:ТОИР](https://www.1cbit.ru/blog/1s-toir-obzor-funktsionalnykh-vozmozhnostey-pri-upravlenii-remontami-i-obsluzhivanii-oborudovaniya/). An Infostart forum on 1С:Документооборот discusses customization but nothing for ideas — [forum.infostart.ru](https://forum.infostart.ru/forum9/topic201123/)
- A Belarusian library review lists registered software for "Автоматизация учета рационализаторских предложений" (RU2022666968), but it is not shown to be 1C-based — [rlst.by](https://rlst.by/informational-resources/izdania/ib-1-2025/147090-2/)
- The 1C link that does exist on the market: Brainforce, a standalone idea platform, "интегрируется с «1С:ЗУП»" for employee data — [CNews, 2026-02-02](https://www.cnews.ru/articles/2026-02-02_kak_tsifrovizatsiya_idej_sotrudnikov)
- Methodology note for data-model design: one industrial company merged «Кайдзен-предложение» and «Рационализаторское предложение» into a single "Предложение по улучшению" with categories 0–5 — [up-pro.ru](https://up-pro.ru/library/production_management/systems/predlozheniya-po-uluchsheniyam/)
- Bitrix24 ↔ 1C integration is an established paid service in Kazakhstan (article exists; price not extracted) — [profi-soft.kz](https://profi-soft.kz/articles/skolko-stoit-integratsiya-bitrix24-i-1s-v-kazahstane-20260830-041037/)

### Inferences
- 1С:УТ is irrelevant as the host for this module: it is a trade, warehouse and sales system with no employee-workflow layer. At most it could feed context. Examples: link an idea or problem to a supplier, order or product, or compute economic effect from sales and purchase data.
- Employee and department master data more naturally comes from Bitrix24's company structure. If they run it, 1С:ЗУП for Kazakhstan is another source; unknown whether they do.
- Building the module inside 1C would be the wrong platform choice for Modus Trade. Employees across sales, engineering and service live in Bitrix24, not in 1C.

### Gaps
- No search of solutions.1c.ru or the Infostart marketplace turned up a current "банк идей" extension. A dedicated catalog search might find small Infostart publications; not verified.
- Whether Modus Trade uses 1С:ЗУП (Kazakhstan edition) is unknown.

## 4. Standalone Russian/CIS products for idea management and employee voice (including Kazakhstan)

### Takeaway
The Russian market has enterprise "фабрика идей" platforms: ТЕКОРА «4И», Atwinta «Цифровая фабрика идей» and Brainforce. They target large industrial holdings (ЕВРАЗ, АЛРОСА, Светогорский ЦБК), are usually on-premise and custom, and do not publish prices. HR and engagement platforms (WebTutor, Happy Job, Сбер «Пульс») cover pieces such as idea-bank apps or survey comments. In Kazakhstan, large companies (KMG refineries including Pavlodar, ERG, КазАзот) run internal "Банк идей" or "Фабрика идей" programs, but no Kazakhstan-origin product for SMBs was found.

### Cited Findings
- **ТЕКОРА «4И» ("Информационный Инкубатор Инновационных Идей").**
  - It is the platform behind ЕВРАЗ «Фабрика идей 2.0», "корпоративная информационная система управления предложениями сотрудников", covering all divisions and subsidiaries — [tekora.ru](https://www.tekora.ru/proekty/fabrika-idey-2-0/), [tekora.ru 4И](https://www.tekora.ru/resheniya/upravlenie-ideyami-4i/proekty/)
  - Submission works from workstations, mobile and a corporate chatbot. Gamification includes a virtual shop, ratings and badges. The vendor claims about 300 proposals published daily (vendor and customer claim, not independently verified) — [globalcio.ru](https://globalcio.ru/projects/28729/)
  - ЕВРАЗ project won "Проект года 2022" — [tekora.ru](https://www.tekora.ru/o_kompanii/otzyvy/1103/)
  - АЛРОСА "Фабрика идей" portal (registration, moderation, classification) replaced the old rationalization-proposal system — [idea.alrosa.ru](https://idea.alrosa.ru/front/system), [tekora.ru](https://www.tekora.ru/press_centr/publikacii/video-sayt-fabrika-idey-zarabotal-dlya-rabotnikov-alrosa/)
  - Price not published.
- **Atwinta «Цифровая фабрика идей».** Positioned as a tool to turn "хаотичных предложений" into a structured pipeline.
  - Features: single idea registry; multi-level online approvals; a **"доска проблем"** (problem board) to pass issues to owners; implementation planner and task tracker; financial and technical effect models; real-time dashboards; automated author bonuses; role-based access; multi-company; optional mobile app.
  - Deployment and pricing: data "на собственных серверах", custom-built, "Нет абонентских платежей", price not published.
  - Claims 40+ companies, about 60 000 users, and a 25 bn ₽ economic effect (vendor claim).
  - Source: [digital-factory.atwinta.ru](https://digital-factory.atwinta.ru/)
- **Brainforce.** Case at Светогорский ЦБК.
  - Features: themed idea contests; comments, likes and dislikes; duplicate-idea hints while typing; all ideas open to all users; every idea answered with a personal notification, including rejections ("Мы всегда отвечаем на все идеи…"); expert committee; rewards including a percentage of savings; analytics on review and implementation rates; points exchangeable for gifts.
  - Deployment and integration: on-premise, integrates with 1С:ЗУП.
  - Price not published.
  - Caveat: the search URL carried an erid ad-tracking parameter, though the article itself is not marked as advertising.
  - Source: [CNews, 2026-02-02](https://www.cnews.ru/articles/2026-02-02_kak_tsifrovizatsiya_idej_sotrudnikov)
- Other Russian industrial "фабрика идей" cases (titles only, not fetched): "Фабрика идей: экосистема из 5 сервисов…" — [ratingruneta.ru](https://ratingruneta.ru/cases/case-14532/); "3 000 предложений, которые принесли компании 20 ярдов выгоды" — [ratingruneta.ru](https://ratingruneta.ru/cases/case-15158/); a 70 000-improvements ecosystem across 24 plants — [ruward.ru](https://ruward.ru/cases/8303/)
- **WebTutor (WebSoft) «Банк идей» app.** Idea submission form; colleague evaluation and discussion; configurable approval rules and themes; admin console with implementation status and a popularity report; digest of new ideas to employee groups. Admin training "за 1 час". "Все приложения доступны бесплатно для клиентов, имеющих конфигурацию не менее LMS". Post dated 13.04.2020, so this is older information — [blog.websoft.ru](https://blog.websoft.ru/2020/04/webtutor.html)
- **Happy Job.** An engagement and loyalty survey platform. Employees can leave suggestions within surveys, including anonymously, with built-in content analysis of open comments. It is a survey tool, not a case-tracking tool — [happy-job.ru reviews](https://happy-job.ru/clients/reviews/), [happy-job.ru](https://happy-job.ru/)
- **Сбер «Пульс».** An HR platform with "более 40 приложений" spanning recruiting to offboarding, including "обратная связь, оценка". It went to the external market in 2022 and was spun off as ООО «Пульс» in July 2024. No ideas or suggestions module was found in sources — [developers.sber.ru](https://developers.sber.ru/portal/products/pulse?attempt=1), [eastrussia.ru](https://www.eastrussia.ru/news/hr-platforma-puls-ot-sbera-vyshla-na-vneshniy-rynok/). MTS Bank's separate internal "Пульс" HR social network is a different product — [vc.ru](https://vc.ru/mtsbank/677043-v-mts-banke-betsya-puls-novaya-hr-platforma-i-socialnaya-set-s-iskusstvennym-intellektom)
- **ELMA365.** A low-code BPM platform. No ready-made "банк идей" template was found in sources — [crmindex.ru](https://crmindex.ru/products/elma365_bpm)
- **Kazakhstan: internal corporate programs, not commercial products:**
  - **KMG «Банк идей»** systemic platform at the refineries in Pavlodar, Atyrau and Shymkent (ПНХЗ, АНПЗ, ПКОП), 2015–2022. About 6 000 users registered and 190 ideas implemented. The platform vendor is not named — [kmg.kz](https://www.kmg.kz/ru/company/projects/all/vnedrenie-sistemnoy-platformy-bank-idey/), portal [idea.kmg.kz](https://idea.kmg.kz/). Pavlodar refinery (ПНХЗ) coverage — [sknews.kz](https://sknews.kz/news/view/pnhz-racionalynyy-bank-idey). КМГ-ПМ patented its "Банк идей" — [inbusiness.kz](https://inbusiness.kz/ru/last/ao-kmg-pm-zapatentovalo-bank-idey-9775). Older, 2016–2022.
  - **ERG «Фабрика идей»**: 32 084 improvement proposals in one year (reported 2021) and 2 500 employees in kaizen teams — [inbusiness.kz](https://inbusiness.kz/ru/news/svyshe-32-tysyach-proektov-po-uluchsheniyu-rabochih-processov-predlozhili-sotrudniki-eurasian-recourses-group-v-2021-godu)
  - **КазАзот «Фабрика идей»**: quarterly and annual prizes, with an effect-based bonus "до 5 млн. тенге" — [kazazot.kz](https://kazazot.kz/karera/fabrika-idey/)

### Inferences
- The standalone "фабрика идей" category is built for thousands of plant workers and economic-effect accounting. It is overkill and likely too expensive for a roughly 100-person distributor/integrator. Prices are not published and products are custom or on-prem.
- The strongest design lessons to borrow are Brainforce's "every idea gets a personal answer, including rejection", Atwinta's separate "доска проблем" next to ideas, and the committee-cadence warning from MCART.
- The Pavlodar refinery's KMG idea bank is a local reference point the hackathon jury may recognize.

### Gaps
- Not verified or no evidence found for an idea or suggestion module in: Mirapolis HCM, Teamly, "Начни Делать?" (could not confirm this product exists), "Ведомости"-style surveys.
- No Kazakhstan-origin commercial idea-management SaaS found.
- No prices published for ТЕКОРА 4И, Atwinta or Brainforce.

## 5. Deployment, language, data localization in Kazakhstan

### Takeaway
Bitrix24 portals on the .kz zone store personal data in a datacenter in Kazakhstan, hosted by PS.KZ, under the RK personal-data law. That is a real advantage of staying inside Bitrix24 versus Russian on-prem or SaaS idea platforms. Marketplace apps such as BARIO claim data stays inside Bitrix24. Kazakh-language support for the apps is unconfirmed.

### Cited Findings
- "Для обеспечения бесперебойной работы сервиса используется датацентр в Республике Казахстан" — [bitrix24.kz/security](https://www.bitrix24.kz/security/)
- The status page says personal data of Bitrix24 portals created in the .KZ zone is placed in a datacenter on RK territory, per the law «О персональных данных и их защите» of 21.05.2013; hosting is by PS.KZ — [status.bitrix24.kz](https://status.bitrix24.kz/)
- The processor is ТОО «1С-Битрикс Казахстан» (Almaty) — [bitrix24.kz DPA](https://www.bitrix24.kz/about/dpa_pers.php)
- BARIO «Банк идей»: "Данные хранятся внутри Битрикс24, внешний сервер не требуется" (paraphrased by the fetch tool) — [bitrix24.ru/apps/app/bario.app3](https://www.bitrix24.ru/apps/app/bario.app3/)
- Deployment options: Bitrix24 cloud or self-hosted box. Box licenses in Russia run from 60 000 ₽/year for a 50-user Корпоративный портал — [bitrix24.ru/apps/subscribe_base.php](https://www.bitrix24.ru/apps/subscribe_base.php). Brainforce is on-prem — [CNews](https://www.cnews.ru/articles/2026-02-02_kak_tsifrovizatsiya_idej_sotrudnikov). Atwinta runs on own servers — [atwinta](https://digital-factory.atwinta.ru/). MCART «Банк Идей» is for the self-hosted 1С-Битрикс portal — [marketplace.1c-bitrix.ru](https://marketplace.1c-bitrix.ru/solutions/mcart.idea/)

### Inferences
- Third-party Marketplace apps that store data on the developer's servers (not stated for Aventra or Brusnika) could undercut the .kz localization advantage. Check each app's data-storage statement before choosing.

### Gaps
- Kazakh-language UI support for Bitrix24 core and for each app was not verified.
- Data-storage location for Aventra, Brusnika and ХайХаб apps was not stated on fetched pages.

## 6. Common complaints and limitations reported

### Takeaway
Reported issues are mostly about Bitrix24 platform friction rather than idea apps per se. Problems include rights complexity, cloud business-process concurrency limits, schema rigidity, REST gaps, implementation overruns, and missing attachments or tasks in lightweight idea apps.

### Cited Findings
- Smart processes: rights must be explicitly granted, and the author cannot see their own item without read rights. Field type cannot be changed after creation. Moving a smart process to another portal is not native, and Excel template import needs a paid app. Some features roll out gradually — [netit24.com](https://netit24.com/smart-processy-v-bitrix24/)
- Cloud limit: no more than two business processes running simultaneously on one CRM element, smart processes included. The limit does not apply to the box version. This comes from a search summary of Bitrix24 helpdesk and was not fetched directly — [helpdesk.bitrix24.ru/open/5671433](https://helpdesk.bitrix24.ru/open/5671433/)
- There is no single built-in list of all smart processes; a third-party BI report app exists for that — [bitrix24.ru app](https://www.bitrix24.ru/apps/app/sites7.spisok_smart_protsessov_otchyet_bi/)
- Integrator warning: large Bitrix24 projects risk overrunning "бюджет и срок внедрения в 2 раза" and ending with conflicting business processes — [workspace.ru](https://workspace.ru/blog/top-10-riskov-i-problem-pri-vnedrenii-i-dorabotke-bitriks24/)
- App-level complaints:
  - Aventra users asked for photo attachments, and a box-version notification link was broken (fixed) — [Aventra listing](https://www.bitrix24.ru/apps/app/aventra.idei_ot_sotrudnikov/)
  - ХайХаб reviews cite errors in space creation and user sync, plus the 5-user free cap — [ХайХаб listing](https://www.bitrix24.ru/apps/app/mcart.idea4cloud/)
  - BARIO lacks stages and deadlines so far — [BARIO listing](https://www.bitrix24.ru/apps/app/bario.app3/)
- An old (2012) article argues Bitrix24 is unsuitable for moderated anonymous communications. It is outdated, and Aventra now claims true anonymity — [aupil.com](https://aupil.com/newpostb24_8_2012/)

### Inferences
- The two-concurrent-BP limit in the cloud pushes a DIY build toward robots and triggers rather than heavy business processes.

### Gaps
- No user reviews specific to "банк идей on smart processes" were found (e.g. on habr or vc.ru).
- No independent reviews of ТЕКОРА, Atwinta or Brainforce were found.

## 7. Fit for Modus Trade: could they just configure Bitrix24 instead of building something new, and what would be missing?

### Takeaway
**Yes, mostly.** A Bitrix24-native solution can cover about 70–80% of the owner's requirements. The fastest route is installing Aventra's «Идеи от сотрудников». The more flexible route, which requires Профессиональный, is a configured smart process: CRM form → stages «Рассмотрение → Принятие решения → Реализация» → robots for reminders and notifications → tasks → reports. What remains weak is a clean **author-facing "my requests" view** with role-scoped visibility, **problem vs. idea triage with per-type SLAs and escalation**, a **management dashboard of stuck and overdue items across departments**, and **intake from chaotic channels** (email, meetings, calls). The hackathon MVP should either build these or present itself as a thin layer on top of Bitrix24.

### Cited Findings
- The smart-process approach is proven for idea banks at a similar portal size (VEKA Rus, 250 users), but it needed integrator customization and admin-driven card movement — [ipg.digital](https://ipg.digital/portfolio/avtomatizatsiya/kak-my-avtomatizirovali-dokumentooborot-komandirovki-i-bank-idey-na-baze-korporativnogo-portala-bitr/)
- Smart processes require Профессиональный (76 000 ₸/month list, 100 users) or Энтерпрайз — [bitrix24.kz/prices](https://www.bitrix24.kz/prices/), [netit24.com](https://netit24.com/smart-processy-v-bitrix24/)
- Aventra's app already provides:
  - the stages Новая/На рассмотрении/Принята/В работе/Реализована/Отклонена;
  - an author ↔ reviewer dialog and author notifications on each decision;
  - anonymous submission with a tracking code;
  - three-working-day reminders and a weekly digest.

  It does not provide tasks or attachments — [Aventra listing](https://www.bitrix24.ru/apps/app/aventra.idei_ot_sotrudnikov/)
- Brusnika's app converts approved ideas into Bitrix24 tasks with deadlines and syncs status from them — [Brusnika listing](https://www.bitrix24.ru/apps/app/novus.ideamanagement/)
- Requests can be captured via CRM forms and shown to employees at all stages (WeJET service-desk pattern) — [wejet.ru](https://wejet.ru/cases/vnedrenie-i-nastroyka-bitriks24-dlya-integratora-leo-telekom.html)
- Data on a .kz portal stays in Kazakhstan — [status.bitrix24.kz](https://status.bitrix24.kz/)
- 1С:УТ has no relevant functionality, and no current 1C idea module was found (see section 3).

### Inferences
**Useful for Modus Trade:**
- Staying inside Bitrix24 keeps a single login, mobile app, notifications, org structure, tasks and KZ data residency.
- A Marketplace app can be piloted in days.
- A smart process gives full control of stages, fields, robots (e.g. "remind the assignee if the item has sat in a stage more than N days", "notify the author on stage change") and reports, at the cost of the Professional plan.

**Not useful:**
- Russian "фабрика идей" enterprise platforms (4И, Atwinta, Brainforce): custom, on-prem, unpriced, built for plants with thousands of workers and rationalization bonuses.
- HR survey platforms (Happy Job, Пульс): no case tracking.
- 1C-based options: wrong user surface, nothing current.
- MCART box module (261 450 ₽): only for a self-hosted portal.

**What would still be missing with pure configuration (candidate MVP value-adds):**
1. **Author-scoped visibility.** Smart-process rights are role, stage and own/department/all based. Making every employee see only their own submissions' stage, while managers see everything, needs careful rights design or a custom "Мои обращения" view. Unverified whether "own" covers the creator.
2. **Problems, not just ideas.** All the apps are idea banks. Operational problems (a blocker in purchasing, an accounting-process issue) need routing to the responsible department, SLAs and escalation; only the DIY smart process or a custom layer handles this.
3. **Owner's control panel.** No app shows "what is stuck where, who is overdue, which departments ignore issues". Bitrix24 reports and the BI constructor can approximate it (BI constructor on Professional), but an at-a-glance overview is a likely MVP differentiator.
4. **Intake from email, meeting notes and calls.** Nothing in the apps converts these into tracked items. A Bitrix24-integrated bot, mailbox or form, or AI summarization, would close the "chaotic channels" pain.
5. **Closing the loop.** Mandatory feedback to the author on rejection, plus "was your issue resolved?" confirmation. Aventra partly has this; DIY setups need robots.

**Recommendation framing for the pitch:** do not compete with Bitrix24. Build the MVP as a Bitrix24 app or REST integration (or a smart process plus a custom UI), and position it against the Aventra and Brusnika apps as "issues + ideas + owner dashboard + intake from chaos".

### Gaps
- Modus Trade's current Bitrix24 plan, headcount (vs. the 50/100-user caps) and whether they already pay for the Marketplace subscription. All three decide cost and feasibility.
- The tenge price of the Marketplace subscription.
- Whether Aventra works on their plan and supports Kazakh.
