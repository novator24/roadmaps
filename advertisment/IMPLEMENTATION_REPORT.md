# IMPLEMENTATION REPORT — ROADMAPS advertisement

## 1. Исходное состояние

`DRAFT.docx` — 30-страничный landscape DOCX, оформленный как презентация с фиксированными page breaks. Сохранены:

- 30 страниц и их исходный порядок;
- заголовки, тайминг, storyline и основной текст;
- исходные изображения, градиенты, таблицы, стили, шрифты и отношения DOCX;
- продуктовая концепция: ROADMAPS.ME, B2B SaaS, marketplace и экспериментальный dispute/Polymarket-модуль;
- исходный `DRAFT.docx` без изменений.

## 2. Замечания преподавателя

Обязательные замечания из `lesson2/README.md`:

- C-level не заменяет структуру разработки; нужна IT/development organization для MVP и будущих периодов;
- первый год желательно разбить на Q1–Q4, а tactical plan детализировать;
- рискам нужны prevention/mitigation и response;
- KPI нужно расширить, включая NPS и security incidents;
- нужна безопасная разработка;
- требуется бюджет разработки, инфраструктуры и ИБ;
- customer interviews нельзя выдавать за подтвержденную гипотезу.

## 3. Что изменено

| Issue | Change | Slide |
|---|---|---:|
| IT structure | Добавлены MVP, Year 1, Year 3 и Year 5 структуры с FTE | 4 |
| C-level vs delivery | Разделены governance и непосредственная IT-разработка | 4 |
| Customer development | 40 интервью обозначены как план; гипотеза — `To be validated` | 9 |
| Quarterly Year 1 plan | Добавлены Q1–Q4 с product, engineering, infrastructure и security инициативами | 10 |
| Year 1 staffing | Зафиксированы 5 FTE в Armenia через ИП как planning assumption | 4, 10, 22 |
| Detailed tactical plan | Initiative / owner / timing / outcome по 6 направлениям | 11 |
| Year 3 staffing | Зафиксированы 30 FTE в UAE и departmental split | 4, 11 |
| Year 5 staffing | Зафиксированы 125 UAE + 1 Hong Kong = 126 | 4, 12, 22 |
| Development/IT budgets | Пересчитаны Year 1, Year 3, Year 5 на основе staffing assumptions | 10–12 |
| Risk mitigation | Для каждого исходного риска добавлены preventive controls | 14 |
| Risk response | Для каждого риска добавлены response, owner и trigger | 14 |
| Metrics | Добавлены Product, Customer, DORA, Reliability, Security и People KPI | 17 |
| NPS/security metrics | Добавлены NPS, incident count, vulnerabilities, MTTR, MFA и patch compliance | 17 |
| Security by design | Добавлен secure SDLC lifecycle | 23 |

## 4. Team structure

| Horizon | Location | Structure | Total |
|---|---|---|---:|
| MVP / as-is | Remote / founder-led | Founder/Product, Tech Lead, Full-stack, QA, DevOps/Infrastructure; partial roles possible | Minimal |
| Year 1 | Armenia / ИП | Tech Lead/Product 1; Software Engineers 2; QA 1; DevOps/Data 1 | 5 |
| Year 3 | UAE | Engineering 18; QA 4; DevOps/SRE 3; Product/Tech 3; Management 2 | 30 |
| Year 5 | UAE | Engineering 80; QA 15; SRE/Platform 10; Product/Data/Security 12; Management 8 | 125 |
| Year 5 | Hong Kong | Regional technology/compliance liaison | 1 |

## 5. Salary research — 2026

Значения ниже — market benchmarks и planning inputs, а не гарантированная зарплата.

| Country | Role | 2026 benchmark | Source | Date |
|---|---|---:|---|---|
| Armenia | Software Engineer | $24k–$45k/year full-stack benchmark; senior examples $42k–$65.4k | [HireTruss Armenia 2026](https://hiretruss.com/2026-tech-salary-guide-for-armenia) | 2026 |
| Armenia | DevOps Engineer | $30k–$52k/year | [HireTruss Armenia 2026](https://hiretruss.com/2026-tech-salary-guide-for-armenia) | 2026 |
| Armenia | Manual / Automated QA | $12k–$22k / $24k–$40k/year | [HireTruss Armenia 2026](https://hiretruss.com/2026-tech-salary-guide-for-armenia) | 2026 |
| Armenia | Product Owner | $28k–$48k/year | [HireTruss Armenia 2026](https://hiretruss.com/2026-tech-salary-guide-for-armenia) | 2026 |
| Armenia | Software Engineer total comp | AMD 19.58M median; AMD 12.09M–25.11M 25th–75th | [Levels.fyi Yerevan](https://www.levels.fyi/t/software-engineer/locations/yerevan-arm) | 2026-08-15 |
| UAE | Full-stack / Backend / Frontend Engineer | AED 24k / 29k / 34k monthly low / typical / high | [Guildhall Dubai Salary Guide 2026](https://guildhall.agency/dubai-salary-guide-2026) | 2026-08-30 |
| UAE | Software QA / DevOps / Data Engineer | AED 24k / 29k / 34k monthly low / typical / high | [Guildhall Dubai Salary Guide 2026](https://guildhall.agency/dubai-salary-guide-2026) | 2026-08-30 |
| UAE | Product Manager | AED 34k / 39k / 43.5k monthly | [Guildhall Dubai Salary Guide 2026](https://guildhall.agency/dubai-salary-guide-2026) | 2026-08-30 |
| UAE | Head of Engineering | AED 43.5k / 56k / 68k monthly | [Guildhall Dubai Salary Guide 2026](https://guildhall.agency/dubai-salary-guide-2026) | 2026-08-30 |
| UAE | Senior Software Engineer | AED 216,948/year average base | [PayScale UAE](https://www.payscale.com/research/AE/Job=Senior_Software_Engineer/Salary) | 2026-07-09 |
| Hong Kong | Software Engineer | HK$746,550/year average gross; entry HK$524,523; senior HK$854,369 | [ERI SalaryExpert](https://www.salaryexpert.com/salary/job/software-engineer/hong-kong-sar) | 2026 |

## 6. Budget assumptions

Base currency: USD. Rounded values intentionally avoid false precision.

| Horizon | People | Infra | Security | Software | Operations / legal / other | Total IT |
|---|---:|---:|---:|---:|---:|---:|
| Year 1 | ~$225k incl. reserve | ~$35k | ~$20k | ~$12k | ~$28k | **~$320k** |
| Year 3 | ~$3.2M | ~$350k | ~$180k | ~$120k | ~$200k | **~$4.1M** |
| Year 5 | ~$13.61M incl. HK | ~$2.2M | ~$0.9M | ~$0.7M | ~$1.1M | **~$18.5M** |

Planning FX:

- 1 USD ≈ 3.673 AED — [Wise 2026 history](https://wise.com/in/currency-converter/usd-to-aed-rate/history);
- 1 USD ≈ 7.84 HKD — [OFX 2026 history](https://www.ofx.com/en-us/forex-news/historical-exchange-rates/usd/hkd);
- Armenia slide inputs use USD ranges reported by the salary guide; employer-side tax/legal treatment is not asserted.

Gross salary, benefits/employer reserve and non-payroll IT cost are separated. Exact employer cost depends on hiring structure. The Armenia ИП model requires local legal and tax validation.

## 7. Risk mitigation

The existing legal, banking, people and smart-contract risks were preserved and expanded to:

`Risk → Mitigation → Response → Owner → Metric/Trigger`

The legal-risk response explicitly includes suspending the affected module and legal escalation. No unverified compliance claim was added.

## 8. Metrics

- Product: MAU/DAU, activation, conversion, retention, churn.
- Customer: NPS, CSAT, first response time.
- Engineering: deployment frequency, lead time, change failure rate, MTTR.
- Reliability: uptime, SLO compliance, incident count/severity.
- Security: security incidents, critical vulnerabilities, remediation time, MFA and patch coverage.
- People: staffing-plan attainment, retention, time-to-hire.

## 9. Validation

```text
DRAFT explicit page count: 30
FINAL explicit page count: 30
LibreOffice-rendered FINAL PDF pages: 30
DOCX ZIP integrity: PASS
Required acceptance phrases: PASS
New TODO/TBD/XXX/Lorem ipsum placeholders: NONE
STATUS: PASS
```

Visual review was performed on all modified slides after LibreOffice rendering. No overflow, clipping, overlap, blank pages or unreadable tables were observed.

## 10. Known limitations

- Salary figures are market benchmarks and planning estimates.
- Exact employer cost depends on employment form, benefits and mandatory contributions.
- FX rates are indicative and should be refreshed for an approved financial plan.
- Armenia ИП, UAE and Hong Kong legal/tax structures require qualified local advice.
- Microsoft Word may render small spacing differences from LibreOffice; structural and page-count checks pass.