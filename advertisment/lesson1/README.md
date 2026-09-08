### >>>

### Изучи https://linkedin.com/in/basovi и предложи моему знакомому , который на базе https://github.com/novator24/ideatalk пишет первые тикеты для asana.com, какие задачи максимально должен делать его портфолио сайт azteam.me , чтобы продавать его как saas по подпискам бизнесам за 30к первые три месяца и 100к в месяц с доработками после, но с доработками в объеме N часов по ставке 6000 р в час. Предполагается, что на сайте будут AI помощники для разных бизнесов, консультирующие по тем инструментам, которыми владеет iurii на линкедин, далее выложено демо видео применения помощника для деплоя и на лендинг этот будет реклама для компаний из ОАЭ. Напиши сразу промт для Cursor IDE и опиши в формате README.md как на Windows с Docker Compose и WSL2 с Ununtu настроить MCP агентов для доработок и тестирования максимально похоже на Replit.com

### <<<

### Я бы **не позиционировал azteam.me как “портфолио AI-разработчика”**. Для цели 30k ₽/мес первые 3 месяца → 100k ₽/мес далее сайт должен продавать **AI Automation as a Service**, а портфолио — лишь доказывать способность это делать.

Я изучил профиль Iurii, репозиторий IdeaTalk и актуальные требования MCP/Cursor/Asana. Профиль действительно хорошо поддерживает позиционирование вокруг **ML/AI + Full Stack + MCP**, а среди публичных материалов есть отдельная статья про Context7/MCP и практический пример расширения MCP-сервера. ([LinkedIn][1]) Репозиторий `ideatalk` при этом уже имеет backend/webapp/shared, Docker Compose, pnpm workspace и Jest — то есть его разумно использовать как основу для инженерного SaaS-подхода, а не начинать архитектуру с нуля. ([GitHub][2])

Сразу оговорка: `azteam.me` сейчас с моей стороны отдаёт 502, поэтому визуальный аудит существующего сайта я провести не смог. Ниже — архитектура и контент, которые я бы закладывал независимо от текущего состояния.

---

# 1. Что именно должен продавать azteam.me

Главный message:

> **AI assistants that operate your business tools — not another chatbot.**

Или для UAE:

> **AI employees for your business workflows. Connected to the tools you already use.**

Это намного дороже воспринимается, чем:

> “We build AI solutions.”

Потому что клиенту не нужен AI. Ему нужны:

* меньше ручной работы;
* быстрее deployment;
* автоматизация CRM;
* обработка документов;
* отчёты;
* customer support;
* project management;
* DevOps;
* интеграции между системами.

### Я бы сделал 5 демонстрационных AI assistants

**1. DevOps / Deployment Assistant**

> “Deploy my application to staging.”

Демонстрирует:

Git → CI/CD → Docker → environment → deployment → logs → rollback.

Это самый технически сильный demo.

---

**2. Project Manager Assistant**

Например:

> “Analyze this week's Asana tasks and identify blocked projects.”

Ассистент:

* читает Asana;
* анализирует задачи;
* ищет просрочки;
* группирует blockers;
* создаёт задачи;
* формирует executive summary.

Asana уже предоставляет официальный MCP V2 server с инструментами для поиска, создания и управления задачами и проектами. ([Asana Docs][3])

---

**3. Sales Assistant**

Например:

> “Analyze new leads and prepare follow-ups.”

Ассистент:

CRM → qualification → summary → next action → task → notification.

---

**4. Operations Assistant**

> “What operational issues require attention today?”

Получает информацию из нескольких систем и выдаёт:

```text
Critical
3 issues

Attention
7 issues

Normal
14 issues
```

И главное — **может не просто отвечать, а выполнять действие**.

---

**5. Knowledge / Company Assistant**

RAG + internal documentation:

> “How do we handle a refund for an enterprise customer?”

Ответ с источниками + возможность создать соответствующую задачу.

---

# 2. Главная идея SaaS

Я бы вообще убрал с первого экрана слова:

> portfolio
> freelancer
> software developer
> custom development

И поставил:

> **Your business already has dozens of tools.
> We give them AI operators.**

Под ним:

> Connect your existing tools.
> Automate repetitive workflows.
> Keep humans in control.

CTA:

**Book a 30-minute AI Workflow Audit**

Второй CTA:

**Watch a real deployment demo**

---

# 3. Что должно быть на сайте

Структура:

```text
/
├── Hero
├── Trusted technologies
├── "See an AI employee in action"
├── AI Assistants
│   ├── DevOps
│   ├── Operations
│   ├── Sales
│   ├── Project Management
│   └── Knowledge
├── How it works
├── Demo
├── Business cases
├── Pricing
├── Security
├── About Iurii
├── FAQ
└── Book an AI Workflow Audit
```

Но **не делать огромный каталог технологий**.

Docker, React, TypeScript, Node, MCP и т.д. должны быть доказательствами, а не продуктом.

Профиль Iurii сейчас описывает его как ML/AI/Full Stack специалиста, а публичные материалы показывают работу с TypeScript, React/TanStack, pnpm/NPNM и MCP/Context7. ([LinkedIn][1])

---

# 4. Самая важная функция — Interactive AI Demo

Вот это я считаю **№1 задачей для azteam.me**.

Пользователь должен открыть сайт и увидеть:

```text
AI DevOps Assistant

You:
Deploy my application to staging.

AI:
I'll check the repository, CI status
and current staging environment.

✓ Repository checked
✓ Tests passed
✓ Docker image built
✓ Deployment started
✓ Health check passed

Deployment successful.

[View logs]
[View deployment]
```

Это продаёт гораздо лучше десяти страниц текста.

Но demo должно быть **sandbox/demo environment**, а не реальный production.

---

# 5. Второй killer feature — AI Workflow Builder

Очень похожий UX стоит сделать на уровне:

```text
Describe what you want to automate.

"When a new enterprise lead appears,
qualify it, summarize the company,
create an Asana task and notify sales."

                  ↓

AI generates

Trigger
  ↓
Lead qualification
  ↓
Company research
  ↓
AI summary
  ↓
Asana task
  ↓
Notification
```

И:

**[Test workflow]**

Это уже начинает выглядеть не как агент-разговорник, а как **SaaS platform**.

---

# 6. Как продавать 30k → 100k

Я бы сформулировал тарифы так.

### AI Pilot — 30,000 ₽ / month

**First 3 months**

Включено:

* 1 AI assistant;
* 1–2 business workflows;
* подключение до 3 tools;
* deployment;
* analytics;
* basic support;
* monthly optimization.

Цель первых трёх месяцев — не заработать максимум, а доказать ROI.

Например:

> “We automated 120 hours of repetitive work per month.”

После этого 100k становится намного легче объяснить.

---

### AI Operations — 100,000 ₽ / month

После pilot:

* multiple AI assistants;
* multiple workflows;
* integrations;
* monitoring;
* analytics;
* continuous optimization;
* priority support;
* monthly improvement budget.

И отдельно:

### Custom Development

**6,000 ₽ / hour**

Например:

```text
Monthly AI Operations
100,000 ₽ / month

Custom engineering
6,000 ₽ / hour

Additional work is approved before implementation.
```

Я бы **не включал бесконечные доработки в 100k**.

Иначе 100k превращаются в обычную зарплату разработчика.

---

# 7. Что означает "100k + N часов"

Нужно сделать это продуктом:

```text
100,000 ₽ / month
+
N engineering hours
×
6,000 ₽ / hour
```

Например:

```text
AI Operations       100,000 ₽
Additional work:
8h × 6,000 ₽         48,000 ₽
----------------------------
Total               148,000 ₽
```

На сайте это должно выглядеть **предсказуемо и профессионально**, а не как:

> “Дальше договоримся.”

---

# 8. UAE — отдельный landing

Я бы не смешивал российскую/русскую коммуникацию и UAE.

Сделал бы:

```text
/uae
```

или отдельный microsite.

Headline:

> **AI Automation for UAE Businesses**

Под ним:

> Reduce repetitive operations, connect your business tools and deploy AI assistants tailored to your workflows.

CTA:

> **Book an AI Automation Audit**

Для UAE особенно хорошо продавать не "AI chatbot", а:

* operations;
* real estate;
* hospitality;
* professional services;
* logistics;
* sales;
* customer support;
* internal knowledge.

---

# 9. Главная архитектурная мысль

`IdeaTalk` я бы превратил из:

> AI bots store

в:

> **AI Workforce Platform**

Технически:

```text
                 azteam.me
                     │
                     ▼
             AI Assistant Layer
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
     CRM           Asana         DevOps
       │             │             │
       └─────────────┼─────────────┘
                     ▼
                   MCP
                     │
                     ▼
              Business systems
```

MCP здесь очень хорошо подходит именно как **integration layer**, а не как маркетинговое слово. Cursor поддерживает локальные и remote MCP servers, project-level `.cursor/mcp.json`, OAuth и Streamable HTTP. ([Cursor][4])

---

# 10. Что я бы поставил первыми Asana tickets

Не начинать с:

> “Сделать красивый navbar.”

При такой бизнес-модели первые тикеты должны быть **sales-critical**.

### Epic 01 — Revenue landing

```text
AZ-1 Hero section
AZ-2 AI Assistant demo
AZ-3 Business outcomes section
AZ-4 Pricing
AZ-5 CTA / lead capture
AZ-6 UAE landing
```

### Epic 02 — Interactive Demo

```text
AZ-10 Demo assistant shell
AZ-11 Streaming responses
AZ-12 Tool execution timeline
AZ-13 Demo sandbox
AZ-14 Deployment demo
AZ-15 Demo reset
```

### Epic 03 — AI Assistant platform

```text
AZ-20 Assistant registry
AZ-21 Assistant configuration
AZ-22 Tool registry
AZ-23 MCP adapter
AZ-24 Conversation state
AZ-25 Execution history
```

### Epic 04 — Business workflows

```text
AZ-30 Asana assistant
AZ-31 DevOps assistant
AZ-32 Sales assistant
AZ-33 Operations assistant
AZ-34 Knowledge assistant
```

### Epic 05 — SaaS

```text
AZ-40 Authentication
AZ-41 Organization/workspace
AZ-42 Subscription
AZ-43 Usage limits
AZ-44 Billing
AZ-45 Admin panel
```

### Epic 06 — Engineering

```text
AZ-50 Docker development environment
AZ-51 Unit tests
AZ-52 Integration tests
AZ-53 E2E tests
AZ-54 CI
AZ-55 MCP test harness
```

---

# 11. Готовый промпт для Cursor

Ниже я бы **прямо вставил этот prompt в Cursor Agent**.

# AZTEAM — Build the AI Workforce SaaS

You are the principal engineer and product architect for AZTEAM.

Your goal is NOT to build another portfolio website.

Your goal is to transform the existing project into a production-oriented SaaS landing + AI assistant platform that can sell AI automation services to businesses.

## BUSINESS MODEL

AZTEAM sells AI automation as a managed SaaS/service.

Initial offer:

* 30,000 RUB/month for the first 3 months
* onboarding and pilot implementation
* one or more AI assistants
* selected business workflows
* integrations with existing business tools

After successful pilot:

* 100,000 RUB/month
* continuous AI assistant operation
* monitoring
* optimization
* additional workflows

Custom engineering:

* 6,000 RUB/hour
* work outside the agreed monthly scope must be explicitly approved
* never silently consume unlimited development hours

The website must communicate this business model clearly.

## PRODUCT POSITIONING

Primary positioning:

"AI assistants that operate your business tools."

Alternative:

"AI employees for repetitive business workflows."

Do NOT position AZTEAM primarily as:

* a freelancer portfolio
* a generic software agency
* a chatbot company
* an AI research project

The visitor must understand within 5 seconds:

1. What AZTEAM does.
2. What business problem it solves.
3. What an AI assistant can actually do.
4. What the next step is.

## TARGET MARKET

Primary:

* UAE businesses
* SMEs
* professional services
* real estate
* hospitality
* logistics
* sales organizations
* companies with repetitive operational workflows

Secondary:

* technology companies
* startups
* internal engineering teams

## CORE PRODUCT EXPERIENCE

The most important feature is an interactive AI assistant demonstration.

Example:

User:

"Deploy my application to staging."

Assistant:

1. inspect repository
2. inspect CI state
3. run tests
4. build Docker image
5. deploy to sandbox
6. perform health check
7. report result

The UI must visually show tool execution:

✓ Repository checked
✓ Tests passed
✓ Docker image built
✓ Deployment started
✓ Health check passed

The demo MUST NOT execute destructive actions against real production infrastructure.

Use a sandbox/mock environment where necessary.

## SECOND CORE EXPERIENCE

Create an AI Workflow Builder.

Example user request:

"When a new enterprise lead appears, qualify it, summarize the company, create an Asana task and notify sales."

The application should represent this as:

Trigger
↓
AI classification
↓
Company research
↓
AI summary
↓
Asana task
↓
Notification

Provide:

* workflow visualization
* test button
* execution status
* execution log
* success/failure state

## AI ASSISTANTS

Implement the architecture so assistants are configurable rather than hard-coded.

Initial assistants:

1. DevOps Assistant
2. Project Manager Assistant
3. Sales Assistant
4. Operations Assistant
5. Knowledge Assistant

Each assistant should have:

* id
* name
* description
* business value
* system instructions
* available tools
* permissions
* demo mode
* execution history

## MCP

MCP must be treated as an integration layer.

Create a clean abstraction:

Assistant
→ Tool Registry
→ MCP Adapter
→ External Tool

Do not couple business logic directly to a specific MCP server.

Support future integrations without rewriting assistants.

The first important external integration is Asana.

Use the current Asana MCP V2 architecture.

Do NOT use the deprecated Asana V1 SSE endpoint.

Asana MCP must be configured as a remote Streamable HTTP MCP server and authenticated using the supported OAuth flow.

Secrets must NEVER be committed.

## EXISTING REPOSITORY

First inspect the existing repository completely.

The current repository contains:

* backend
* webapp
* shared
* Dockerfile
* docker-compose.yml
* pnpm workspace
* Jest configuration

Do NOT rewrite the application from scratch.

Preserve useful existing architecture.

Before changing code:

1. inspect package.json
2. inspect pnpm workspace
3. inspect backend
4. inspect webapp
5. inspect shared
6. inspect Docker configuration
7. inspect tests
8. inspect environment configuration

Then produce a short architecture assessment.

Only after that start implementation.

## FRONTEND

The frontend should feel like a modern AI SaaS product.

Desired visual direction:

* premium
* minimal
* dark/light compatible
* strong typography
* subtle animations
* generous whitespace
* technical credibility
* enterprise feel

Do not create visual clutter.

The homepage should contain:

1. Hero
2. CTA
3. Interactive assistant demo
4. Business outcomes
5. AI assistants
6. Workflow visualization
7. Real deployment demo
8. Technology/integration proof
9. Pricing
10. Security
11. About Iurii
12. FAQ
13. CTA

## HERO COPY

Use a variation of:

"AI assistants that operate your business."

Supporting copy:

"Connect your existing tools, automate repetitive workflows and give your team AI operators that can actually take action."

Primary CTA:

"Book an AI Workflow Audit"

Secondary CTA:

"Watch the demo"

Do not overuse the word "AI".

## PRICING

Display:

AI Pilot

30,000 ₽ / month
First 3 months

Includes:

* AI workflow audit
* assistant configuration
* selected integrations
* initial workflow automation
* deployment
* monitoring
* monthly optimization

Then:

AI Operations

100,000 ₽ / month

Includes:

* multiple assistants
* multiple workflows
* integrations
* monitoring
* optimization
* priority support

Additional engineering:

6,000 ₽ / hour

Clearly state that additional engineering is performed only after approval.

## UAE LANDING PAGE

Create a dedicated UAE-oriented landing page.

Positioning:

"AI Automation for UAE Businesses"

Focus on:

* operations
* customer service
* sales
* real estate
* hospitality
* logistics
* professional services

CTA:

"Book an AI Automation Audit"

Do not make unsupported claims about UAE regulations, certifications or customers.

## DEMO

The deployment demo should be the flagship technical proof.

The demo must communicate:

"We don't just generate text.
Our assistants can operate systems."

Show:

User request
→ AI reasoning summary
→ tool execution
→ result
→ audit trail

Never expose secrets, real credentials or production infrastructure.

## LEAD GENERATION

Implement a simple lead capture flow.

Fields:

* name
* company
* work email
* company website
* business area
* biggest repetitive workflow
* preferred contact method

Do not require excessive fields.

After submission:

* validate
* persist safely
* show success state
* create a structured lead object

Make the backend implementation provider-agnostic so CRM/email integrations can be added later.

## SECURITY

Never expose:

* API keys
* OAuth secrets
* MCP credentials
* internal system prompts
* production credentials

Never put secrets in frontend code.

All external integrations must be server-side.

Add explicit permission boundaries for tools.

Destructive tools must require confirmation.

## TESTING

Every meaningful feature must have tests.

Minimum:

* unit tests
* backend integration tests
* frontend component tests where applicable
* E2E tests for critical user journeys

Critical E2E journey:

Landing page
→ assistant demo
→ workflow builder
→ lead submission

Critical MCP journey:

Assistant
→ tool selection
→ MCP call
→ result
→ audit record

Create deterministic mocks for external services.

Do not make CI depend on real production APIs.

## DOCKER

The application must run through Docker Compose.

The developer experience should be:

docker compose up --build

and the application should become available locally.

Provide:

* development mode
* test mode
* production-like mode where practical

Use health checks.

Make service dependencies explicit.

## WSL2

The preferred Windows development environment is:

Windows
→ WSL2
→ Ubuntu
→ Docker Desktop WSL2 backend
→ Docker Compose

The source repository should preferably live inside the Linux filesystem rather than /mnt/c for better performance.

## CURSOR

Create:

.cursor/
mcp.json
rules/
architecture.mdc
security.mdc
testing.mdc
product.mdc

Also create:

AGENTS.md

The rules must make Cursor behave like a persistent engineering team.

## AGENT BEHAVIOR

Before implementation:

* inspect existing code
* identify dependencies
* identify affected files
* make a plan
* implement the smallest coherent change
* run tests
* run lint/typecheck
* inspect git diff
* report what changed

Never blindly rewrite working code.

Never invent APIs.

When external APIs are involved, consult current official documentation through MCP/web tooling where possible.

## MCP SERVERS

The development environment should support:

1. Asana
2. Context7/documentation
3. filesystem/repository inspection
4. browser/E2E testing where supported
5. project-specific test automation

Use MCP only when it provides meaningful capability.

Do not add unnecessary MCP servers.

## ASANA TICKETS

Structure work around business outcomes.

First epics:

EPIC 1 — Revenue Landing
EPIC 2 — Interactive AI Demo
EPIC 3 — AI Assistant Platform
EPIC 4 — MCP Integrations
EPIC 5 — Workflow Builder
EPIC 6 — SaaS Billing
EPIC 7 — Testing & Reliability
EPIC 8 — UAE Go-To-Market

Every task should contain:

* business goal
* acceptance criteria
* technical notes
* dependencies
* test requirements

Do not create tickets such as "improve code" without measurable acceptance criteria.

## DEFINITION OF DONE

A feature is done only when:

* implemented
* tested
* typechecked
* linted
* documented
* Docker-compatible
* no secrets committed
* acceptance criteria verified
* git diff reviewed

## FIRST TASK

Do NOT immediately write code.

First:

1. inspect the entire repository
2. summarize architecture
3. identify the current product state
4. identify missing capabilities
5. propose the first 10 implementation tasks
6. rank them by impact on revenue
7. identify technical risks

Then wait for implementation approval.

When implementation starts, work in small vertical slices.

Prioritize:

REVENUE → DEMO → ASSISTANTS → MCP → SaaS → POLISH

The product must demonstrate business value before adding secondary features.

---

# 12. README.md для Windows + WSL2 + Docker + Cursor + MCP

Ниже — README, который я бы положил прямо в репозиторий как `README.md`.

# AZTEAM AI Workforce Platform

AI assistants that operate business tools.

AZTEAM is a SaaS/service platform for building and operating AI assistants that can connect to business systems, execute workflows and automate repetitive operational work.

## Business model

### AI Pilot

**30,000 ₽ / month — first 3 months**

The pilot includes:

* AI workflow audit
* initial assistant configuration
* selected integrations
* initial automation workflows
* deployment
* monitoring
* monthly optimization

### AI Operations

**100,000 ₽ / month**

After the pilot:

* multiple AI assistants
* multiple workflows
* integrations
* monitoring
* optimization
* priority support

### Custom engineering

**6,000 ₽ / hour**

Additional engineering work is performed only after approval.

---

# Architecture

```text
                       AZTEAM
                          |
             +------------+------------+
             |                         |
          Web App                   API
             |                         |
             +------------+------------+
                          |
                   Assistant Runtime
                          |
                    Tool Registry
                          |
                  +-------+-------+
                  |       |       |
                 MCP     API    Sandbox
                  |       |       |
             External  Business  Demo
              Tools    Systems
```

The core architectural principle is:

```text
Assistant
    ↓
Tool Registry
    ↓
Integration Adapter
    ↓
External System
```

Business logic must not be tightly coupled to a particular external provider.

---

# Repository structure

Expected structure:

```text
.
├── backend/
├── webapp/
├── shared/
├── tests/
├── .cursor/
│   ├── mcp.json
│   └── rules/
│       ├── architecture.mdc
│       ├── product.mdc
│       ├── security.mdc
│       └── testing.mdc
├── AGENTS.md
├── Dockerfile
├── docker-compose.yml
├── package.json
├── pnpm-workspace.yaml
└── README.md
```

The existing IdeaTalk architecture should be reused where practical.

Do not rewrite the repository without first understanding the current implementation.

---

# Windows development environment

Recommended environment:

```text
Windows 11
   ↓
WSL2
   ↓
Ubuntu
   ↓
Docker Desktop
   ↓
Docker Compose
   ↓
AZTEAM
```

Docker Desktop supports WSL2 integration and exposes Docker commands directly inside the selected WSL distribution.

Keep the source code inside the Linux filesystem for the best development performance.

Example:

```bash
mkdir -p ~/projects
cd ~/projects
git clone <repository>
cd <repository>
```

Avoid developing directly from:

```text
/mnt/c/...
```

when possible.

---

# 1. Install WSL2

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart Windows if requested.

Check:

```powershell
wsl --status
```

Check installed distributions:

```powershell
wsl -l -v
```

Ubuntu should use:

```text
VERSION 2
```

If required:

```powershell
wsl --set-version Ubuntu 2
```

---

# 2. Install Docker Desktop

Install Docker Desktop for Windows.

During setup use the WSL2 backend.

Then open:

```text
Docker Desktop
→ Settings
→ General
→ Use WSL 2 based engine
```

Enable:

```text
Settings
→ Resources
→ WSL Integration
→ Ubuntu
```

Restart Docker Desktop.

Verify from Ubuntu:

```bash
docker version
docker compose version
```

Both commands must work.

---

# 3. Install development tools in Ubuntu

Update Ubuntu:

```bash
sudo apt update
sudo apt upgrade -y
```

Install common tools:

```bash
sudo apt install -y \
  git \
  curl \
  build-essential \
  ca-certificates \
  jq
```

Install Node.js according to the project's `.nvmrc`.

If the project uses nvm:

```bash
curl -o- <NVM_INSTALLER> | bash
```

Restart the shell:

```bash
exec $SHELL
```

Then:

```bash
nvm install
nvm use
```

Install pnpm:

```bash
corepack enable
corepack prepare pnpm@latest --activate
```

Verify:

```bash
node --version
pnpm --version
```

---

# 4. Start the project

From Ubuntu:

```bash
cd ~/projects/<repository>
```

Install dependencies:

```bash
pnpm install
```

Create the environment file:

```bash
cp env.docker.example .env
```

Edit:

```bash
nano .env
```

Never commit `.env`.

Start the environment:

```bash
docker compose up --build
```

Run in background:

```bash
docker compose up -d --build
```

View logs:

```bash
docker compose logs -f
```

Stop:

```bash
docker compose down
```

---

# 5. Development workflow

Preferred workflow:

```text
Cursor on Windows
       ↓
project stored in WSL2 Ubuntu
       ↓
Docker Desktop
       ↓
Docker Compose
```

Cursor should open the WSL2 project directly.

The goal is to keep:

* source code
* node_modules
* build artifacts
* Docker development environment

inside the Linux filesystem.

---

# 6. Cursor project rules

Cursor supports project-level MCP configuration and project rules.

Create:

```text
.cursor/
├── mcp.json
└── rules/
    ├── architecture.mdc
    ├── product.mdc
    ├── security.mdc
    └── testing.mdc
```

Rules are version controlled.

## architecture.mdc

```text
---
description: AZTEAM architecture rules
alwaysApply: true
---

Follow the existing repository architecture.

Do not rewrite working modules without a clear reason.

Prefer small vertical changes.

Keep business logic independent from external integrations.

External integrations must be implemented behind adapters.

Do not put API credentials in frontend code.
```

## product.mdc

```text
---
description: Product and business requirements
alwaysApply: true
---

AZTEAM is an AI workforce SaaS.

Prioritize features that improve:

1. customer conversion
2. AI demo quality
3. assistant capabilities
4. workflow automation
5. integrations
6. reliability

Do not optimize secondary UI details before core business workflows work.

Every feature must have a measurable business outcome.
```

## security.mdc

```text
---
description: Security requirements
alwaysApply: true
---

Never commit secrets.

Never expose OAuth tokens in frontend code.

Never expose MCP credentials to the browser.

Destructive tools require explicit confirmation.

Production systems must never be used as uncontrolled demo environments.

External API calls must be server-side unless explicitly designed otherwise.
```

## testing.mdc

```text
---
description: Testing requirements
alwaysApply: true
---

Every meaningful feature must include tests.

Run:

- typecheck
- lint
- unit tests
- integration tests where relevant
- E2E tests for critical user flows

External APIs must be mocked in deterministic tests.

Do not make CI depend on live production credentials.
```

---

# 7. MCP configuration

Cursor supports MCP through:

```text
.cursor/mcp.json
```

Use project-specific configuration for AZTEAM.

Example structure:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": [
        "-y",
        "@upstash/context7-mcp"
      ]
    }
  }
}
```

Additional MCP servers should only be added when they provide meaningful capabilities.

---

# 8. Asana MCP

AZTEAM uses Asana as the project management layer.

The current Asana MCP integration uses the V2 server and Streamable HTTP.

Do not use the deprecated V1 SSE server.

The Asana MCP endpoint is configured through the environment/configuration layer and authenticated through OAuth.

Required environment variable:

```text
ASANA_MCP_URL
```

Its value must be the current official Asana MCP V2 endpoint.

Never commit OAuth secrets.

Recommended variables:

```text
ASANA_MCP_URL=
ASANA_CLIENT_ID=
ASANA_CLIENT_SECRET=
```

Keep them in:

```text
.env
```

and never in Git.

---

# 9. Asana workflow

The development process is:

```text
Business requirement
        ↓
Asana task
        ↓
Cursor Agent
        ↓
Implementation
        ↓
Automated tests
        ↓
Review
        ↓
Pull Request
        ↓
Merge
```

Every implementation task should contain:

## Business goal

Why does the feature exist?

## Acceptance criteria

What must be true when the task is complete?

## Technical notes

Important architectural constraints.

## Tests

How the feature must be verified.

---

# 10. Recommended Asana epics

## EPIC — Revenue Landing

```text
AZ-1 Hero
AZ-2 Interactive AI demo
AZ-3 Business outcomes
AZ-4 Pricing
AZ-5 Lead capture
AZ-6 UAE landing
```

## EPIC — AI Demo

```text
AZ-10 Assistant shell
AZ-11 Streaming responses
AZ-12 Tool execution timeline
AZ-13 Sandbox
AZ-14 Deployment demo
AZ-15 Demo reset
```

## EPIC — AI Assistants

```text
AZ-20 Assistant registry
AZ-21 Assistant configuration
AZ-22 Tool registry
AZ-23 Execution history
AZ-24 Permissions
```

## EPIC — MCP

```text
AZ-30 MCP adapter
AZ-31 Asana integration
AZ-32 Context7 integration
AZ-33 MCP error handling
AZ-34 MCP integration tests
```

## EPIC — Workflow Builder

```text
AZ-40 Workflow model
AZ-41 Workflow editor
AZ-42 Workflow execution
AZ-43 Workflow logs
AZ-44 Workflow testing
```

## EPIC — SaaS

```text
AZ-50 Authentication
AZ-51 Organizations
AZ-52 Subscription
AZ-53 Usage limits
AZ-54 Billing
AZ-55 Admin
```

---

# 11. Testing architecture

Tests must not depend on production services.

Use:

```text
                    E2E
                     |
              Application
                     |
          +----------+----------+
          |                     |
       Internal              Mock MCP
       services              services
```

For MCP integrations:

```text
Assistant
   ↓
Tool Registry
   ↓
Mock MCP server
   ↓
Expected result
```

This makes CI deterministic.

---

# 12. Critical E2E scenarios

## Scenario 1 — Lead generation

```text
Open landing
↓
Read value proposition
↓
Open AI demo
↓
Run demo
↓
Open contact form
↓
Submit
↓
Show success
```

## Scenario 2 — AI assistant

```text
Open assistant
↓
Enter request
↓
Assistant plans action
↓
Tool execution appears
↓
Result appears
↓
Execution is stored
```

## Scenario 3 — Workflow

```text
Open workflow builder
↓
Describe automation
↓
AI generates workflow
↓
Review workflow
↓
Run test
↓
See execution result
```

## Scenario 4 — Asana

```text
Connect Asana
↓
Authorize
↓
Select project
↓
Read tasks
↓
AI analyzes tasks
↓
AI creates approved task
↓
Audit event stored
```

---

# 13. AI safety

AI assistants are allowed to:

* read
* analyze
* summarize
* recommend
* create draft actions

Sensitive/destructive actions require confirmation.

Examples:

```text
DELETE
DEPLOY PRODUCTION
SEND CUSTOMER EMAIL
CHANGE BILLING
MODIFY ACCESS
```

must not happen silently.

The UI should show:

```text
The assistant wants to:

Create Asana task
Project: Sales
Assignee: John
Due date: Friday

[Approve]
[Cancel]
```

---

# 14. Production principles

Never assume that an LLM is deterministic.

All important actions must have:

* validation
* permissions
* audit logs
* retries
* timeout
* error handling
* human confirmation where required

AI output must never be trusted as an authorization mechanism.

---

# 15. Definition of Done

A task is complete only when:

```text
[ ] Code implemented
[ ] Unit tests pass
[ ] Integration tests pass
[ ] E2E tests pass where applicable
[ ] Typecheck passes
[ ] Lint passes
[ ] Docker build passes
[ ] Docker Compose starts
[ ] No secrets committed
[ ] Acceptance criteria verified
[ ] Git diff reviewed
[ ] Documentation updated
```

---

# 16. Daily AI development loop

Use the following workflow:

```text
1. Select Asana task
        ↓
2. Ask Cursor to inspect repository
        ↓
3. Cursor creates implementation plan
        ↓
4. Review plan
        ↓
5. Cursor implements
        ↓
6. Run tests
        ↓
7. Run E2E
        ↓
8. Review diff
        ↓
9. Create commit
        ↓
10. Update Asana
```

Never ask an AI agent to "build the whole application" in one step.

Use small vertical slices.

---

# 17. Product priority

Always prioritize in this order:

```text
1. Revenue
2. Interactive demo
3. AI assistants
4. Workflow automation
5. MCP integrations
6. SaaS infrastructure
7. Analytics
8. Visual polish
```

A beautiful landing page without a convincing working demo is not enough.

The central product proof is:

```text
USER
  ↓
AI ASSISTANT
  ↓
REAL TOOL
  ↓
REAL ACTION
  ↓
AUDITABLE RESULT
```

That is the core AZTEAM product.

---

## Важный технический нюанс по MCP

Я бы **не копировал буквально старые инструкции из блогов**, где Asana подключается через `https://mcp.asana.com/sse`. У Asana V1 Beta уже deprecated; актуальный V2 использует `https://mcp.asana.com/v2/mcp`, Streamable HTTP и OAuth. ([Asana Docs][3])

Для Cursor это хорошо ложится на текущую модель MCP: workspace-level `.cursor/mcp.json`, переменные окружения и remote HTTP servers поддерживаются непосредственно Cursor. ([Cursor][4])

И ещё один важный момент: Cursor сейчас поддерживает не только MCP, но и **Rules, Skills, Subagents, Commands и Hooks**. Поэтому для того, чтобы приблизиться к developer experience уровня Replit, я бы постепенно строил не просто `.cursor/mcp.json`, а целый **AZTEAM Engineering Agent Layer**: правила → специализированные агенты → MCP → тестовые hooks → Asana. ([Cursor][5])

### В итоге

Я бы строил azteam.me вокруг одного доказательства:

> **“Give us one repetitive business workflow. In the demo, we will show an AI assistant actually operating the tools instead of merely talking about them.”**

Это значительно сильнее продаёт чек **30k → 100k ₽/мес**, чем обычное портфолио с 20 карточками проектов.

А `IdeaTalk` становится не самим продуктом, а **технологическим ядром AI Workforce Platform**. ([GitHub][2])

Для UAE я бы уже на первой версии сайта сделал отдельный `/uae` landing и английский copy, а основной `/` оставил как product/engineering proof.

[1]: https://ru.linkedin.com/in/basovi?utm_source=chatgpt.com "Iurii B. – Sberbank | LinkedIn"
[2]: https://github.com/novator24/ideatalk "GitHub - novator24/ideatalk: AI bots store · GitHub"
[3]: https://developers.asana.com/docs/integrating-with-asanas-mcp-server?utm_source=chatgpt.com "Integrating with Asana's MCP Server"
[4]: https://prod.cursor.com/docs/mcp?utm_source=chatgpt.com "Model Context Protocol (MCP) | Cursor Docs"
[5]: https://prod.cursor.com/docs/customize-cursor?utm_source=chatgpt.com "Overview | Cursor Docs"
