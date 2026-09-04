### What changes, and why

### Checks

```bash
python3 scripts/check.py
python3 -m unittest discover -s tests
```

- [ ] Both pass
- [ ] Version bumped in all four places if anything under `plugins/lifeyoda/` changed —
      Claude Code silently skips an install at a version it already has
- [ ] `CHANGELOG.md` updated
- [ ] No real Notion ID, calendar ID, Gmail label, Slack ID, or absolute home path anywhere,
      including fixtures and the commit message
- [ ] If a config field or enum value was added, some workflow actually reads it — this
      repository has repeatedly shipped configuration that nothing consumed
