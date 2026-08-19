# Daily Journal Schema

Daily Journal writes happen in the wrapup workflow after explicit confirmation.

Hard rule: every Daily Journal must have a matching Daily Plan row.

If the Daily Plan does not exist, the wrapup workflow must propose creating a fallback Daily Plan row first. The fallback plan body should only say `See journal`.

Build the Daily Journal page body from `templates/daily-journal-page.template`.
Do not put journal page-template or format-reference choices in private config.

Icon rule:

- All planned checklist items completed: `✅`
- Partial completion: `📓`

Status rule:

- All planned checklist items completed: set matching Daily Plan `Status` to `done`.
- Partial completion: set matching Daily Plan `Status` to `partial`.

Extra bonus rule:

- If the user mentioned unplanned work, record it.
- If not, ask whether any unplanned work should be recorded.
