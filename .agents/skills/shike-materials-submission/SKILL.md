---
name: shike-materials-submission
description: Prepare Shike competition materials and submission packages: demo script, evidence checklist, prototype exports, and the strict core-20-file package verifier.
---

# shike-materials-submission

## When to use

- Editing competition materials: demo script, poster copy, preliminary deck, submission checklist.
- Producing or updating the 6 evidence recordings and ensuring names/flows match validators.
- Exporting prototype HTML/PDF artifacts for demos.
- Preparing / verifying the "core 20 file" submission package.

## Must read first

1. `AGENTS.md`
2. `materials/submission-checklist.md`
3. `materials/device-demo-checklist.md`
4. `materials/demo-script.md`
5. `prototype/demo.html` and `prototype/index.html`
6. `scripts/verify_core20_package.py`
7. `validation/validate_demo_acceptance.py`
8. `README.md`

## Existing project facts (from repo)

- The demo acceptance validator enforces:
  - evidence file naming,
  - key flows (course via gallery, event via camera, fallback/offline, restart restore, delivery readiness),
  - and consistent command style across README/checklist/demo console.
  - See `validation/validate_demo_acceptance.py`.
- The strict submission boundary is the "core 20 file package":
  - Verified by `scripts/verify_core20_package.py` which checks exact file list, file count (20/20),
    APK SHA-256, and that packaged docs reference the key validators (structure/action/unit tests).
- Prototype artifacts:
  - Multi-page prototype: `prototype/index.html` (+ `prototype/index.pdf`).
  - One-page demo console: `prototype/demo.html` (+ `prototype/demo.pdf`).

## Recommended workflow

1. Keep narratives consistent:
   - If you change commands, paths, or validator names in README, update demo checklist and demo console together.
2. Update materials incrementally:
   - Avoid mixing product changes and materials changes unless required.
3. Before producing evidence:
   - Run `python3 shike/validation/validate_real_world_ready.py` to ensure the demo isn't recording a broken build.
4. Prepare the core-20 package:
   - Copy only the expected 20 files into a clean folder.
   - Run the verifier script against that folder.

## Reusable modules or commands

```bash
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
python3 shike/scripts/verify_core20_package.py "/path/to/core20-package"
```

## High-risk mistakes

- Recording real personal data (notifications, contacts, real chat screenshots).
- Including secrets (AppKEY, tunnel tokens) in docs, recordings, or prototype screenshots.
- Changing user flows without updating checklist/demo console/validators.
- Adding extra files to the core-20 package or forgetting a required file.
- Shipping a core-20 package that does not reference the required validators (verifier will fail).

## Validation

- Demo package consistency:
  - `python3 shike/validation/validate_demo_acceptance.py`
- End-to-end readiness:
  - `python3 shike/validation/validate_real_world_ready.py`
- Core-20 strict package:
  - `python3 shike/scripts/verify_core20_package.py "<package_dir>"` must show `CORE20_FILE_COUNT 20/20`.

