# Codex Desktop Connector Notes

Codex Desktop runtime differences:

- Gmail can be read directly through the Gmail connector when connected.
- Slack can be read directly through the Slack connector when connected.
- Google Calendar can be read directly when connected.
- Outlook Calendar may fail for school accounts that require additional security approval. In that case, use Slack notifications from the Outlook Calendar app as a proxy for fixed-event awareness.

Slack calendar notifications are not a full Outlook API substitute. They should be used to identify likely fixed constraints and changes, not to reconstruct the entire calendar.

If both direct Outlook and Slack Outlook notifications are unavailable, mark Outlook Calendar as unavailable.

