# Course Task Sources

Course tasks are a generic source interface. The toolkit must not assume a specific learning platform, Notion setup, or page layout.

Each configured course source should return:

- `course`: course label
- `title`: task title
- `due`: due date or timing, if known
- `completed`: true, false, or unknown
- `citation`: direct link, block reference, message link, file path, or source description

Supported source types in the initial schema:

- `notion_checkbox_block`
- `notion_database`
- `local_markdown_checklist`
- `gmail_label`
- `drive_doc`
- `manual`

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

