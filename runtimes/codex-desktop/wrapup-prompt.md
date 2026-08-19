Run the LifeYoda wrapup workflow.

Repository path:
<LifeYoda repository root — set this when you create the scheduled task>

Use:
- workflows/wrapup-journal.workflow
- templates/daily-journal-page.template
- templates/daily-plan-page.template
- config/public.defaults.json
- private/local.json
- private/state.json if available

Only write after explicit user confirmation of the proposed wrapup batch.

Rules:
- Every Daily Journal must have a matching Daily Plan.
- If no Daily Plan exists for the date, propose creating a fallback Daily Plan row whose body says only `See journal`.
- Use `templates/daily-journal-page.template` for the Daily Journal body.
- Use `✅` as the journal icon when every planned checklist item is complete.
- Use `📓` as the journal icon when completion is partial.
- Update the matching Daily Plan Status to `done` or `partial` based on Today's checklist completion.
- If the user did not mention extra unplanned work, ask whether anything outside the plan should be recorded before writing.

