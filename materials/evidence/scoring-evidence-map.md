# Shike Scoring Evidence Map

Status: local evidence mapped; user-research and cloud-device strict evidence
remain `待采集`.

This file translates the product-manager review guide into a scoring evidence
map for the contest narrative. It must not contain AppKEY, backend tokens, real
personal data, raw screenshots, full OCR text, or fabricated interview results.

## Score Dimensions

| Dimension | Weight | Current Evidence | Gap | Gate |
|---|---:|---|---|---|
| Innovation | 40% | Confirmation-first flow, action planner, inbox tracking, competitor differentiation | Real cloud-device videos still missing | `DEMO_ACCEPTANCE_METRIC 18/18` |
| Application value | 30% | Synthetic scenarios, user research plan, interview summary template, bounded value claim | Real interviews and survey metrics are 待采集 | `USER_RESEARCH_EVIDENCE_METRIC 8/8` |
| Completion | 20% | Android APK, FastAPI backend, SQLite inbox, release evidence index, cloud-device prep package, backend audit log boundary, no-default-image-upload boundary, Android image preprocessing boundary | 9 cloud-device MP4 files, filled report, non-placeholder logcat | `LANDING_RELEASE_CANDIDATE_METRIC 63/63`; `BACKEND_AUDIT_LOG_METRIC 8/8`; `ANDROID_IMAGE_PREPROCESS_METRIC 15/15` |
| Model ability | 10% | BlueLM adapter, vivo OCR adapter, schema validation, redacted live smoke, 110-case eval | Strict cloud-device proof must show HTTPS backend and BlueLM route | `BLUELM_ADAPTER_METRIC 8/8`; `VIVO_OCR_ADAPTER_METRIC 11/11` |

## Evidence Chain

| Claim | Evidence File | What It Proves | What It Does Not Prove |
|---|---|---|---|
| Shike is not just OCR | `docs/delivery-boundary-and-scoring.md` | OCR-to-action differentiation and score mapping | Real user adoption |
| Shike can call model services safely | `docs/bluelm-integration-runbook.md` and `materials/evidence/cloud-device/backend-redacted-access-log.txt` | Server-side BlueLM/OCR boundaries and redacted live smoke | Android-side model credentials |
| Shike has a release handoff package | `materials/evidence/release-evidence-index.md` | Local gates, rebuild commands, strict blocker boundary | Completed cloud-device strict release |
| Shike has an application-value research plan | `docs/user-research-plan.md` | Sampling, questions, privacy boundaries, completion criteria | Collected interview results |
| Shike has no fabricated user evidence | `docs/user-interview-summary.md` | Results are clearly marked planned / 待采集 | Real aggregate metrics |
| Shike can answer scoring questions | `materials/preliminary-deck.md` and `materials/demo-script.md` | Deck/script point to evidence and blockers | Real judge feedback |

## User Research Boundary

Do not fabricate interview data. The only allowed current user-research claim is:

```text
User research is planned and instrumented; collected findings are 待采集.
```

The following claims are blocked until real fieldwork exists:

- target users confirmed the pain frequency,
- target users accepted the UX,
- target users preferred the privacy settings,
- target users reduced missed actions after using Shike.

## Required Rebuild Commands

```bash
python3 shike/validation/validate_user_research_evidence.py
python3 shike/validation/validate_requirement_matrix.py
python3 shike/validation/validate_release_evidence_index.py
```
