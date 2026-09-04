# Course Task Sources

Course tasks are a generic source interface. The toolkit must not assume a specific learning platform, Notion setup, or page layout.

Each configured course source should return:

- `course`: course label
- `title`: task title
- `due`: due date or timing, if known
- `completed`: true, false, or unknown
- `citation`: direct link, block reference, message link, file path, or source description

Supported source types:

- `notion_checkbox_block` — a heading on a Notion page whose unchecked to-do blocks are the
  tasks. The `locator` names the page and the heading.
- `manual` — nothing is read. The source exists so its label appears in the brief and the
  user is asked about it during the question round.

Two types, not more, because each one is a read path that has to be written, tested, and
kept working. A Notion database, a markdown checklist, a Gmail label, and a Drive document
are all plausible next adapters; none is implemented, so none is offered. Adding one means
adding its read instruction to the Checklist Sources step of the morning brief and a value
to the `type` enum, in that order.

## Notion Checkbox Source

Private config may point to a Notion page, block, or callout containing checkbox tasks.

Default completion rule:

- checked: complete
- unchecked: pending

This is only one adapter. Public workflows should refer to it as a course task source, not as a hard-coded course or Notion block.

## Local Markdown Checklist Source

Useful for users without Notion.

Expected pattern:

```markdown
- [ ] Task title, due YYYY-MM-DD
- [x] Completed task
```

## Manual Source

Manual sources are suitable for first setup. The user can paste or maintain a small list of tasks in private config.

