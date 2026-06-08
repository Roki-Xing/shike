# Shike User Research Plan

Status: planned evidence only; interviews and survey responses are not yet collected.

This plan supports the application-value scoring claim without fabricating user
evidence. Do not fabricate interview data. Until fieldwork is complete, every
result cell stays marked as `待采集`.

## Research Goal

Validate whether Shike's core loop is valuable for users who save
time-sensitive tasks in screenshots, photos, shared text, or manual notes:

```text
capture -> AI structured extraction -> user confirmation -> calendar/reminder/map -> inbox tracking
```

## Participant Sample

| Segment | Target Count | Why It Matters | Status |
|---|---:|---|---|
| College students | 4 | Courses, homework, club notices, event posters | 待采集 |
| Club or event organizers | 2 | Frequent poster and registration-deadline handling | 待采集 |
| Interns or young professionals | 2 | Meetings, interviews, commute/location details | 待采集 |
| Frequent event or travel users | 2 | Tickets, venue changes, itinerary reminders | 待采集 |

Total planned sample: 10 participants.

## Interview Questions

1. In the last seven days, how many screenshots or photos contained a task you
   needed to act on?
2. How many of those tasks were actually added to a calendar, reminder, map, or
   task list?
3. Did any screenshot or saved image cause a missed class, deadline, event,
   interview, or travel action?
4. Which fields would you expect Shike to extract before you trust it: title,
   time, location, deadline, contact, URL, or materials?
5. Would you accept an action card that always waits for your confirmation
   before opening calendar, reminder, or map actions?
6. Which privacy behavior do you prefer: keep raw OCR text, keep only redacted
   summaries, or clear all local evidence after action?
7. What would make a wrong AI extraction acceptable: low-confidence warning,
   missing-field checklist, editable fields, or manual paste fallback?

## Survey Metrics

| Metric | Collection Method | Current Value | Evidence Rule |
|---|---|---|---|
| Screenshot task count in last 7 days | Participant self-report | 待采集 | Record count only, no real screenshot text |
| Tasks manually converted to calendar/reminder/map | Participant self-report | 待采集 | Record count and channel |
| Missed or delayed actions caused by saved images | Participant self-report | 待采集 | Use synthetic paraphrase only |
| Willingness to try confirmable action cards | 1-5 rating | 待采集 | Store aggregate rating only |
| Privacy preference | Multiple choice | 待采集 | No personal identifiers |
| Wrong-action concern | 1-5 rating + short paraphrase | 待采集 | Redact names, phone, email, student IDs |

## Evidence Handling

- Store only participant segment, aggregate counts, and synthetic paraphrases.
- Do not store raw screenshots, raw OCR text, chat logs, phone numbers, emails,
  student IDs, names, addresses, AppKEY, backend tokens, or real notification
  content.
- If a quote is useful for the deck, rewrite it as a synthetic paraphrase and
  label it as `paraphrased`.
- Keep all system actions in the product claim confirmation-first: Shike opens
  calendar/reminder/map actions only after the user confirms extracted fields.

## Completion Criteria

The research evidence can move from `planned` to `collected` only when:

1. At least 8 participant rows are collected across at least 3 segments.
2. Aggregate metrics are filled without real personal data.
3. `docs/user-interview-summary.md` has no `待采集` values in the collected
   results section.
4. `python3 shike/validation/validate_user_research_evidence.py` still passes.
