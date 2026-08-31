# Privacy and Local Config

All user-specific configuration belongs in:

```text
private/
```

This folder is ignored by git.

Examples of private values:

- Notion database IDs
- Notion block IDs
- Course task locators
- Slack channel IDs
- Slack DM IDs
- Gmail label IDs
- Calendar IDs
- Active GitHub repos
- Local repo paths
- Last successful run timestamps
- Processed thread/message IDs

Public files should contain schemas, placeholders, and general rules only.

When adding a new feature, first decide whether its values are public design or private user data. If it identifies a person, account, workspace, class, repo, database, document, or schedule, put it under `private/`.

