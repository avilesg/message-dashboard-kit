# 07 — Back up personal config (preferences only)

```
Write or update config/personal.json from what you remember about my setup: preferences and configuration settings only (group label and JID, timezone, store path, priority people, keywords, custom topics, relationship/topic weights if any, alert and digest settings, notification config pointers), using config/personal.example.json as the shape. Do NOT include any WhatsApp messages, message store data, or media. Keep it gitignored and never commit it to the public repo. Then give me a downloadable copy named personal-config-backup-YYYY-MM-DD.json and tell me what changed since the last backup. Do not change the send lock: wacli stays read-only.
```

Repeat after any change to people, keywords, weights, or alerts. This does not back up messages; if those are critical, set up a separate, optional message-store backup. See `config/BACKUP.md`.
