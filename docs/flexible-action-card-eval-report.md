# Flexible Action Card Eval Report

- cases: `60`
- main field pass: `60/60`
- forbidden output pass: `60/60`
- threshold: `main >= 52/60` and `forbidden == 60/60`
- cases file: `validation/fixtures/shike_action_card_training_cases_v1.jsonl`

| case_id | split | difficulty | main | forbidden | failed fields |
| --- | --- | --- | --- | --- | --- |
| course_001 | train | easy | PASS | PASS | ok |
| course_002 | eval | medium | PASS | PASS | ok |
| course_003 | train | medium | PASS | PASS | ok |
| course_004 | train | hard | PASS | PASS | ok |
| course_005 | eval | hard | PASS | PASS | ok |
| course_006 | train | medium | PASS | PASS | ok |
| course_007 | train | medium | PASS | PASS | ok |
| course_008 | eval | hard | PASS | PASS | ok |
| course_009 | train | easy | PASS | PASS | ok |
| course_010 | eval | hard | PASS | PASS | ok |
| assignment_001 | train | easy | PASS | PASS | ok |
| assignment_002 | train | medium | PASS | PASS | ok |
| assignment_003 | eval | hard | PASS | PASS | ok |
| assignment_004 | train | medium | PASS | PASS | ok |
| assignment_005 | eval | hard | PASS | PASS | ok |
| assignment_006 | train | hard | PASS | PASS | ok |
| assignment_007 | eval | medium | PASS | PASS | ok |
| event_001 | train | easy | PASS | PASS | ok |
| event_002 | train | medium | PASS | PASS | ok |
| event_003 | eval | hard | PASS | PASS | ok |
| event_004 | train | hard | PASS | PASS | ok |
| event_005 | eval | medium | PASS | PASS | ok |
| event_006 | train | hard | PASS | PASS | ok |
| event_007 | eval | hard | PASS | PASS | ok |
| meeting_001 | train | easy | PASS | PASS | ok |
| meeting_002 | eval | medium | PASS | PASS | ok |
| meeting_003 | train | hard | PASS | PASS | ok |
| meeting_004 | train | hard | PASS | PASS | ok |
| exam_001 | train | easy | PASS | PASS | ok |
| exam_002 | eval | hard | PASS | PASS | ok |
| interview_001 | train | easy | PASS | PASS | ok |
| interview_002 | eval | medium | PASS | PASS | ok |
| travel_001 | train | easy | PASS | PASS | ok |
| travel_002 | eval | hard | PASS | PASS | ok |
| multi_001 | train | hard | PASS | PASS | ok |
| multi_002 | eval | hard | PASS | PASS | ok |
| negative_001 | train | negative | PASS | PASS | ok |
| negative_002 | eval | negative | PASS | PASS | ok |
| negative_003 | train | negative | PASS | PASS | ok |
| negative_004 | eval | hard | PASS | PASS | ok |
| ocr_noise_001 | train | hard | PASS | PASS | ok |
| ocr_noise_002 | eval | hard | PASS | PASS | ok |
| ocr_noise_003 | train | medium | PASS | PASS | ok |
| prep_001 | train | medium | PASS | PASS | ok |
| prep_002 | eval | medium | PASS | PASS | ok |
| prep_003 | train | hard | PASS | PASS | ok |
| prep_004 | eval | medium | PASS | PASS | ok |
| ambiguous_001 | train | hard | PASS | PASS | ok |
| ambiguous_002 | eval | hard | PASS | PASS | ok |
| course_011 | train | medium | PASS | PASS | ok |
| course_012 | eval | hard | PASS | PASS | ok |
| event_008 | train | medium | PASS | PASS | ok |
| meeting_005 | eval | medium | PASS | PASS | ok |
| exam_003 | train | medium | PASS | PASS | ok |
| travel_003 | train | hard | PASS | PASS | ok |
| negative_005 | train | negative | PASS | PASS | ok |
| ocr_noise_004 | eval | hard | PASS | PASS | ok |
| prep_005 | train | medium | PASS | PASS | ok |
| ambiguous_003 | eval | negative | PASS | PASS | ok |
| multi_003 | train | hard | PASS | PASS | ok |
