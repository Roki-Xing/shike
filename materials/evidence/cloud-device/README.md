# Cloud Device Evidence Package

This folder stages the cloud-device evidence bundle for Shike.

Populate it with the recorded videos and redacted text artifacts listed in
`cloud-device-manifest.md`, including `cloud-device-test-report.md`.

Use this folder together with the release handoff files:

- `materials/evidence/release-evidence-index.md` is the top-level evidence index.
- `RELEASE_EVIDENCE_INDEX_METRIC 10/10` is the current release evidence index gate, including `docs/optimization-log.md` current handoff summary and README public entrypoint checks.
- `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md` is the desktop guidance source for the current landing-readiness audit.
- `materials/evidence/requirement-matrix.md` maps the desktop guidance stages A-E to local evidence and strict cloud-device blockers, guarded by `REQUIREMENT_MATRIX_METRIC 9/9`.
- `materials/evidence/blocking-report.md` lists the current strict evidence blockers.
- `python3 shike/validation/validate_landing_release_candidate.py` must stay at `LANDING_RELEASE_CANDIDATE_METRIC 52/52`.
- `python3 shike/validation/validate_landing_release_candidate.py --strict` is expected to stay blocked at `LANDING_RELEASE_CANDIDATE_STRICT_EVIDENCE 3/7` until the real cloud-device recordings and filled report are collected.

Before recording, refresh the APK hash and generate the operator checklist:

```bash
python3 shike/scripts/prepare_cloud_device_evidence.py
```

The prep helper must pass at `CLOUD_DEVICE_PREP_METRIC 5/5`. Until the real cloud-device recordings are collected, `CLOUD_DEVICE_PREP_MISSING_VIDEOS 9/9` is the expected state and must not be treated as release-ready strict evidence.
Before recording, also complete the `cloud-device-test-report.md` `Pre-recording Evidence Gate`: confirm the current handoff still points back to `/mnt/c/Users/Xing/Desktop/1. 当前仓库总体判断.md`, `REQUIREMENT_MATRIX_METRIC 9/9` still passes, all 9 real cloud-device MP4 files are present, and no placeholder fields remain after capture.

Then run:

```bash
python3 shike/validation/validate_cloud_device_package.py
python3 shike/validation/validate_cloud_device_package.py --strict
```

The non-strict check must pass at `CLOUD_DEVICE_PACKAGE_METRIC 27/27`; it validates package structure, device-runbook release handoff steps, release handoff links, the generated capture TODO handoff template, the release evidence `10/10` gate, the desktop guidance matrix pointer, the expected strict blocker state, and redaction surfaces.
The strict check is for the final cloud-device recording set.

Do not put AppKEY, backend tokens, full OCR text, phone numbers, emails,
student IDs, or personal notifications in videos, logs, filenames, or reports.
