---
name: shike-ui-product-polish
description: Productize Shike UI: align Compose screens with prototype, keep action-centered design, preserve risk/confirmation cues, and avoid breaking validators that rely on key copy.
---

# shike-ui-product-polish

## When to use

- Android UI polish: spacing, typography, icons, states (loading/empty/error), visual consistency.
- Splitting the long demo-style Compose page into real app screens (home/import/confirm/plan/inbox/settings).
- Aligning Android UI with `prototype/index.html` and competition narrative.
- Refining demo UX while keeping validators and red lines intact.

## Must read first

1. `AGENTS.md`
2. `docs/product-spec.md`
3. `docs/SHIKE_LANDING_APP_OPTIMIZATION_GUIDE.md` (UI productization requirements)
4. `prototype/index.html` and `prototype/demo.html`
5. `materials/demo-script.md`
6. Android UI directory: `android-mvp/app/src/main/java/cn/shike/app/ui/`
7. Validators that may grep copy:
   - `validation/validate_demo_acceptance.py`
   - `validation/validate_real_world_ready.py`

## Existing project facts (from repo)

- Product principle: action-centered, not chat-centered (see `docs/product-spec.md`).
- Prototype exists and includes multiple pages (`prototype/index.html` + PDFs).
- Android UI currently prioritizes a demo-friendly long page composition (see `cn.shike.app.ui.ShikeMainScreen`).
- Risk and missing-fields cues exist in UI and are part of acceptance narrative; do not remove them.
- Validators may rely on specific Chinese tokens in docs/demo pages; changing text can break validations.

## Recommended workflow

1. Decide if change is visual-only or structural navigation:
   - Visual-only changes should avoid changing validator-grepped copy.
   - Structural changes should be incremental: introduce one screen boundary at a time.
2. Keep the red lines visible:
   - Confirmation requirement should remain explicit in critical flows.
   - Disable system actions until confirm + required fields are present.
3. Align to prototype by extracting reusable UI components rather than rewriting.
4. Verify with validators after each slice:
   - `validate_android_structure.py` to keep file boundaries stable.
   - `validate_demo_acceptance.py` and `validate_real_world_ready.py` to ensure narrative stays consistent.

## Reusable modules or commands

Reusable UI modules live in:

- `android-mvp/app/src/main/java/cn/shike/app/ui/`

Commands:

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
```

## High-risk mistakes

- Turning the UI into a generic chatbot or a static prototype that is not data-driven.
- Hiding or removing risk/missing-field panels.
- Making system actions available before confirmation.
- Changing demo narrative copy without updating validators/docs/checklists together.
- Collapsing extracted UI boundaries back into large files (structure guard will fail).

## Validation

```bash
python3 shike/validation/validate_android_structure.py
python3 shike/validation/validate_demo_acceptance.py
python3 shike/validation/validate_real_world_ready.py
```

