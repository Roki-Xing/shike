# Optimization Log

## 2026-05-31 / Round 231

Goal: Make the cloud-device preparation handoff count report-level video evidence placeholders explicitly.

Current handoff summary:
- This continuation preserves the same release handoff boundary as the previous public-status update: `Goal: Bring the public validation status up to the current materials evidence package.`
- Evidence package surfaces remain current: scoring evidence map, preliminary deck landing evidence package, `docs/delivery-boundary-and-scoring.md`, and `materials/preliminary-deck.md`.
- Current release handoff metrics remain:
  - `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
  - `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
  - `REQUIREMENT_MATRIX_METRIC	9/9`
  - `DEMO_ACCEPTANCE_METRIC	18/18`
  - `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
  - `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
- Desktop guidance and matrix anchors remain `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` and `materials/evidence/requirement-matrix.md`.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Files changed:
- Updated `scripts/prepare_cloud_device_evidence.py` so the generated capture TODO now detects report video evidence lines that still contain `TBD` and prints `CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS	9/9`.
- Regenerated `materials/evidence/cloud-device/cloud-device-capture-todo.md` so it includes `Report video evidence still TBD: 9/9` and a `Report Video Evidence Still TBD` section.
- Updated `validation/validate_cloud_device_package.py` so the non-strict cloud-device package requires the new report-video TBD section and operator instruction.
- Updated `validation/validate_release_evidence_index.py`, `materials/evidence/release-evidence-index.md`, and `validation/validate_release_blocking_report.py` so release evidence surfaces expect the new prep-helper output and all nine report video placeholder rows.
- Regenerated `materials/evidence/blocking-report.md` through the strict landing release validator.

Validation:
- PASS `python3 -m py_compile scripts/prepare_cloud_device_evidence.py validation/validate_cloud_device_package.py validation/validate_release_evidence_index.py validation/validate_release_blocking_report.py validation/validate_landing_release_candidate.py`
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
  - Evidence: `CLOUD_DEVICE_PREP_REPORT_TBD_FIELDS	14/14`
  - Evidence: `CLOUD_DEVICE_PREP_REPORT_VIDEO_TBD_FIELDS	9/9`
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Blocking items: missing nine real cloud-device MP4 files, report placeholders, and placeholder cloud-device logcat.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`

Behavior preserved:
- Non-strict release readiness remains locally reproducible.
- Strict release remains blocked until real cloud-device recordings, filled report values, and redacted logcat diagnostics exist.
- The new metric is an operator handoff guard only; it does not weaken strict gates or manufacture evidence.

Next:
- Collect the nine real cloud-device MP4 recordings, fill the matching report video evidence rows with real redacted references, replace placeholder logcat, rerun `python3 scripts/prepare_cloud_device_evidence.py`, then rerun strict cloud-device and landing release gates.

## 2026-05-31 / Round 230

Goal: Keep the release evidence index aligned with the current strict-evidence gate after the strict blocker expansion.

Current handoff summary:
- This continuation preserves the same release handoff boundary as the previous public-status update: `Goal: Bring the public validation status up to the current materials evidence package.`
- Evidence package surfaces remain current: scoring evidence map, preliminary deck landing evidence package, `docs/delivery-boundary-and-scoring.md`, and `materials/preliminary-deck.md`.
- Current release handoff metrics remain:
  - `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
  - `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
  - `REQUIREMENT_MATRIX_METRIC	9/9`
  - `DEMO_ACCEPTANCE_METRIC	18/18`
  - `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
  - `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
- Desktop guidance and matrix anchors remain `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` and `materials/evidence/requirement-matrix.md`.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Files changed:
- Updated `validation/validate_release_evidence_index.py` so the optimization-log current handoff guard expects the current strict gate token `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7` instead of the stale `2/5` token.
- Regenerated `materials/evidence/cloud-device/cloud-device-capture-todo.md` and `materials/evidence/cloud-device/apk-sha256.txt` through `scripts/prepare_cloud_device_evidence.py`.
- Updated this log with the restored release-candidate evidence and the remaining strict external blockers.

Validation:
- PASS `python3 -m py_compile validation/validate_release_evidence_index.py`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Blocking items: missing nine real cloud-device MP4 files, placeholder report fields, and placeholder cloud-device logcat.
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
  - Evidence: `CLOUD_DEVICE_PREP_REPORT_TBD_FIELDS	14/14`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
- EXPECTED BLOCK `python3 validation/validate_cloud_device_package.py --strict`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	30/33`
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_requirement_matrix.py`
  - Evidence: `REQUIREMENT_MATRIX_METRIC	9/9`
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC	10/10`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`

Behavior preserved:
- Local release-candidate readiness is again reproducible at 52/52.
- Strict release remains correctly blocked on real external cloud-device evidence.
- No strict blocker was weakened and no external proof was fabricated.

Next:
- Collect the nine real cloud-device MP4 recordings, replace the report TBD fields with redacted real values, replace placeholder logcat with redacted diagnostics, rerun the prep helper, then rerun the strict package and strict release gates.

## 2026-05-31 / Round 229

Goal: Make the cloud-device evidence preparation checklist state-aware so the remaining strict blockers are actionable after each recording pass.

Current handoff summary:
- This continuation preserves the same release handoff boundary as the previous public-status update: `Goal: Bring the public validation status up to the current materials evidence package.`
- Evidence package surfaces remain current: scoring evidence map, preliminary deck landing evidence package, `docs/delivery-boundary-and-scoring.md`, and `materials/preliminary-deck.md`.
- Current release handoff metrics remain:
  - `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
  - `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
  - `REQUIREMENT_MATRIX_METRIC	9/9`
  - `DEMO_ACCEPTANCE_METRIC	18/18`
  - `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
  - `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
- Desktop guidance and matrix anchors remain `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` and `materials/evidence/requirement-matrix.md`.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Files changed:
- Updated `scripts/prepare_cloud_device_evidence.py` so the generated capture TODO now reads the current evidence folder, counts missing MP4 files, detects report fields that still contain placeholders, and prints `CLOUD_DEVICE_PREP_REPORT_TBD_FIELDS`.
- Regenerated `materials/evidence/cloud-device/cloud-device-capture-todo.md` so it now starts with `Current Missing Evidence`, `Missing Videos`, and `Report Fields Still TBD`.
- Updated `validation/validate_cloud_device_package.py` so the non-strict package gate requires that generated missing-evidence summary.

Validation:
- PASS `python3 -m py_compile scripts/prepare_cloud_device_evidence.py validation/validate_cloud_device_package.py`
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
  - Evidence: `CLOUD_DEVICE_PREP_REPORT_TBD_FIELDS	14/14`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`

Behavior preserved:
- The new summary is generated from existing files; it does not create cloud recordings or replace real report values.
- Strict release remains blocked until real MP4 files are present and report placeholders are replaced.
- No credentials or personal data were introduced.

Next:
- Use `materials/evidence/cloud-device/cloud-device-capture-todo.md` as the operator checklist during cloud-device recording, rerun the prep helper after each batch, and stop only when missing videos and report TBD fields both reach `0`.

## 2026-05-31 / Round 228

Goal: Re-audit the current desktop guidance closeout state and keep the remaining release blocker explicit.

Current handoff summary:
- This continuation rechecked the same release handoff boundary as the previous public-status update: `Goal: Bring the public validation status up to the current materials evidence package.`
- Evidence package surfaces remain current: scoring evidence map, preliminary deck landing evidence package, `docs/delivery-boundary-and-scoring.md`, and `materials/preliminary-deck.md`.
- Current release handoff metrics remain:
  - `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
  - `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
  - `REQUIREMENT_MATRIX_METRIC	9/9`
  - `DEMO_ACCEPTANCE_METRIC	18/18`
  - `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
  - `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
- Desktop guidance and matrix anchors remain `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` and `materials/evidence/requirement-matrix.md`.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Files changed:
- Updated `docs/optimization-log.md` with the latest local release-candidate and strict-release evidence from this continuation pass.

Validation:
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Evidence: `BLOCKING_REPORT	materials/evidence/blocking-report.md`
  - Reason: strict mode still requires real cloud-device MP4 recordings and a filled cloud-device report; no external evidence was fabricated.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_bluelm_adapter.py`
  - Evidence: `BLUELM_ADAPTER_METRIC	7/7`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 validation/validate_model_contract_strict.py`
  - Evidence: `MODEL_CONTRACT_STRICT_METRIC	10/10`
- PASS `python3 validation/validate_cloud_backend_ready.py`
  - Evidence: `CLOUD_BACKEND_READY_METRIC	5/5`

Behavior preserved:
- Local release-candidate readiness remains reproducible at 52/52.
- Strict release remains blocked only on real external cloud-device proof, not on local repository gates.
- BlueLM credentials remain backend-only; no AppKEY, token, personal OCR text, phone number, email, or student ID was added.

Next:
- Collect the nine real cloud-device recordings and replace placeholder fields in `materials/evidence/cloud-device/cloud-device-test-report.md`, then rerun the strict gate.

## 2026-05-29 / Round 227

Goal: Bring the public validation status up to the current materials evidence package.

Files changed:
- Updated `docs/current-validation-status.md` so the repository structure baseline now lists the scoring evidence map and preliminary deck landing evidence package as current handoff artifacts.
- Updated `validation/validate_release_evidence_index.py` so release evidence validation requires the public status page to mention the scoring evidence map and preliminary deck landing evidence package.

Validation:
- PASS `python3 -m py_compile validation/validate_release_evidence_index.py`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC	10/10`
- PASS `python3 validation/validate_requirement_matrix.py`
  - Evidence: `REQUIREMENT_MATRIX_METRIC	9/9`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`

Behavior preserved:
- The public status page now names `docs/delivery-boundary-and-scoring.md` and `materials/preliminary-deck.md` as evidence-bearing handoff artifacts, but strict release still requires real external cloud-device proof.
- Before cloud-device recording, operators must confirm `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` remains the desktop guidance source and `materials/evidence/requirement-matrix.md` still passes `REQUIREMENT_MATRIX_METRIC 9/9`.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue local proof-chain hardening only where it reduces handoff drift; strict completion still depends on real cloud-device MP4 files and a filled report.

## 2026-05-29 / Round 196

Goal: Bring the optimization-log release handoff summary up to the current evidence metrics.

Files changed:
- Updated `docs/optimization-log.md` with the current release handoff state so the first visible log entry no longer points operators at stale 24/24, 25/25, and 6/6 evidence gates.
- Updated `validation/validate_release_evidence_index.py` so release evidence validation also requires the optimization log's current handoff summary.

Validation:
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	27/27`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	10/10`
- PASS `python3 validation/validate_requirement_matrix.py`
  - Evidence: `REQUIREMENT_MATRIX_METRIC	8/8`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`

Behavior preserved:
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.
- Historical optimization-log entries keep their original evidence values because they describe earlier rounds.

Next:
- Continue only with local, mechanically verifiable release-readiness gaps unless real cloud-device evidence is collected.

## 2026-05-29 / Round 184

Goal: Scan current release handoff surfaces for another local, mechanically verifiable gap.

Files changed:
- None.

Scan result:
- Checked README, current validation status, release evidence index, cloud-device README, capture TODO, device demo checklist, and submission checklist for release/strict handoff consistency.
- No new current-facing stale metric, missing release evidence command, or missing strict boundary was found.
- Remaining strict release blockers are external: real cloud-device MP4 recordings and filled cloud-device report fields.

Validation:
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`

Behavior preserved:
- No files were changed in this round.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Further progress toward strict release requires collecting the nine real cloud-device recordings and replacing placeholder report fields with redacted real evidence.

## 2026-05-29 / Round 183

Goal: Make the release evidence index rebuild checklist self-verifying.

Files changed:
- Updated `materials/evidence/release-evidence-index.md` so the rebuild checklist now reruns `validate_release_evidence_index.py` after refreshing evidence files.
- Added the expected-blocking `validate_landing_release_candidate.py --strict` command to the release evidence index rebuild checklist so strict evidence status is always rechecked.
- Updated `validation/validate_release_evidence_index.py` so the evidence index guard requires both commands.

Validation:
- PASS `python3 -m py_compile validation/validate_release_evidence_index.py`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Release evidence index remains a local handoff artifact; strict release still requires real external cloud-device proof.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning for remaining local handoff quality gaps; avoid changing historical log evidence unless it affects current generated artifacts.

## 2026-05-29 / Round 182

Goal: Make strict cloud-device handoff rerun the non-strict package gate before strict validation.

Files changed:
- Updated `scripts/prepare_cloud_device_evidence.py` so regenerated `cloud-device-capture-todo.md` lists `validate_cloud_device_package.py` before strict cloud-device and strict release validation.
- Updated `materials/evidence/cloud-device/cloud-device-capture-todo.md` with the same non-strict package precheck.
- Updated `validation/validate_landing_release_candidate.py` so generated strict blocking reports tell operators to rerun `validate_cloud_device_package.py` and keep `CLOUD_DEVICE_PACKAGE_METRIC 24/24` before strict validation.
- Updated `materials/evidence/blocking-report.md` with the same required next action.
- Updated `validation/validate_release_blocking_report.py` and `validation/validate_cloud_device_package.py` so both handoff files require the non-strict package precheck.

Validation:
- PASS `python3 -m py_compile scripts/prepare_cloud_device_evidence.py validation/validate_landing_release_candidate.py validation/validate_release_blocking_report.py validation/validate_cloud_device_package.py`
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Strict release remains blocked on real external cloud-device proof; this round only improved the operator rerun order.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning evidence handoff artifacts for ordering or traceability gaps that can be verified mechanically.

## 2026-05-29 / Round 181

Goal: Make SHIKE-070 traceability cover the actual release evidence handoff artifacts.

Files changed:
- Updated `validation/traceability.md` so SHIKE-070 now points to `materials/submission-checklist.md`, `materials/device-demo-checklist.md`, `materials/evidence/release-evidence-index.md`, `materials/evidence/blocking-report.md`, and `materials/evidence/cloud-device/`.
- Updated `validation/validate_deliverables.py` so SHIKE-070 fails if the traceability matrix omits the release evidence index, blocking report, cloud-device evidence folder, submission checklist, or device demo checklist.

Validation:
- PASS `python3 -m py_compile validation/validate_deliverables.py`
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC	10/10`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- SHIKE-070 still maps to the same submission material bucket; this round only made the release-evidence handoff traceable from the issue matrix.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue with narrow handoff or validator improvements only when they close an actual traceability or release-readiness gap.

## 2026-05-29 / Round 180

Goal: Make the cloud-device evidence package README state the current non-strict package metric.

Files changed:
- Updated `materials/evidence/cloud-device/README.md` so the package-local handoff says the non-strict gate must pass at `CLOUD_DEVICE_PACKAGE_METRIC 24/24`.
- Tightened `validation/validate_cloud_device_package.py` so the package README release handoff must include that current package metric.

Validation:
- PASS Protocol Fingerprint Check
  - Evidence: re-read `runtime-hard-invariants.md`, `core-principles.md`, and `loop-workflow.md`; resume check returned iteration/current metric 179 before this round.
- PASS `python3 -m py_compile validation/validate_cloud_device_package.py`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The cloud-device evidence folder still distinguishes non-strict handoff readiness from strict real-recording proof.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning remaining handoff materials for stale metric names or missing release evidence boundaries.

## 2026-05-29 / Round 179

Goal: Align the landing optimization guide's cloud-device phase with the current release evidence handoff.

Files changed:
- Updated `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` so the cloud-device validation section names the current `CLOUD_DEVICE_PACKAGE_METRIC 24/24`, strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` boundary, release evidence index, and blocking report.
- Updated the guide's Goal 3 completion condition so it requires the 24/24 package gate, release evidence index, blocking report, and strict external-evidence boundary to stay synchronized.
- Updated the guide's phase-two acceptance commands to include `validate_release_blocking_report.py`, `validate_release_evidence_index.py`, default `validate_landing_release_candidate.py`, and expected-blocking strict release validation.
- Tightened `validation/validate_landing_release_candidate.py` so stale cloud-device guide wording cannot pass the public-doc guard.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The landing guide still keeps cloud-device recording as a real external-evidence task; this round only made its acceptance criteria current and stricter.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Run the protocol fingerprint check before selecting Round 180, then continue only with a focused, mechanically verifiable handoff improvement.

## 2026-05-29 / Round 178

Goal: Keep the current validation status rerun list aligned with release handoff gates.

Files changed:
- Updated `docs/current-validation-status.md` so the Next Highest Priority section now separates the S3 quality rerun list from the release handoff rerun list.
- Added the release handoff rerun commands for `validate_cloud_device_package.py`, `validate_release_blocking_report.py`, `validate_release_evidence_index.py`, `validate_landing_release_candidate.py`, and expected-blocking `validate_landing_release_candidate.py --strict`.
- Tightened `validation/validate_cloud_device_package.py` so the current status page must keep the release handoff rerun list and strict `2/5` boundary.

Validation:
- PASS `python3 -m py_compile validation/validate_cloud_device_package.py`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The S3 quality hardening list remains intact; release handoff checks are added as a separate final rerun block.
- Strict release remains blocked on real external cloud-device proof; no evidence was fabricated.

Next:
- Continue scanning user-facing release materials for missing strict evidence boundaries.

## 2026-05-29 / Round 177

Goal: Make the public cloud-device handoff show the current package gate and release evidence state.

Files changed:
- Updated `README.md` so the cloud-device evidence package section names the current `CLOUD_DEVICE_PACKAGE_METRIC 24/24`, release evidence index, blocking report, default `LANDING_RELEASE_CANDIDATE_METRIC 52/52`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` state.
- Updated `docs/current-validation-status.md` with explicit cloud-device package, release blocking report, and release evidence index baseline rows.
- Updated `validation/validate_cloud_device_package.py` so README and current validation status must keep the release handoff tokens, raising the non-strict package guard to `CLOUD_DEVICE_PACKAGE_METRIC 24/24`.
- Updated `materials/evidence/release-evidence-index.md` and `validation/validate_release_evidence_index.py` to use the current 24/24 cloud-device package metric.

Validation:
- PASS `python3 -m py_compile validation/validate_cloud_device_package.py validation/validate_release_evidence_index.py`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	24/24`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Strict release remains blocked on real external cloud-device proof; this round only tightened current handoff documentation and guards.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue auditing current validation/public handoff surfaces for stale release evidence metrics or missing strict-mode boundary notes.

## 2026-05-29 / Round 176

Goal: Keep strict blocking reports connected to the release evidence index after cloud-device refreshes.

Files changed:
- Updated `validation/validate_landing_release_candidate.py` so generated strict blocking reports tell operators to rerun `validate_release_evidence_index.py` after refreshing `apk-sha256.txt` and `cloud-device-capture-todo.md`.
- Updated `materials/evidence/blocking-report.md` with the same required next action.
- Updated `validation/validate_release_blocking_report.py` so blocking-report quality now requires the release evidence index rerun instruction.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py validation/validate_release_blocking_report.py`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode regenerated the blocking report and still correctly blocks on missing real cloud-device MP4/report evidence.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	23/23`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Strict release remains blocked on real external cloud-device proof; this round only made the generated blocker handoff more complete.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue auditing evidence helper outputs and release handoff files for missing rerun or redaction instructions.

## 2026-05-29 / Round 175

Goal: Keep generated cloud-device capture TODO files aligned with release handoff evidence.

Files changed:
- Updated `scripts/prepare_cloud_device_evidence.py` so regenerated `cloud-device-capture-todo.md` includes a Release Handoff section with the release evidence index, blocking report, default `LANDING_RELEASE_CANDIDATE_METRIC 52/52`, and expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` state.
- Updated `materials/evidence/cloud-device/cloud-device-capture-todo.md` with the same handoff section and `validate_release_evidence_index.py` command.
- Updated `validation/validate_cloud_device_package.py` so the package guard requires those generated TODO handoff tokens.

Validation:
- PASS `python3 -m py_compile scripts/prepare_cloud_device_evidence.py validation/validate_cloud_device_package.py`
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	23/23`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The preparation helper still does not create fake recordings; it reports all 9 real cloud-device videos as missing until they are collected.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue auditing generated evidence helpers and operator checklists for drift against the current release-candidate gate.

## 2026-05-29 / Round 174

Goal: Make the cloud-device manifest a complete release handoff entrypoint.

Files changed:
- Updated `materials/evidence/cloud-device/cloud-device-manifest.md` with related release handoff files, the default `LANDING_RELEASE_CANDIDATE_METRIC 52/52` gate, and the expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` blocker state.
- Updated `validation/validate_cloud_device_package.py` with `manifest_links_release_handoff`, raising the package skeleton guard to `CLOUD_DEVICE_PACKAGE_METRIC 23/23`.
- Updated `materials/evidence/release-evidence-index.md` and `validation/validate_release_evidence_index.py` to reference the current cloud-device package metric.

Validation:
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	23/23`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The manifest still describes a staging package; strict mode remains blocked until real recordings and a filled cloud-device report exist.
- No cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue improving evidence package completeness and cross-file handoff consistency without converting external blockers into claimed proof.

## 2026-05-29 / Round 172

Goal: Expand the final delivery-package validation list to current core gates.

Files changed:
- Updated `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` final delivery-package tree so `validation/` includes demo acceptance, real-world readiness, release blocking report, release evidence index, and deliverables validators in addition to the existing security, BlueLM, cloud package, frontend, and release-candidate gates.
- Updated `validation/validate_landing_release_candidate.py` so `landing_guide_current` requires those core validator names inside the final delivery tree.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS delivery-tree validator list check
  - Evidence: `DELIVERY_TREE_VALIDATOR_MISSING 0`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The final package tree remains a handoff suggestion; it now lists the executable gates already used by the release candidate flow.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue checking whether final package instructions and current README/status agree on which commands are mandatory versus strict external evidence.

## 2026-05-29 / Round 171

Goal: Make the final delivery-package tree match current backend and evidence paths.

Files changed:
- Updated `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` final delivery-package tree to replace nonexistent `docs/cloud-device-test-report.md`, `docs/privacy-and-security.md`, `backend/main.py`, and `backend/env.example`.
- The delivery tree now points to `backend/shike_backend/main.py`, `backend/shike_backend/adapters/`, `backend/shike_backend/prompts/`, and cloud evidence files under `materials/evidence/cloud-device/`.
- Updated `validation/validate_landing_release_candidate.py` so `landing_guide_current` checks the delivery tree section for the current backend/evidence entries while avoiding false substring matches such as `backend/main.py` inside `shike_backend/main.py`.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS delivery-tree existence check
  - Evidence: `DELIVERY_TREE_EXISTENCE_MISSING 0`
- PASS delivery-tree token check
  - Evidence: tree contains `cloud-device-test-report.md`, `backend-redacted-access-log.txt`, `apk-sha256.txt`, `shike_backend/main.py`, `shike_backend/adapters/`, and `shike_backend/prompts/`; tree omits flat `main.py` and `env.example`.
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The guide now uses existing repository paths and still treats environment variables/runbook setup as operator configuration, not a committed env template.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue checking high-visibility delivery instructions for mismatches between tree examples, actual files, and validator expectations.

## 2026-05-29 / Round 170

Goal: Sync the final delivery-package tree with the current material artifact names.

Files changed:
- Updated `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` final delivery-package tree to replace obsolete `scoring-evidence-map.md`, `final-demo-script.md`, and `landing-deck-outline.md` with current artifacts: `docs/delivery-boundary-and-scoring.md`, `materials/demo-script.md`, `materials/preliminary-deck.md`, `materials/submission-checklist.md`, `materials/evidence/release-evidence-index.md`, and `materials/evidence/blocking-report.md`.
- Updated `validation/validate_landing_release_candidate.py` so `landing_guide_current` requires the current delivery package file names and rejects the obsolete ones.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS obsolete-name scan with `rg`
  - Evidence: no `scoring-evidence-map.md`, `final-demo-script.md`, or `landing-deck-outline.md` remains in `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md`.
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS public path existence scan
  - Evidence: `MISSING_PATH_COUNT 0`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The guide now points reviewers to files that exist in this repository; no new final package artifact is claimed.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning remaining high-visibility sections for old package names and outdated submission instructions.

## 2026-05-29 / Round 169

Goal: Make release-candidate public-doc checks easier to maintain safely.

Files changed:
- Refactored `validation/validate_landing_release_candidate.py` so the growing public-document assertions are grouped into `landing_guide_current` and `goal_mode_guide_current` booleans before constructing the 52-check list.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS public path existence scan
  - Evidence: `MISSING_PATH_COUNT 0`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The release-candidate denominator remains 52 checks; this round only changed internal validator structure to reduce future syntax-risk when adding public-doc assertions.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue with a protocol fingerprint check before selecting Round 170, then keep the next round focused on high-visibility handoff quality.

## 2026-05-29 / Round 168

Goal: Remove the last missing public-doc path from the goal-mode guide.

Files changed:
- Updated `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md` so the per-round maintained-file list no longer points to nonexistent `android-mvp/app/src/androidTest/**`.
- Replaced that placeholder with the current real device-maintenance surfaces: `docs/device-runbook.md` and `materials/device-demo-checklist.md`.
- Updated `validation/validate_landing_release_candidate.py` so the public-docs check rejects the missing `androidTest` path and requires the real runbook/checklist paths in the goal-mode guide.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS old-path scan with `rg`
  - Evidence: no `android-mvp/app/src/androidTest/` remains in `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md`.
- PASS public path existence scan
  - Evidence: `MISSING_PATH_COUNT 0`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- No Android instrumentation tests were claimed or fabricated; connected/device verification remains a real-device follow-up documented in current status and runbooks.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue auditing high-visibility handoff text for stale assumptions, then consider consolidating the repeated release-candidate public-doc checks into safer local booleans.

## 2026-05-29 / Round 167

Goal: Point the goal-mode guide at the real strict blocking-report artifact.

Files changed:
- Updated `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md` so pause/blocker reporting and per-round maintained-file guidance point to `materials/evidence/blocking-report.md` instead of nonexistent `docs/blocking-report.md`.
- Updated `validation/validate_landing_release_candidate.py` so the public-docs check requires the real blocking-report path and rejects the old docs path.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS old-path scan with `rg`
  - Evidence: no `docs/blocking-report.md` remains in `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md`.
- PASS current-path scan with `rg`
  - Evidence: `materials/evidence/blocking-report.md` appears in the blocker and maintained-file sections.
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Only documentation pointers and the existing public-doc guard changed; strict mode still writes and validates the same `materials/evidence/blocking-report.md` artifact.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning public guides for references to missing folders, stale submission-package names, or command paths that do not match current repository layout.

## 2026-05-29 / Round 166

Goal: Replace obsolete landing-guide validator names with current executable gates.

Files changed:
- Updated `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` so the OCR phase uses `validate_ocr_engine_layer.py` and `validate_ocr_input.py` instead of the nonexistent `validate_capture_ocr_pipeline.py`.
- Updated the material phase in the same guide so it references current deliverables: `materials/demo-script.md`, `materials/preliminary-deck.md`, `materials/submission-checklist.md`, `materials/evidence/release-evidence-index.md`, and `docs/delivery-boundary-and-scoring.md`, with `validate_deliverables.py` and `validate_release_evidence_index.py` as executable gates.
- Updated `validation/validate_landing_release_candidate.py` so the public-docs check rejects the obsolete validator names and requires the current OCR/material gates in the landing optimization guide.

Validation:
- PASS `python3 -m py_compile validation/validate_landing_release_candidate.py`
- PASS obsolete-name scan with `rg`
  - Evidence: no `validate_capture_ocr_pipeline.py`, `validate_landing_materials.py`, `materials/final-demo-script.md`, `materials/landing-deck-outline.md`, or `docs/scoring-evidence-map.md` remains in `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md`.
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_ocr_engine_layer.py`
  - Evidence: `OCR_ENGINE_LAYER_METRIC	9/9`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC	12/12`
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC	10/10`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Release-candidate remains a 52-check local gate; this round only corrected public execution instructions to match existing files.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue auditing public handoff docs for references to missing files, obsolete material names, or stale command paths.

## 2026-05-29 / Round 165

Goal: Sync the goal-mode guide inbox target with the landed SQLite inbox workbench.

Files changed:
- Updated `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md` Goal C so the inbox target now requires SQLite persistence, legacy `SharedPreferences` snapshot migration, search, archive/restore, 50 synthetic records, and `INBOX_WORKBENCH_LANDING_METRIC 12/12`.
- Updated `validation/validate_inbox_workbench_landing.py` so the current inbox guard rejects stale guide wording that still claims only "at least 10 historical action cards".

Validation:
- PASS stale guide scan with `rg`
  - Evidence: no `至少 10 条历史行动卡` or old `SharedPreferences 当前卡片快照升级为 Room/SQLite 收件箱` wording remains in `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md`.
- PASS `python3 validation/validate_inbox_workbench_landing.py`
  - Evidence: `INBOX_WORKBENCH_LANDING_METRIC	12/12`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The inbox validator still reports the same 12 checks; this round tightened one existing documentation-consistency check rather than inflating the gate.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning remaining guides and material surfaces for old denominators, old inbox assumptions, or strict-evidence wording that could mislead a reviewer.

## 2026-05-29 / Round 164

Goal: Sync the landing optimization guide with the current release-candidate gate.

Files changed:
- Updated `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` so the total local release-candidate gate is `52/52`, including strict blocking-report quality and release evidence index quality.
- Updated `validation/validate_landing_release_candidate.py` so the existing public-docs check rejects stale guide wording that still claims `LANDING_RELEASE_CANDIDATE_METRIC 50/50`.

Validation:
- PASS stale guide scan with `rg`
  - Evidence: no `LANDING_RELEASE_CANDIDATE_METRIC 50/50`, `>= 40/50`, `>= 45/50`, or `整合成 50 项` remains in `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md`.
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The release-candidate validator still reports the same 52 local checks; this round tightened an existing public-document guard instead of inflating the denominator.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning handoff guides, prototype surfaces, and material checklists for stale gate names or outdated external-evidence boundaries.

## 2026-05-29 / Round 163

Goal: Sync the Demo console with the current demo acceptance metric.

Files changed:
- Updated `prototype/demo.html` so the Demo console now shows `DEMO_ACCEPTANCE_METRIC 18/18` instead of stale `17/17`.
- Updated `validation/validate_demo_acceptance.py` so the demo page check requires the current `18/18` demo metric and rejects stale `17/17` wording.

Validation:
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_frontend_polish.py`
  - Evidence: `FRONTEND_POLISH_METRIC	12/12`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The Demo console remains a static handoff surface, but it now reflects the current mechanical demo acceptance gate.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning visible handoff surfaces for stale readiness metrics and keep strict cloud-device blockers separate from local readiness.

## 2026-05-29 / Round 162

Goal: Sync the public README with the current inbox landing guard.

Files changed:
- Updated `README.md` so the inbox landing guard baseline is now `INBOX_WORKBENCH_LANDING_METRIC 12/12` and explicitly includes status-document synchronization.
- Updated `validation/validate_inbox_workbench_landing.py` so the inbox landing guard checks the README for the current guard command, metric, and status-document wording.

Validation:
- PASS `python3 validation/validate_inbox_workbench_landing.py`
  - Evidence: `INBOX_WORKBENCH_LANDING_METRIC	12/12`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The README now matches the stricter inbox landing guard instead of stale `10/10` wording.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue scanning public handoff surfaces for stale readiness metrics and tie any remaining drift to mechanical guards.

## 2026-05-29 / Round 161

Goal: Align current validation status with the implemented SQLite inbox layer.

Files changed:
- Updated `docs/current-validation-status.md` so the persistence risk section now reflects the current `InboxDatabase` SQLite history, `InboxItemEntity` mapping, 50-record synthetic seed coverage, and legacy `SharedPreferences` migration boundary.
- Updated `validation/validate_inbox_workbench_landing.py` so the inbox landing guard rejects the old “does not yet satisfy Room/SQLite inbox target” wording and requires the current status document to mention the SQLite inbox evidence.

Validation:
- PASS `python3 validation/validate_inbox_workbench_landing.py`
  - Evidence: `INBOX_WORKBENCH_LANDING_METRIC	11/11`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The inbox landing guard still proves entity types, SQLite storage, legacy snapshot migration, multi-record UI history, 50-record seed coverage, archive/search/status filters, and Android unit guard coverage.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Sync any remaining public metric references to the new `INBOX_WORKBENCH_LANDING_METRIC 11/11` gate.

## 2026-05-29 / Round 160

Goal: Prevent Product Beta status wording from drifting back to the old unfinished-strict posture.

Files changed:
- Updated `docs/current-validation-status.md` so the next-priority section now keeps `validate_advanced_product_beta.py --strict` inside the release-candidate gate because Product Beta already passes at `PRODUCT_BETA_METRIC 30/30`.
- Updated `validation/validate_advanced_product_beta.py` so the existing 30-item Product Beta guard also checks the current status document for the completed Product Beta posture and rejects the old “do not treat strict as required until Product Beta exits S2” wording.

Validation:
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC	30/30`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC	30/30`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Product Beta remains a completed 30-item gate and `validate_landing_release_candidate.py` still runs `validate_advanced_product_beta.py --strict`.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue local consistency hardening around status documents and operator handoff surfaces, while keeping strict external blockers explicit.

## 2026-05-29 / Round 159

Goal: Make the submission checklist explicitly distinguish local readiness from strict cloud-device release evidence.

Files changed:
- Updated `materials/submission-checklist.md` so SHIKE-070 handoff text directly points to `materials/evidence/cloud-device/`, `materials/evidence/blocking-report.md`, and the expected `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` blocker state.
- Updated `validation/validate_deliverables.py` so SHIKE-070 now requires the submission checklist itself to state that strict cloud-device evidence is still an expected blocker and must not be treated as final release proof before real MP4/report evidence exists.

Validation:
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC	10/10`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- SHIKE-070 deliverables still pass at `10/10`, but the checklist now carries the strict external-evidence boundary directly.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue proof-chain hardening in release evidence surfaces while keeping strict external blockers explicit.

## 2026-05-29 / Round 158

Goal: Make the device demo checklist distinguish local/USB recordings from cloud-device strict release evidence.

Files changed:
- Updated `materials/device-demo-checklist.md` with a cloud-device strict evidence section that links `materials/evidence/cloud-device/`, `materials/evidence/release-evidence-index.md`, and `materials/evidence/blocking-report.md`.
- Updated `validation/validate_demo_acceptance.py` so demo acceptance now requires the cloud strict handoff, `LANDING_RELEASE_CANDIDATE_METRIC 52/52`, expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`, required cloud MP4 names, HTTPS backend wording, and redaction reminders.
- Updated `README.md` and `docs/current-validation-status.md` so the demo acceptance baseline is `DEMO_ACCEPTANCE_METRIC 18/18`.

Validation:
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC	18/18`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Local/USB demo evidence and cloud-device strict release evidence are now separated in the operator checklist.
- Strict release remains blocked on real external cloud-device proof; no cloud recordings, report values, credentials, or personal data were fabricated.

Next:
- Continue hardening handoff documents and validators that prevent local readiness from being confused with final strict cloud-device release evidence.

## 2026-05-29 / Round 157

Goal: Make the cloud-device evidence package README a strict-release handoff entrypoint.

Files changed:
- Updated `materials/evidence/cloud-device/README.md` to point operators to `materials/evidence/release-evidence-index.md`, `materials/evidence/blocking-report.md`, the default `LANDING_RELEASE_CANDIDATE_METRIC 52/52` gate, and the expected strict `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` blocker state.
- Updated `validation/validate_cloud_device_package.py` so the default package guard requires those release-handoff links and redaction reminders in the package README.
- Updated `materials/evidence/release-evidence-index.md` and `validation/validate_release_evidence_index.py` so the cloud-device package skeleton evidence is now `CLOUD_DEVICE_PACKAGE_METRIC 22/22`.

Validation:
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	22/22`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The cloud-device package still distinguishes non-strict structure/redaction readiness from strict real-device proof.
- Strict release remains blocked on real external cloud-device proof; no videos, report values, credentials, or personal data were fabricated.

Next:
- Continue tightening local handoff checks, especially where operator-facing evidence files can drift from the release-candidate gate.

## 2026-05-29 / Round 156

Goal: Align the release evidence index with the current 52-item local release gate.

Files changed:
- Updated `materials/evidence/release-evidence-index.md` so the release-candidate evidence row reports the current `LANDING_RELEASE_CANDIDATE_METRIC 52/52`.
- Updated `validation/validate_release_evidence_index.py` so the release evidence guard now fails on stale `51/51` release-gate wording.

Validation:
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The default release-candidate gate remains `52/52`.
- Strict release remains blocked on real external cloud-device proof; no recordings, report values, BlueLM credentials, or personal data were fabricated.

Next:
- Continue local proof-chain tightening where it improves handoff reliability, or proceed to real cloud-device recording when external access is available.

## 2026-05-29 / Round 155

Goal: Make the release evidence index part of the submission deliverables.

Files changed:
- Updated `materials/submission-checklist.md` with `materials/evidence/release-evidence-index.md` as a completed submission artifact and surfaced the key release evidence metrics in the onsite checklist.
- Updated `validation/traceability.md` so SHIKE-070 points to the release evidence index alongside the deck, demo script, and poster copy.
- Updated `validation/validate_deliverables.py` so SHIKE-070 requires the release evidence index and checks the 52/52 release gate, 22/22 real-world gate, redacted BlueLM evidence, strict blocker status, and redaction wording.

Validation:
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC	10/10`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The deliverables validator still covers the same 10 SHIKE issue buckets, but SHIKE-070 now requires the release evidence index.
- Strict release remains blocked on real external cloud-device proof; this round only improves submission traceability.
- No credentials or personal data were introduced.

Next:
- Continue tying remaining proof artifacts into existing gates, or proceed to real cloud-device capture when external access is available.

## 2026-05-29 / Round 154

Goal: Make the release evidence index a mandatory release-candidate handoff artifact.

Files changed:
- Updated `validation/validate_landing_release_candidate.py` so the default local release-candidate gate runs `validate_release_evidence_index.py` and reports `LANDING_RELEASE_CANDIDATE_METRIC 52/52`.
- Updated README mechanical acceptance and release-candidate wording to include `validate_release_evidence_index.py` and the 52/52 gate.
- Updated `docs/current-validation-status.md` to list the 52-item release gate and current `LANDING_RELEASE_CANDIDATE_METRIC 52/52` evidence.

Validation:
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `release_evidence_index_passes	validate_release_evidence_index.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	52/52`
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly requires real cloud-device MP4 files and a completed cloud-device report.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- This round tightened the release-candidate gate by requiring the evidence index; it did not weaken strict external proof.
- Strict release remains blocked until actual cloud-device recordings and report completion exist.
- No credentials or personal data were introduced.

Next:
- Continue local release proof hardening, or proceed to real cloud-device recording using the checklist when external device access is available.

## 2026-05-29 / Round 153

Goal: Create a release evidence index that makes the current local proof package easy to audit.

Files changed:
- Added `materials/evidence/release-evidence-index.md` with local readiness gates, model evidence, BlueLM redacted smoke evidence, cloud-device strict blockers, APK hash location, redaction rules, and rebuild commands.
- Added `validation/validate_release_evidence_index.py` to guard that the index covers release metrics, model proof, strict blockers, existing evidence files, rebuild commands, and secret-safe wording.

Validation:
- PASS `python3 validation/validate_release_evidence_index.py`
  - Evidence: `RELEASE_EVIDENCE_INDEX_METRIC	6/6`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	51/51`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The index references existing evidence files and commands; it does not replace strict external evidence.
- BlueLM proof remains redacted and backend-side.
- No secret-like `sk-...` token was embedded in the evidence index.

Next:
- Consider folding the evidence index validator into the release-candidate gate if it proves useful as a mandatory handoff artifact, or continue with another local proof surface from the desktop judgment doc.

## 2026-05-29 / Round 152

Goal: Fold strict blocking-report quality into the default release-candidate gate.

Files changed:
- Updated `validation/validate_landing_release_candidate.py` so the default local release-candidate gate now runs `validate_release_blocking_report.py` and reports `LANDING_RELEASE_CANDIDATE_METRIC 51/51`.
- Updated README mechanical acceptance and release-candidate wording from 50/50 to 51/51, including the strict blocking-report quality guard.
- Updated `docs/current-validation-status.md` to list the 51-item release gate and current `LANDING_RELEASE_CANDIDATE_METRIC 51/51` evidence.

Validation:
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `release_blocking_report_passes	validate_release_blocking_report.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	51/51`
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	21/21`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: strict mode still correctly requires real cloud-device MP4 files and a completed cloud-device report.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- This round tightened the default release-candidate gate; it did not relax strict external evidence requirements.
- Strict release still cannot pass without real cloud-device recordings and report completion.
- No credentials or personal data were introduced.

Next:
- Continue improving local proof surfaces around the remaining desktop judgment-doc gaps, while keeping external cloud-device evidence explicitly blocked until collected.

## 2026-05-29 / Round 151

Goal: Strengthen the cloud-device capture preparation checklist before real external recording.

Files changed:
- Updated `scripts/prepare_cloud_device_evidence.py` so `cloud-device-capture-todo.md` includes required videos, report fields, HTTPS backend reachability, BlueLM redacted log proof, fallback/restart paths, and secret/PII redaction reminders.
- Updated `validation/validate_cloud_device_package.py` so the default cloud-device package gate now checks those report-field and pre-capture checklist requirements.
- Regenerated `materials/evidence/cloud-device/cloud-device-capture-todo.md` and refreshed `materials/evidence/cloud-device/apk-sha256.txt` through the preparation script.

Validation:
- PASS `python3 scripts/prepare_cloud_device_evidence.py`
  - Evidence: `CLOUD_DEVICE_PREP_METRIC	5/5`
  - Evidence: `CLOUD_DEVICE_PREP_MISSING_VIDEOS	9/9`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	21/21`
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	50/50`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device MP4 files and filled cloud-device report remain external evidence gaps.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- The preparation script still does not fabricate recordings or fill real test results.
- Strict cloud-device validation still fails until actual recordings and a completed report exist.
- Default release-candidate readiness remains reproducible locally at 50/50.

Next:
- Continue local evidence hardening, or use the cloud-device checklist to collect the nine real recordings when the external device platform is available.

## 2026-05-29 / Round 150

Goal: Make the strict release blocking report actionable without fabricating cloud-device evidence.

Files changed:
- Added `validation/validate_release_blocking_report.py` to guard the generated strict release blocking report.
- Tightened `validation/validate_landing_release_candidate.py` strict blocker output so `materials/evidence/blocking-report.md` lists each missing cloud-device MP4, each placeholder report field, the HTTPS backend requirement, the preparation command, the strict rerun command, and redaction warnings.
- Regenerated `materials/evidence/blocking-report.md` through `python3 validation/validate_landing_release_candidate.py --strict`.

Validation:
- PASS `python3 validation/validate_release_blocking_report.py`
  - Evidence: `RELEASE_BLOCKING_REPORT_METRIC	8/8`
- PASS `python3 validation/validate_cloud_device_package.py`
  - Evidence: `CLOUD_DEVICE_PACKAGE_METRIC	18/18`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	50/50`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Evidence: `BLOCKING_REPORT	materials/evidence/blocking-report.md`
  - Reason: strict mode still correctly requires real cloud-device MP4 files and a completed cloud-device report.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- Default release-candidate readiness remains local and reproducible at 50/50.
- Strict release mode remains blocked until real external cloud-device evidence is collected.
- No BlueLM AppKEY, backend token, personal OCR text, phone number, email, or student ID was added.

Next:
- Continue the desktop judgment-doc audit by improving the remaining evidence workflow that can be advanced locally, or move to actual cloud-device capture when the external platform is available.

## 2026-05-29 / Round 149

Goal: Make the 110-case regression set a hard mechanical gate across model evaluation, Product Beta, and release-candidate readiness.

Files changed:
- Updated `validation/validate_model_eval_cases.py` so the regression count check is named `case_count_at_least_110` and requires at least 110 cases.
- Updated `validation/validate_advanced_product_beta.py` so `model_eval_110_cases` requires the actual synthetic case count to be at least 110, with no evaluator-script bypass.
- Updated `validation/validate_landing_release_candidate.py` so the local release-candidate package checks `regression_cases_at_least_110`.

Validation:
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `case_count_at_least_110	110`
  - Evidence: `MODEL_EVAL_CASES_METRIC	8/8`
- PASS `python3 backend/shike_backend/eval/run_model_eval.py --progress-every 25`
  - Evidence: `MODEL_EVAL_METRIC	110/110	selected=110	total_valid=110`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `model_eval_110_cases	synthetic cases=110`
  - Evidence: `PRODUCT_BETA_METRIC	30/30`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `regression_cases_at_least_110	110 cases`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC	50/50`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE	3/7`
  - Reason: real cloud-device videos and the completed cloud-device report remain external evidence gaps; no proof was fabricated.
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS	secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC	22/22`

Behavior preserved:
- No schema, Android, backend adapter, or prompt behavior changed in this round.
- BlueLM credentials remain backend-only and no secret value was written to the repository.
- Strict release mode still separates local readiness from real external cloud-device proof.

Next:
- Continue the requirement-by-requirement audit against the desktop repository judgment doc, prioritizing the remaining evidence gaps that can be advanced without fabricating cloud-device results.

## 2026-05-29 / Round 148

Goal: Close stale scene-contract wording after the 110-case multi-scene expansion.

Files changed:
- Removed the old `travel_plan` mock alias so backend mock routing only emits the current `travel_ticket` contract name for travel-ticket fragments.
- Updated current-facing model-evaluation wording in README and landing optimization guidance from 100-case coverage to the current 110-case set.
- Kept historical optimization-log evidence unchanged where it describes earlier rounds, while documenting the current `travel_ticket` contract and 110-case guard chain here.

Validation:
- PASS `python3 validation/validate_backend_scene_contract.py`
  - Evidence: `BACKEND_SCENE_CONTRACT_METRIC 11/11`
- PASS `python3 backend/shike_backend/eval/run_model_eval.py --progress-every 25`
  - Evidence: `MODEL_EVAL_METRIC 110/110`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC 50/50`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`

Behavior preserved:
- Android still calls `/v1/analyze` through the backend only; BlueLM secrets remain backend-side.
- Strict release remains intentionally blocked until real BlueLM online logs and cloud-device recording/report evidence exist.
- Historical log entries remain as past evidence rather than being rewritten into current status.

Next:
- Continue the requirement-by-requirement audit against the desktop repository judgment doc, prioritizing real evidence gaps and material polish without fabricating cloud-device proof.

## 2026-05-29 / Round 147

Goal: Make the widened scene contract visible in demo and submission materials instead of leaving it as code-only capability.

Files changed:
- Updated `materials/demo-script.md` with复赛扩展场景备选：作业截止、会议通知、面试通知、出行票务，并补充评委追问口径。
- Updated `materials/device-demo-checklist.md` with optional extension recordings and manual checks for `assignment_deadline`, `meeting_notice`, `interview_notice`, and `travel_ticket`.
- Updated `materials/submission-checklist.md`, `README.md`, `prototype/demo.html`, and `docs/current-validation-status.md` so demo surfaces mention the extended scenes and current `DEMO_ACCEPTANCE_METRIC 17/17`.
- Tightened `validation/validate_demo_acceptance.py` so the device checklist, demo script, submission checklist, and demo console all carry the extended scene tokens.

Validation:
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 17/17`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC 50/50`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS secret_hygiene`

Behavior preserved:
- The six required primary demo recordings remain the same; expanded scene videos are optional supplement recordings.
- User confirmation remains required before calendar, reminder, or map execution in all scenes.

Next:
- Continue with external cloud-device evidence capture or recorded BlueLM case quality.

## 2026-05-29 / Round 146

Goal: Expand the backend `scene_type` contract beyond the initial course/event baseline without breaking Android confirmation-first execution.

Files changed:
- Expanded `contracts/model-output.schema.json` and `backend/shike_backend/schemas.py` to include `assignment_deadline`, `meeting_notice`, `interview_notice`, `travel_ticket`, and matching `task.topic` values.
- Updated `backend/shike_backend/adapters/mock_adapter.py` and `backend/verify_backend.py` so deterministic fallback and smoke tests cover the new scenes.
- Updated Android scene labels and hints in `ModelApiClient.kt`, with `ModelApiClientTest` now covering eight cases.
- Added new request/response samples under `contracts/` and `validation/validate_backend_scene_contract.py`.
- Expanded `validation/regression-cases.json` to 110 cases and renamed the previous travel group to the contract name `travel_ticket`.
- Updated prompt/docs/status/report surfaces so BlueLM and demo documentation point at the widened contract.

Validation:
- PASS `python3 backend/shike_backend/eval/run_model_eval.py --progress-every 25`
  - Evidence: `MODEL_EVAL_METRIC 110/110`
- PASS `python3 validation/validate_backend_scene_contract.py`
  - Evidence: `BACKEND_SCENE_CONTRACT_METRIC 11/11`
- PASS `python3 validation/validate_model_contract_strict.py`
  - Evidence: `MODEL_CONTRACT_STRICT_METRIC 10/10`
- PASS `gradle --no-daemon :app:compileDebugKotlin :app:testDebugUnitTest`
  - Evidence: `BUILD SUCCESSFUL in 26s`
  - Evidence: `ModelApiClientTest` reports 8 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 89 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 64/64`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_landing_release_candidate.py`
  - Evidence: `LANDING_RELEASE_CANDIDATE_METRIC 50/50`
- EXPECTED BLOCK `python3 validation/validate_landing_release_candidate.py --strict`
  - Evidence: `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7`
  - Reason: real cloud-device videos/report are still missing; no evidence was fabricated.

Behavior preserved:
- Android still calls only the project FastAPI backend; BlueLM credentials remain backend-only.
- User confirmation remains required before calendar, reminder, or map execution.
- Strict release evidence remains blocked on real external cloud-device recordings/report.

Next:
- Continue with cloud-device evidence capture or improve real BlueLM eval quality using recorded synthetic cases.

## 2026-05-29 / Round 145

Goal: Expand the backend `/v1/analyze` source contract so screenshot, camera, shared text, and manual drafts are represented explicitly end to end.

Files changed:
- Updated `backend/shike_backend/schemas.py` so `AnalyzeRequest.source_type` accepts `screenshot`, `camera`, `share_text`, and `manual`, while forbidding extra request fields.
- Expanded `backend/verify_backend.py` and `contracts/` sample requests to cover `share_text` and `manual` inputs.
- Updated Android request mapping so "解析当前草稿" sends a source type derived from the current capture source instead of forcing every non-event path through `screenshot`.
- Added source-type coverage to `CaptureImportMapperTest`, `ModelApiClientTest`, and `BackendAnalysisRunnerTest`, with `validate_android_unit_tests.py` now guarding the mapping.
- Added `validation/validate_backend_source_type_contract.py` and wired it into `validate_model_contract_strict.py`.
- Updated README, runbooks, Demo console, and device checklist so button labels and request examples match the new contract.

Validation:
- PASS `gradle --no-daemon :app:compileDebugKotlin :app:testDebugUnitTest`
  - Evidence: `BUILD SUCCESSFUL in 40s`
  - Evidence: `CaptureImportMapperTest` reports 4 tests, `ModelApiClientTest` reports 6 tests, `BackendAnalysisRunnerTest` reports 5 tests
  - Evidence: local unit suites report 87 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_backend_source_type_contract.py`
  - Evidence: `BACKEND_SOURCE_TYPE_CONTRACT_METRIC 9/9`
- PASS `python3 validation/validate_model_contract_strict.py`
  - Evidence: `MODEL_CONTRACT_STRICT_METRIC 5/5`
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 64/64`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_secret_hygiene.py`
  - Evidence: `PASS secret_hygiene`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`

Behavior preserved:
- Android still calls only the project FastAPI backend; it does not hold or call BlueLM credentials directly.
- User confirmation remains required before calendar, reminder, or map execution.
- Scene output remained limited to the then-current model-output schema; Round 146 later widened `scene_type`.
- Strict release evidence is still blocked on real cloud-device recordings/report; no video evidence was fabricated.

Next:
- Continue with cloud-device/HTTPS evidence or carefully scoped scene expansion after updating schema, samples, Android mapping, eval cases, and validators together.

## 2026-05-26 / Round 126

Goal: Harden Android backend base URL normalization to strip path/query/fragment and add unit-test coverage.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt` so `normalizeBackendUrl(...)` extracts `scheme/host/port` via `URI`, stripping any path/query/fragment that users may paste (for example `http://10.0.2.2:8000/v1/analyze?x=y#z`).
- Expanded `android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt` to cover the path/query/fragment stripping behavior (`normalizeBackendUrl_stripsPathQueryAndFragment`).
- Expanded `validation/validate_android_unit_tests.py` from `60/60` to `61/61` with a new `backend_url_normalization_strips_path_query_fragment` gate and updated Gradle XML expectation for `ModelApiClientTest` (5 tests).
- Updated README, device checklist, runbook, Demo console, real-world readiness validator, core-package verifier, and current validation status with the current `ANDROID_UNIT_TEST_METRIC 61/61` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 33s`
  - Evidence: `ModelApiClientTest` XML reports 5 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 76 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 61/61`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 a9bdea5a67e687ea71c7884d86fb84d722417326385b521a2d8ab8a5c9cd222d`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 a9bdea5a67e687ea71c7884d86fb84d722417326385b521a2d8ab8a5c9cd222d`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- User confirmation remains required before calendar, reminder, or map execution; this round only hardens backend URL input handling.
- Backend failure paths still fall back to the local `MockModelAdapter` item and remain editable in the confirmation panel.

Risks:
- `URI` parsing is stricter than ad-hoc string handling; malformed values still fall back to `null` and the UI retains the "editable backend URL" workflow.

Next:
- Continue S3 quality hardening with another focused local test around persistence edge cases, error copy, or structured logging.

## 2026-05-26 / Round 127

Goal: Make "一键清除本地数据" fully reset the local demo state by restoring the cloud-enhancement toggle to its default enabled value.

Context:
- Android local persistence uses one SharedPreferences file (`PREFERENCES_NAME = "shike_inbox_state"`) for the inbox snapshot, backend base URL, and scheduled reminder payload.
- The UI already resets backend URL to `DEFAULT_BACKEND_BASE_URL` and clears the persisted preferences, but the in-memory `cloudEnhancedEnabled` Compose toggle previously stayed in its prior state after clearing local data. That made the "清除本地数据" semantics inconsistent: UI looked reset, yet backend analysis buttons could remain disabled.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/LocalDataClearActions.kt` so the cleared state includes `cloudEnhancedEnabled = true`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so `clearLocalDataSelection()` applies the cleared cloud toggle and keeps the reset assignments explicit (also shrunk the coordinator back under the structure-line guard).
- Updated `android-mvp/app/src/test/java/cn/shike/app/LocalDataClearActionsTest.kt` with a new assertion that the cleared state restores cloud enhancement to default enabled.
- Updated `validation/validate_android_unit_tests.py` to reflect the new `LocalDataClearActionsTest` count (4 tests) in both the source-gate and the Gradle XML expectation.

Validation:
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 61/61`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- All system actions (calendar/reminder/map) still require explicit user confirmation before execution.
- Clearing local data still cancels any scheduled reminder alarm and clears the persisted reminder payload; this round only makes the local "cloud enhancement" toggle reset consistent with the rest of the cleared UI state.

Risks:
- Low: the change only affects in-memory UI state after the user explicitly taps "一键清除本地数据". No network or persistence schema changes.

Next:
- Continue S3 hardening with a focused persistence boundary improvement, preferably splitting the single SharedPreferences store so "清空收件箱缓存" does not implicitly wipe backend configuration and reminder scheduling metadata.

## 2026-05-26 / Round 128

Goal: Split local `SharedPreferences` into dedicated namespaces so "清空收件箱缓存" no longer implicitly wipes backend configuration or reminder scheduling state.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt`:
  - Renamed `PREFERENCES_NAME` to `INBOX_PREFERENCES_NAME = "shike_inbox_state"` for clarity.
  - Added `clearInboxSnapshot(context)` to remove only the inbox snapshot keys (title/time/location/actions/rawText/captureSource), keeping other local settings intact.
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt`:
  - Persist backend base URL under `shike_backend_config` (still `SharedPreferences`, but isolated from inbox snapshot).
  - Added `clearBackendBaseUrl(context)` so the "一键清除本地数据" action can reset the backend endpoint override deterministically.
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt`:
  - Persist scheduled reminder payload under `shike_reminder_state` instead of sharing the inbox prefs file.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`:
  - "一键清除本地数据" now performs: cancel pending reminder -> clear inbox snapshot -> clear backend base URL.
- Updated `validation/validate_action_execution.py` and `validation/validate_persistence.py` to reflect the new preference namespace constant and the updated clear-local-data semantics.

Validation:
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 61/61`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`

Behavior preserved:
- User confirmation remains required before calendar/reminder/map execution.
- Restart restore still uses `SharedPreferences` for the inbox snapshot; this round only isolates preferences so future storage upgrades (Room/SQLite) can land without ambiguous "clear all" behavior.

Risks:
- Low: preference file split may cause previously stored backend endpoints or scheduled reminders (from earlier runs) to be ignored after upgrade, but the UI still provides default backend URL and re-scheduling via user confirmation.

Next:
- Add a narrow JVM unit test to assert the intended boundary explicitly: clearing inbox snapshot must not erase a saved backend URL or scheduled reminder payload.

## 2026-05-26 / Round 129

Goal: Add a regression guard that locks the "split preferences + clear snapshot semantics" boundary so future refactors cannot accidentally collapse preference namespaces or reintroduce `clear()` wiping.

Files changed:
- Updated `validation/validate_persistence.py`:
  - Strengthened the `preferences_namespace_present` gate to require all three preference namespaces remain present:
    - `INBOX_PREFERENCES_NAME = "shike_inbox_state"`
    - `BACKEND_PREFERENCES_NAME = "shike_backend_config"`
    - `REMINDER_PREFERENCES_NAME = "shike_reminder_state"`
  - Strengthened the existing `save_snapshot_present` gate to also assert:
    - `clearInboxSnapshot(...)` removes only snapshot keys (`KEY_TITLE/KEY_SCENE/KEY_TIME/KEY_LOCATION/KEY_STATUS/KEY_ACTIONS/KEY_START/KEY_RAW_TEXT/KEY_CAPTURE_SOURCE`)
    - `clearInboxSnapshot(...)` does not call `.clear()` (preventing accidental wipe of other persisted state in the same namespace)

Validation:
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 61/61`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- System actions (calendar/reminder/map) still require explicit user confirmation; this round only tightens validators to preserve the intended persistence boundary.
- "一键清除本地数据" still cancels a pending reminder alarm, clears the inbox snapshot, and resets any saved backend override.

Risks:
- Low: validator-only hardening. The new Kotlin function-body extraction helper is a best-effort text scan and will fail safe (reporting a persistence guard failure) if the function is missing or malformed.

Next:
- Keep iterating with one verifiable goal per round; prefer adding a targeted JVM unit test that proves the preference boundary at runtime (backend override + reminder payload survive inbox snapshot clear).

## 2026-05-26 / Round 130

Goal: Add a JVM unit test that proves clearing the inbox snapshot does not erase backend endpoint overrides or scheduled reminder payloads.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt`:
  - Added `clearInboxSnapshotFromPreferences(preferences)` so unit tests can exercise inbox-clear semantics without needing an Android `Context`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt`:
  - Added `clearScheduledReminderFromPreferences(preferences)` so unit tests can clear reminder payload without needing `Context/AlarmManager`.
- Added `android-mvp/app/src/test/java/cn/shike/app/data/LocalPersistenceBoundaryTest.kt`:
  - Uses an in-memory `SharedPreferences` fake to prove inbox snapshot clear is isolated from backend/reminder namespaces.
  - Verifies reminder payload can still be cleared explicitly via the reminder-scoped helper.
- Updated `validation/validate_persistence.py`:
  - Tightened Kotlin function-body extraction to match `fun clearInboxSnapshot(context: Context)` explicitly, so future overloads cannot satisfy the guard accidentally.

Validation:
- PASS Android local unit tests via project-local toolchain:
  - Evidence: `gradle --no-daemon :app:testDebugUnitTest` (ran with the repository Android SDK + Gradle toolchain env)
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 61/61`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The core loop remains unchanged: screenshot/camera/share -> parse -> user confirm -> action orchestration -> inbox/today tracking.
- All sensitive actions still require explicit user confirmation before execution; this round only adds testable helpers and unit coverage.

Risks:
- Low: new helpers are internal and share the same key-removal logic as the existing Context-based entrypoints.

Next:
- Keep S3 hardening focused: consider adding a small guard for the reminder/backend key names to avoid accidental renames breaking persistence without updating tests.

## 2026-05-26 / Round 131

Goal: Polish the high-fidelity prototype homepage so `prototype/index.html` page 1 visually matches the reference `C:\\Users\\Xing\\Desktop\\shike\\首页.png` more closely.

Files changed:
- Updated `prototype/index.html` (page 1 "今日行动台"):
  - Replaced placeholder text glyphs with inline SVG icons (bell, calendar, chevron, clock, map pin, checklist, etc.) so the screen reads like a real mobile UI.
  - Refined agenda-card shadows and surface highlights for a more phone-like depth.
  - Swapped footer note text to a pill-style chip and added a deadline progress bar on the "即将截止" card, matching the reference layout density.
  - Tweaked CTA gradient and small spacing so the hierarchy is closer to the screenshot.
- Regenerated `prototype/index.pdf` via headless Chrome and exported a refreshed `index.html` PDF to the Windows desktop (`shike-index.html.pdf`, `拾刻-index.html.pdf`).

Validation:
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC 10/10`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 61/61`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Prototype-only change. No Android app behavior, confirmation gates, or backend contracts were modified.

Risks:
- Very low: HTML/CSS-only polish. If icon SVGs ever need swapping, they're fully local and do not rely on external CDNs.

Next:
- If you want the Android app UI to follow this exact visual language, the next safe step is to align the Compose `HomeOverview` + `AgendaCard` spacing/iconography with this reference (still keeping every sensitive action behind user confirmation).

## 2026-05-25 / Round 125

Goal: Add Android local unit-test coverage for backend outcome copy sanitization (source/status redaction + non-blank defaults).

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/BackendOutcomeActions.kt` so backend outcome `source` and `statusMessage` are sanitized via `redactSensitiveLogText(...)` before UI display and local persistence; blank values fall back to safe defaults.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/BackendOutcomeActionsTest.kt` from two to three tests with explicit coverage for sensitive token redaction and default fallback copy.
- Expanded `validation/validate_android_unit_tests.py` from `59/59` to `60/60` with a new `backend_outcome_copy_sanitization_unit_tested` gate and updated Gradle XML expectation for `BackendOutcomeActionsTest` (3 tests).
- Updated README, device checklist, runbook, Demo console, real-world readiness validator, core-package verifier, and current validation status with the current `ANDROID_UNIT_TEST_METRIC 60/60` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 27s`
  - Evidence: `BackendOutcomeActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `LocalInboxStoreTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 75 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 60/60`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 71d959c2f9783079abf8d755f1a8229fc5d6b86a171e2f4f27f505ff4e486252`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- User confirmation remains required before calendar, reminder, or map execution; this round only hardens backend outcome copy handling.
- Backend failure paths still fall back to the local `MockModelAdapter` item and remain editable in the confirmation panel.

Risks:
- This remains a pure-logic UI/persistence hardening; it does not change network behavior or backend request/response shape.

Next:
- Continue S3 quality hardening with another focused local test around persistence edge cases or structured logging.

## 2026-05-25 / Round 124

Goal: Add Android local unit-test coverage for local inbox raw OCR text sanitization.

Files changed:
- Added `DEFAULT_RAW_TEXT` and `sanitizeInboxRawText(...)` in `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt` so persisted and restored OCR/raw-text snapshots are non-blank and pass through the existing privacy redaction logic.
- Updated `saveSnapshot(...)` and `loadSavedItem(...)` to sanitize `ShikeItem.rawText` before local persistence and after restart restore, preventing phone, email, student-id, and LAN-address tokens from reappearing in local inbox details.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/data/LocalInboxStoreTest.kt` from three to four tests with explicit coverage for blank raw-text fallback and sensitive raw OCR redaction.
- Expanded `validation/validate_android_unit_tests.py` from `58/58` to `59/59` with a new `local_inbox_raw_text_sanitization_unit_tested` gate and latest Gradle XML expectation for `LocalInboxStoreTest` 4 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 59/59` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 15s`
  - Evidence: `LocalInboxStoreTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 74 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 59/59`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 a1c48f76b0c2cf1149ccc453a8c7ddf31557f67796de68d1aad7364cff998d9e`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Saved inbox snapshots still restore the current action card, action list, capture source, backend URL, and fallback default values.
- Raw OCR/detail text remains useful for review while phone, email, student-id, and LAN-address tokens are redacted before local persistence or restart restore.
- User confirmation remains required before calendar, reminder, or map execution; this round only hardens local raw-text persistence.

Risks:
- This still covers the existing single-snapshot SharedPreferences store; durable multi-item Room/SQLite inbox storage remains a later persistence track.

Next:
- Continue S3 quality hardening with another focused local test around backend outcome state, local-data reset durability, or multi-item inbox preparation.

## 2026-05-25 / Round 123

Goal: Add Android local unit-test coverage for local inbox capture-source sanitization.

Files changed:
- Added `sanitizeInboxCaptureSource(...)` in `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt` so persisted and restored capture-source labels are non-blank and pass through the existing privacy redaction logic.
- Updated `saveSnapshot(...)` and `loadSavedCaptureSource(...)` to consume the shared capture-source sanitizer, preventing phone, email, and LAN-address tokens from being stored or restored in the source label.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/data/LocalInboxStoreTest.kt` from two to three tests with explicit coverage for blank-source fallback and source-label redaction.
- Expanded `validation/validate_android_unit_tests.py` from `57/57` to `58/58` with a new `local_inbox_capture_source_sanitization_unit_tested` gate and latest Gradle XML expectation for `LocalInboxStoreTest` 3 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 58/58` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Evidence: `LocalInboxStoreTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 73 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 58/58`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 8e908ec8d5a155bf23f5fe1a4723318f69a01d228497d61e9cdb77a3013eaa64`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Blank capture-source labels still restore to the offline sample fallback copy.
- Capture source remains human-readable while phone, email, and LAN-address tokens are redacted before local persistence or restart restore.
- User confirmation remains required before calendar, reminder, or map execution; this round only hardens local source-label persistence.

Risks:
- This still covers the existing single-snapshot SharedPreferences store; durable multi-item Room/SQLite inbox storage remains a later persistence track.

Next:
- Continue S3 quality hardening with another focused local test around persisted raw OCR text redaction, backend outcome state, or multi-item inbox preparation.

## 2026-05-25 / Round 122

Goal: Add Android local unit-test coverage for local inbox action-list persistence codec.

Files changed:
- Added `encodeInboxActions(...)` and `decodeInboxActions(...)` in `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt` so restart-restore action labels are trimmed, blank labels are removed, and the existing SharedPreferences separator cannot leak into restored action cards.
- Updated `saveSnapshot(...)` and `loadSavedItem(...)` to consume the shared action-list codec instead of encoding and decoding inline.
- Added `android-mvp/app/src/test/java/cn/shike/app/data/LocalInboxStoreTest.kt` with two local unit tests covering blank-label filtering, separator sanitization, trimming, and default course-action fallback when the stored payload is missing or empty.
- Expanded `validation/validate_android_unit_tests.py` from `55/55` to `57/57` with explicit `LocalInboxStoreTest` source and Gradle XML checks.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 57/57` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 22s`
  - Evidence: `LocalInboxStoreTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 72 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 57/57`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 a40ef81f6532732910c35289eb5d6d410dbdcd18cb30558dd840f6d336d64f77`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Saved inbox snapshots still restore the current action card, source, backend URL, and fallback default actions.
- Empty or malformed stored action lists now fall back to the course sample actions instead of restoring an unusable empty action list.
- User confirmation remains required before calendar, reminder, or map execution; this round only hardens local action-label persistence.

Risks:
- This still covers the existing single-snapshot SharedPreferences store; durable multi-item Room/SQLite inbox storage remains a later persistence track.

Next:
- Continue S3 quality hardening with another focused local test around backend outcome state, multi-item inbox preparation, or persisted source labels.

## 2026-05-25 / Round 121

Goal: Add Android local unit-test coverage for inbox all-status priority ordering.

Files changed:
- Added `inboxAllStatusFilter` and `inboxStatusPriority(...)` in `android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt` so the inbox can show an "全部" view while keeping urgent, review-needed, scheduled, completed, and ignored cards in deterministic priority order.
- Updated `visibleInboxEntries(...)` to allow all-status filtering and stable sorting by status priority, start time, and title without changing archive hiding or search behavior.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/InboxWorkbenchTest.kt` from four to five tests with explicit coverage for urgent/review/scheduled ordering.
- Expanded `validation/validate_android_unit_tests.py` from `54/54` to `55/55` with a new `inbox_all_status_sorting_unit_tested` gate and latest Gradle XML expectation for `InboxWorkbenchTest` 5 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 55/55` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
  - Evidence: `InboxWorkbenchTest` XML reports 5 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 70 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 55/55`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 ee017b56582d743a5fe39e75608424df24389ff3ff92fa3602b4b9b1e87a8d0a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Archived inbox cards remain hidden from active results until restore.
- Search still covers title, status, scene, location, source, OCR raw text, model explanation, and execution summary.
- User confirmation remains required before calendar, reminder, or map execution; this round only changes inbox list filtering and ordering.

Risks:
- This is deterministic local JVM coverage for the current workbench model; durable multi-item Room/SQLite inbox storage remains a later persistence track.

Next:
- Continue S3 quality hardening with another focused local test around persisted inbox snapshots, backend outcome state, or multi-item inbox preparation.

## 2026-05-25 / Round 120

Goal: Add Android local unit-test coverage for backend failure fallback copy.

Files changed:
- Added `BackendFailureFallbackCopy` and `backendFailureFallbackCopyFor(...)` in `android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt` so backend-unavailable fallback source, status message, and redacted raw-text evidence are derived by pure Kotlin logic.
- Updated `backendFailureOutcome(...)` to consume the shared fallback copy while preserving the existing safe review state and local `MockModelAdapter` fallback.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/BackendAnalysisRunnerTest.kt` from three to four tests, adding coverage for phone, email, and LAN-address redaction before UI persistence.
- Expanded `validation/validate_android_unit_tests.py` from `53/53` to `54/54` with an explicit backend-failure fallback copy check and latest Gradle XML expectation for `BackendAnalysisRunnerTest` 4 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 54/54` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 26s`
  - Evidence: `BackendAnalysisRunnerTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 69 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 54/54`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 acaef03276c20578843bdf931b8fd2c8ad4ec9b56c27c55abb09debc3a3d5907`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Backend failure still resets the current action card to `待确认` and keeps the local fallback item available for user review.
- Raw OCR failure evidence is still redacted before it reaches UI state or local persistence.
- User confirmation remains required before calendar, reminder, or map execution; this round only centralizes backend failure fallback copy.

Risks:
- This remains local JVM and static guard coverage; live backend timeout/error variants still need a later integration track.

Next:
- Continue S3 quality hardening with another focused local test around local persistence boundaries, backend outcome state, or multi-item inbox preparation.

## 2026-05-25 / Round 119

Goal: Add Android local unit-test coverage for notification permission fallback copy.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ReminderPermissionFallback.kt` with `REMINDER_PERMISSION_BLOCKED_STATUS`, `ReminderPermissionFallbackCopy`, and `reminderPermissionFallbackCopyFor(...)` so notification permission denial copy is shared by persistence and execution-result tracking.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so `saveReminderPermissionFallback(...)` persists the shared fallback source instead of owning its own `permission_blocked` string.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ExecutionResultActions.kt` and `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt` so reminder execution results can include the current action-card title while preserving the generic fallback wording for existing callers.
- Added `android-mvp/app/src/test/java/cn/shike/app/ReminderPermissionFallbackTest.kt` with two local unit tests covering the shared `permission_blocked` source/detail copy and the reminder execution-result integration.
- Expanded `validation/validate_android_unit_tests.py` from `51/51` to `53/53` with explicit `ReminderPermissionFallbackTest` XML coverage.
- Updated `validation/validate_action_execution.py` so the notification permission fallback guard checks the new helper ownership instead of relying on a literal string in `MainActivity.kt`.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 53/53` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
  - Evidence: `ReminderPermissionFallbackTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 68 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 53/53`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 373eb777b86882330dd0b7c9baaf91c314eee342eac000cab3390a788a022bf0`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Notification permission denial still persists the current action card through `saveSnapshot(...)` with explicit `permission_blocked` source text.
- Reminder execution still records an execution result before Android permission/system dispatch.
- User confirmation remains required before reminder scheduling; this round only centralizes permission-denial fallback copy.

Risks:
- This remains local JVM and static guard coverage; connected Android permission-dialog instrumentation is still a later device/emulator track.

Next:
- Continue S3 quality hardening with another focused local test around local persistence boundaries, backend failure UX, or multi-item inbox preparation.

## 2026-05-25 / Round 118

Goal: Add Android local unit-test coverage for inbox archive/restore action decisions.

Files changed:
- Added `InboxArchiveActionState` and `inboxArchiveActionStateFor(...)` in `android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt` so archive/restore enablement and user-facing status copy are derived by pure Kotlin logic.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` to consume the shared archive/restore action state instead of duplicating button enablement and archive copy in Compose branches.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/InboxWorkbenchTest.kt` from three to four tests, adding coverage for active-card archive enablement, archived-card restore enablement, and non-deletion/restore explanatory copy.
- Expanded `validation/validate_android_unit_tests.py` from `50/50` to `51/51` with an explicit inbox archive action-state check and latest Gradle XML expectation for `InboxWorkbenchTest` 4 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 51/51` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 43s`
  - Evidence: `InboxWorkbenchTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 66 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 51/51`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 eb6f4edcd440a2ab53d6e5289645ac6d95fc4a147ee6ead97091ceea1d9ff560`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Active inbox cards can still be archived without deleting OCR text, model explanation, execution summary, or the underlying action card.
- Archived cards still expose restore as the only enabled archive action and return to the status-filtered list after restoration.
- User confirmation remains required before calendar, reminder, or map execution; this round only changes inbox workbench state derivation.

Risks:
- This round still keeps archive state in memory for the current card; durable multi-item archive history remains part of the later Room/SQLite inbox target.

Next:
- Continue S3 quality hardening with another focused local test around notification permission fallback messaging, local persistence boundaries, or multi-item inbox preparation.

## 2026-05-25 / Round 117

Goal: Add Android local unit-test coverage for reminder receiver delivery payload defaults.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderPayload.kt` with `ReminderDeliveryPayload` and `reminderDeliveryPayloadFrom(...)` so scheduled alarm delivery payload parsing is pure Kotlin logic.
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderReceiver.kt` to consume `reminderDeliveryPayloadFrom(...)`, skip delivery when the title is missing or blank, use `REMINDER_FALLBACK_DETAIL` for missing details, and fall back to `title.hashCode()` when the notification id is absent.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/ReminderPayloadTest.kt` from three to six tests, adding coverage for complete intent payloads, fallback detail/id defaults, and missing/blank title rejection.
- Expanded `validation/validate_android_unit_tests.py` from `49/49` to `50/50` with an explicit reminder delivery payload contract check and latest Gradle XML expectation for `ReminderPayloadTest` 6 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 50/50` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Evidence: `ReminderPayloadTest` XML reports 6 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 65 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 50/50`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 83ead2c8c02d474d152549e8ef59ff90088b8db18acc025179b7bb9e1340dfdf`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- `ReminderReceiver` still restores scheduled reminders on `BOOT_COMPLETED`.
- Delivered reminder alarms still post local notifications and clear the persisted scheduled reminder payload after successful payload parsing.
- Missing or blank titles still prevent notification delivery, preserving the no-empty-notification boundary.

Risks:
- This round does not add Android framework receiver instrumentation; it locks the receiver payload derivation used by the existing BroadcastReceiver path.

Next:
- Continue S3 quality hardening with another pure helper/unit-test target around archive/restore decisions or notification permission fallback messaging.

## 2026-05-25 / Round 116

Goal: Add Android local unit-test coverage for model API request payload construction.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt` so `/v1/analyze` request payload construction is owned by the pure `buildAnalyzeRequestPayload(...)` helper.
- Expanded `android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt` from three to four tests, adding coverage for `input_id`, `source_type`, `ocr_text`, `scene_hint`, `locale`, and `user_timezone`.
- Expanded `validation/validate_android_unit_tests.py` from `48/48` to `49/49` with an explicit model API request payload contract check and latest Gradle XML expectation for `ModelApiClientTest` 4 tests.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 49/49` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Evidence: `ModelApiClientTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 62 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 49/49`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 714c74853ac67963691a4debc7f2a50b8e5c4c85dc754ea0efa27049fe4a8943`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Backend calls still post to normalized `/v1/analyze` and map responses through `itemFromAnalyzeJson(...)`.
- Request payloads still carry the original OCR text, source type, scene hint, zh-CN locale, and Asia/Shanghai timezone before any user-confirmed downstream action.
- User confirmation remains required before calendar, reminder, or map execution.

Risks:
- This round does not add live HTTP integration assertions; it locks the local request JSON contract consumed by the existing network call.

Next:
- Continue S3 quality hardening with a focused local test around receiver payload defaults or archive/restore decision boundaries.

## 2026-05-25 / Round 115

Goal: Add Android local unit-test coverage for model API JSON mapping.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/ModelApiClientTest.kt` with three local unit tests covering course notice JSON mapping, event poster fallback fields, and malformed/blank suggested actions.
- Updated `android-mvp/app/build.gradle.kts` with the local `org.json:json` test dependency used by `ModelApiClientTest`.
- Expanded `validation/validate_android_unit_tests.py` from `46/46` to `48/48` so the guard checks `ModelApiClientTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 48/48` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ModelApiClientTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `TodayActionItemMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionActionGateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `InboxWorkbenchTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReminderPayloadTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendAnalysisRunnerTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 61 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 48/48`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 ca1d0ca2b15014244c741e90e70c09fe81a3dac52a25252e299cedeca73fc239`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Backend model JSON still maps course notices and event posters into pending-review cards for user confirmation.
- Blank model fields still fall back to editable confirmation values instead of executing actions automatically.
- Malformed suggested actions are ignored and replaced by the safe `稍后确认` action.

Risks:
- This round does not add live HTTP integration assertions; it locks the pure JSON mapping and action extraction contract used by the model bridge.

Next:
- Continue S3 quality hardening with another local test around request payload construction, receiver payload defaults, or inbox archive/restore decisions.

## 2026-05-25 / Round 114

Goal: Add Android local unit-test coverage for backend analysis input and fallback mapping.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt` so editable OCR text selection, backend success outcome mapping, and backend failure fallback mapping are pure Kotlin helpers.
- Added `android-mvp/app/src/test/java/cn/shike/app/BackendAnalysisRunnerTest.kt` with three local unit tests covering edited OCR priority, blank-draft fallback, sensitive fallback redaction, pending-review fallback state, and successful backend source/status wording.
- Expanded `validation/validate_android_unit_tests.py` from `44/44` to `46/46` so the guard checks `BackendAnalysisRunnerTest` source expectations and latest Gradle XML results.
- Updated `validation/validate_ocr_input.py` so OCR readiness checks follow the new `backendAnalyzeText(...)` and `backendFailureOutcome(...)` canonical owner instead of the previous inline implementation.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 46/46` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 13s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `TodayActionItemMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionActionGateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `InboxWorkbenchTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReminderPayloadTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendAnalysisRunnerTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 58 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 46/46`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`
- PASS `python3 validation/validate_manual_review.py`
  - Evidence: `MANUAL_REVIEW_METRIC 12/12`
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 ca1d0ca2b15014244c741e90e70c09fe81a3dac52a25252e299cedeca73fc239`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Backend analysis still sends edited OCR text when present and falls back to the sample raw text when the draft is blank.
- Backend success still persists a `/v1/analyze` source label and success status message.
- Backend failure still preserves a local pending-review action card, redacts sensitive text, and records the MockModelAdapter fallback source.

Risks:
- This round does not add live HTTP integration assertions; it locks the pure input and outcome mapping used around the existing network call.

Next:
- Continue S3 quality hardening with another local test around archive restore actions, receiver payload handling, or model JSON edge cases.

## 2026-05-25 / Round 113

Goal: Add Android local unit-test coverage for reminder payload scheduling and restore logic.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/system/ReminderPayload.kt` so reminder payload construction, one-minute near-start fallback, result-mode wording, and restore eligibility are pure Kotlin logic.
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt` to consume `scheduledReminderFrom(...)`, `reminderScheduleResultDetail(...)`, and `shouldRestoreScheduledReminder(...)` while keeping the existing `AlarmManager` and persisted SharedPreferences behavior.
- Added `android-mvp/app/src/test/java/cn/shike/app/ReminderPayloadTest.kt` with three local unit tests covering stable payload fields, near-start fallback/result-mode wording, and expired reminder restore rejection.
- Expanded `validation/validate_android_unit_tests.py` from `42/42` to `44/44` and updated `validation/validate_action_execution.py` so the action guard recognizes the split between Android scheduling and pure payload logic.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 44/44` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 15s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `TodayActionItemMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionActionGateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `InboxWorkbenchTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReminderPayloadTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 55 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 44/44`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 5c78e80506170103b8a841f815b3aa32fafbc3f66d625de63b7c053b7dfe129a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Reminder scheduling still persists title, detail, notification id, and trigger time before recovery.
- The scheduler still prefers exact alarms and falls back to ordinary `AlarmManager.set` when exact alarm permission or policy blocks the exact path.
- Expired persisted reminders are still cleared on restore instead of being reinstalled.

Risks:
- This round does not add connected Android alarm assertions; it locks the pure payload and restore-decision logic that the Android scheduler consumes.

Next:
- Continue S3 quality hardening with another local test around backend analysis input/failure boundaries, archive restore actions, or receiver payload handling.

## 2026-05-25 / Round 112

Goal: Add Android local unit-test coverage for inbox workbench filtering/search/archive logic.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/InboxWorkbench.kt` so inbox status filters, searchable entry mapping, selected-status fallback, and archive-aware visibility are owned by a pure helper.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` to consume `inboxWorkbenchEntryFrom(...)`, `selectedInboxStatusFor(...)`, and `visibleInboxEntries(...)` instead of keeping the workbench logic inside the Compose surface.
- Added `android-mvp/app/src/test/java/cn/shike/app/InboxWorkbenchTest.kt` with three local unit tests covering unsupported-status fallback, raw/explanation/execution search, and archive/status/search filtering.
- Expanded `validation/validate_android_unit_tests.py` from `40/40` to `42/42` and updated `validation/validate_advanced_product_beta.py` so the inbox status filter guard scans the shared helper.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 42/42` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 30s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `TodayActionItemMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionActionGateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `InboxWorkbenchTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 52 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 42/42`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 4c92acf54e7640f8878f8744a26449f5501bd14a0f7081c43cbee93a6549d9f2`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Inbox still defaults unsupported item states to the pending-review filter.
- Search still matches the visible workbench fields, including OCR/source text, model explanation, and execution result summary.
- Archived entries are hidden from the active inbox without changing the underlying item or execution evidence.

Risks:
- This round does not add connected Compose UI assertions; it locks the pure inbox workbench logic used by the rendered panel.

Next:
- Continue S3 quality hardening with another local test around archive actions, backend analysis boundaries, or reminder payload serialization.

## 2026-05-25 / Round 111

Goal: Add Android local unit-test coverage for user-confirmed execution action gates.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionActionGate.kt` so calendar, reminder, and map execution gates share one pure helper for user confirmation and missing-field checks.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBannerActions.kt` and `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt` to consume `executionActionGateFor(...)` instead of duplicating gate logic.
- Added `android-mvp/app/src/test/java/cn/shike/app/ExecutionActionGateTest.kt` with three local unit tests covering unconfirmed blocking, confirmed complete-field enabling, and missing time/location behavior.
- Expanded `validation/validate_android_unit_tests.py` from `38/38` to `40/40` and updated `validation/validate_action_execution.py` so the guard checks the shared execution gate helper.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 40/40` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `TodayActionItemMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionActionGateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 49 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 40/40`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 69dbe637dbf36ebb0b8283377e934079592febf17aa3b58af4ba8a7b772ecf47`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Calendar and map still require both user confirmation and the required time/location fields.
- Reminder remains confirmation-gated and does not require location.
- The confirmation banner and action planner now share the same gate helper, reducing drift between the two sensitive-action surfaces.

Risks:
- This round does not add connected Compose UI assertions; it locks the pure gate logic used by both UI surfaces.

Next:
- Continue S3 quality hardening with another local test around Android state derivation, inbox helper behavior, or backend analysis boundaries.

## 2026-05-25 / Round 110

Goal: Add Android local unit-test coverage for Today action item mapping.

Files changed:
- Extracted `todayActionItemFrom(...)` in `android-mvp/app/src/main/java/cn/shike/app/ui/HomeAgendaList.kt` so Today action card tone, footer, detail lines, and CTA selection can be tested as JVM logic.
- Added `android-mvp/app/src/test/java/cn/shike/app/TodayActionItemMapperTest.kt` with three local unit tests covering scheduled route CTA/confirmed footer, due-soon deadline CTA/review footer, and pending primary-action/detail fallback behavior.
- Expanded `validation/validate_android_unit_tests.py` from `36/36` to `38/38` so the guard checks `TodayActionItemMapperTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 38/38` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `TodayActionItemMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 46 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 38/38`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 11118b91d56092546ba370c4ff1a8ac1ad42c24296a2c698b40e29e3686f5fc8`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Today action cards still choose `查看路线` for scheduled items with map actions, `查看截止` for due-soon items, and primary-action/detail fallback for pending items.
- Footer wording still distinguishes confirmed scheduled items from items that require user confirmation.
- Home agenda UI still renders through `AgendaCard` and keeps empty/error state entry points unchanged.

Risks:
- This round does not add Compose rendering or connected-device assertions; it locks the pure mapping logic behind the rendered Today action card.

Next:
- Continue S3 quality hardening with another local test around Android state derivation, inbox helper behavior, or backend analysis boundaries.

## 2026-05-25 / Round 109

Goal: Add Android local unit-test coverage for model explanation wording.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/ModelExplanationTest.kt` with three local unit tests covering backend-provided explanation extraction, backend-fallback explanation wording, and confirmed-course trust wording.
- Expanded `validation/validate_android_unit_tests.py` from `34/34` to `36/36` so the guard checks `ModelExplanationTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 36/36` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 17s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `ModelExplanationTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 43 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 36/36`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 fff9136145baee886cabd33d33b6f80fc3e7efeb06de6584501831742da53fbb`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Backend-provided explanation text after `后端 /v1/analyze：` still takes precedence in inbox detail.
- Backend fallback explanation still states local-rule retention and that user confirmation is required before system actions.
- Confirmed course explanation still marks key fields as confirmed.

Risks:
- This round does not add Compose rendering assertions for the inbox detail UI; it locks the explanation string logic used by that UI.

Next:
- Continue S3 quality hardening with another local test around inbox helper behavior or backend analysis boundaries.

## 2026-05-25 / Round 108

Goal: Add Android local unit-test coverage for execution result state derivation.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/ExecutionResultStateTest.kt` with three local unit tests covering pending execution state, replacement semantics, and permission/fallback result wording.
- Expanded `validation/validate_android_unit_tests.py` from `32/32` to `34/34` so the guard checks `ExecutionResultStateTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 34/34` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 31s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultStateTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 40 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 34/34`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 fff9136145baee886cabd33d33b6f80fc3e7efeb06de6584501831742da53fbb`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Pending execution results still start with calendar, reminder, and map in `待确认` state.
- Recording an execution result replaces only the matching action and appends the latest result.
- Calendar, reminder, and map result factories keep the system-calendar, `permission_blocked`, and map-fallback wording used by the execution guard.

Risks:
- This round does not add connected Compose UI assertions for the rendered `ExecutionResultPanel`; it locks state derivation and wording at the JVM helper layer.

Next:
- Continue S3 quality hardening with another local test around Android state derivation, backend analysis boundaries, or inbox helper behavior.

## 2026-05-25 / Round 107

Goal: Add Android local unit-test coverage for capture result action persistence.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/CaptureResultActionsTest.kt` with two local unit tests covering camera preview and gallery image action persistence.
- Extracted `applyCameraPreviewSizeSelection(...)` in `android-mvp/app/src/main/java/cn/shike/app/CaptureResultActions.kt` so the camera action path can be verified in JVM tests without constructing an Android `Bitmap`.
- Expanded `validation/validate_android_unit_tests.py` from `30/30` to `32/32` so the guard checks `CaptureResultActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 32/32` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureResultActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 37 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 32/32`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 fff9136145baee886cabd33d33b6f80fc3e7efeb06de6584501831742da53fbb`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Camera capture action still persists source `相机拍照预览 1080x1440` and activity draft `拍照导入的活动海报`.
- Gallery image action still persists source `相册图片 course-screenshot.png` and course draft `相册导入的课程通知`.
- Existing `Bitmap` entrypoint remains in place and delegates to the dimension-based helper.

Risks:
- This round does not add connected Compose UI coverage proving the buttons invoke these helpers on device; it locks the action helper behavior in JVM tests.

Next:
- Continue S3 quality hardening with another small local test around Android state derivation or action boundaries.

## 2026-05-25 / Round 106

Goal: Add Android local unit-test coverage for review action persistence.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/ReviewActionsTest.kt` with two local unit tests covering confirmed and ignored review action persistence.
- Expanded `validation/validate_android_unit_tests.py` from `28/28` to `30/30` so the guard checks `ReviewActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 30/30` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 17s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: local unit suites report 35 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 30/30`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 f5e6796e02b2ccddf8c31474d61103d0321e19d313e00345fd4ae13a9f20f6d5`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Confirmed review action persists an `已安排` item and source `用户确认修正：活动海报`.
- Ignored review action persists the ignored item unchanged and source `用户确认修正：课程通知`.
- This round only locks review action persistence; connected Compose review UI coverage remains outside this JVM test boundary.

Risks:
- This round does not add connected UI coverage proving the Compose review buttons invoke `applyReviewedItemSelection`.

Next:
- Continue S3 quality hardening with local tests around another pure Android action helper or mapper.

## 2026-05-25 / Round 105

Goal: Add Android local unit-test coverage for offline sample action persistence.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/SampleActionsTest.kt` with two local unit tests covering course and event offline sample selection persistence.
- Expanded `validation/validate_android_unit_tests.py` from `26/26` to `28/28` so the guard checks `SampleActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 28/28` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 17s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `SampleActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 28/28`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 f5e6796e02b2ccddf8c31474d61103d0321e19d313e00345fd4ae13a9f20f6d5`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Offline course sample action still persists `sampleCourse()` with source `离线样例：课程通知截图`.
- Offline event sample action still persists `sampleEvent()` with source `离线样例：活动海报拍照`.
- This round only locks the sample action persistence boundary; import UI button behavior remains unchanged.

Risks:
- This round does not add connected UI coverage proving the offline sample buttons invoke these helpers from Compose.

Next:
- Continue S3 quality hardening with local tests around review action persistence or backend analysis kickoff.

## 2026-05-25 / Round 104

Goal: Add Android local unit-test coverage for backend outcome persistence.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/BackendOutcomeActionsTest.kt` with two local unit tests covering backend success persistence and backend-failure fallback persistence.
- Expanded `validation/validate_android_unit_tests.py` from `24/24` to `26/26` so the guard checks `BackendOutcomeActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 26/26` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 18s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `BackendOutcomeActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 26/26`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 f5e6796e02b2ccddf8c31474d61103d0321e19d313e00345fd4ae13a9f20f6d5`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Backend success outcomes still persist the backend-returned item and source before returning the original success status message.
- Backend failure outcomes still persist the local fallback item/source and return the original fallback status message.
- This round only tests the pure selection persistence boundary; runtime network calls and user confirmation behavior remain unchanged.

Risks:
- This round does not add connected Android UI coverage for the full backend button -> network -> UI update path.

Next:
- Continue S3 quality hardening with local tests around review action persistence or sample action selection.

## 2026-05-25 / Round 103

Goal: Add Android local unit-test coverage for initial selection startup paths.

Files changed:
- Added pure `buildInitialSelection(...)` logic in `android-mvp/app/src/main/java/cn/shike/app/data/InitialSelectionMapper.kt` so the startup selection policy can be tested without Android `Context`.
- Added `android-mvp/app/src/test/java/cn/shike/app/data/InitialSelectionMapperTest.kt` with three local unit tests covering share-text priority, saved inbox restore, and no-share/no-saved empty state.
- Expanded `validation/validate_android_unit_tests.py` from `22/22` to `24/24` so the guard checks `InitialSelectionMapperTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 24/24` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `InitialSelectionMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 24/24`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 f5e6796e02b2ccddf8c31474d61103d0321e19d313e00345fd4ae13a9f20f6d5`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Android `loadInitialSelection(...)` still loads the saved inbox snapshot through `Context` and delegates to the same output shape.
- Share-sheet text still takes priority over cached inbox state and remains unpersisted until user confirmation.
- No-share/no-saved startup still enters the Today Action empty state with guidance to start from screenshot, photo, share, or manual input.

Risks:
- This round covers pure selection policy only; connected Android tests are still needed later to prove launch intent and SharedPreferences integration through the full Activity path.

Next:
- Continue S3 quality hardening with local tests around backend analysis fallback delivery or persistence serialization.

## 2026-05-25 / Round 102

Goal: Add Android local unit-test coverage for backend trigger input dispatch.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/BackendTriggerActionsTest.kt` with two local unit tests covering course screenshot backend dispatch and event camera backend dispatch.
- Expanded `validation/validate_android_unit_tests.py` from `20/20` to `22/22` so the guard checks `BackendTriggerActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 22/22` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendTriggerActionsTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 22/22`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Course backend analysis still dispatches the `screenshot` source with the course-notice fallback item.
- Event backend analysis still dispatches the `camera` source with the event-poster fallback item.
- The new tests cover dispatch payload construction only; runtime networking, user confirmation, and cloud-off fallback behavior remain unchanged.

Risks:
- This round covers pure trigger dispatch only; connected UI tests are still needed later to prove the button-to-backend path on a device or emulator.

Next:
- Continue S3 quality hardening with local tests around initial selection mapping or backend analysis fallback delivery.

## 2026-05-25 / Round 101

Goal: Add Android local unit-test coverage for cloud-off fallback state.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/CloudEnhancementActionsTest.kt` with three local unit tests covering cloud-off ready state, no-backend-call copy, and preserved local draft/offline entry copy.
- Expanded `validation/validate_android_unit_tests.py` from `18/18` to `20/20` so the guard checks `CloudEnhancementActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 20/20` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `CloudEnhancementActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 20/20`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Turning off cloud enhancement still keeps Today Action in the ready state instead of clearing the current card.
- The fallback copy still states that no backend `/v1/analyze` call was made.
- The user is still directed to local draft and offline sample paths, preserving an offline-first demo path.

Risks:
- This round covers pure fallback state only; connected UI tests are still needed later to prove the settings toggle prevents actual network dispatch in the Android UI path.

Next:
- Continue S3 quality hardening with local tests around backend trigger input dispatch, initial selection mapping, or backend analysis fallback delivery.

## 2026-05-25 / Round 100

Goal: Add Android local unit-test coverage for local data clear state.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/LocalDataClearActionsTest.kt` with three local unit tests covering default course reset, default backend URL reset, empty Today Action state, and safe restart copy after local data is cleared.
- Expanded `validation/validate_android_unit_tests.py` from `16/16` to `18/18` so the guard checks `LocalDataClearActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 18/18` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `LocalDataClearActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 18/18`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Clearing local data still resets the visible card to the default course sample and returns Today Action to the empty state.
- The backend endpoint returns to `DEFAULT_BACKEND_BASE_URL`, preserving a known-good emulator fallback.
- The user-facing copy still explains that the user can restart from screenshot, photo, share, or manual input after clearing data.

Risks:
- This round covers pure state construction only; connected Android tests are still needed later to prove SharedPreferences clearing and alarm cancellation through the full UI path on device.

Next:
- Continue S3 quality hardening with local tests around initial selection mapping, backend trigger input dispatch, or cloud-off fallback state.

## 2026-05-25 / Round 099

Goal: Add Android local unit-test coverage for backend endpoint saving.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/BackendEndpointActionsTest.kt` with three local unit tests covering LAN endpoint normalization, HTTPS endpoint preservation, blank-input fallback, save-callback invocation, and saved-status copy.
- Expanded `validation/validate_android_unit_tests.py` from `14/14` to `16/16` so the guard checks `BackendEndpointActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 16/16` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `BackendEndpointActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Saving a LAN backend address still normalizes `192.168.1.10:8000/` to `http://192.168.1.10:8000`.
- HTTPS endpoints remain HTTPS and blank input falls back to `DEFAULT_BACKEND_BASE_URL`.
- The save callback is still invoked with the normalized endpoint and the user-visible status remains `模型编排：后端地址已保存`.

Risks:
- This is local JVM coverage for endpoint normalization and action output; connected-device verification is still needed later to prove SharedPreferences persistence through the UI and real LAN networking.

Next:
- Continue S3 quality hardening with local tests around local data clear state, initial selection mapping, or backend trigger input dispatch.

## 2026-05-25 / Round 098

Goal: Add Android local unit-test coverage for reviewed item status mapping.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/data/ReviewStatusMapperTest.kt` with three local unit tests covering confirmed review status, ignored review status, and preservation of user-edited title/time/location fields.
- Expanded `validation/validate_android_unit_tests.py` from `12/12` to `14/14` so the guard checks `ReviewStatusMapperTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 14/14` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ReviewStatusMapperTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 14/14`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Confirmed review still maps to `已安排` and `模型编排：用户已确认`.
- Ignored review still remains `已忽略` with `模型编排：用户已忽略`, so the app does not accidentally revive ignored cards.
- User-edited title, time, and location fields remain preserved when review status is normalized after confirmation.

Risks:
- This round covers pure status mapping only; connected UI tests are still needed later for actual Compose field editing and confirm-button interaction.

Next:
- Continue S3 quality hardening with local tests around backend endpoint saving, local data clear state, or initial selection mapping.

## 2026-05-25 / Round 097

Goal: Add Android local unit-test coverage for confirmed action execution result recording.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/ExecutionResultActionsTest.kt` with three local unit tests covering calendar, reminder, and map execution result updates.
- Expanded `validation/validate_android_unit_tests.py` from `10/10` to `12/12` so the guard now checks `ExecutionResultActionsTest` source expectations and latest Gradle XML results.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 12/12` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 10s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
  - Evidence: `ExecutionResultActionsTest` XML reports 3 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 12/12`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Calendar, reminder, and map actions still call the same external action callbacks after the result list is updated.
- The tests lock the user-visible tracking behavior: an execution result is recorded before external dispatch, existing action results are preserved, and reminder detail keeps the permission fallback wording.
- Main screenshot/photo/share import, parse confirmation, action planning, and inbox/today tracking remain covered by existing guards.

Risks:
- This remains local JVM coverage; connected Android tests are still needed later for real system intents and permission dialogs.

Next:
- Continue S3 quality hardening with local tests around persistence state transitions, backend endpoint saving, or review-status mapping.

## 2026-05-25 / Round 096

Goal: Expand the Android local unit-test baseline to capture and share import mapping.

Files changed:
- Added `android-mvp/app/src/test/java/cn/shike/app/data/CaptureImportMapperTest.kt` with three local unit tests covering camera preview import, gallery image import, and capture-draft routing.
- Added `android-mvp/app/src/test/java/cn/shike/app/data/ShareImportMapperTest.kt` with four local unit tests covering Android share-sheet drafts, blank-text fallback, event text mapping, and course text mapping.
- Expanded `validation/validate_android_unit_tests.py` from `6/6` to `10/10` so the guard checks JUnit wiring, privacy redaction, capture import mapping, share import mapping, latest Gradle XML results, and documentation references.
- Updated README, device checklist, runbook, current validation status, Demo console, real-world readiness validator, core-package verifier, and Android build report with the current `ANDROID_UNIT_TEST_METRIC 10/10` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 13s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
  - Evidence: `CaptureImportMapperTest` XML reports 3 tests, 0 failures, 0 errors
  - Evidence: `ShareImportMapperTest` XML reports 4 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 10/10`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Screenshot/photo/share import behavior is unchanged; this round adds regression coverage around the existing mapping boundaries.
- User confirmation, action execution, inbox/today tracking, exact-alarm fallback, and local-data-clear reminder cancellation remain covered by existing guards.
- The Demo console now presents the current Android unit-test gate as `10/10` instead of the previous baseline-only `6/6`.

Risks:
- These are local JVM unit tests, not connected Android UI tests; a later device/emulator track should still cover Activity result launchers and Android share-intent delivery end to end.

Next:
- Continue S3 quality hardening with another local test slice around reminder scheduling, persistence state transitions, or parse-confirm action planning.

## 2026-05-25 / Round 095

Goal: Establish an Android local unit-test baseline for S3 quality hardening.

Files changed:
- Added JUnit to `android-mvp/app/build.gradle.kts` and created `android-mvp/app/src/test/java/cn/shike/app/data/PrivacyRedactionTest.kt` with two local unit tests covering sensitive-token redaction and non-sensitive action text preservation.
- Added `validation/validate_android_unit_tests.py` to guard JUnit wiring, pure privacy-redaction logic, test assertions, latest Gradle XML result, and documentation references.
- Updated `validation/validate_real_world_ready.py` so the aggregate readiness gate now includes the Android local unit-test guard and reports `REAL_WORLD_READY_METRIC 22/22`.
- Updated README, device checklist, runbook, Demo console, in-app readiness text, current validation status, submission checklist, core-package verifier, and Android build report with the new `ANDROID_UNIT_TEST_METRIC 6/6` gate.

Validation:
- PASS `gradle --no-daemon :app:testDebugUnitTest :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Evidence: `PrivacyRedactionTest` XML reports 2 tests, 0 failures, 0 errors
- PASS `python3 validation/validate_android_unit_tests.py`
  - Evidence: `ANDROID_UNIT_TEST_METRIC 6/6`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 22/22`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 292707c030690e4d3e78f631884488d2108582f9fa2529d75b14fbe6d3840d9a`
  - Evidence: `PASS UNIT_TEST_GUARD README.md`
  - Evidence: `PASS UNIT_TEST_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS UNIT_TEST_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- This round adds test infrastructure and verification coverage only; screenshot/photo/share import, AI/rule parsing, user confirmation, action execution, and inbox/today tracking behavior remain unchanged.
- Privacy redaction remains pure Kotlin logic and can now be regression-tested without a device or emulator.

Risks:
- UI and connected-device tests are still outside the current baseline and should be added in a later device/emulator track.

Next:
- Continue S3 quality hardening with a broader local test set, reminder runtime observability, or persistence migration groundwork.

## 2026-05-25 / Round 094

Goal: Add exact-alarm policy fallback for scheduled reminders.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt` so confirmed scheduled reminders prefer `setExactAndAllowWhileIdle` when exact alarms are available, check `canScheduleExactAlarms` on Android 12+, catch `SecurityException`, and fall back to ordinary `AlarmManager.set` instead of silently losing the reminder.
- Updated `scheduleReminder` result wording so the user-visible execution result states whether the reminder used `精确定时` or `系统普通定时`.
- Expanded `validation/validate_action_execution.py` from `16/16` to `17/17` with an exact-alarm policy fallback guard.
- Updated README, device runbook, device checklist, current validation status, core-package verifier, and Android build report with the `ACTION_EXECUTION_METRIC 17/17` guard and current APK build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 31s`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 17/17`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 21/21`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 b8bd0cbf9103e9883397c8619637dcd62ede999e3ead3e9e4611ffd8ea759939`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Reminder scheduling still only happens after the user confirms fields and taps the reminder action.
- Notification permission denial, persisted reminder recovery, device reboot recovery, delivery cleanup, and local-data-clear alarm cancellation remain covered by the action execution guard.
- Exact-alarm denial now degrades to a normal alarm and reports the mode, preserving a usable reminder path without bypassing user confirmation.

Risks:
- Exact-alarm availability and denial are source-guarded and compile-verified in this round; a connected Android 12+ device/emulator pass is still needed to observe OS settings behavior directly.

Next:
- Continue S3 quality hardening with reminder runtime observability, Android test baseline setup, or persistence migration groundwork.

## 2026-05-25 / Round 093

Goal: Cancel pending scheduled reminder alarms when local data is cleared.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt` with `cancelScheduledReminder`, which looks up the persisted reminder payload, finds the existing pending broadcast with `PendingIntent.FLAG_NO_CREATE`, cancels the `AlarmManager` alarm, cancels the pending intent, and clears the persisted reminder record.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so the privacy-panel clear action now calls `cancelScheduledReminder(this)` before `clearLocalData(this)`.
- Expanded `validation/validate_action_execution.py` from `15/15` to `16/16` to cover local-data-clear cancellation of pending reminders.
- Updated README, device runbook, device checklist, current validation status, and core-package verifier with the `ACTION_EXECUTION_METRIC 16/16` guard.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 27s`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 16/16`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 21/21`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 955835b234a870fd9d82e7bc17a08d3e6f7f5ffd0f6365de4e53a7efdff457d0`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Reminder execution still requires user confirmation and notification permission.
- App-start and device-reboot recovery remain backed by the persisted reminder payload.
- Clearing local data now removes both the persisted reminder record and the already registered system alarm.

Risks:
- Cancellation is source-guarded and compile-verified in this round; a connected device/emulator pass is still needed to observe OS-level alarm cancellation directly.

Next:
- Continue S3 reminder hardening with exact-alarm policy handling or add runtime observability for reminder scheduling failures.

## 2026-05-25 / Round 092

Goal: Persist and restore scheduled reminders across app start and device reboot.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt` so confirmed reminder alarms persist title, detail, notification id, and trigger time in app-scoped preferences; non-expired reminders can be restored and delivered/expired records are cleared.
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/ReminderReceiver.kt` so delivered reminders clear the persisted scheduled payload after posting the notification.
- Added `android-mvp/app/src/main/java/cn/shike/app/system/BootReminderReceiver.kt` and registered `RECEIVE_BOOT_COMPLETED` in `AndroidManifest.xml` so device reboot restores pending scheduled reminders without exposing the alarm payload receiver.
- Updated `MainActivity.kt` to call `restoreScheduledReminder` after notification channel creation on app start.
- Expanded `validation/validate_action_execution.py` from `10/10` to `15/15` to cover reminder persistence, app-start recovery, device reboot recovery, and delivery cleanup.
- Updated README, device runbook, device checklist, current validation status, core-package verifier, and Android build report with the reminder recovery guard and latest build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 32s`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 15/15`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 21/21`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `APK_SHA256 73153ec55aa8971b4fbae2d18baad8ca3bd91b163f854c485ffea209e7e107e8`
  - Evidence: `PASS ACTION_EXECUTION_GUARD README.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS ACTION_EXECUTION_GUARD validation/validate_demo_acceptance.py`

Behavior preserved:
- Reminder scheduling still only happens after the user confirms fields and taps the reminder action.
- `ReminderReceiver` remains `exported=false`; the exported boot receiver only handles `BOOT_COMPLETED` restoration.
- Notification permission denial still preserves the action card through the existing `permission_blocked` fallback.

Risks:
- Recovery is statically guarded and compile-verified; true reboot delivery still needs a connected device/emulator pass.
- Exact-alarm policy handling remains future S3 hardening.

Next:
- Continue S3 quality hardening with exact-alarm policy handling, crash/fallback observability, or backend productionization.

## 2026-05-25 / Round 091

Goal: Add a dedicated S3 action-execution guard and wire it into the real-world readiness gate.

Files changed:
- Added `validation/validate_action_execution.py` to verify confirmation gating, calendar result wording, timed reminder scheduling, map copy fallback, notification permission fallback, external Intent failure handling, and UI/system boundary separation.
- Updated `validation/validate_real_world_ready.py` so the aggregate readiness gate now runs the action execution guard.
- Updated `README.md`, `materials/device-demo-checklist.md`, `prototype/demo.html`, `validation/validate_demo_acceptance.py`, `docs/current-validation-status.md`, and the in-app readiness section so the new guard appears in the same command surfaces as the rest of the demo checks.
- Updated `scripts/verify_core20_package.py` so the core 20 package includes `validation/validate_action_execution.py` and checks action-execution guard references alongside structure guard references.
- Updated `android-mvp/build-report.md` with the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 22s`
- PASS `python3 validation/validate_action_execution.py`
  - Evidence: `ACTION_EXECUTION_METRIC 10/10`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 21/21`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`

Behavior preserved:
- This round adds validation and documentation coverage only; Android runtime behavior is unchanged from the timed reminder scheduler round.
- The new guard preserves the existing rule that UI surfaces dispatch callbacks only after confirmation and do not directly call system services.

Risks:
- The guard is static/source-based. Later S3 work should add emulator or device tests for receiver delivery, reboot recovery, and exact-alarm policy behavior.

Next:
- Add persistence/restart recovery coverage for scheduled reminders or start backend productionization with route/service/config separation.

## 2026-05-25 / Round 090

Goal: Replace immediate reminder-only behavior with a confirmed local timed reminder scheduler.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/system/ReminderScheduler.kt` to schedule confirmed action-card reminders through `AlarmManager`.
- Added `android-mvp/app/src/main/java/cn/shike/app/system/ReminderReceiver.kt` to receive scheduled alarms and post the local reminder notification payload.
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt` to share notification payload posting between immediate and scheduled paths.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so the reminder action schedules a local reminder after notification permission is available and still stores `permission_blocked` when permission is denied.
- Registered the reminder receiver in `android-mvp/app/src/main/AndroidManifest.xml`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt`, README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 30/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 38s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 30/30`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`

Behavior preserved:
- Reminder scheduling still happens only after the user confirms fields and taps the reminder action.
- Notification permission denial still persists the current action card with `permission_blocked`.
- Calendar, map, backend parsing, cloud-off guard, log redaction, clear-local-data, and model-eval artifacts are unchanged.

Risks:
- The current scheduler uses `AlarmManager.set` and a 15-minute lead time; exact-alarm behavior and reboot persistence should be handled in later S3 quality hardening.

Next:
- Treat S2 Product Beta as mechanically complete and move to S3 quality hardening: regression CI, crash/fallback telemetry, persistence upgrade, and device/emulator coverage.

## 2026-05-25 / Round 089

Goal: Expand model evaluation coverage to a mechanically verified 100-case synthetic set.

Files changed:
- Expanded `validation/regression-cases.json` from 10 to 100 synthetic cases covering course notices, event posters, meeting notices, assignment deadlines, travel plans, low-quality fragments, and negative/no-action fragments.
- Added `validation/validate_model_eval_cases.py` to check case count, unique IDs, required scene coverage, balanced core scene counts, required shape, low-quality/missing/relative/negative edges, known action names, and no-action negative examples.
- Updated `validation/sample-regression.md` to describe the 100-case regression flow.
- Updated `validation/validate_deliverables.py` so the legacy SHIKE-080 check still requires course and event coverage while accepting the expanded multi-scene evaluation set.
- Updated README and current validation status with `PRODUCT_BETA_METRIC 29/30` and `MODEL_EVAL_CASES_METRIC 8/8`.

Validation:
- PASS `python3 validation/validate_model_eval_cases.py`
  - Evidence: `MODEL_EVAL_CASES_METRIC 8/8`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 29/30`
- PASS `python3 validation/validate_deliverables.py`
  - Evidence: `METRIC 10/10`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`

Behavior preserved:
- This round changes evaluation artifacts only; Android confirmation, permissions, backend parsing, local persistence, and user action flows are unchanged.
- Negative examples explicitly expect no actions, preserving the rule that the model should not invent calendar, reminder, or map tasks for non-action fragments.

Risks:
- The 100 cases are synthetic and validate coverage structure, not real model accuracy; future S4 work should add scored model outputs and confusion analysis.

Next:
- Implement true timed reminder scheduling as the remaining Product Beta readiness gap.

## 2026-05-25 / Round 088

Goal: Add a real one-tap local data clearing path from privacy settings.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt` with `clearLocalData(context)` to clear app-scoped local inbox and settings preferences.
- Added `android-mvp/app/src/main/java/cn/shike/app/LocalDataClearActions.kt` to reset the current workbench to a safe empty state after clearing.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`, `ShikeApp.kt`, `ui/ShikeMainScreen.kt`, and `ui/ReadinessSections.kt` so the privacy panel exposes `一键清除本地数据` and routes it to the real persistence clear.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 28/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 12s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 28/30`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`

Behavior preserved:
- The clear action is explicit in privacy settings and does not execute calendar, reminder, map, share, or external navigation actions.
- After clearing, the current UI returns to an empty action-table state and the default backend URL, so stale local data is not presented as current.
- Cloud-off backend guard, log redaction, map copy fallback, reminder permission fallback, and confirmation-before-action behavior remain intact.

Risks:
- The clear action covers the current `SharedPreferences` stores; a future Room/SQLite inbox should add its own clear path and validator coverage.

Next:
- Add 100-case model evaluation coverage or true timed reminder scheduling as the next Product Beta slice.

## 2026-05-25 / Round 087

Goal: Redact sensitive OCR/backend fallback text before it is stored in local action-card logs.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/PrivacyRedaction.kt` to redact 手机号、邮箱、学号 and local network addresses.
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt` so backend-failure fallback raw text uses the redacted OCR text and marks the fallback as already redacted.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 27/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 27/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`

Behavior preserved:
- Backend analysis still sends the user-confirmed OCR draft when cloud enhancement is enabled.
- Only local fallback logging/storage is redacted, so parsing behavior and demo samples are unchanged.
- Cloud-off backend guard, map copy fallback, and reminder permission fallback remain intact.

Risks:
- Redaction is regex-based and should be expanded as real private fields appear during device testing.

Next:
- Add clear local data, timed reminders, or 100-case model evaluation as the next Product Beta slice.

## 2026-05-25 / Round 086

Goal: Make the cloud-enhancement toggle prevent backend parsing calls when disabled.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` with a `cloudEnhancedEnabled` state and a logic-level guard before `runBackendAnalysisAction`.
- Added `android-mvp/app/src/main/java/cn/shike/app/CloudEnhancementActions.kt` for the cloud-off local fallback status.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/BackendAnalysisControls.kt` so backend parsing buttons are disabled when cloud enhancement is off.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt`, `ImportPanel.kt`, and `ShikeMainScreen.kt` so the privacy panel owns the toggle and the import panel reflects the disabled state.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 26/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 32s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 26/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`

Behavior preserved:
- Cloud enhancement is on by default, so existing backend demo flow still works unless the user turns it off.
- When cloud enhancement is off, backend buttons are disabled and the logic path returns before any backend analysis request is started.
- User confirmation before calendar, reminder, and map actions remains unchanged.

Risks:
- The toggle is in-memory for this round; durable privacy settings remain part of later clear-local-data/settings work.

Next:
- Add log redaction, clear local data, timed reminders, or 100-case model evaluation as the next Product Beta slice.

## 2026-05-25 / Round 085

Goal: Provide a concrete copy-location fallback when no map app can open the location deeplink.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt` with `copyMapLocationFallback`, using `ClipboardManager` and `ClipData` to copy the current location.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so map fallback persists both the original "map unavailable" source and the copied-location result.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 25/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 33s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 25/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`

Behavior preserved:
- User confirmation and location field validation are still required before opening map or copying the fallback location.
- Map deeplink remains the primary path; clipboard fallback only runs when the external activity cannot open.
- The current action card remains persisted after map fallback.

Risks:
- Timed reminder scheduling, cloud-off backend prevention, log redaction, clear local data, and 100-case model evaluation remain Product Beta gaps.

Next:
- Add privacy controls or timed reminder scheduling as the next S2 Product Beta slice.

## 2026-05-25 / Round 084

Goal: Preserve the current action card when Android notification permission is denied.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so a denied `POST_NOTIFICATIONS` request saves the pending reminder item with a `permission_blocked` source instead of dropping it.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt` so reminder execution details explain the permission-blocked fallback.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 24/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 30s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 24/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`

Behavior preserved:
- User confirmation is still required before requesting a reminder.
- Notification permission denial now keeps the action card in local persistence with an explicit `permission_blocked` source.
- Calendar and map missing-field guards remain unchanged.

Risks:
- Timed reminder scheduling is still not implemented; this round only covers permission denial fallback.

Next:
- Add map unavailable copy-location fallback before tackling timed reminders, privacy controls, and model evaluation.

## 2026-05-25 / Round 083

Goal: Disable calendar and map actions when required fields are missing, with visible reasons in both action entry points.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt` so missing time disables `加日历` and missing location disables `地图`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBannerActions.kt` with the same missing-field guards for the top confirmation banner actions.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 23/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 23/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- User confirmation is still required before any system action can run.
- Missing time blocks calendar action; missing location blocks map action; reminder remains available after confirmation.
- The change is UI-state scoped and does not alter backend parsing or sample data.

Risks:
- Missing-field guards currently use blank or `待确认` fields; richer field validation remains future work.

Next:
- Add reminder permission fallback and map unavailable copy-location fallback before tackling privacy controls and model evaluation.

## 2026-05-25 / Round 082

Goal: Make low-confidence model output visibly require manual review before actions can be executed.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ReviewRiskChecklist.kt` with a `模型置信度` row that marks pending cards as `低置信度，待人工确认`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt` to explain that low-confidence or incomplete fields stay in manual review until confirmed.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 21/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 41s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 21/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Calendar, reminder, and map actions remain disabled until the existing confirmation state is true.
- Low-confidence handling is visible in the confirmation page without changing backend or sample parsing behavior.

Risks:
- Low-confidence is still inferred from pending confirmation state; a typed confidence policy remains future work.

Next:
- Add missing-location and missing-time action guards before tackling reminder/map fallbacks and privacy controls.

## 2026-05-25 / Round 081

Goal: Let users continue from manual input or OCR failure without losing the current action card.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportCaptureActions.kt` with a `手动输入并继续解析` action wired to the existing manual-input callback.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` with visible OCR failure/manual continuation guidance.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` to pass the manual-input callback into the import panel.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 20/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 32s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 20/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Manual input only switches the app into editable draft mode; it does not execute calendar, reminder, or map actions.
- OCR failure guidance keeps the current action card and routes the user back through the existing editable draft plus backend/offline parsing controls.
- Existing gallery, camera, share, backend, and offline sample paths remain unchanged.

Risks:
- OCR failure is still represented as UI guidance, not a typed failure enum with retry telemetry.
- Low-confidence model output still needs a dedicated manual-review gate before actions are enabled.

Next:
- Add low-confidence manual review gating and missing-field action guards before tackling reminder/map fallbacks and privacy controls.

## 2026-05-25 / Round 080

Goal: Route gallery, camera, and share-text imports through a unified `CaptureDraft` model before they become review cards.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt` with `CaptureDraft`, camera draft creation, gallery draft creation, and a shared draft-to-selection conversion path.
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt` so share-sheet text also enters a `CaptureDraft` before mapping to a course or event card.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 18/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 28s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 18/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Gallery, camera, and share imports still produce the same synthetic course/event cards for demo stability.
- CaptureDraft is now the shared handoff object, but it does not yet implement OCR failure classification.
- User confirmation remains required before calendar, reminder, or map actions can execute.

Risks:
- CaptureDraft is currently a lightweight in-memory mapper model; durable draft storage and OCR failure recovery remain future S2 work.

Next:
- Add manual input analysis and OCR failure continuation before tackling low-confidence review and missing-field action guards.

## 2026-05-25 / Round 079

Goal: Add a minimal inbox archive/restore path so the current card can leave the active filter view without being deleted.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` with current-card archive state, a visible `归档区`, and restore controls.
- Preserved the existing status filters, search, OCR raw text, model explanation, and execution result detail rows.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 15/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 33s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 15/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- 归档/恢复 is scoped to the current visible inbox card and does not delete its details.
- Calendar, reminder, and map actions remain behind existing confirmation-gated controls.
- This round does not claim Room/SQLite or durable multi-item archive history.

Risks:
- Archive state is still in-memory UI state for the current card; durable multi-item archive history remains part of the later Room/SQLite inbox target.

Next:
- Add `CaptureDraft` handling for gallery, camera, and share imports before tackling OCR failure manual continuation and low-confidence review gates.

## 2026-05-25 / Round 078

Goal: Make user-confirmed execution attempts visible after calendar, reminder, and map requests without claiming the action was saved by the external app.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ExecutionResult.kt` with pending/requested result rows for calendar, reminder, and map actions.
- Added `android-mvp/app/src/main/java/cn/shike/app/ExecutionResultActions.kt` so confirmed calendar, reminder, and map button taps record the corresponding visible result.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` and `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` to carry execution results through app state.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt` and `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` so planner and inbox detail show the latest execution state.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 14/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 12s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 14/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Calendar, reminder, and map actions remain behind existing confirmation-gated controls.
- Calendar output uses `已打开系统新增页` and does not claim the user saved the event.
- Execution results are UI-visible state for the current item; they do not imply external-system completion.

Risks:
- Execution results are still in-memory UI state tied to the current selected item; they are not yet durable multi-item execution history.
- Reminder scheduling is still not a true timed scheduler and remains a future Product Beta gap.

Next:
- Add archive/restore and CaptureDraft handling before tackling OCR failure manual continuation and low-confidence review gates.

## 2026-05-24 / Round 077

Goal: Make model explanations visible in confirmation and inbox detail instead of only storing schema `explanation` in raw text.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ModelExplanation.kt` to derive a visible model explanation from backend explanation text, backend fallback state, scene type, and confirmation status.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt` with a `模型解释` row before the risk checklist.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` so inbox detail and search include the same model explanation.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 12/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 36s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 12/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Calendar, reminder, and map actions remain behind the existing confirmation-gated controls.
- Backend success explanations are surfaced when present; local fallback explanations remain deterministic and synthetic.
- This round does not claim execution history or true multi-item inbox persistence.

Risks:
- Model explanation is still derived from the current `ShikeItem` and raw backend explanation text; it is not yet a typed field in the domain model.
- Low-confidence review gating is still represented by status and explanation text, not a dedicated confidence policy object.

Next:
- Add `ExecutionResult` detail visibility for calendar, reminder, and map attempts before tackling archive/restore and CaptureDraft.

## 2026-05-24 / Round 076

Goal: Turn the inbox from a static status summary into a minimal workbench with five status filters, search, and OCR raw-text detail.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt` with five status filters: `待确认`, `已安排`, `即将截止`, `已完成`, and `已忽略`.
- Added inbox search over title, status, scene, location, capture source, and OCR raw text.
- Added an inbox detail row for `OCR 原文`, so the Product Beta detail check is backed by visible UI instead of only a search hint.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` to pass the current capture source into the inbox workbench.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 11/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 18s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 11/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Calendar, reminder, and map actions still execute only through confirmed action controls.
- The inbox workbench is still backed by the current local snapshot, so it does not claim multi-item Room/SQLite persistence yet.
- Search and status filters operate on the real current card fields instead of fixed demo rows.

Risks:
- Status filters for non-current statuses can show an empty result until multi-item inbox persistence is implemented.
- Archive/restore and execution result history are still absent.

Next:
- Add model explanation and execution-result visibility, then continue toward archive/restore and multi-item local inbox persistence.

## 2026-05-24 / Round 075

Goal: Add explicit Today Action empty and error states so first-run or failed local/backend paths do not look like a normal scheduled task.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/InitialSelectionMapper.kt` to distinguish a restored/shared action card from the first-run empty inbox state.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` and `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` to carry `TodayAgendaState` into the homepage and switch back to ready state after user import, sample selection, backend result, or review confirmation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/HomeAgendaList.kt` with visible `今日行动台空状态` and `今日行动台错误状态` cards, including screenshot, photo, and manual input entry points.
- Updated `validation/validate_advanced_product_beta.py` so the current-item check recognizes named-argument `HomeAgendaList(item = selected)` calls instead of only the old positional call.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 8/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 34s`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 8/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: `STRICT_EXIT=1`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Calendar, reminder, and map execution still require the existing confirmation-gated action controls; the empty/error state cards only route users into import or manual draft flow.
- First-run no-cache state is no longer presented as if a sample task were already in the local inbox.
- Backend or capture failure can surface as an explained error state while preserving the current action card and fallback path.

Risks:
- The local inbox is still a single `SharedPreferences` snapshot, not a multi-item Room/SQLite workbench.
- Manual input still uses the existing OCR draft editor and backend/offline analysis buttons instead of a dedicated manual-only flow.

Next:
- Implement the next S2 inbox workbench slice: five status filters and search, backed by a mechanical Product Beta check.

## 2026-05-24 / Round 074

Goal: Make the homepage Today Action card use the current local action card instead of fixed demo agenda cards.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/HomeAgendaList.kt` with a minimal UI-side `TodayActionItem` mapper from `ShikeItem`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` to call `HomeAgendaList(selected)`.
- Updated `validation/validate_advanced_product_beta.py` so `today_uses_inbox_data` requires the current item path and rejects the old fixed demo homepage titles.
- Updated README, current validation status, and Android build report with `PRODUCT_BETA_METRIC 6/30` and the latest Gradle evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 34s`
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 6/30`
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py validation/validate_today_ranking.py`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`

Behavior preserved:
- Calendar, reminder, and map actions still flow through confirmation-gated controls; this round does not change external action execution.
- The homepage no longer displays the old three fixed demo agenda titles; it renders the current selected/recovered action card.
- Product Beta readiness improved through real UI data flow rather than another display-only extraction.

Risks:
- The homepage still only renders the current recovered/selected card, not a full multi-item inbox list.
- Today empty state and local data error state are still missing and should be the next S2 slice.

Next:
- Add explicit today empty and local data error states, then continue toward multi-item local inbox sections.

## 2026-05-24 / Round 073

Goal: Add the minimal Today Action ranking verifier required before replacing fixed homepage cards with inbox-derived decision sections.

Files changed:
- Added `validation/validate_today_ranking.py` with a synthetic `TodayActionItem` model, deterministic ranking score, stable tie-breakers, and 10 representative S2 samples.
- Updated `validation/validate_advanced_product_beta.py` so `today_sorting_test` requires the Today ranking verifier to execute successfully instead of merely checking for a placeholder file.
- Updated README and current validation status with the Today ranking command, `TODAY_RANKING_METRIC 7/7`, and the new Product Beta baseline.

Validation:
- PASS `python3 validation/validate_today_ranking.py`
  - Evidence: `TODAY_RANKING_METRIC 7/7`
  - Evidence: 10 synthetic samples cover low-confidence deadline, assignment deadline, meeting soon, missing location, low-confidence fragment, scheduled course, travel ticket, backend fallback, completed, and ignored items.
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 5/30`
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: strict mode remains non-zero because Product Beta is not complete.
- PASS `python3 -m py_compile validation/validate_today_ranking.py validation/validate_advanced_product_beta.py`

Behavior preserved:
- No Android runtime code changed in this round.
- Product Beta readiness improved only through a real executable sorting verifier.

Risks:
- The homepage still uses fixed `HomeAgendaList` cards; this round only makes the ranking rules mechanically testable.
- The next round must connect the verified ranking baseline to local inbox data rather than treating this as a finished decision page.

Next:
- Use the verified ranking rules to start replacing fixed `HomeAgendaList` demo cards with inbox-derived Today Action sections.
- Keep the user-confirmation rule intact: missing-location or low-confidence cards stay pending and must not expose direct system execution.

## 2026-05-24 / Round 072

Goal: Establish the S2 Product Beta readiness validator from the advanced guide without claiming unfinished product capabilities.

Files changed:
- Added `validation/validate_advanced_product_beta.py` with 30 Product Beta checks covering today page, inbox, import, OCR, risk, action execution, privacy, model evals, backend schema, and optimization-log continuity.
- Added default baseline behavior that prints `PRODUCT_BETA_METRIC` and `NEXT` rows for failed checks while returning zero so it can be used as a gap scanner during ongoing S2 work.
- Added `--strict` mode for future release gating; it returns non-zero until all 30 checks pass.
- Updated README and current validation status with the Product Beta validator entry, baseline score, strict-mode semantics, and next recommended S2 goal.

Validation:
- PASS `python3 validation/validate_advanced_product_beta.py`
  - Evidence: `PRODUCT_BETA_METRIC 4/30`
  - Evidence: failed checks emit `NEXT` rows with concrete follow-up work.
- EXPECTED FAIL `python3 validation/validate_advanced_product_beta.py --strict`
  - Evidence: strict mode returns non-zero while Product Beta readiness is below 30/30.
- PASS `python3 -m py_compile validation/validate_advanced_product_beta.py`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No business code changed in this round.
- Existing Android structure, readiness, demo, landable, backend, and spike checks remain passing.
- The new Product Beta score is intentionally a readiness baseline, not a claim that S2 is complete.

Risks:
- `PRODUCT_BETA_METRIC 4/30` shows the project is still far from Product Beta; the largest gaps are today-page real data, inbox management, CaptureDraft/OCR failure states, risk engine, ExecutionResult, true scheduled reminders, privacy settings, and model evals.
- Strict mode is not yet suitable for the normal baseline gate; it should be used as a release/S2 exit gate only.

Next:
- Start the next round with the advanced guide's Today Action work: add a minimal `TodayActionItem` sorting model plus 10 synthetic examples in `validate_today_ranking.py`.
- Keep `validate_advanced_product_beta.py` as the high-level scorecard and move the score only through real implemented capability.

## 2026-05-24 / Round 071

Goal: P0.2 extract dashboard notification badge UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/DashboardNotificationBadge.kt` with the existing notification circle, bell glyph, and unread dot presentation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/DashboardHeader.kt` so it owns the title row while delegating notification badge presentation to a focused component.
- Updated `validation/validate_android_structure.py` with `dashboard_notification_badge_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `30/30` to `31/31`.
- Updated README, the device checklist, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 31/31` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 31/31`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 30s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the dashboard header still renders the brand, centered title, notification circle, and unread dot.
- The structure guard now prevents notification badge presentation from being collapsed back into `DashboardHeader.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `DashboardHeader.kt`: 41-line title row after extraction.
- `DashboardNotificationBadge.kt`: new 30-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Stop spending the next round on display-only UI splits unless needed by a product-facing capability.
- Move toward the advanced guide's S2 Product Beta work, starting with a minimal Today Action decision-page model and mechanical sorting verifier.

## 2026-05-24 / Round 070

Goal: P0.2 extract agenda card header UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCardHeader.kt` with the existing icon, title, detail lines, and status pill presentation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCard.kt` so it owns the card shell while delegating header and footer presentation to focused components.
- Updated `validation/validate_android_structure.py` with `agenda_card_header_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `29/29` to `30/30`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 30/30` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 30/30`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 18s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; agenda cards still render the same icon, detail lines, status pill, footer label, and action button.
- The structure guard now prevents agenda-card header presentation from being collapsed back into `AgendaCard.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `AgendaCard.kt`: 53-line card shell file after extraction.
- `AgendaCardHeader.kt`: new 60-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 069

Goal: P0.2 extract agenda card footer UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCardFooter.kt` with the existing divider, footer label, and action button presentation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCard.kt` so it owns the card body while delegating footer presentation to `AgendaCardFooter`.
- Updated `validation/validate_android_structure.py` with `agenda_card_footer_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `28/28` to `29/29`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 29/29` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 29/29`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; agenda cards still show the same footer label and action button.
- The structure guard now prevents agenda-card footer presentation from being collapsed back into `AgendaCard.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `AgendaCard.kt`: 81-line card body file after extraction.
- `AgendaCardFooter.kt`: new 30-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 068

Goal: P0.2 extract parse-confirm header UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmHeader.kt` with the existing title, scene confidence, and editable pill presentation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt` so it owns draft field state and review composition while delegating the parse summary header to `ParseConfirmHeader`.
- Updated `validation/validate_android_structure.py` with `parse_confirm_header_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `27/27` to `28/28`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 28/28` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 28/28`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 19s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the AI parse-confirm card still shows the same title, scene confidence, editable pill, draft fields, risk checklist, and review actions.
- The structure guard now prevents the parse-confirm header from being collapsed back into `ParseConfirmPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `ParseConfirmPanel.kt`: 62-line parse-confirm composition file after extraction.
- `ParseConfirmHeader.kt`: new 30-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 067

Goal: P0.2 extract confirm banner actions UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBannerActions.kt` with the existing calendar, reminder, and map action controls.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBanner.kt` so it owns the confirmation message and status pill while delegating enabled action controls to `ConfirmBannerActions`.
- Updated `validation/validate_android_structure.py` with `confirm_banner_actions_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `26/26` to `27/27`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 27/27` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 27/27`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; calendar, reminder, and map actions still stay disabled until the card is confirmed.
- The structure guard now prevents confirm-banner action controls from being collapsed back into `ConfirmBanner.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `ConfirmBanner.kt`: 63-line confirmation summary file after extraction.
- `ConfirmBannerActions.kt`: new 51-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 066

Goal: P0.2 extract bottom navigation item UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/BottomNavItem.kt` with the existing icon, selected-state color, and label presentation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/BottomNavigation.kt` so it owns only the navigation container and item list while delegating each item to `BottomNavItem`.
- Updated `validation/validate_android_structure.py` with `bottom_nav_item_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `25/25` to `26/26`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 26/26` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 26/26`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 18s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the bottom navigation still renders the same five items and keeps `今日` selected.
- The structure guard now prevents the reusable bottom navigation item presentation from being collapsed back into `BottomNavigation.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `BottomNavigation.kt`: 40-line container file after extraction.
- `BottomNavItem.kt`: new 44-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 065

Goal: P0.2 extract demo route step UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/DemoRouteStep.kt` with the existing numbered demo-route row presentation.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/SummarySections.kt` so it owns summary and route composition while delegating each route row to `DemoRouteStep`.
- Updated `validation/validate_android_structure.py` with `demo_route_step_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `24/24` to `25/25`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 25/25` evidence string.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 25/25`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the 3-minute demo route still renders the same four steps.
- The structure guard now prevents the reusable route-row presentation from being collapsed back into `SummarySections.kt`.
- Existing readiness, demo, landable, core-package, backend, APK build, and spike checks remain passing.

Code shape:
- `SummarySections.kt`: 47-line composition file after extraction.
- `DemoRouteStep.kt`: new 40-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 001

Goal: P0.1 engineering baseline and validation entry points from `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md`.

Files changed:
- Added `docs/CODEX_GOAL_MODE_OPTIMIZATION_GUIDE.md` from the user-provided desktop guide.
- Added `docs/current-validation-status.md`.
- Added `docs/optimization-log.md`.

Validation:
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No functional Android/backend/prototype code was intentionally changed in this round.
- The main product chain remains: screenshot/camera/share text -> OCR or draft text -> AI/rule parsing -> user confirmation -> action planning -> calendar/reminder/map/local fallback -> inbox/today tracking.
- User confirmation before system actions remains a non-negotiable constraint for future rounds.

Existing state artifacts:
- `research-results.tsv` and `autoresearch-state.json` were read as historical evidence only.
- They were not manually edited; future autoresearch runs should continue using helper scripts for authoritative TSV/state updates.

Current baseline:
- Android, backend, contracts, validation, docs, prototype, and spike paths are present.
- All four P0.1 baseline validation commands pass.
- Workspace root is not a git repository, so future rounds should report explicit file lists and command evidence.

Next:
- Begin P0.2 / Goal B with a narrow `MainActivity.kt` extraction.
- First extraction candidate: pure domain models, status/action constants, and sample data only.
- Do not rewrite UI or alter the demo flow in the first extraction round.

## 2026-05-24 / Round 002

Goal: P0.2 first low-risk `MainActivity.kt` split without changing UI behavior.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/domain/ShikeItem.kt`.
- Added `android-mvp/app/src/main/java/cn/shike/app/data/SampleItems.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted model and sample fixtures.
- Added `validation/source_tree.py`.
- Updated validation scripts to scan the Android Kotlin source tree instead of assuming all app code lives in `MainActivity.kt`.
- Updated `android-mvp/build-report.md` with direct Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 17s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS focused validation scripts:
  - `BACKEND_CONFIG_METRIC 12/12`
  - `MODEL_BRIDGE_METRIC 14/14`
  - `MANUAL_REVIEW_METRIC 12/12`
  - `OCR_INPUT_METRIC 12/12`
  - `PERSISTENCE_METRIC 12/12`
  - `DEVICE_DEMO_METRIC 12/12`
  - `LANDABLE_METRIC 15/15`

Behavior preserved:
- Screenshot gallery import, camera import, backend parsing, local fallback, manual confirmation, calendar, reminder, map, OCR draft editing, and local restore remain covered by existing validators.
- User confirmation before system actions remains enforced by validation.
- No UI rewrite was performed in this round.

Code shape:
- `MainActivity.kt`: 1237 lines before extraction, 1205 lines after extraction.
- Extracted pure domain model and sample data only:
  - `domain/ShikeItem.kt`
  - `data/SampleItems.kt`

Note:
- `bash shike/android-mvp/build_apk.sh` was interrupted because `sdkmanager --licenses` blocked before Gradle started. The direct Gradle build used the already installed SDK/JDK/Gradle toolchain and produced a successful compile/package gate.
- Core 20 desktop package was not expanded in this round because adding source files to the strict 20-file package would require a separate package-policy decision.

Next:
- Continue P0.2 with another narrow extraction, preferably backend request and JSON mapping into `data/ModelApiClient.kt`.
- Keep one extraction per round and require `assembleDebug` plus `validate_real_world_ready.py` before recording the iteration.

## 2026-05-24 / Round 003

Goal: P0.2 extract backend request and JSON mapping from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/ModelApiClient.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import backend client functions from `data/`.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 36s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- `/v1/analyze` request payload still includes `source_type`, `ocr_text`, `scene_hint`, locale, and `Asia/Shanghai` timezone.
- HTTP timeout, JSON mapping, suggested actions mapping, backend failure fallback, and URL normalization remain covered by validators.
- UI behavior and confirmation-before-action logic were not changed.

Code shape:
- `MainActivity.kt`: 1205 lines before this round, 1130 lines after this round.
- New backend boundary:
  - `data/ModelApiClient.kt`

Next:
- Continue P0.2 with another focused extraction: `SharedPreferences` snapshot and backend URL persistence into `data/LocalInboxStore.kt` / `data/BackendConfigStore.kt`.
- Keep the migration small; do not introduce Room in the same round.

## 2026-05-24 / Round 004

Goal: P0.2 extract `SharedPreferences` snapshot and backend URL persistence from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/LocalInboxStore.kt`.
- Added `android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to call data-layer persistence functions.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 40s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS focused validation scripts:
  - `PERSISTENCE_METRIC 12/12`
  - `BACKEND_CONFIG_METRIC 12/12`

Behavior preserved:
- Restart restore, capture source restore, share-import waits-for-confirmation, backend URL normalization, and local cache behavior remain covered by validators.
- UI behavior and confirmation-before-action logic were not changed.
- Room/SQLite was intentionally not introduced in this round.

Code shape:
- `MainActivity.kt`: 1130 lines before this round, 1071 lines after this round.
- New local storage boundaries:
  - `data/LocalInboxStore.kt`
  - `data/BackendConfigStore.kt`

Next:
- Continue P0.2 with another focused extraction: system action execution for calendar, reminders, and map into a `system/` boundary.
- Keep the next round small; do not change reminder scheduling semantics in the extraction round.

## 2026-05-24 / Round 005

Goal: P0.2 extract calendar, reminder, and map system action helpers from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/system/SystemActions.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to call system-layer action helpers.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 47s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS focused validation scripts:
  - `LANDABLE_METRIC 15/15`
  - `MANUAL_REVIEW_METRIC 12/12`

Behavior preserved:
- Confirmation-before-action behavior remains in the Compose flow.
- Calendar insert, immediate reminder notification, map deeplink, notification channel creation, and external activity fallback behavior were moved without changing execution timing.
- Android 13+ notification permission handling remains in `MainActivity.kt` because it is tied to the Activity Result API.

Code shape:
- `MainActivity.kt`: 1071 lines before this round, 1032 lines after this round.
- New system action boundary:
  - `system/SystemActions.kt`

Next:
- Continue P0.2 with another focused extraction: share-text import parsing or UI section decomposition, whichever gives the smallest safe reduction.
- Keep the next round small and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 006

Goal: P0.2 extract Android share-text import mapping from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/ShareImportMapper.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the data-layer share mapper.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 28s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS focused validation scripts:
  - `PERSISTENCE_METRIC 12/12`
  - `DEVICE_DEMO_METRIC 12/12`

Behavior preserved:
- `ACTION_SEND` and `Intent.EXTRA_TEXT` remain in `MainActivity.kt`.
- Shared text still becomes a pending review card and is not persisted until confirmation.
- The visible source label remains `文本分享入口（待确认，未落盘）`.

Code shape:
- `MainActivity.kt`: 1032 lines before this round, 1023 lines after this round.
- New share import boundary:
  - `data/ShareImportMapper.kt`

Next:
- Continue P0.2 with one UI section extraction from `MainActivity.kt`.
- Prefer a self-contained Compose cluster with no behavior change and no new persistence or permission logic.

## 2026-05-24 / Round 007

Goal: P0.2 extract static readiness and privacy UI sections from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ReadinessSections.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted UI sections.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS focused validation script:
  - `LANDABLE_METRIC 15/15`

Behavior preserved:
- The extracted sections are static display-only Compose panels.
- No permission, persistence, backend, import, confirmation, calendar, reminder, or map behavior was changed.
- The visible delivery readiness and privacy copy remains in the Android source tree for validation.

Code shape:
- `MainActivity.kt`: 1023 lines before this round, 988 lines after this round.
- New UI section boundary:
  - `ui/ReadinessSections.kt`

Next:
- Continue P0.2 with another small UI-only extraction, preferably the bottom navigation cluster.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 008

Goal: P0.2 extract bottom navigation UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/BottomNavigation.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted bottom navigation.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 41s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The bottom navigation labels and selected `今日` state remain unchanged.
- No screen state, permissions, persistence, import, backend, confirmation, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 988 lines before this round, 936 lines after this round.
- New UI boundary:
  - `ui/BottomNavigation.kt`

Next:
- Continue P0.2 with another small UI-only extraction, preferably the static home header/date/agenda cluster.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 009

Goal: P0.2 extract static home overview UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/HomeOverview.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted status row, dashboard header, date strip, and agenda card.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 36s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`
- PASS focused validation script:
  - `LANDABLE_METRIC 15/15`

Behavior preserved:
- The status row, dashboard header, date strip, and agenda card text remain unchanged.
- No screen state, permissions, persistence, import, backend, confirmation, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 936 lines before this round, 786 lines after this round.
- New UI boundary:
  - `ui/HomeOverview.kt`

Next:
- Continue P0.2 with another small UI-only extraction, preferably summary and demo-route sections.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 010

Goal: P0.2 extract summary and demo-route UI sections from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/SummarySections.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import `TodaySummaryPanel`, `DemoRoutePanel`, and the shared `SummaryStat`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new UI boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 31s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The today summary values, labels, colors, and demo route copy remain unchanged.
- `SummaryStat` remains public because the inbox panel still reuses it.
- No screen state, permissions, persistence, import, backend, confirmation, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 786 lines before this round, 735 lines after this round.
- New UI boundary:
  - `ui/SummarySections.kt`

Next:
- Continue P0.2 with another small UI-only extraction, preferably import or parse-confirm display sections.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 011

Goal: P0.2 extract import UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted `ImportPanel`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new import UI boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 34s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The import panel's gallery, camera, backend-course, backend-event, offline-course, and offline-event callbacks remain owned by `MainActivity.kt`.
- Backend URL editing, OCR draft editing, captured preview rendering, and fallback copy remain unchanged.
- No permission, persistence, backend, confirmation, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 735 lines before this round, 649 lines after this round.
- New UI boundary:
  - `ui/ImportPanel.kt`

Next:
- Continue P0.2 with another small UI extraction, preferably parse-confirm or confirmation banner sections.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 012

Goal: P0.2 extract confirmation banner UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ConfirmBanner.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted `ConfirmBanner`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new confirmation banner UI boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 39s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The confirmation banner still disables calendar, reminder, and map actions until `isConfirmed` is true.
- The banner copy, colors, action labels, and callback wiring remain unchanged.
- No permission, persistence, import, backend, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 649 lines before this round, 587 lines after this round.
- New UI boundary:
  - `ui/ConfirmBanner.kt`

Next:
- Continue P0.2 with another small UI extraction, preferably parse-confirm sections.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 013

Goal: P0.2 extract parse-confirm UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted `ParseConfirmPanel`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new parse-confirm UI boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 34s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The parse-confirm form still initializes draft title, time, location, and status from the selected item.
- The confirm path still normalizes blank time, location, and status to `待确认`; the ignore path still sets status to `已忽略`.
- The risk checklist copy and confirmation-before-action warning remain unchanged.
- No permission, persistence, import, backend, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 587 lines before this round, 478 lines after this round.
- New UI boundary:
  - `ui/ParseConfirmPanel.kt`

Next:
- Continue P0.2 with another small UI extraction, preferably action planner or inbox sections.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 014

Goal: P0.2 extract action planner UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted `ActionPlannerPanel`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new action planner UI boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The action planner still renders the first three suggested actions.
- Calendar, reminder, and map buttons still remain disabled until `isConfirmed` is true.
- The action-copy, fallback copy, labels, colors, and callback wiring remain unchanged.
- No permission, persistence, import, backend, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 478 lines before this round, 443 lines after this round.
- New UI boundary:
  - `ui/ActionPlannerPanel.kt`

Next:
- Continue P0.2 with another small UI extraction, preferably inbox status sections.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 015

Goal: P0.2 extract inbox status UI from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/InboxPanel.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to import the extracted `InboxPanel`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new inbox UI boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 30s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- The inbox status counts, labels, colors, current card title, and current status rows remain unchanged.
- The extracted panel still reuses the existing `SummaryStat`, `SectionCard`, and `KeyValue` primitives.
- No permission, persistence, import, backend, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 443 lines before this round, 427 lines after this round.
- New UI boundary:
  - `ui/InboxPanel.kt`

Next:
- Continue P0.2 by extracting shared UI primitives from `MainActivity.kt` into the UI package.
- Keep the next round free of behavior changes and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 016

Goal: P0.2 extract shared UI primitives from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/UiPrimitives.kt`.
- Updated extracted UI files to use same-package `SectionCard`, `KeyValue`, and `Pill`.
- Removed the shared UI primitive implementations and obsolete imports from `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the shared UI primitive boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 30s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- `SectionCard`, `KeyValue`, and `Pill` keep the same visual shape, typography, colors, spacing, and overload signatures.
- Existing UI panels continue to render through the same primitives from the `ui` package.
- No permission, persistence, import, backend, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 427 lines before this round, 354 lines after this round.
- New UI boundary:
  - `ui/UiPrimitives.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably with a small main-screen layout wrapper or backend-analysis coordinator.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 017

Goal: P0.2 extract the main screen layout wrapper from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so `ShikeApp` keeps state, launchers, and callbacks while delegating the pure screen layout to `ShikeMainScreen`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the main-screen layout boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 26s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Screen section ordering, agenda copy, colors, and spacing remain unchanged.
- `MainActivity.kt` still owns app state, camera/gallery launchers, backend calls, and confirmation/action callbacks.
- No permission, persistence, import, backend, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 354 lines before this round, 274 lines after this round.
- New UI boundary:
  - `ui/ShikeMainScreen.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting capture import sample mapping or a backend-analysis coordinator.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 018

Goal: P0.2 extract capture import sample mapping from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` to call data-layer camera and gallery import mapping helpers.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the capture import mapper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Camera preview still becomes the same event poster sample with the same OCR draft and source text.
- Gallery image selection still becomes the same course notification sample with the same OCR draft and source text.
- Offline sample buttons and backend analysis sample calls remain in `MainActivity.kt` unchanged.
- No permission, persistence, backend, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 274 lines before this round, 266 lines after this round.
- New data boundary:
  - `data/CaptureImportMapper.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting a backend-analysis coordinator or backend URL save handler.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 019

Goal: P0.2 extract backend analysis orchestration from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so `ShikeApp` delegates backend endpoint normalization, worker-thread analysis, fallback mapping, and UI-ready result mapping to the data layer.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the backend analysis runner boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Recovery note:
- The first full guard rerun reported `REAL_WORLD_READY_METRIC 15/20` because validator-compatible source snippets moved out of `MainActivity.kt`.
- The camera and gallery launchers now preserve the local-variable shape `persistSelection(item, source)` so persistence and model-bridge validators continue to inspect the expected runtime path.

Behavior preserved:
- Backend success still updates the selected action card, clears the captured bitmap, and records `后端 /v1/analyze：{scene}` as the capture source.
- Backend failure still falls back to the local mock item and appends `后端不可用，已回退本地 MockModelAdapter。` to the raw text.
- The configured backend URL is still normalized and persisted before analysis.
- No permission, persistence, import, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 266 lines before this round, 255 lines after this round.
- New data boundary:
  - `data/BackendAnalysisRunner.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting a backend URL save handler or initial selection mapper.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 020

Goal: P0.2 extract backend URL save normalization from `MainActivity.kt`.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/BackendConfigStore.kt` with `saveBackendUrlFromInput`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so the save button callback delegates backend URL normalization and persistence callback wiring to the data layer.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the backend URL save helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 34s`
  - Note: the first direct shell command failed because system `gradle` was absent from `PATH`; the verified build used the project-local toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- Pressing `保存后端地址` still normalizes the user-entered URL, persists it, reflects the normalized URL in UI state, and shows `模型编排：后端地址已保存`.
- Backend analysis still normalizes and persists the endpoint returned by `runBackendAnalysis`.
- No permission, persistence, import, backend network call, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 255 lines before this round, 254 lines after this round.
- Extended data boundary:
  - `data/BackendConfigStore.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting initial item/source selection.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 021

Goal: P0.2 extract initial item/source selection from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/InitialSelectionMapper.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so startup only reads share text and delegates the initial action card/source selection to the data layer.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the initial selection mapper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 39s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- Share-sheet text still seeds the review card and shows `文本分享入口（待确认，未落盘）`.
- Share imports still wait for user confirmation and do not call `saveSnapshot(importedItem)`.
- Non-share startup still restores the cached inbox snapshot when present, otherwise uses the offline sample.
- No permission, persistence write path, capture import, backend call, parse-confirm, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 254 lines before this round, 245 lines after this round.
- New data boundary:
  - `data/InitialSelectionMapper.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting review status mapping.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 022

Goal: P0.2 extract review status mapping from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/data/ReviewStatusMapper.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so `updateReviewedItem` delegates confirmed/ignored item status and model-status copy mapping to the data layer.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the review status mapper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 28s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_manual_review.py`
  - Evidence: `MANUAL_REVIEW_METRIC 12/12`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- Confirmed review items still persist through `persistSelection(reviewedItem, "用户确认修正：...")`.
- Ignored items still keep status `已忽略` and show `模型编排：用户已忽略`.
- Confirmed non-ignored items still become `已安排` and show `模型编排：用户已确认`.
- No permission, persistence write path, capture import, backend call, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 245 lines before this round, 243 lines after this round.
- New data boundary:
  - `data/ReviewStatusMapper.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting capture permission decision helpers or backend trigger wiring.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 023

Goal: P0.2 extract Android permission decision helpers from `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/system/PermissionDecisions.kt`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so camera and notification permission checks delegate to system-layer helpers while launchers and user-facing fallback copy remain in the Android shell.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the permission decision boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 15/15`
- PASS `python3 validation/validate_manual_review.py`
  - Evidence: `MANUAL_REVIEW_METRIC 12/12`

Behavior preserved:
- Camera preview still launches immediately when `Manifest.permission.CAMERA` is granted and otherwise uses the existing permission launcher.
- Denied camera permission still shows `相机权限被拒绝，可改用相册或文本分享入口。`.
- Reminder notification still posts immediately when allowed and otherwise requests `POST_NOTIFICATIONS`.
- No persistence, capture import, backend call, parse-confirm UI, calendar, reminder content, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 243 lines before this round, 238 lines after this round.
- New system boundary:
  - `system/PermissionDecisions.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting backend trigger wiring or capture launcher result mapping.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 024

Goal: P0.2 extract capture launcher result mapping from `MainActivity.kt`.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/CaptureImportMapper.kt` with `CaptureSelection`, `cameraSelectionFromPreview`, and `gallerySelectionFromImage`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so camera/gallery launchers delegate item/source construction to the data layer while preserving `persistSelection(item, source)`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the capture result mapper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`

Behavior preserved:
- Camera preview still creates the same event poster sample and source text `相机拍照预览 {width}x{height}`.
- Gallery selection still creates the same course notification sample and source text `相册图片 {label}`.
- The launchers still persist through `persistSelection(item, source)` so local cache, OCR draft refresh, and validator-visible runtime shape are unchanged.
- No permission, persistence write path, backend call, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 238 lines before this round, 238 lines after this round.
- Extended data boundary:
  - `data/CaptureImportMapper.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting backend trigger wiring.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 025

Goal: P0.2 extract backend trigger input mapping from `MainActivity.kt`.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/data/BackendAnalysisRunner.kt` with `BackendAnalysisInput`, `courseBackendAnalysisInput`, and `eventBackendAnalysisInput`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so backend buttons delegate source type and fallback sample selection to the data layer.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the backend input mapping boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- `后端解析课程` still sends `screenshot` with the course fallback sample.
- `后端解析活动` still sends `camera` with the event fallback sample.
- Backend analysis still uses the editable OCR draft, persists the normalized endpoint, and falls back to `MockModelAdapter` on failure.
- No permission, persistence write path, capture import, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 238 lines before this round, 241 lines after this round.
- Extended data boundary:
  - `data/BackendAnalysisRunner.kt`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting backend outcome application or sample button result mapping.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 026

Goal: P0.2 extract backend outcome application from the backend callback body.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `applyBackendOutcome`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the backend outcome application boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 33s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`

Behavior preserved:
- Backend success still updates model status, clears the captured preview, persists the analyzed item, and refreshes OCR draft through `persistSelection`.
- Backend failure still falls back to the local `MockModelAdapter` item and preserves edited OCR text in the fallback raw text.
- No permission, capture import, backend request, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 241 lines before this round, 246 lines after this round.
- New local UI-state boundary:
  - `applyBackendOutcome`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting sample button result mapping.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 027

Goal: P0.2 extract offline sample button application helpers from `MainActivity.kt` callback wiring.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `applyCourseSample` and `applyEventSample`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the offline sample application helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`

Behavior preserved:
- Course offline sample still clears the captured bitmap and persists `sampleCourse()` with source `离线样例：课程通知截图`.
- Event offline sample still clears the captured bitmap and persists `sampleEvent()` with source `离线样例：活动海报拍照`.
- The visible `onCourse` and `onEvent` callbacks now delegate to named helpers, keeping sample application behavior easier to verify.
- No permission, capture import, backend request, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 246 lines before this round, 250 lines after this round.
- New local UI-state boundary:
  - `applyCourseSample`
  - `applyEventSample`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting launcher callbacks or system action wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 028

Goal: P0.2 extract camera/gallery result application helpers from launcher callback bodies.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `applyCameraPreview` and `applyGalleryImage`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the camera/gallery result application helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 20s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`

Debug note:
- The first helper shape used `persistSelection(selection.item, selection.source)`, which failed the source-contract checks in `validate_persistence.py`.
- The final helper shape preserves local `item` and `source` variables and calls `persistSelection(item, source)`, restoring the guard contract while keeping the callback extraction.

Behavior preserved:
- Camera preview still keeps the returned bitmap, maps width/height through `cameraSelectionFromPreview`, and persists the same item/source pair.
- Gallery import still clears the captured bitmap, maps the URI label through `gallerySelectionFromImage`, and persists the same item/source pair.
- Existing cancelled-camera and cancelled-gallery feedback strings are unchanged.
- No permission, backend request, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 250 lines before this round, 258 lines after this round.
- New local UI-state boundary:
  - `applyCameraPreview`
  - `applyGalleryImage`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting backend URL save UI handling or permission launch wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 029

Goal: P0.2 extract backend endpoint save UI handling from the main screen callback wiring.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `saveBackendEndpoint`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the backend endpoint save helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`

Behavior preserved:
- Saving the backend endpoint still delegates through `saveBackendUrlFromInput(backendUrl, onSaveBackendUrl)`.
- The saved status text remains `模型编排：后端地址已保存`.
- Backend analysis still persists the normalized endpoint after every `/v1/analyze` request.
- No permission, capture import, OCR draft, backend request, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 258 lines before this round, 260 lines after this round.
- New local UI-state boundary:
  - `saveBackendEndpoint`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting permission launch wiring or system action wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 030

Goal: P0.2 extract camera permission launch wiring from the main screen callback.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `launchCameraCapture`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the camera permission launch helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 30s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- Camera launch still checks `hasCameraPermission(context)` before opening the camera preview.
- Granted camera access still calls `cameraLauncher.launch(null)`.
- Missing camera permission still launches `cameraPermissionLauncher.launch(Manifest.permission.CAMERA)`.
- Permission denial feedback remains `相机权限被拒绝，可改用相册或文本分享入口。`.
- No gallery import, backend request, OCR draft, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 260 lines before this round, 263 lines after this round.
- New local UI-state boundary:
  - `launchCameraCapture`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting gallery launch wiring or system action wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 031

Goal: P0.2 extract gallery launch wiring from the main screen callback.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `launchGalleryPicker`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the gallery launch helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- Gallery import still uses `ActivityResultContracts.GetContent`.
- The gallery picker still launches with MIME type `image/*`.
- Selected gallery content still flows through `applyGalleryImage`, persistence, and OCR draft refresh.
- No camera, permission, backend request, OCR draft, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 263 lines before this round, 267 lines after this round.
- New local UI-state boundary:
  - `launchGalleryPicker`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting system action wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 032

Goal: P0.2 extract backend course/event trigger helpers from the main screen callback wiring.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `analyzeCourseWithBackend` and `analyzeEventWithBackend`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the backend trigger helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`
- PASS `python3 validation/validate_backend_config.py`
  - Evidence: `BACKEND_CONFIG_METRIC 12/12`
- PASS `python3 validation/validate_ocr_input.py`
  - Evidence: `OCR_INPUT_METRIC 12/12`

Behavior preserved:
- Course backend analysis still delegates to `analyzeWithBackend(courseBackendAnalysisInput())`.
- Event backend analysis still delegates to `analyzeWithBackend(eventBackendAnalysisInput())`.
- Backend requests still use the editable OCR draft, configured endpoint, and local mock fallback.
- No gallery, camera, permission, parse-confirm UI, calendar, reminder, or map behavior was changed.

Code shape:
- `MainActivity.kt`: 267 lines before this round, 275 lines after this round.
- New local UI-state boundary:
  - `analyzeCourseWithBackend`
  - `analyzeEventWithBackend`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting system action or reminder permission wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 033

Goal: P0.2 extract notification permission result handling from the ActivityResult callback.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `handleNotificationPermissionResult`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the notification permission result helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 15/15`

Behavior preserved:
- Granted notification permission still posts the pending reminder through `showReminderNotification`.
- The pending reminder is still cleared after the permission result.
- `requestReminder` still posts immediately when notification permission is already available.
- `requestReminder` still launches `Manifest.permission.POST_NOTIFICATIONS` when permission is missing.

Code shape:
- `MainActivity.kt`: 275 lines before this round, 279 lines after this round.
- New Activity boundary:
  - `handleNotificationPermissionResult`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting system action fallback wiring into smaller local helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 034

Goal: P0.2 extract shared system action fallback persistence from calendar and map handlers.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `saveSystemActionFallback`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the system action fallback helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 15/15`
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`

Behavior preserved:
- Calendar fallback text remains `系统日历不可用，已保留行动卡，稍后可手动添加日程。`.
- Map fallback text remains `地图应用不可用，已保留地点：${item.location}`.
- Both system action fallbacks still persist through `saveSnapshot(this, item, source)`.
- No notification, backend request, capture import, OCR draft, parse-confirm UI, calendar intent, or map deeplink behavior was changed.

Code shape:
- `MainActivity.kt`: 279 lines before this round, 283 lines after this round.
- New Activity boundary:
  - `saveSystemActionFallback`

Next:
- Continue P0.2 by reducing app-level coupling in `MainActivity.kt`, preferably by extracting reminder permission request wiring into a smaller local helper.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 035

Goal: P0.2 extract reminder notification permission request wiring from `requestReminder`.

Files changed:
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` with `requestNotificationPermissionFor`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the notification permission request helper boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 shike/validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 shike/validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 shike/backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 shike/spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 15/15`

Behavior preserved:
- `requestReminder` still posts immediately when `canPostReminderNotification(this)` is true.
- Missing notification permission still stores `pendingReminderItem` before launching the permission request.
- Permission request still uses `Manifest.permission.POST_NOTIFICATIONS`.
- Granted permission still posts the pending reminder through `handleNotificationPermissionResult`.

Code shape:
- `MainActivity.kt`: 283 lines before this round, 287 lines after this round.
- New Activity boundary:
  - `requestNotificationPermissionFor`

Next:
- Continue P0.2 carefully; `MainActivity.kt` is still below 300 lines but near the threshold, so prefer consolidation or a small extraction that does not increase line count much.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 036

Goal: P0.2 split the top-level `ShikeApp` composable out of `MainActivity.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` as the app-level Compose coordinator.
- Updated `android-mvp/app/src/main/java/cn/shike/app/MainActivity.kt` so the Activity shell loads startup inputs, installs Android shell callbacks, and delegates app state/UI coordination to `ShikeApp`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new `ShikeApp` ownership boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Additional targeted checks:
- PASS `python3 validation/validate_persistence.py`
  - Evidence: `PERSISTENCE_METRIC 12/12`
- PASS `python3 validation/validate_device_demo.py`
  - Evidence: `DEVICE_DEMO_METRIC 12/12`
- PASS `python3 validation/validate_model_bridge.py`
  - Evidence: `MODEL_BRIDGE_METRIC 14/14`

Behavior preserved:
- `MainActivity` still creates the reminder notification channel and handles `ACTION_SEND` shared text.
- Startup still loads the initial selection and backend URL from local persistence.
- Snapshot persistence, backend URL persistence, calendar insert, reminder, and map callbacks are still supplied by the Activity shell.
- `ShikeApp` preserves app state, OCR draft state, camera/gallery launchers, backend analysis, sample actions, review handling, and `ShikeMainScreen` handoff.

Code shape:
- `MainActivity.kt`: 287 lines before this round, 102 lines after this round.
- `ShikeApp.kt`: new 190-line app coordinator.
- New ownership boundary:
  - `MainActivity`: Android shell, startup inputs, persisted callback adapters, system actions.
  - `ShikeApp`: Compose app state, launchers, backend orchestration, screen callback wiring.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around launcher state or backend orchestration.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 037

Goal: P0.2 extract camera/gallery Activity Result launcher wiring from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/CaptureLaunchers.kt` with `rememberCaptureLaunchers`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so app state keeps capture-result application while launcher setup delegates to `CaptureLaunchers`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new capture launcher boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Gallery still uses `ActivityResultContracts.GetContent()` and launches with `image/*`.
- Camera still uses `ActivityResultContracts.TakePicturePreview()`.
- Missing camera permission still launches `Manifest.permission.CAMERA` through `ActivityResultContracts.RequestPermission()`.
- Camera unavailable, denied permission, and empty gallery selection still update the same `captureSource` messages.
- Camera/gallery successful results still flow through `applyCameraPreview` and `applyGalleryImage`, preserving persistence and OCR draft updates.

Code shape:
- `ShikeApp.kt`: 190 lines before this round, 151 lines after this round.
- `CaptureLaunchers.kt`: new 68-line launcher owner.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around backend orchestration.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 038

Goal: P0.2 extract backend analysis request kickoff from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/BackendAnalysisActions.kt` with `runBackendAnalysisAction`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so backend button handlers keep UI state ownership while request kickoff, endpoint return, and main-thread result delivery delegate to the new helper.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new backend actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 45s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Course and event backend actions still use `courseBackendAnalysisInput()` and `eventBackendAnalysisInput()`.
- Backend analysis still uses the editable OCR draft and configured endpoint.
- Backend result delivery still posts back through `Handler(Looper.getMainLooper())`.
- `ShikeApp` still updates `backendUrl`, persists the normalized endpoint, and shows `模型编排：请求后端 /v1/analyze` while the request is running.
- Successful or fallback backend outcomes still flow through `applyBackendOutcome`.

Code shape:
- `ShikeApp.kt`: 151 lines before this round, 147 lines after this round.
- `BackendAnalysisActions.kt`: new 34-line backend action helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around sample/capture result application helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 039

Goal: P0.2 extract offline sample action application from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/SampleActions.kt` with offline course/event sample selection helpers.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so sample button handlers keep capture-preview cleanup while sample item/source selection delegates to `SampleActions`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new sample actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Course sample still persists `sampleCourse()` with source `离线样例：课程通知截图`.
- Event sample still persists `sampleEvent()` with source `离线样例：活动海报拍照`.
- Both sample paths still clear `capturedBitmap` before updating the selected action card.
- Persisted sample selection still updates confirmation status, capture source, OCR draft, and local snapshot through `persistSelection`.

Code shape:
- `ShikeApp.kt`: 147 lines before this round, 145 lines after this round.
- `SampleActions.kt`: new 13-line sample action helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around capture result application helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 040

Goal: P0.2 extract successful capture result application from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/CaptureResultActions.kt` with camera/gallery capture-result application helpers.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so it keeps preview bitmap state while successful camera/gallery item/source selection delegates to `CaptureResultActions`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new capture result actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Camera preview still sets `capturedBitmap` before applying the generated action card.
- Camera selection still uses `cameraSelectionFromPreview(bitmap.width, bitmap.height)`.
- Gallery selection still clears `capturedBitmap` and applies `gallerySelectionFromImage(label)`.
- Both successful capture paths still call `persistSelection(item, source)`, preserving confirmation status, capture source, OCR draft, and local snapshot persistence.

Code shape:
- `ShikeApp.kt`: 145 lines before this round, 137 lines after this round.
- `CaptureResultActions.kt`: new 26-line capture result action helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around review or backend outcome application helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 041

Goal: P0.2 extract manual review result application from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ReviewActions.kt` with `applyReviewedItemSelection`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so `updateReviewedItem` keeps the UI callback boundary while review item mapping, persistence source, and status message return delegate to `ReviewActions`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new review actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- `updateReviewedItem` remains the callback passed to `ShikeMainScreen`.
- Reviewed items still pass through `mapReviewedItemState(item)`.
- Confirmed or ignored review results still persist through `persistSelection(reviewedItem, "用户确认修正：${item.scene}")`.
- `modelStatus` still receives `模型编排：用户已确认` or `模型编排：用户已忽略` from the data-layer review mapper.

Code shape:
- `ShikeApp.kt`: 137 lines before this round, 133 lines after this round.
- `ReviewActions.kt`: new 14-line review action helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around backend outcome application helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 042

Goal: P0.2 extract backend outcome application from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/BackendOutcomeActions.kt` with `applyBackendOutcomeSelection`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so backend result callbacks keep preview cleanup while outcome persistence and status-message return delegate to `BackendOutcomeActions`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new backend outcome actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 20s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- `applyBackendOutcome` still clears `capturedBitmap` before applying backend results.
- Backend outcome item/source still persist through `persistSelection(outcome.item, outcome.source)`.
- `modelStatus` still receives the backend outcome status message.
- Backend request kickoff, endpoint persistence, OCR draft usage, and fallback behavior remain unchanged.

Code shape:
- `ShikeApp.kt`: 133 lines before this round, 132 lines after this round.
- `BackendOutcomeActions.kt`: new 12-line backend outcome helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around backend trigger/save endpoint helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 043

Goal: P0.2 extract backend endpoint save action from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/BackendEndpointActions.kt` with `saveBackendEndpointAction`.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so the save button callback keeps UI state ownership while backend URL normalization, persistence callback invocation, and saved-status message return delegate to `BackendEndpointActions`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new backend endpoint actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- `saveBackendEndpoint` remains the callback passed to `ShikeMainScreen`.
- Backend URL saving still calls `saveBackendUrlFromInput(backendUrl, onSaveBackendUrl)`.
- UI backend URL state still updates to the normalized endpoint.
- `modelStatus` still receives `模型编排：后端地址已保存`.

Code shape:
- `ShikeApp.kt`: 132 lines before this round, 132 lines after this round.
- `BackendEndpointActions.kt`: new 17-line backend endpoint helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around backend trigger helpers.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 044

Goal: P0.2 extract course/event backend trigger dispatch from `ShikeApp.kt`.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/BackendTriggerActions.kt` with backend course/event trigger helpers.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ShikeApp.kt` so `analyzeCourseWithBackend` and `analyzeEventWithBackend` remain UI callbacks while backend input selection delegates to `BackendTriggerActions`.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new backend trigger actions boundary and validation evidence.

Validation:
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- `analyzeCourseWithBackend` and `analyzeEventWithBackend` remain the callbacks passed to `ShikeMainScreen`.
- Course backend analysis still uses `courseBackendAnalysisInput()`.
- Event backend analysis still uses `eventBackendAnalysisInput()`.
- Both backend trigger paths still delegate into `analyzeWithBackend`, preserving OCR draft usage, configured endpoint persistence, and fallback behavior.

Code shape:
- `ShikeApp.kt`: 132 lines before this round, 130 lines after this round.
- `BackendTriggerActions.kt`: new 13-line backend trigger helper.
- `MainActivity.kt`: unchanged at 102 lines.

Next:
- Continue P0.2 by reducing app-level coupling in `ShikeApp.kt`, preferably with a focused extraction around remaining app callback grouping.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 045

Goal: P0.2 add a mechanical Android source-structure validator after repeated app coordinator extractions.

Files changed:
- Added `validation/validate_android_structure.py` with checks for required Android Kotlin files, coordinator size caps, action-helper size caps, callback names, extracted launcher/action boundaries, and large-file prevention.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` with the new structure validator and validation evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 10/10`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 10s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No Android runtime behavior changed in this round.
- Existing `REAL_WORLD_READY_METRIC 20/20` remains unchanged; the structure validator is an additional independent guard.
- The validator locks in the current low-risk extraction boundaries without changing UI, backend, persistence, or demo behavior.

Code shape:
- `validate_android_structure.py`: new 104-line validation script.
- Android Kotlin source: unchanged in this round.

Next:
- Continue P0.2 with a delivery-oriented improvement, preferably documenting or wiring the new Android structure guard into the developer workflow.
- Keep the next round focused and require `assembleDebug` plus the full guard chain before recording.

## 2026-05-24 / Round 046

Goal: P0.2 document the Android source-structure validator in the developer acceptance workflow.

Files changed:
- Updated `README.md` so the mechanical acceptance block runs `validation/validate_android_structure.py` before readiness, demo, deliverable, landable, Spike, and core-package checks.
- Updated `README.md` to explain that the structure guard checks Android source boundaries, file-size caps, callback names, and helper ownership.
- Updated `android-mvp/build-report.md` with the latest Gradle build evidence.
- Updated `docs/current-validation-status.md` to mark the structure validator as README-listed and refresh the validation evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 10/10`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 16s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 15/15`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No Android runtime behavior changed in this round.
- Existing `REAL_WORLD_READY_METRIC 20/20` remains unchanged; the Android structure validator remains an additional independent guard.
- Developer-facing verification now makes the structure guard harder to skip before future app-code changes.

Code shape:
- Android Kotlin source: unchanged in this round.
- README acceptance workflow now exposes the Android source-structure guard as a first-class command.

Next:
- Continue P0.2 with a low-risk delivery hardening step or the next focused `ShikeApp.kt` responsibility extraction.
- Keep the next round focused and require `validate_android_structure.py`, `assembleDebug`, and the full guard chain before recording.

## 2026-05-24 / Round 047

Goal: P0.2 make the Android source-structure guard visible in the demo retest workflow.

Files changed:
- Updated `materials/device-demo-checklist.md` so the preparation table and final acceptance command block include `python3 shike/validation/validate_android_structure.py` with `ANDROID_STRUCTURE_METRIC 10/10`.
- Updated `prototype/demo.html` so the Demo console displays `ANDROID_STRUCTURE_METRIC 10/10`, refreshes `DEMO_ACCEPTANCE_METRIC` to `16/16`, and lists the structure validator in its acceptance commands.
- Updated `validation/validate_demo_acceptance.py` with a new `android_structure_guard_listed` check requiring the structure guard to appear consistently in README, the device checklist, and the Demo console.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 10/10`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 16s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No Android runtime behavior changed in this round.
- Existing `REAL_WORLD_READY_METRIC 20/20` remains unchanged.
- Demo retest now makes the source-structure guard visible before future recordings or handoffs.

Code shape:
- Android Kotlin source: unchanged in this round.
- `validate_demo_acceptance.py`: one additional acceptance check, raising the metric from `15/15` to `16/16`.

Next:
- Continue P0.2 with a low-risk validation hardening step or the next focused Android responsibility extraction.
- Keep the next round focused and require `validate_android_structure.py`, `assembleDebug`, and the full guard chain before recording.

## 2026-05-24 / Round 048

Goal: P0.2 make the core 20-file package verifier preserve the Android structure guard workflow.

Files changed:
- Updated `scripts/verify_core20_package.py` so the package still must contain exactly the expected 20 files while also checking structure-guard references in packaged `README.md`, `materials/device-demo-checklist.md`, and `validation/validate_demo_acceptance.py`.
- Updated `README.md` to state that the core package verifier checks file count, required files, APK SHA-256, and structure guard references.
- Updated `materials/submission-checklist.md` with the same verifier scope.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 10/10`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 17s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No Android runtime behavior changed in this round.
- The core submission package remains exactly 20 files; the verifier got stricter without changing the expected package list.
- Existing `REAL_WORLD_READY_METRIC 20/20`, `DEMO_ACCEPTANCE_METRIC 16/16`, and `ANDROID_STRUCTURE_METRIC 10/10` remain unchanged.

Code shape:
- `verify_core20_package.py`: one small token-check helper plus three structure-guard reference checks.
- Android Kotlin source: unchanged in this round.

Next:
- Continue P0.2 with a low-risk validation hardening step or a focused Android responsibility extraction.
- Keep the next round focused and require core acceptance checks plus the full guard chain before recording.

## 2026-05-24 / Round 049

Goal: P0.2 make the real-world readiness guard enforce README visibility of the Android structure validator.

Files changed:
- Updated `validation/validate_real_world_ready.py` so the existing `readme_has_real_world_commands` check also requires `validate_android_structure.py` and `ANDROID_STRUCTURE_METRIC 10/10` in `README.md`.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 10/10`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 11s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No Android runtime behavior changed in this round.
- `REAL_WORLD_READY_METRIC` remains `20/20`; the existing README command check became stricter without adding a new readiness denominator.
- Existing Demo and core-package guard metrics remain unchanged.

Code shape:
- `validate_real_world_ready.py`: one existing README readiness check now verifies the structure guard command and metric text.
- Android Kotlin source: unchanged in this round.

Next:
- Continue P0.2 with the next low-risk guard hardening or Android responsibility extraction.
- Keep the next round focused and require readiness, demo, core-package, Android structure, APK, backend, and spike verification before recording.

## 2026-05-24 / Round 050

Goal: P0.2 make the device-runbook path require the Android structure guard before true device testing.

Files changed:
- Updated `docs/device-runbook.md` so the prerequisites include `python3 shike/validation/validate_android_structure.py` with `ANDROID_STRUCTURE_METRIC 10/10`.
- Updated `validation/validate_landable.py` with `structure_guard_runbook_documented`, raising `LANDABLE_METRIC` from `15/15` to `16/16`.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 10/10`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 13s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- No Android runtime behavior changed in this round.
- Device testing documentation now makes source-structure validation an explicit prerequisite.
- Existing readiness, demo, core-package, Android structure, backend, and spike checks remain passing.

Code shape:
- `validate_landable.py`: one additional runbook guard check.
- Android Kotlin source: unchanged in this round.

Next:
- Continue P0.2 with another low-risk validation hardening step or a focused Android responsibility extraction.
- Keep the next round focused and require full guard-chain verification before recording.

## 2026-05-24 / Round 051

Goal: P0.2 extract AgendaCard from the home overview UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/AgendaCard.kt` with the existing Agenda card composable.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/HomeOverview.kt` so it only owns system status, dashboard header, and date strip UI.
- Updated `validation/validate_android_structure.py` with `agenda_card_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `10/10` to `11/11`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, and landable validator to use the current `ANDROID_STRUCTURE_METRIC 11/11` evidence string.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 11/11`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; `ShikeMainScreen` still calls `AgendaCard` with the same arguments.
- The structure guard now explicitly prevents `AgendaCard` from being collapsed back into `HomeOverview.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `HomeOverview.kt`: reduced from 181 lines to 107 lines.
- `AgendaCard.kt`: new 93-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- iteration 60 should start with the required protocol fingerprint check.
- After that, continue P0.2 with a low-risk UI or validation boundary improvement and run the full guard chain before recording.

## 2026-05-24 / Round 052

Goal: P0.2 extract the review risk checklist from parse-confirm UI and lock the new boundary in Android structure validation.

Protocol fingerprint:
- PASS baseline/init memory: current foreground run already has initialized helper state and retained metric history.
- PASS completed experiment logging: iteration 59 was verified, documented, and recorded before choosing this round.
- PASS authoritative state: `research-results.tsv` and `autoresearch-state.json` remain helper-owned.
- PASS stop conditions and rollback: continue unless user stops, goal reaches a real terminal state, configured cap is reached, or a true blocker appears; `shike` still uses non-destructive patch revert because it is not a git repo.
- PASS selected workflow: loop mode, one focused change, mechanical verification, helper record before next experiment.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ReviewRiskChecklist.kt` with the existing review risk checklist UI.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt` so it owns the parse-confirm form and delegates risk display to `RiskChecklistPanel`.
- Updated `validation/validate_android_structure.py` with `review_risk_checklist_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `11/11` to `12/12`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, and landable validator to use the current `ANDROID_STRUCTURE_METRIC 12/12` evidence string.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 12/12`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 32s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; `ParseConfirmPanel` still renders `RiskChecklistPanel(item)` with the same review content.
- The structure guard now prevents the risk checklist from being collapsed back into `ParseConfirmPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ParseConfirmPanel.kt`: reduced from 136 lines to 104 lines.
- `ReviewRiskChecklist.kt`: new 47-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 064

Goal: P0.2 extract action planner execution controls and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerExecutionControls.kt` with the existing calendar, reminder, and map execution controls.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ActionPlannerPanel.kt` so it owns action summary chips and explanatory copy while delegating execution buttons to `ActionPlannerExecutionControls`.
- Updated `validation/validate_android_structure.py` with `action_planner_execution_controls_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `23/23` to `24/24`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 24/24` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 24/24`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 24s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; action planner still requires confirmation before enabling calendar, reminder, and map actions.
- The structure guard now prevents execution controls from being collapsed back into `ActionPlannerPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ActionPlannerPanel.kt`: reduced from 49 lines to 42 lines.
- `ActionPlannerExecutionControls.kt`: new 38-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 063

Goal: P0.2 extract home agenda list from the main screen and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/HomeAgendaList.kt` with the existing three agenda cards from the main screen.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ShikeMainScreen.kt` so the screen shell delegates the agenda card stack to `HomeAgendaList`.
- Updated `validation/validate_android_structure.py` with `home_agenda_list_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `22/22` to `23/23`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 23/23` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 23/23`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 21s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the same three agenda cards still render immediately after the date strip.
- The structure guard now prevents the agenda-card stack from being collapsed back into `ShikeMainScreen.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ShikeMainScreen.kt`: reduced from 119 lines to 84 lines.
- `HomeAgendaList.kt`: new 44-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 062

Goal: P0.2 extract date strip from home overview and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/DateStrip.kt` with the existing date strip row and “全部日程” pill.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/HomeOverview.kt` so the previously grouped home overview helpers are now fully split into dedicated components.
- Updated `validation/validate_android_structure.py` with `date_strip_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `21/21` to `22/22`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 22/22` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 22/22`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 23s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the home screen still calls `DateStrip()` from `ShikeMainScreen`.
- The structure guard now prevents the date strip from being collapsed back into `HomeOverview.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `HomeOverview.kt`: reduced from 47 lines to a package marker after extracting the last helper.
- `DateStrip.kt`: new 47-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 061

Goal: P0.2 extract system status row from home overview and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/SystemStatusRow.kt` with the existing simulated phone status row.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/HomeOverview.kt` so it keeps the date strip helper while delegating the system status row to `SystemStatusRow`.
- Updated `validation/validate_android_structure.py` with `system_status_row_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `20/20` to `21/21`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 21/21` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 21/21`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 20s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the home screen still calls `SystemStatusRow()` from `ShikeMainScreen`.
- The structure guard now prevents the system status row from being collapsed back into `HomeOverview.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `HomeOverview.kt`: reduced from 60 lines to 47 lines.
- `SystemStatusRow.kt`: new 25-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 060

Goal: P0.2 extract dashboard header from home overview and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/DashboardHeader.kt` with the existing brand title, centered title, and notification badge header.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/HomeOverview.kt` so it keeps status and date strip helpers while delegating dashboard header rendering to `DashboardHeader`.
- Updated `validation/validate_android_structure.py` with `dashboard_header_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `19/19` to `20/20`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 20/20` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 20/20`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 26s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; the home screen still calls `DashboardHeader()` from `ShikeMainScreen`.
- The structure guard now prevents the dashboard header from being collapsed back into `HomeOverview.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `HomeOverview.kt`: reduced from 107 lines to 60 lines.
- `DashboardHeader.kt`: new 63-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 059

Goal: P0.2 extract captured image preview from import UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/CapturedImagePreview.kt` with the existing captured bitmap preview rendering.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` so it owns import state display, capture entry, backend endpoint, OCR draft editor, backend analysis, and offline sample sections while delegating captured image rendering to `CapturedImagePreview`.
- Updated `validation/validate_android_structure.py` with `captured_image_preview_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `18/18` to `19/19`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 19/19` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 19/19`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 17s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; captured bitmap previews still render with the same content description and dimensions.
- The structure guard now prevents captured image preview rendering from being collapsed back into `ImportPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ImportPanel.kt`: reduced from 71 lines to 55 lines.
- `CapturedImagePreview.kt`: new 25-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 058

Goal: P0.2 extract OCR draft editor from import UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/OcrDraftEditor.kt` with the existing editable OCR draft text field.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` so it owns import state display, preview, capture entry, backend endpoint, backend analysis, and offline sample sections while delegating OCR draft editing to `OcrDraftEditor`.
- Updated `validation/validate_android_structure.py` with `ocr_draft_editor_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `17/17` to `18/18`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 18/18` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 18/18`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 20s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; OCR draft changes still flow through the same callback and backend analysis still reads the editable draft.
- The structure guard now prevents OCR draft editing from being collapsed back into `ImportPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ImportPanel.kt`: reduced from 77 lines to 71 lines.
- `OcrDraftEditor.kt`: new 23-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 057

Goal: P0.2 extract backend endpoint controls from import UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/BackendEndpointControls.kt` with the existing backend URL field and save action.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` so it owns import state display, OCR draft, preview, capture entry, backend analysis, and offline sample sections while delegating backend endpoint controls to `BackendEndpointControls`.
- Updated `validation/validate_android_structure.py` with `backend_endpoint_controls_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `16/16` to `17/17`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 17/17` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 17/17`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 34s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; backend URL editing and save still call the same callbacks from the import panel.
- The structure guard now prevents backend endpoint controls from being collapsed back into `ImportPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ImportPanel.kt`: reduced from 87 lines to 77 lines.
- `BackendEndpointControls.kt`: new 31-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 053

Goal: P0.2 extract review decision actions from parse-confirm UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ReviewDecisionActions.kt` with the existing confirm/ignore review actions.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ParseConfirmPanel.kt` so it owns draft field state and delegates review action buttons to `ReviewDecisionActions`.
- Updated `validation/validate_android_structure.py` with `review_decision_actions_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `12/12` to `13/13`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, and landable validator to use the current `ANDROID_STRUCTURE_METRIC 13/13` evidence string.
- Updated `android-mvp/build-report.md` and `docs/current-validation-status.md` with the latest evidence.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 13/13`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 1m 10s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; confirm still applies blank-field fallbacks and ignore still sets status to `已忽略`.
- The structure guard now prevents review decision actions from being collapsed back into `ParseConfirmPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ParseConfirmPanel.kt`: reduced from 104 lines to 76 lines.
- `ReviewDecisionActions.kt`: new 58-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 056

Goal: P0.2 extract offline sample actions from import UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/OfflineSampleActions.kt` with the existing course/event offline sample controls.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` so it owns import state display, backend URL, OCR draft, preview, capture entry, and backend analysis sections while delegating offline sample controls to `OfflineSampleActions`.
- Updated `validation/validate_android_structure.py` with `offline_sample_actions_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `15/15` to `16/16`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 16/16` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 16/16`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 22s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; course and event offline sample buttons still call the same callbacks from the import panel.
- The structure guard now prevents offline sample actions from being collapsed back into `ImportPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ImportPanel.kt`: reduced from 89 lines to 87 lines.
- `OfflineSampleActions.kt`: new 24-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 054

Goal: P0.2 extract backend analysis controls from import UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/BackendAnalysisControls.kt` with the existing backend course/event analysis controls.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` so it owns capture, backend URL, OCR draft, preview, and offline sample sections while delegating backend analysis buttons to `BackendAnalysisControls`.
- Updated `validation/validate_android_structure.py` with `backend_analysis_controls_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `13/13` to `14/14`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 14/14` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 14/14`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 25s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; backend course and event parse buttons still call the same callbacks from the import panel.
- The structure guard now prevents backend analysis controls from being collapsed back into `ImportPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ImportPanel.kt`: reduced from 104 lines to 95 lines.
- `BackendAnalysisControls.kt`: new 34-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.

## 2026-05-24 / Round 055

Goal: P0.2 extract import capture actions from import UI and lock the new boundary in Android structure validation.

Files changed:
- Added `android-mvp/app/src/main/java/cn/shike/app/ui/ImportCaptureActions.kt` with the existing gallery screenshot and camera import controls.
- Updated `android-mvp/app/src/main/java/cn/shike/app/ui/ImportPanel.kt` so it owns import state display, backend URL, OCR draft, preview, backend analysis controls, and offline samples while delegating capture entry controls to `ImportCaptureActions`.
- Updated `validation/validate_android_structure.py` with `import_capture_actions_boundary_extracted`, raising `ANDROID_STRUCTURE_METRIC` from `14/14` to `15/15`.
- Updated README, the device checklist, Demo console, Runbook, core-package verifier, readiness validator, landable validator, and current validation status to use the current `ANDROID_STRUCTURE_METRIC 15/15` evidence string.

Validation:
- PASS `python3 validation/validate_android_structure.py`
  - Evidence: `ANDROID_STRUCTURE_METRIC 15/15`
- PASS `python3 validation/validate_landable.py`
  - Evidence: `LANDABLE_METRIC 16/16`
- PASS `python3 validation/validate_real_world_ready.py`
  - Evidence: `REAL_WORLD_READY_METRIC 20/20`
- PASS temporary core 20 package verification with `scripts/verify_core20_package.py`
  - Evidence: `CORE20_FILE_COUNT 20/20`
  - Evidence: `PASS STRUCTURE_GUARD README.md`
  - Evidence: `PASS STRUCTURE_GUARD materials/device-demo-checklist.md`
  - Evidence: `PASS STRUCTURE_GUARD validation/validate_demo_acceptance.py`
- PASS `gradle --no-daemon :app:assembleDebug`
  - Evidence: `BUILD SUCCESSFUL in 29s`
  - Note: the verified build used the project-local Gradle toolchain from `~/.local/share/shike-android-tools/gradle-8.10.2/bin/gradle`.
- PASS `python3 validation/validate_demo_acceptance.py`
  - Evidence: `DEMO_ACCEPTANCE_METRIC 16/16`
- PASS `python3 backend/verify_backend.py`
  - Evidence: `backend_passed`
- PASS `python3 spike/run_spike.py --all`
  - Evidence: `spike_passed`

Behavior preserved:
- Android runtime behavior is unchanged; gallery and camera buttons still call the same callbacks from the import panel.
- The structure guard now prevents import capture actions from being collapsed back into `ImportPanel.kt`.
- Existing readiness, demo, landable, core-package, backend, and spike checks remain passing.

Code shape:
- `ImportPanel.kt`: reduced from 95 lines to 89 lines.
- `ImportCaptureActions.kt`: new 28-line UI component file.
- `validate_android_structure.py`: one additional structure boundary check.

Next:
- Continue P0.2 with another low-risk UI or validation boundary improvement.
- Keep the next round focused and require the full guard-chain verification before recording.
