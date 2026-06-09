# CodeShua Goal Mode Product Guidance

Last reviewed: 2026-06-09

## Purpose

This file is the next-run instruction for Codex goal mode. It exists because the repository has many completed micro tasks, but the product still does not feel like the intended CodeShua experience.

The next goal-mode run must stop optimizing for task count and start optimizing for a user-visible product loop.

## Current Repository Reading

Read these files before doing anything else:

1. `AGENTS.md`
2. `README.md`
3. `HANDOFF.md`
4. `TASK_LEDGER.md`
5. `docs/codex-goal-project-split-guide.md`
6. This file: `docs/product/codeshua-goal-mode-product-guidance.md`

The important current facts are:

- `AGENTS.md` says this is a multi-project workbench and every task must declare exactly one lane.
- `AGENTS.md` also says the active git workspace/publish mirror is `CodeShua-publish`; do not rewind to stale sibling snapshots.
- `README.md` says the current scope already includes Android import, problem list/detail, favorites, mastery/review counts, CodeShua-focused entry copy, AI explanations, AxonHub gateway path, Daily Coding Brief generation, 今日题单, and the content production pipeline.
- `HANDOFF.md` shows the latest work has reached Task 303, including many content-bank expansions and DeepSeek/gateway-related utility work.
- The product problem is not absence of work. The product problem is that many tasks are too fine-grained and do not necessarily add up to a satisfying mobile刷题 loop.

## Diagnosis

The project currently has strong engineering discipline but weak product acceptance.

Good parts:

- Baseline-first and evidence-first rules exist.
- Lanes exist and prevent mixing mobile, blog, gateway, DailyBrief, Pi, and references.
- There are many original programming problems.
- There are deterministic verifier scripts.
- Secrets are treated carefully.

Main failure mode:

- A task can pass scripts while the user experience still feels unfinished.
- Too many tasks are micro-level: labels, accessibility text, count cues, clamps, one more problem, one more verifier, one more env helper.
- The repo reads like an implementation ledger, not like a product with a crisp V1.
- CodeShua Mobile, Blog, AI Gateway, DailyBrief, and tooling all exist, but the next goal-mode run must make one product lane feel complete before continuing auxiliary lanes.

## Product North Star

The primary product is:

> CodeShua: a mobile-first programming practice app where the user can open the phone, see what to solve today, read a LeetCode-style original problem, get structured AI explanation, mark mastery, and return later for weak-point review.

The first good version is not a full online judge.

The first good version is a complete local learning loop:

1. Open App.
2. Enter CodeShua without confusion from old Pei-Pei-Shua / civil-service exam identity.
3. See 今日题单.
4. Open one problem.
5. Read title, difficulty, tags, statement, examples, constraints, hints, and reference explanation.
6. Ask for AI 讲解.
7. Mark the problem as 掌握 / 模糊 / 不会 / 需要复习.
8. Return to a review or weak-point page and see the consequence of that action.
9. Repeat tomorrow with a clear daily/review path.

## Immediate Rule Change For Goal Mode

For the next run, do not continue the old pattern of tiny tasks.

Do not start with:

- another single problem addition,
- another single label/accessibility/count cue,
- another gateway helper,
- another Pi package note,
- another deployment/DNS/server task,
- another DeepSeek generation enhancement.

Start with a product acceptance audit.

## Next Task

### Task 304: CodeShua Mobile V1 Product Acceptance Audit

Lane: `codeshua-mobile`

This task must be read-only except for product documentation and log updates. It must not implement Android features yet.

Goal:

Create a product acceptance baseline that tells us exactly why the mobile app still does not feel good, then define the smallest follow-up tasks that will make it good.

Required output files:

1. `docs/product/codeshua-mobile-v1-acceptance.md`
2. `docs/product/codeshua-mobile-v1-gap-audit.md`

Allowed changes:

- Product docs under `docs/product/`.
- Log updates in `TASK_LEDGER.md`, `VERIFICATION_LOG.md`, `DECISION_LOG.md`, `HANDOFF.md`.
- Lightweight verifier only if necessary to prove the docs exist and contain required sections.

Forbidden changes in Task 304:

- No Android source edits.
- No content-bank problem additions.
- No DailyBrief regeneration.
- No Blog/Yunyu changes.
- No AI gateway changes.
- No Pi package install or config.
- No live deployment, DNS, server, database, or secret handling.

### Required contents of `codeshua-mobile-v1-acceptance.md`

It must define the mobile V1 in user-facing terms:

1. Target user.
2. Product promise.
3. 10-minute demo script.
4. Required screens.
5. Required user actions.
6. Required content quality bar.
7. Required AI explanation quality bar.
8. Required review/weak-point loop.
9. Non-goals.
10. Acceptance checklist.

Use this acceptance checklist as the minimum:

| Area | V1 acceptance |
| --- | --- |
| Identity | App entry and primary flow say CodeShua / programming practice, not civil-service exam first. |
| Today | User can see a 今日题单 with problem count, estimated time, and clear start path. |
| Problem Detail | Detail page has title, difficulty, tags, statement, examples, constraints, hints, and solution/explanation sections. |
| AI Explanation | AI output is structured as restatement, brute force, insight, solution, code, complexity, edge cases, mistakes, review questions. |
| State | User can mark mastery/review state from the problem experience. |
| Review | User can find not-mastered or review-needed problems later. |
| Local-first | V1 works with local bundled content and mock/no-key AI fallback. |
| Demo | A human can complete the demo without reading developer docs. |

### Required contents of `codeshua-mobile-v1-gap-audit.md`

It must compare the current app/repo to the acceptance checklist.

Use this table:

| Acceptance item | Current evidence | Gap | Severity | Follow-up task |
| --- | --- | --- | --- | --- |

Severity values:

- `P0`: blocks the V1 demo.
- `P1`: hurts the experience but does not block the demo.
- `P2`: polish after the V1 loop works.

Follow-up tasks must be product-sized, not micro-sized.

Good follow-up task examples:

- `Task 305: CodeShua Mobile Home And Today Entry Cleanup`
- `Task 306: Problem Detail Learning Layout Pass`
- `Task 307: AI Explanation Quality Contract`
- `Task 308: Mastery And Review Loop UX Pass`
- `Task 309: V1 Demo APK And Smoke Script`

Bad follow-up task examples:

- `Task 305: rename one label`
- `Task 306: add one accessibility sentence`
- `Task 307: add one more verifier`
- `Task 308: add one more sample problem`

## Task 305-309 Recommended Roadmap

Only execute these after Task 304 finishes and logs are updated.

### Task 305: CodeShua Mobile Home And Today Entry Cleanup

Lane: `codeshua-mobile`

Goal:

Make the app entry feel like CodeShua, not a repurposed civil-service helper.

Acceptance:

- The main entry path to programming practice is obvious.
- 今日题单 is reachable in one or two taps.
- Old Pei-Pei-Shua / 公务员 / 行测 concepts do not dominate the CodeShua flow.
- No blog/gateway/Pi/content generation changes.

### Task 306: Problem Detail Learning Layout Pass

Lane: `codeshua-mobile`

Goal:

Make one problem detail page feel like a mobile LeetCode-style learning page.

Acceptance:

- The page clearly shows statement, examples, constraints, hints, solution, complexity, edge cases.
- The layout is readable on a phone.
- It is obvious what to do next: think, view hint, ask AI, mark state, review later.

### Task 307: AI Explanation Quality Contract

Lane: `codeshua-mobile`

Goal:

Make AI 讲解 predictable and useful.

Acceptance:

- The prompt/output contract requires: restatement, brute force, key insight, algorithm, code, complexity, edge cases, common mistakes, review questions.
- If no key is configured, mock/local preview still follows the same structure.
- Verification checks structure, not just existence of a response.

### Task 308: Mastery And Review Loop UX Pass

Lane: `codeshua-mobile`

Goal:

Make state changes visible and meaningful.

Acceptance:

- User can mark 掌握 / 模糊 / 不会 / 需要复习 or an equivalent small state set.
- Review-needed items can be found later.
- Weak-point recap uses actual state, tags, and recent review behavior.
- The loop is clear without reading logs.

### Task 309: V1 Demo APK And Smoke Script

Lane: `codeshua-mobile`

Goal:

Produce a demoable mobile V1 handoff.

Acceptance:

- Build or clearly record the exact blocker.
- Produce/update APK handoff artifact if build passes.
- Write a 10-minute demo script.
- Smoke script follows the V1 path: open, today, detail, AI, mark, review.

## Product Acceptance Evidence

Every `codeshua-mobile` task after Task 304 must include a new section in its completion report:

```markdown
## Product Acceptance Evidence

- User entry:
- User action:
- Screen/result:
- Why this is better:
- Demo impact:
- Remaining friction:
```

A task is not done if it only says scripts pass. It must explain the user-visible improvement.

## Stop Conditions

Stop and report instead of continuing if any of these happen:

- The task starts touching more than one lane.
- Android changes require blog/gateway/Pi/server edits.
- A verifier passes but the user path is still unclear.
- The next planned task is smaller than a user-visible improvement.
- A secret, DNS, live server, or production credential is required.
- The app cannot be built and the blocker has not been isolated.

## What Not To Optimize Yet

Until the V1 mobile loop works, deprioritize:

- More content-bank volume beyond the current baseline.
- DeepSeek live generation improvements.
- AxonHub real-provider work.
- Pi package experiments.
- Blog publishing improvements.
- DNS / server deployment / TLS / backup tasks.
- Accessibility micro-polish unless it is part of a full screen UX pass.

These are useful later, but not the current bottleneck.

## Goal Mode Prompt

Paste this into Codex goal mode:

```text
Read AGENTS.md, README.md, HANDOFF.md, TASK_LEDGER.md, docs/codex-goal-project-split-guide.md, and docs/product/codeshua-goal-mode-product-guidance.md.

The project has enough micro-task completion. The next goal is product quality, not task count.

Start with Task 304: CodeShua Mobile V1 Product Acceptance Audit.
Lane: codeshua-mobile only.

Do not edit Android source, content-bank problems, DailyBrief outputs, Yunyu blog, AI gateway, Pi config, live deployment, DNS, or secrets in Task 304.

Create docs/product/codeshua-mobile-v1-acceptance.md and docs/product/codeshua-mobile-v1-gap-audit.md. Define the V1 mobile刷题 acceptance checklist and audit the current app/repo against it. Then update TASK_LEDGER.md, VERIFICATION_LOG.md, DECISION_LOG.md, and HANDOFF.md. If you add a verifier, keep it lightweight and doc-only.

After Task 304, propose product-sized follow-up tasks only: home/today entry cleanup, problem detail learning layout, AI explanation quality contract, mastery/review loop UX, and V1 demo APK/smoke. Do not create micro tasks for one label, one count, one accessibility string, or one extra problem.
```

## Final Reminder

The goal is not to prove that Codex did many tasks.

The goal is to make a person open the phone and say:

> This is clearly a programming-practice app. I know what to solve today, I can learn from the explanation, and I know what to review next.
