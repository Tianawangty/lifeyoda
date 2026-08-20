Run the LifeYoda apply-daily-plan workflow.

Repository path:
<LifeYoda repository root — set this when you create the scheduled task>

Use:
- workflows/apply-daily-plan.md
- config/public.defaults.json
- private/local.json
- the confirmed Draft Day Plan from the current conversation

Only proceed if the user explicitly confirmed the plan or gave concrete edits to apply.

Write rules:
- Create or update the Daily Plan destination configured in private config.
- Set Daily Plan Status to planned when creating it from the daily workflow.
- Use a random emoji for the new Daily row/icon.
- Write Focus as 3-5 bullet points.
- Build the Daily Plan page from `templates/daily-plan-page.template`.
- Mirror only confirmed dated/time-blocked items to the configured planning calendar.
- Do not create a Daily Journal.

Return a concise apply report listing what was written and what was skipped.
