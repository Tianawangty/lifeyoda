# Daily Plan Schema

Daily Plan writes happen only in the apply-daily-plan workflow after explicit confirmation.

Required behavior:

- Create one row per date.
- Use the fixed toolkit date-title format defined in `templates/daily-plan-page.md`.
- Pick one random emoji for the new Daily row/icon.
- Set `Status` to `planned` when created by the daily workflow.
- Write `Focus` as 3-5 bullet points.
- Build the page body from `templates/daily-plan-page.md`.
- Do not put page-template or format-reference choices in private config.

The public toolkit does not assume a specific Notion database ID or property ID. Those belong in `private/`.

If a plan is created during wrapup because the user forgot to plan in advance, the body should only say:

```text
See journal
```
